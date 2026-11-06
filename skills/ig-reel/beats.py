#!/usr/bin/env python3
"""
beats.py - convierte el guion de un reel en una hoja de escenas con tiempos,
antes de grabarlo.

Adaptado al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol).

Estima cuánto se demora en decirse cada línea, las apila en códigos de tiempo y
marca las cuatro cosas que matan un reel en la edición: un gancho que pasa los
tres segundos, una escena tan larga que la gente se va, una seguidilla de
líneas sin nada concreto, y un largo total que no calza con lo que dijiste que
ibas a hacer.

Los tiempos salen de contar palabras a un ritmo de palabras por minuto. Sirven
para planificar la edición, no reemplazan grabarlo. Ajusta tu ritmo con --wpm
cuando te hayas cronometrado leyendo un guion en voz alta: en español la
mayoría queda entre 140 y 190, y acá el valor por defecto es 160.

Uso
  python3 beats.py guion.txt
  python3 beats.py guion.txt --target 30
  python3 beats.py guion.txt --wpm 175 --target 45
  pbpaste | python3 beats.py -
  python3 beats.py guion.txt --json
"""

import argparse
import json
import re
import sys

LETRAS = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
WORD_RE = re.compile(rf"[{LETRAS}0-9$%'’-]+")
SENT_RE = re.compile(r"[^.!?]+[.!?]*")
CONCRETE_RE = re.compile(r"\$\s?\d|\b\d[\d.,]*\b|(?<![¿¡])(?<![.!?:]\s)(?<!^)\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}\b", re.MULTILINE)
# Un guion se escribe como se dice: "dos años" es tan concreto como "2 años".
NUMEROS_DICHOS = re.compile(
    r"(?i)\b(?:dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|quince|veinte|"
    r"treinta|cuarenta|cincuenta|cien|mil|millones?|mitad|doble|lunes|martes|miércoles|jueves|"
    r"viernes|sábado|domingo|enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|"
    r"octubre|noviembre|diciembre)\b")
STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "pero", "si",
    "de", "del", "a", "al", "en", "con", "por", "para", "que", "qué", "es", "son",
    "era", "fue", "ser", "está", "esta", "este", "esto", "eso", "ese", "esa",
    "tú", "tu", "te", "yo", "me", "mi", "nos", "se", "le", "les", "lo", "su",
    "sus", "no", "ya", "más", "mas", "muy", "como", "cómo", "hay", "uno",
    "todo", "todos", "cuando", "sí", "así", "también",
}

HOOK_WINDOW = 3.0        # segundos. Pasado esto, el pulgar ya decidió.
MAX_BEAT = 4.0           # segundos en una idea sin que cambie nada en pantalla.
ABSTRACT_RUN = 3         # escenas seguidas sin nada verificable.


def words(text):
    # "$18.000" se dice como una palabra, así que acá también es una.
    return WORD_RE.findall(re.sub(r"(?<=\d)\.(?=\d{3}\b)", "", text))


def pretty(token):
    """Devuelve el punto de miles para mostrar."""
    return re.sub(r"(\d)(?=(\d{3})+$)", r"\1.", token)


def dec(n):
    return f"{n:.1f}".replace(".", ",")


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}".replace(".", ",")


def split_beats(raw, wps):
    """Una línea es una escena, salvo que sea demasiado larga para serlo."""
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if len(words(line)) / wps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        # Párrafo largo: se corta donde terminan las oraciones para que los
        # tiempos signifiquen algo.
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            candidate = (buf + " " + part).strip()
            if buf and len(words(candidate)) / wps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, wpm=160, target=None):
    wps = wpm / 60.0
    beats = split_beats(raw, wps)
    if not beats:
        return None

    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        n = len(words(text))
        dur = n / wps
        rows.append({
            "n": i + 1,
            "start": round(clock, 2),
            "dur": round(dur, 2),
            "words": n,
            "text": text,
            "concrete": len(CONCRETE_RE.findall(text)) + len(NUMEROS_DICHOS.findall(text)),
            "label": "",
            "flags": [],
        })
        clock += dur
    total = clock

    # Las posiciones sobre las que de verdad se arma un reel.
    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "GANCHO"
    rows[-1]["label"] = "CIERRE" if rows[-1]["label"] != "GANCHO" else "GANCHO/CIERRE"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "MITAD"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"el gancho dura {dec(rows[0]['dur'])}s, pasa los {HOOK_WINDOW:.0f}s")
        notes.append(f"La escena 1 se demora {dec(rows[0]['dur'])}s en decirse. Déjala en "
                     f"{int(HOOK_WINDOW * wps)} palabras o menos, o el gancho llega después "
                     "de que la persona ya decidió.")
    if rows[0]["concrete"] == 0:
        notes.append("La escena 1 no tiene ni un número ni un nombre. Los ganchos sin algo "
                     "verificable son los que se pasan de largo.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{dec(r['dur'])}s en una sola escena")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(f"Las escenas {', '.join(map(str, long_beats))} pasan los {MAX_BEAT:.0f}s. "
                     "Corta la línea o cambia lo que se ve en pantalla dentro de ella. "
                     "Un cuadro quieto es donde la gente se va.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"Las escenas {start}-{r['n']} no tienen nada concreto. "
                             "Pon un número, un nombre o un monto en alguna.")
        else:
            run, start = 0, None

    # ¿La última línea te devuelve a la primera?
    first = {w.lower() for w in words(rows[0]["text"]) if w.lower() not in STOPWORDS}
    last = {w.lower() for w in words(rows[-1]["text"]) if w.lower() not in STOPWORDS}
    loop = sorted(pretty(w) for w in first & last)
    if loop:
        notes.append(f"Hace loop: la última escena repite «{', '.join(loop[:3])}» del gancho. "
                     "La segunda vista es alcance gratis.")
    else:
        notes.append("Sin loop. La última escena no comparte ninguna palabra con el gancho, "
                     "así que el video termina plano. Repetir una palabra de la escena 1 es "
                     "la segunda vista más barata que hay.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"El largo está en la meta ({dec(total)}s contra {target:g}s).")
        elif delta > 0:
            notes.append(f"{dec(delta)}s sobre la meta. Corta unas {int(delta * wps)} palabras.")
        else:
            notes.append(f"{dec(-delta)}s bajo la meta. Agrega {int(-delta * wps)} palabras "
                         "o grábalo más corto. Más corto suele ser lo correcto.")

    return {
        "wpm": wpm, "target": target,
        "total_seconds": round(total, 2),
        "total_words": sum(r["words"] for r in rows),
        "beats": rows,
        "notes": notes,
    }


def render(a, out=sys.stdout):
    head = (f"HOJA DE ESCENAS  ·  {a['total_words']} palabras  ·  ~{dec(a['total_seconds'])}s "
            f"a {a['wpm']:g} ppm" + (f"  ·  meta {a['target']:g}s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<14}" if r["label"] else " " * 14
        print(f"  {tc(r['start'])}  {dec(r['dur']):>4}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<14}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Convierte un guion de reel en hoja de escenas con tiempos.")
    ap.add_argument("input", nargs="?", default="-", help="archivo del guion, o - para stdin")
    ap.add_argument("--wpm", type=float, default=160, help="ritmo al hablar, palabras por minuto (160)")
    ap.add_argument("--target", type=float, help="largo meta en segundos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, wpm=args.wpm, target=args.target)
    if not a:
        print("guion vacío", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
