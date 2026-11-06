#!/usr/bin/env python3
"""
caption.py - revisa el texto de un post de Instagram y muestra exactamente lo
que se ve en el feed antes del «... más».

Adaptado al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol).

Instagram muestra unos 125 caracteres del texto en el feed y esconde el resto
detrás de un toque. Casi todo texto que falla, falla ahí: el gancho está en la
tercera oración, o la primera línea es un saludo, o parte con un hashtag. Esto
imprime esa ventana como una caja, para leerla como la lee alguien que va
pasando, y después revisa las cosas que vale la pena revisar.

El corte en 125 es aproximado: cambia con el teléfono, el tamaño de letra y
dónde caen los saltos de línea. Por eso conviene dejar margen y no un texto
calculado para terminar justo en 125. Cámbialo con --truncate.

Uso
  python3 caption.py texto.txt
  python3 caption.py texto.txt --keywords "carreras online,estudiar trabajando"
  pbpaste | python3 caption.py -
  python3 caption.py texto.txt --json
"""

import argparse
import json
import re
import sys
import textwrap

LIMIT = 2200             # Límite duro de Instagram.
TRUNCATE = 125           # Más o menos donde el feed corta a «... más».
HASHTAG_LIMIT = 5        # Tope de Instagram por post o reel desde el
                         # 18-12-2025; antes eran 30.

LETRAS = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
HASHTAG_RE = re.compile(rf"(?:^|\s)(#[{LETRAS}0-9_]+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[A-Za-z0-9_.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:cl|com|co|io|net|org|ai|app)(?:/\S*)?\b",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
CONCRETE_RE = re.compile(r"\$\s?\d|\b\d[\d.,]*\b|(?<![¿¡])(?<![.!?:]\s)(?<!^)\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}\b", re.MULTILINE)

ASKS = [
    # Sin (?i): la palabra clave va en MAYÚSCULAS o entre comillas. Con (?i),
    # "comenta si te pasó" contaba como pedir comentar la palabra "si".
    (re.compile(r"\b[Cc]omenta(?:nos|me)?\s+(?:la palabra\s+)?(?:[«\"][^»\"]{2,20}[»\"]|[A-ZÁÉÍÓÚÑ0-9]{2,}\b)"), "comentar una palabra"),
    (re.compile(r"(?i)\b(?:escr[ií]be(?:nos|me)|m[aá]nda(?:nos|me) un (?:dm|mensaje)|h[aá]blanos|al (?:dm|interno|inbox))\b"), "escribir por DM"),
    (re.compile(r"(?i)\bguarda(?:lo|la)?\s+(?:este|esta|para)\b|\bgu[aá]rdalo\b"), "guardar"),
    (re.compile(r"(?i)\bcomp[aá]rte(?:lo|la)\b|\bcomparte (?:este|esta|con)\b|\bm[aá]ndaselo\b"), "compartir"),
    (re.compile(r"(?i)\bs[ií]gue(?:nos|me)\b"), "seguir"),
    (re.compile(r"(?i)\b(?:link|enlace) (?:en (?:la|nuestra|mi) )?bio\b"), "link en la bio"),
    (re.compile(r"(?i)\bdesliza\b|\bpasa (?:a la|al) (?:siguiente|lado)\b"), "deslizar"),
    (re.compile(r"(?i)\bcu[eé]nta(?:nos|me)\b|\bd[ií](?:nos|me)\b|\bqu[eé] (?:opinas|har[ií]as)\b|\bcu[aá]l (?:eliges|prefieres)\b"), "responder una pregunta"),
    (re.compile(r"(?i)\bpostula\b|\bmatric[uú]late\b|\binscr[ií]bete\b|\bagenda\b|\bcotiza\b"), "postular o inscribirse"),
    (re.compile(r"(?i)\bescr[ií]benos al whatsapp\b|\bwhatsapp\b"), "WhatsApp"),
]

FILLER_TAGS = {"#viral", "#fyp", "#parati", "#foryou", "#foryoupage", "#explore", "#explorar",
               "#explorepage", "#tendencia", "#trending", "#instagood", "#love", "#follow",
               "#like4like", "#reels", "#reelsinstagram", "#viralreels", "#instadaily",
               "#chile", "#motivacion", "#motivación"}


def visible_window(text, cut):
    """Lo que muestra el feed. Instagram corta a mitad de palabra, así que esto también."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  LO QUE MUESTRA EL FEED", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... más" if truncated else "(cabe completo)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    text = text.rstrip()
    stripped = text.strip()
    chars = len(stripped)
    lines = [l for l in stripped.split("\n")]
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = [name for pattern, name in ASKS if pattern.search(stripped)]
    # "link en la bio" y "escribir por WhatsApp" suelen ir juntos como una sola acción.
    if "WhatsApp" in asks and len(asks) > 1:
        asks.remove("WhatsApp")
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("LARGO", "FALLA" if chars > LIMIT else "OK",
        f"{chars} / {LIMIT} caracteres" + (f", {chars - LIMIT} sobre el límite"
                                           if chars > LIMIT else ""))

    if not first_line:
        add("PRIMERA LÍNEA", "FALLA", "el texto parte con una línea en blanco")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("PRIMERA LÍNEA", "FALLA",
            "parte con un hashtag o una mención, que es el único lugar que vale una oración")
    elif re.match(r"(?i)^\s*(?:hola|holi|buenas|buenos d[ií]as|qu[eé] tal|bienvenid)", first_line):
        add("PRIMERA LÍNEA", "FALLA", "parte con un saludo: se gasta la ventana visible en nada")
    elif len(first_line) > cut:
        add("PRIMERA LÍNEA", "OJO",
            f"{len(first_line)} caracteres, así que se corta en {cut} a mitad de idea. "
            "Sirve si el corte deja con ganas, no si corta una frase subordinada")
    else:
        add("PRIMERA LÍNEA", "OK", f"{len(first_line)} caracteres, se ve completa")

    add("GANCHO CONCRETO", "OK" if CONCRETE_RE.search(window) else "OJO",
        f"{len(CONCRETE_RE.findall(window))} número(s) o nombre(s) en la ventana visible"
        + ("" if CONCRETE_RE.search(window) else " - nada verificable antes del toque"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAGS", "FALLA", f"{len(tags)} hashtags, sobre el tope de {HASHTAG_LIMIT} de Instagram. "
                                 "Del sexto en adelante no cuentan y el bloque se lee antiguo")
    elif len(tags) == HASHTAG_LIMIT and filler:
        add("HASHTAGS", "OJO", f"{len(tags)} hashtags, en el tope, y "
                               f"{len(filler)} genéricos. Gasta los cinco en temas")
    elif filler:
        add("HASHTAGS", "OJO", f"{len(tags)} hashtags, {len(filler)} genéricos "
                               f"({', '.join(filler[:3])}). Esos no describen nada")
    else:
        add("HASHTAGS", "OK", f"{len(tags)} hashtag(s)" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("UBICACIÓN TAGS", "OK", "no hay hashtags que ubicar")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"(?![\w])", window) for t in tags):
        add("UBICACIÓN TAGS", "OJO", "hay un hashtag dentro de la ventana visible, "
                                     "gastando espacio del feed en una etiqueta")
    else:
        add("UBICACIÓN TAGS", "OK", "los hashtags quedan bajo el corte")

    add("LINKS", "OJO" if links else "OK",
        f"{len(links)} link(s) en el texto, y el texto no es clicable. "
        f"Llévalo a la bio o al DM" if links else "no hay links muertos en el cuerpo")

    if len(asks) == 1:
        add("UNA SOLA ACCIÓN", "OK", f"una llamada a la acción: {asks[0]}")
    elif not asks:
        add("UNA SOLA ACCIÓN", "OJO", "no hay llamada a la acción. Decide para qué es este post")
    else:
        add("UNA SOLA ACCIÓN", "OJO", f"{len(asks)} acciones ({', '.join(asks)}). "
                                     "Dos acciones es lo mismo que ninguna")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJIS", "OJO" if density > 4 else "OK",
        f"{len(emoji)} emoji, {density:.1f} cada 100 caracteres".replace(".", ",")
        + (" - se lee como decoración" if density > 4 else ""))

    if keywords:
        low = stripped.lower()
        found = [k for k in keywords if k.lower() in low]
        missing = [k for k in keywords if k.lower() not in low]
        in_window = [k for k in found if k.lower() in window.lower()]
        status = "OK" if not missing else ("OJO" if found else "FALLA")
        add("BÚSQUEDA", status,
            f"{len(found)}/{len(keywords)} presentes"
            + (f", {len(in_window)} en la ventana visible" if found else "")
            + (f". Faltan: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "FALLA")
    warns = sum(1 for c in checks if c["status"] == "OJO")
    verdict = "ARREGLAR" if fails else ("REVISAR" if warns else "LISTO")

    return {
        "characters": chars, "limit": LIMIT, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


def render(a, out=sys.stdout):
    head = (f"REVISIÓN DEL TEXTO  ·  {a['characters']} / {a['limit']} caracteres  ·  "
            f"{len(a['hashtags'])} hashtags  ·  {len(a['asks'])} acción(es)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<6} {c['check']:<16} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  VEREDICTO  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Revisa el texto de un post de Instagram.")
    ap.add_argument("input", nargs="?", default="-", help="archivo con el texto, o - para stdin")
    ap.add_argument("--truncate", type=int, default=TRUNCATE,
                    help=f"caracteres visibles antes de «... más» (por defecto {TRUNCATE})")
    ap.add_argument("--keywords", default="", help="términos separados por coma por los que quieres aparecer")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "LISTO" else 1)


if __name__ == "__main__":
    main()
