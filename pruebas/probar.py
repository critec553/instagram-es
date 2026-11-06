#!/usr/bin/env python3
"""
probar.py - comprueba que las cinco herramientas funcionan en español.

No mide si los puntajes predicen vistas: eso no se ha medido. Comprueba que
las herramientas no se rompen con tildes, eñes, ¿¡ y "$1.800.000", que pillan
lo que dicen pillar, y que las 26 fórmulas se reconocen a sí mismas.

Uso
  python3 pruebas/probar.py
"""

import importlib.util
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(RAIZ, "skills")


def cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, os.path.join(SK, ruta))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fallas = []


def comprobar(descripcion, condicion, detalle=""):
    print(f"  {'OK   ' if condicion else 'FALLA'}  {descripcion}" + (f"  ({detalle})" if detalle and not condicion else ""))
    if not condicion:
        fallas.append(descripcion)


hs = cargar("hookscore", "ig-reel/hookscore.py")
bt = cargar("beats", "ig-reel/beats.py")
cp = cargar("caption", "ig-caption/caption.py")
dt = cargar("detect", "ig-human/detect.py")
hm = cargar("humanize", "ig-human/humanize.py")
sw = cargar("swipe", "ig-viral/swipe.py")
lex = json.load(open(os.path.join(SK, "ig-human/slop.json"), encoding="utf-8"))
hooks = json.load(open(os.path.join(SK, "ig-reel/hooks.json"), encoding="utf-8"))

print("\nhookscore.py")
_, bueno, v_bueno, _ = hs.run("Me costó $1.800.000 no leer una sola cláusula del contrato.")
_, saludo, _, flags_saludo = hs.run("Hola a todos, hoy les quiero contar sobre nuestras carreras")
_, preambulo, _, flags_pre = hs.run("En este video te voy a mostrar cómo organizar tu semana")
_, plano, _, _ = hs.run("La educación es importante para el futuro")
comprobar("un gancho concreto con monto chileno sale FUERTE", v_bueno == "FUERTE", f"{bueno:.1f} {v_bueno}")
comprobar("el saludo se descalifica", any("Saludo" in f for f in flags_saludo))
comprobar("el preámbulo se descalifica", any("Preámbulo" in f for f in flags_pre))
comprobar("el gancho plano sale bajo 50", plano < 50, f"{plano:.1f}")
comprobar("$1.800.000 cuenta como una palabra", len(hs.words("Me costó $1.800.000")) == 3)
comprobar("«también» es una sola palabra", hs.words("también") == ["también"])
r, _, _, _ = hs.run("Perdí un semestre por no leer el reglamento")
comprobar("«Perdí» se reconoce como primera persona", r["A QUIÉN"][0] == 70.0, r["A QUIÉN"][1])

print("\nbeats.py")
a = bt.analyse("Estudié de noche dos años mientras trabajaba en una bodega.\n"
               "Un domingo anoté todo en una sola hoja.\n"
               "Así terminé los dos años sin congelar ningún semestre.", wpm=160, target=30)
comprobar("detecta el loop por «años»", any("loop" in n.lower() and "años" in n for n in a["notes"]))
comprobar("el gancho de 10 palabras pasa los 3 segundos", a["beats"][0]["dur"] > 3.0)
comprobar("«dos años» cuenta como concreto", a["beats"][0]["concrete"] >= 1)

print("\ncaption.py")
malo = cp.analyse("Hola a todos! Hoy les queremos contar algo 🚀\nSíguenos y link en la bio.\n"
                  "#educacion #online #estudiar #chile #viral #parati #futuro")
estado = {c["check"]: c["status"] for c in malo["checks"]}
comprobar("reprueba el saludo en la primera línea", estado["PRIMERA LÍNEA"] == "FALLA")
comprobar("reprueba 7 hashtags", estado["HASHTAGS"] == "FALLA")
comprobar("cuenta dos acciones", len(malo["asks"]) == 2, malo["asks"])
bien = cp.analyse("Comenta BECA y te mandamos el requisito que casi nadie revisa.\n\n#estudiaronline")
comprobar("«Comenta BECA» es una sola acción", bien["asks"] == ["comentar una palabra"], bien["asks"])
comentar_si = cp.analyse("Comenta si te pasó algo parecido.")
comprobar("«comenta si» no se confunde con palabra clave", "comentar una palabra" not in comentar_si["asks"])
comprobar("un hashtag con tilde se reconoce", cp.analyse("Texto.\n#educación")["hashtags"] == ["#educación"])

print("\nhumanize.py + detect.py")
borrador = ("Imagina que puedes estudiar desde cualquier lugar. En el mundo actual, estudiar online "
            "no es solo una opción, es una necesidad.\n\nCabe destacar que nuestra propuesta innovadora "
            "te permite potenciar tus habilidades — todo desde la comodidad de tu hogar. Sin lugar a "
            "dudas, es una oportunidad única.\n\nNo te lo pierdas. ¡¡Tu futuro empieza hoy!! Síguenos "
            "para más contenido y etiqueta a alguien que necesite esto.\n")
limpio, informe = hm.humanize(borrador, lex)
comprobar("quita la raya", "—" not in limpio)
comprobar("quita «cabe destacar»", "cabe destacar" not in limpio.lower())
comprobar("no deja signos vacíos «¡!»", "¡!" not in limpio and "¡¡" not in limpio)
comprobar("no deja «., »", "., " not in limpio, limpio)
comprobar("marca «no es solo X, es Y»", any("No es solo" in s["name"] for s in informe["structures"]))
comprobar("marca «Imagina que»", any("Imagina" in s["name"] for s in informe["structures"]))
r_antes, antes, _ = dt.run(borrador, lex)
r_despues, despues, _ = dt.run(limpio, lex)
# Limpiar no agrega números: CONCRECIÓN sigue en cero y pone techo al total.
# Lo que sí tiene que pasar es que RELLENO y HUELLA queden limpios y el total suba.
comprobar("RELLENO y HUELLA quedan en 100 después de limpiar",
          r_despues["RELLENO"][0] == 100 and r_despues["HUELLA"][0] == 100)
comprobar("el puntaje humano sube después de limpiar", despues > antes, f"{antes:.1f} -> {despues:.1f}")
url = hm.humanize("Revisa https://www.ejemplo.cl/sede—online hoy.\n", lex)[0]
comprobar("no toca los links", "https://www.ejemplo.cl/sede—online" in url, url)

print("\nhooks.json + swipe.py")
by = {h["id"]: h for h in hooks["hooks"]}
propias = 0
for h in hooks["hooks"]:
    got = next((i for i in hooks["classify_order"] if re.search(by[i]["match"], h["example"], re.IGNORECASE)), None)
    propias += got == h["id"]
comprobar("las 26 fórmulas reconocen su propio ejemplo", propias == 26, f"{propias}/26")
formulas = sw.load_formulas(os.path.join(SK, "ig-reel/hooks.json"))
comprobar("clasifica una pregunta textual", sw.classify("¿Se puede estudiar enfermería online?", formulas)[1] == "La pregunta textual")
comprobar("un saludo queda sin clasificar", sw.classify("Hola chiquillos, hoy les traigo algo", formulas)[1] == "sin clasificar")

print("\nslop.json")
finds = [e["find"].lower() for e in lex["words"] + lex["phrases"]]
comprobar("sin entradas duplicadas", len(finds) == len(set(finds)))
comprobar("todas las estructuras compilan", all(re.compile(s["regex"]) for s in lex["structures"]))

print(f"\n{'Todo OK.' if not fallas else str(len(fallas)) + ' falla(s): ' + '; '.join(fallas)}\n")
sys.exit(1 if fallas else 0)
