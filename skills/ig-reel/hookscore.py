#!/usr/bin/env python3
"""
hookscore.py - puntúa la primera línea de un reel en las cinco cosas que tienen
en común los ganchos que retienen, y ordena varios ganchos entre sí.

Adaptado al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol). La lógica es la misma; lo que cambia es todo lo que dependía del
inglés: acentos y eñes, "$18.000" con punto de miles, los números dichos en voz
alta ("dos años", "18 lucas"), las palabras que ponen algo en juego, los
saludos y preámbulos que se comen el primer segundo.

Qué es:  cinco heurísticas locales, calculadas en tu máquina con el texto
solamente. Un largo que se dice en menos de tres segundos, algo concreto, algo
en juego, lo interesante al principio y no al final, y alguien a quien se le
habla.

Qué NO es:  un predictor de vistas. El original se midió contra 74 ganchos
reales en inglés: separa bien un gancho real de uno escrito para ser malo
(AUC 0,83) y casi nada los aciertos de los fracasos de un mismo creador
(AUC 0,56; 0,50 es lanzar una moneda). Esta versión en español NO se ha medido
contra un corpus propio todavía. Úsalo para lo que sí sirve: pillar saludos,
preámbulos, ganchos sin nada concreto y ganchos que tardan cinco segundos en
decirse. Qué gancho bueno viaja más lo decide la retención, no un script.

Cada chequeo va de 0 a 100. Más alto es mejor.

Uso
  python3 hookscore.py ganchos.txt              # un gancho por línea, ordenados
  python3 hookscore.py --hook "Me costó $1.800.000 no leer una cláusula."
  pbpaste | python3 hookscore.py -
  python3 hookscore.py ganchos.txt --json
"""

import argparse
import json
import re
import statistics
import sys
import unicodedata

LETRAS = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
WORD_RE = re.compile(rf"[{LETRAS}0-9$%'’-]+")
NUMBER_RE = re.compile(
    r"\$\s?\d[\d.]*(?:,\d+)?"                          # plata: $18.000, $2,5
    r"|\b\d[\d.]*(?:,\d+)?\s?"                          # una cifra, con o
    r"(?:%|k\b|x\b|hrs?\b|horas?\b|min\b|minutos?\b"    # sin unidad
    r"|d[ií]as?\b|semanas?\b|mes(?:es)?\b|años?\b|lucas?\b|mil\b|millones\b)?",
    re.IGNORECASE)
PROPER_RE = re.compile(rf"(?<![¿¡])(?<![.!?:]\s)(?<!^)\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{{2,}}\b")
HASHTAG_RE = re.compile(rf"(?:^|\s)#[{LETRAS}0-9_]+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

# Los números dichos en voz alta son tan concretos como los escritos. "Uno" y
# "primero" quedan fuera a propósito: casi siempre son relleno.
SPOKEN_NUMBERS = {
    "cero", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
    "diez", "once", "doce", "quince", "veinte", "treinta", "cuarenta",
    "cincuenta", "sesenta", "setenta", "ochenta", "noventa", "cien", "ciento",
    "mil", "millón", "millon", "millones", "docena", "mitad", "doble", "triple",
    "semestre", "semestres",
}
# En español los días y los meses van en minúscula, así que no los pilla la
# regla de nombres propios que en inglés sí los contaba. Son igual de concretos.
DIAS_MESES = {
    "lunes", "martes", "miércoles", "miercoles", "jueves", "viernes", "sábado",
    "sabado", "domingo", "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
}
MONEY_WORDS = {
    "pesos", "lucas", "luca", "palos", "dólares", "dolares", "porciento",
    "sueldo", "arancel", "matrícula", "matricula", "cuota", "cuotas", "beca",
    "crédito", "credito", "deuda", "gratis", "gratuito", "descuento", "precio",
    "becas", "aranceles", "sueldos", "descuentos", "gratuidad",
}

# Palabras que ponen algo en juego. Un gancho sin ninguna es una afirmación;
# con una, es una razón para seguir mirando.
STAKES = {
    "nunca", "jamás", "jamas", "nadie", "nada", "no", "ni", "sin", "deja",
    "dejes", "dejen",
    "error", "errores", "equivocado", "equivocada", "mal", "perdí", "perdi",
    "perder", "pierdes", "perdiste", "costó", "costo", "cuesta", "caro",
    "fracasé", "fracase", "fracaso", "reprobé", "reprobe", "renuncié",
    "renuncie", "dejé", "deje", "dejar", "despidieron", "rechazaron",
    "gratis", "pagué", "pague", "pagar", "ahorré", "ahorre", "primera",
    "prohibido", "peor", "odio", "odiaba", "mentira", "verdad", "secreto",
    "oculto", "antes", "hasta", "pero", "excepto", "salvo", "problema",
    "riesgo", "cuidado", "ojo", "arrepiento", "arrepentí", "ojalá", "ojala",
    "deberías", "deberias", "todavía", "todavia", "aún", "aun", "ya", "solo",
    "sólo", "versus", "vs", "realmente", "miedo", "tarde", "vergüenza",
    "verguenza", "casi", "evita", "evitar", "trampa",
}

# Aperturas que gastan el primer segundo sin decir nada.
WEAK_OPENERS = [
    "hola", "holi", "buenas", "buenos", "bueno", "ya", "oye", "chiquillos",
    "chiquillas", "amigos", "amigas", "gente", "hoy", "básicamente",
    "basicamente", "honestamente", "mira", "miren", "escucha", "eh", "em",
    "entonces", "así", "bienvenidos", "bienvenidas", "quiero", "les quiero",
    "te quiero", "les queremos", "te queremos", "les voy", "te voy", "vamos a", "voy a", "en este", "en el video",
    "sabías que", "sabias que", "sabían que", "has pensado", "alguna vez",
    "te has", "una de", "el tema", "hay mucha", "hay muchos", "esto es",
    "como todos", "cuando se", "si alguna", "tú sabes", "tu sabes",
]

# Imperativos que se ganan el primer lugar.
IMPERATIVES = {
    "para", "deja", "roba", "copia", "borra", "prueba", "mira", "lee", "guarda",
    "usa", "arma", "haz", "escribe", "manda", "toma", "empieza", "renuncia",
    "nunca", "evita", "ojo", "anota", "pregunta", "calcula", "revisa", "no",
}

DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:no (?:hagas|sigas haciendo) scroll|no (?:sigas )?desliz|para de (?:deslizar|scrollear)|deja de scrollear|no scrollees)"),
     "Abre con «no hagas scroll». Pedir atención demuestra que no te la ganaste."),
    (re.compile(r"(?i)\b(?:en (?:este|el) (?:video|reel|post)(?: de hoy)?|en el video de hoy|(?:hoy )?(?:les|te) voy a (?:mostrar|contar|enseñar)|(?:les|te) (?:quiero|queremos) (?:contar|mostrar|hablar)|(?:les|te) vamos a (?:mostrar|contar|enseñar))\b"),
     "Preámbulo de video. Bórralo y parte por lo que prometes."),
    (re.compile(r"(?i)^\s*(?:hola|holi|buenas|buenos d[ií]as|qu[eé] tal|bienvenid[oa]s?|hey)\b"),
     "Saludo. Nadie entró al feed para que lo saluden."),
    (HASHTAG_RE,
     "Hashtag en el gancho. Los hashtags van al final del texto, si es que van."),
    (EMOJI_RE,
     "Emoji en el gancho. El texto en pantalla a tamaño de gancho tiene espacio para palabras o para un emoji, no para los dos."),
]


def clamp(n):
    return max(0.0, min(100.0, n))


def normal(w):
    return w.lower().strip("'’¿?¡!.,;:")


def words(text):
    # "$18.000" se dice como una palabra, así que acá también es una.
    return WORD_RE.findall(re.sub(r"(?<=\d)\.(?=\d{3}\b)", "", text))


def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def check_length(text):
    """El gancho tiene que llegar antes de que se mueva el pulgar."""
    w = words(text)
    n = len(w)
    secs = n / 2.7                       # ~160 palabras por minuto, hablado
    chars = len(text.strip())
    if 5 <= n <= 12:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 12) * 11)
    if chars > 65:                       # dos líneas de texto grande en pantalla
        score -= 12
    return clamp(score), f"{n} palabras, {chars} caracteres, ~{fmt(secs)}s dicho (ideal 5-12 palabras)"


def check_specificity(text):
    """Una cosa concreta le gana a tres abstractas."""
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    propers = set(PROPER_RE.findall(text))
    low = [normal(w) for w in words(text)]
    spoken = [w for w in low if w in SPOKEN_NUMBERS or w in MONEY_WORDS or w in DIAS_MESES]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, (f"{hits} marcador(es) concreto(s)" + (f": {found}" if found else
                   " - sin número, sin nombre, nada verificable"))


def check_stakes(text):
    """Tensión, costo, negación. Algo que quien mira podría perder."""
    w = [normal(x) for x in words(text)]
    hits = [x for x in w if x in STAKES]
    markers = sorted(set(hits))
    if re.search(r"\$\s?\d", text):
        markers.append("un precio")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} marcador(es) de tensión" + (f": {', '.join(markers[:4])}" if markers else
                                              " - nada está en juego en esta línea")
    return clamp(score), detail


def check_frontload(text):
    """La palabra interesante no puede estar en la posición nueve."""
    w = words(text)
    if not w:
        return 0.0, "vacío"
    low = [normal(x) for x in w]
    opener = sin_tildes(" ".join(low[:2]))
    penalty = 0
    hit_opener = None
    for weak in WEAK_OPENERS:
        weak_n = sin_tildes(weak)
        if opener.startswith(weak_n + " ") or opener == weak_n or sin_tildes(low[0]) == weak_n:
            penalty, hit_opener = 30, weak
            break
    payload = None
    for i, token in enumerate(low):
        if (token in STAKES or token in SPOKEN_NUMBERS or token in MONEY_WORDS or token in DIAS_MESES
                or NUMBER_RE.match(w[i]) or (i and PROPER_RE.match(w[i]))):
            payload = i
            break
    if payload is None:
        base = 30.0
        where = "no hay ninguna palabra con carga en la línea"
    elif payload <= 3:
        base = 100.0
        where = f"la carga está en la palabra {payload + 1}"
    elif payload <= 6:
        base = 70.0
        where = f"la carga está en la palabra {payload + 1}, podría ir antes"
    else:
        base = 40.0
        where = f"la carga está en la palabra {payload + 1}, demasiado tarde"
    detail = where + (f"; apertura débil «{hit_opener}»" if hit_opener else "")
    return clamp(base - penalty), detail


SEGUNDA_PERSONA = re.compile(
    r"\b(?:tú|tu|tus|te|ti|contigo|usted|ustedes|les|vos)\b"
    r"|\b(?:puedes|quieres|tienes|estás|estas|eres|haces|sabes|sabías|necesitas|"
    r"crees|piensas|pagas|trabajas|estudias|vives|buscas|dejas|pierdes|ganas|"
    r"postulas|deberías|podrías)\b", re.IGNORECASE)
PRIMERA_PERSONA = re.compile(r"\b(?:yo|me|mi|mis|conmigo|nosotros|nosotras|nos|nuestro|nuestra|nuestros|nuestras)\b",
                             re.IGNORECASE)
# En español el pronombre se omite: "Perdí", "Estudié", "Subí" ya son primera
# persona. Se reconocen por el pretérito en -é / -í, menos las palabras comunes
# que terminan igual y no son verbos.
PRETERITO_YO = re.compile(r"\b[a-záéíóúñ]{2,}[éí]\b", re.IGNORECASE)
NO_VERBOS = {"qué", "café", "bebé", "aquí", "allí", "así", "ahí", "sí", "mí", "ti",
             "quizá", "jamás", "también", "según", "rubí", "maní", "ají", "comité", "puré"}


def check_address(text):
    """Le habla a una persona, o flota en el aire."""
    w = [normal(x) for x in words(text)]
    if SEGUNDA_PERSONA.search(text):
        return 100.0, "le habla a quien mira"
    # "Para" solo es imperativo en "para de...": sin eso es la preposición.
    imperativo = w and w[0] in IMPERATIVES and (w[0] != "para" or w[1:2] == ["de"])
    if imperativo:
        return 90.0, f"abre con imperativo («{w[0]}»)"
    if PRIMERA_PERSONA.search(text) or any(m.lower() not in NO_VERBOS for m in PRETERITO_YO.findall(text)):
        return 70.0, "primera persona, no le habla a nadie"
    return 35.0, "tercera persona, nadie en la sala"


CHECKS = ["LARGO", "CONCRECIÓN", "TENSIÓN", "CARGA ADELANTE", "A QUIÉN"]


def run(text):
    results = {
        "LARGO": check_length(text),
        "CONCRECIÓN": check_specificity(text),
        "TENSIÓN": check_stakes(text),
        "CARGA ADELANTE": check_frontload(text),
        "A QUIÉN": check_address(text),
    }
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # La propiedad más débil pone techo: con una mala basta para que el pulgar siga.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "FUERTE" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "DÉBIL")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def fmt(n):
    return f"{n:.1f}".replace(".", ",")


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nPUNTAJE DEL GANCHO", file=out)
    print("=" * 64, file=out)
    print(f"  «{text.strip()}»\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<15} {bar(score)} {fmt(score):>5}", file=out)
        print(f"  {'':<15} {detail}", file=out)
    print("-" * 64, file=out)
    print(f"  {'PUNTAJE':<15} {bar(overall)} {fmt(overall):>5}   {verdict}", file=out)
    for f in flags:
        print(f"\n  DESCALIFICA  {f}", file=out)
    if verdict != "FUERTE":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Propiedad más débil: {weakest}. Arregla esa y vuelve a correrlo.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nGANCHOS ORDENADOS\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 60 else r["hook"][:57] + "..."
        print(f"{mark} {fmt(r['score']):>5} {r['verdict']:<7} {hook}", file=out)
        print(f"        más débil: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        descalifica: {f}", file=out)
    print("\nGraba el primero. Si el primero está bajo 50, ninguno de estos es el gancho.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Puntúa un gancho de reel en cinco propiedades.")
    ap.add_argument("input", nargs="?", default="-", help="archivo con un gancho por línea, o -")
    ap.add_argument("--hook", help="puntúa un solo gancho escrito en la línea de comandos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("no hay nada que puntuar", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line)
        payload.append({
            "hook": line,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0])
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
