#!/usr/bin/env python3
"""
humanize.py - quita la huella de máquina de un borrador.

Adaptado al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol). Las pasadas son las mismas; el léxico es español, las mayúsculas
entienden tildes, eñes y los signos de apertura ¿ y ¡, y los conectores que
arregla después de borrar una raya son los del español.

Tres pasadas, en este orden:

  1. INVISIBLES   borra o normaliza los caracteres que un teclado nunca
                  produce: espacios de ancho cero, unidores, guiones blandos,
                  BOM, caracteres de etiqueta Unicode, espacios duros y
                  angostos. Sobreviven al copiar y pegar y son la señal más
                  mecánica de un texto generado.
  2. TIPOGRAFÍA   raya -> coma, guion medio -> guion, comillas tipográficas y
                  angulares -> rectas, puntos suspensivos -> tres puntos,
                  viñeta -> guion.
  3. LÉXICO       reemplaza el léxico de slop.json por palabras simples,
                  respetando mayúsculas y sin tocar los links.

Las señales estructurales («no es solo X, es Y», tríadas, muros de hashtags)
se INFORMAN, nunca se reescriben solas: cambiar la forma de una oración pide
criterio, y eso le toca al modelo, no a una expresión regular.

Uso
  python3 humanize.py borrador.txt
  python3 humanize.py borrador.txt --report
  pbpaste | python3 humanize.py - --report
  python3 humanize.py borrador.txt --json
  python3 humanize.py borrador.txt -o limpio.txt
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
MINUS = "a-záéíóúüñ"
MAYUS = "A-ZÁÉÍÓÚÜÑ"


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    """'U+200B' -> 0x200b;  'U+E0000-U+E007F' -> (inicio, fin)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    """Cambia los links por marcadores para que ninguna pasada escriba dentro de uno."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    """Borra o convierte en espacio los caracteres invisibles. Devuelve (texto, hallazgos)."""
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": entry["action"]})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Cualquier carácter de formato (Cf) que quede es invisible por definición.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "otros caracteres de formato invisibles", "count": len(stray),
                     "action": "delete"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n, "to": entry["to"].strip() or "(espacio)"})
        if ch == "—":
            # " palabra — palabra " y "palabra—palabra" quedan en coma y espacio.
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)      # 5–10 -> 5-10
            text = re.sub(r"\s+–\s+", ", ", text)            # usado como raya
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    # Una coma puesta antes de otra puntuación se lee mal.
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    # Una raya que abría la oración deja una coma al principio.
    text = re.sub(r"(?m)^\s*,\s*", "", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def lex_pattern(find):
    return re.compile(r"(?<![\wáéíóúñ])" + re.escape(find).replace(r"\ ", r"\s+") + r"(?![\wáéíóúñ])",
                      re.IGNORECASE)


def pass_lexical(text, lex):
    """Reemplaza palabras y frases de relleno. Las más largas primero, para que ganen las frases."""
    hits = []
    entries = sorted(lex["phrases"] + lex["words"],
                     key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        pattern = lex_pattern(entry["find"])
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": entry["find"], "replace": entry["replace"] or "(borrado)",
                     "count": len(found), "family": entry["family"]})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    # Limpieza después de borrar. Borrar una frase entera deja puntuación
    # huérfana ("sistema. ." o una línea que ahora parte con coma), y eso se lee
    # peor que el relleno.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:]+[ \t]*)+", "", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)       # un espacio que dejó un borrado.
                                                      # Las sangrías más hondas son a propósito.
    text = re.sub(r"[ \t]+([,.;:!?])", r"\1", text)
    text = re.sub(r",[ \t]*([,.;:!?])", r"\1", text)
    text = re.sub(r"(?m)^[ \t]*[.!?]+[ \t]*$", "", text)   # línea que quedó en puro punto
    text = re.sub(r"([¿¡])\s+", r"\1", text)           # "¿ Qué" -> "¿Qué"
    text = re.sub(r"¡+\s*!+|¿+\s*\?+", "", text)       # signos que quedaron vacíos
    text = re.sub(r"([.!?])\s*,\s*", r"\1 ", text)      # "hogar., es" -> "hogar. es"
    text = re.sub(r"[ \t]+(?:y|o|e|u|pero|con|para|de)[ \t]*([.!?])", r"\1", text)  # "contenido y." -> "contenido."
    text = text.replace("...", "\x00ELL\x00")          # protege los puntos suspensivos reales
    text = re.sub(r"\.[ \t]*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = text.replace("\x00ELL\x00", "...")
    text = re.sub(r"(?m)^[ \t]*[.!?¡¿,;:]+[ \t]*$", "", text)   # línea que quedó en pura puntuación
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Una raya que pasó a coma, seguida de un conector, deja dos oraciones
    # pegadas ("es importante, también, es la prueba"). Se sube a punto.
    text = re.sub(r",\s*(también|así que|igual|al final|entonces)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    # Que todas las oraciones midan lo mismo también es una señal estructural.
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "name": f"Oraciones del mismo largo (variación {cv:.2f})".replace(".", ","),
                "count": len(lens),
                "fix": "Parte una oración en dos. Deja que otra se alargue. Las máquinas escriben parejo.",
            })
    return flags


def restore_capitals(original, text):
    """Borrar una apertura deja la palabra siguiente en minúscula.

    Solo se arregla si quien escribe usa mayúscula al empezar oraciones: una voz
    en minúsculas a propósito es un estilo, no un defecto.
    """
    starts = re.findall(rf"(?:^|[.!?]\s+|\n)\s*[¿¡]?([{MAYUS}{MINUS}])", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    return re.sub(rf"(?:^|(?<=[.!?] )|(?<=[.!?]\n)|(?<=\n))(\s*[¿¡]?)([{MINUS}])",
                  lambda m: m.group(1) + m.group(2).upper(), text)


def humanize(text, lex):
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "structures": scan_structures(text, lex),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + sum(h["count"] for h in report["lexical"])

    head("INFORME DE HUMANIZACIÓN")
    print(f"{total} artefactos de máquina quitados, "
          f"{len(report['structures'])} señales estructurales para reescribir", file=out)

    if report["invisible"]:
        head("1. CARACTERES INVISIBLES")
        for h in report["invisible"]:
            accion = "borrado" if h["action"] == "delete" else "espacio"
            print(f"  {h['count']:>3}x  {h['name']}  -> {accion}", file=out)
    if report["typographic"]:
        head("2. TIPOGRAFÍA")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. LÉXICO DE RELLENO")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["structures"]:
        head("4. SEÑALES ESTRUCTURALES  (no se arreglan solas: reescríbelas tú)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("LIMPIO")
        print("  No hay nada que quitar.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Quita la huella de máquina de un borrador.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para stdin")
    ap.add_argument("-o", "--out", help="escribe el texto limpio acá en vez de la salida estándar")
    ap.add_argument("--report", action="store_true", help="imprime qué cambió, por stderr")
    ap.add_argument("--json", action="store_true", help="devuelve {text, report} como JSON")
    ap.add_argument("--lexicon", default=LEX, help="ruta a slop.json")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"escrito {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
