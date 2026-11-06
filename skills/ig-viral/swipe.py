#!/usr/bin/env python3
"""
swipe.py - ordena los reels que juntaste según cuánto le ganaron a su propia
cuenta, nombra la fórmula de gancho de cada uno y escribe el archivo de
referencias.

Adaptado al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol). Acepta las columnas en español o en inglés.

El punto de este script es una sola corrección: las vistas brutas no son
evidencia. Una cuenta de 2.000.000 de seguidores con 400.000 vistas tuvo un día
tranquilo. Una de 4.000 seguidores con 400.000 vistas encontró algo. Esto
ordena por el múltiplo sobre la base de la propia cuenta, que es la única
versión de «se hizo viral» que te dice algo que puedas copiar.

La entrada es un archivo separado por tabulaciones que llenas mientras miras,
un reel por fila, con una línea de encabezado:

    cuenta    seguidores   mediana   vistas   gancho
    @alguien  48000        11000     412000   nadie te dice que el primer semestre es el peor

`mediana` son las vistas típicas recientes de esa cuenta y es la mejor base. Si
solo tienes `seguidores`, deja fuera la mediana y el script lo avisa. `gancho`
es la primera línea del reel, hablada o en pantalla, con sus palabras.

Uso
  python3 swipe.py capturados.tsv
  python3 swipe.py capturados.tsv --out ~/.claude/instagram/CUENTA/swipe.md
  python3 swipe.py capturados.tsv --json
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(HERE, "..", "ig-reel", "hooks.json")
WORD_RE = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9$%'’-]+")

try:                                              # opcional: también puntúa los ganchos
    sys.path.insert(0, os.path.join(HERE, "..", "ig-reel"))
    from hookscore import run as score_hook       # noqa: E402
except Exception:                                 # ig-viral copiado solo
    score_hook = None


def load_formulas(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        return None
    by_id = {h["id"]: h for h in d["hooks"]}
    order = d.get("classify_order") or sorted(by_id)
    return [(by_id[i]["id"], by_id[i]["name"],
             re.compile(by_id[i]["match"], re.IGNORECASE)) for i in order if i in by_id]


def classify(hook, formulas):
    if not formulas:
        return None, "sin clasificar"
    for fid, name, pattern in formulas:
        if pattern.search(hook):
            return fid, name
    return None, "sin clasificar"


def read_rows(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    ALIAS = {"cuenta": "account", "seguidores": "followers", "mediana": "median",
             "vistas": "views", "gancho": "hook", "largo": "length", "pantalla": "on-screen"}
    head = [ALIAS.get(c.strip().lower(), c.strip().lower()) for c in lines[0].split("\t")]
    if "views" in head and "hook" in head:
        cols, body = head, lines[1:]
    else:
        cols, body = ["account", "followers", "views", "hook"], lines
    rows = []
    for line in body:
        cells = line.split("\t")
        if len(cells) < len(cols):
            cells += [""] * (len(cols) - len(cells))
        r = dict(zip(cols, [c.strip() for c in cells]))
        try:
            r["views"] = int(re.sub(r"[^\d]", "", r.get("views", "")) or 0)
        except ValueError:
            continue
        for k in ("followers", "median"):
            digits = re.sub(r"[^\d]", "", r.get(k, "") or "")
            r[k] = int(digits) if digits else None
        if r["views"] and r.get("hook"):
            rows.append(r)
    return rows


def analyse(rows, formulas):
    used_median = any(r.get("median") for r in rows)
    for r in rows:
        base = r.get("median") or r.get("followers") or 0
        r["baseline"] = base
        r["outlier"] = round(r["views"] / base, 2) if base else None
        r["formula_id"], r["formula"] = classify(r["hook"], formulas)
        r["words"] = len(WORD_RE.findall(r["hook"]))
        if score_hook:
            _, overall, verdict, _ = score_hook(r["hook"])
            r["hook_score"], r["hook_verdict"] = round(overall, 1), verdict
        else:
            r["hook_score"], r["hook_verdict"] = None, None
    ranked = sorted(rows, key=lambda r: -(r["outlier"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def med(items, key):
        vals = [i[key] for i in items if i.get(key) is not None]
        return round(statistics.median(vals), 1) if vals else None

    counts = {}
    for r in top:
        counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    return {
        "baseline": "mediana de la cuenta" if used_median else "seguidores",
        "n": len(ranked),
        "accounts": len({r.get("account", "") for r in ranked}),
        "reels": ranked,
        "top_formulas": sorted(counts.items(), key=lambda kv: -kv[1]),
        "top_hook_score": med(top, "hook_score"),
        "bottom_hook_score": med(bottom, "hook_score"),
        "top_words": med(top, "words"),
        "bottom_words": med(bottom, "words"),
        "unclassified": sum(1 for r in ranked if r["formula"] == "sin clasificar"),
    }


def render(a, out=sys.stdout):
    head = (f"REFERENCIAS  ·  {a['n']} reels  ·  {a['accounts']} cuentas  ·  "
            f"base: {a['baseline']}")
    print("\n" + head, file=out)
    print("=" * max(len(head), 78), file=out)
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x".replace(".", ",") if r["outlier"] else "   ?"
        score = f"{r['hook_score']:.0f}" if r["hook_score"] is not None else " -"
        fid = f"#{r['formula_id']:<2}" if r["formula_id"] else "-  "
        vistas = f"{r['views']:,}".replace(",", ".")
        print(f"  {mult:>7}  gancho {score:>3}  {fid} {r['formula'][:22]:<22} "
              f"{r.get('account', '')[:16]:<16} {vistas:>9}", file=out)
        print(f"           «{r['hook'][:96]}»", file=out)
    print("-" * max(len(head), 78), file=out)
    print("QUÉ ESTÁ FUNCIONANDO EN ESTE LOTE", file=out)
    if a["top_formulas"]:
        print("  tercio de arriba:         "
              + ", ".join(f"{n} x{c}" for n, c in a["top_formulas"][:4]), file=out)
    if a["top_hook_score"] is not None:
        print(f"  puntaje mediano gancho:   arriba {a['top_hook_score']:.0f}  "
              f"vs abajo {a['bottom_hook_score']:.0f}", file=out)
    print(f"  largo mediano del gancho: arriba {a['top_words']} palabras  "
          f"vs abajo {a['bottom_words']} palabras".replace(".", ","), file=out)
    print(f"  sin clasificar:           {a['unclassified']} de {a['n']}. Léelos a mano: "
          "ahí se esconde una fórmula que todavía no tienes.", file=out)
    print("\n  Un lote juntado a mano es evidencia, no prueba. Doce reels no muestran "
          "nada;\n  cuarenta de seis cuentas muestran algo. Junta más antes de creerlo.\n", file=out)


def to_markdown(a):
    lines = ["# Referencias", "",
             f"{a['n']} reels de {a['accounts']} cuentas. "
             f"Ordenados por múltiplo sobre {a['baseline']}.", ""]
    miles = lambda n: f"{n:,}".replace(",", ".")
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x".replace(".", ",") if r["outlier"] else "?"
        lines += [f"## {mult}  {r['formula']}  ({r.get('account', '')})",
                  f"- vistas: {miles(r['views'])}  base: {miles(r['baseline'])}",
                  f"- puntaje del gancho: {str(r['hook_score']).replace('.', ',')}  palabras: {r['words']}",
                  f"- gancho: «{r['hook']}»", ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Ordena los reels juntados por múltiplo sobre su cuenta.")
    ap.add_argument("input", nargs="?", default="-", help="archivo TSV, o - para stdin")
    ap.add_argument("--hooks", default=HOOKS, help="ruta a ig-reel/hooks.json")
    ap.add_argument("--out", help="además escribe las referencias en markdown acá")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = read_rows(args.input)
    if not rows:
        print("no hay filas usables. Hace falta un archivo separado por tabulaciones con al menos vistas y gancho.",
              file=sys.stderr)
        sys.exit(2)
    formulas = load_formulas(args.hooks)
    a = analyse(rows, formulas)
    if not formulas:
        print("ojo: no se encontró hooks.json, las fórmulas quedan sin nombre. Usa --hooks.", file=sys.stderr)
    if score_hook is None:
        print("ojo: no se pudo importar hookscore.py, se omiten los puntajes.", file=sys.stderr)

    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    if args.out:
        path = os.path.expanduser(args.out)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(to_markdown(a))
        print(f"escrito {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
