# Instagram en español de Chile

Trece skills de Claude para llevar una cuenta de Instagram. Adaptación al
español de Chile de [instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill)
(MIT, Jake Schincariol).

Las comparte [@recomendai_cl](https://www.instagram.com/recomendai_cl/), gratis.

**No publican nada.** Escriben, puntúan y ordenan. La persona publica.

## Qué cambió respecto del original

No es una traducción de las guías: los cinco scripts dependían del inglés y se
reescribieron para el español.

| | original | esta versión |
| --- | --- | --- |
| Letras | `A-Za-z`: «también» se partía en dos | tildes, eñe, ¿ y ¡ |
| Montos | `$18,000` | `$1.800.000`, «18 lucas», «dos millones» |
| Concreción | nombres propios con mayúscula | también días y meses, que en español van en minúscula |
| Primera persona | «I», «my» | también el verbo sin pronombre: «Perdí», «Estudié» |
| Chequeo de VOZ | cuenta contracciones | cuenta oralidad (¿? ¡! y muletillas): el español no tiene contracciones |
| Saludos y preámbulos | «hey guys», «in this video» | «hola a todos», «hoy les queremos contar», «en este video te voy a mostrar» |
| Léxico de relleno | 154 frases en inglés | 165 propias del español: «cabe destacar», «potenciar», «tu futuro empieza hoy» |
| Estructuras | «it's not just X, it's Y» | «no es solo X, es Y», «no se trata de X», «Imagina que...» |
| Fórmulas de gancho | 26 con ejemplos gringos | las mismas 26, con plantillas, ejemplos y reconocimiento en español |
| Hashtags genéricos | #fyp, #explorepage | también #parati, #explorar, #chile, #motivacion |
| Cuentas | un solo `voice.md` | una carpeta por cuenta; nunca se mezclan cifras entre cuentas |
| Ritmo al hablar | 165 ppm | 160 ppm por defecto |

Se agregaron reglas que el original no tenía: no prometer lo que una cuenta
regulada no puede prometer (en educación: empleabilidad, sueldos, becas sin
condiciones), las reglas vigentes de la respuesta privada a un comentario, y
cuidado con los datos personales que la gente deja en los comentarios.

## Lo que NO se ha medido

El original midió su puntaje de ganchos contra 74 ganchos reales en inglés:
separa bien un gancho malo de uno real (AUC 0,83) y casi nada un acierto de un
fracaso del mismo creador (AUC 0,56). **Esta versión no se ha medido contra
ganchos reales en español.** Los umbrales vienen del original. Úsala para lo que
sí sirve: descartar ganchos con saludo, preámbulo o sin nada concreto. Cuál de
dos ganchos buenos viaja más lo dice la retención de la cuenta, no un script.

## Las trece

| comando | qué hace |
| --- | --- |
| `/ig-reel` | una idea a un reel: tres ganchos puntuados, guion, texto en pantalla y hoja de escenas con tiempos |
| `/ig-viral` | busca qué funciona en el rubro y lo ordena por múltiplo sobre la propia cuenta |
| `/ig-caption` | el texto del post, revisado: muestra los 125 caracteres que se ven antes del «... más» |
| `/ig-carousel` | carruseles: portada, texto por lámina y archivos de 1080x1350 |
| `/ig-story` | la secuencia de historias del día y el embudo a DM |
| `/ig-profile` | puntaje del perfil sobre 100 y reescritura en orden de arreglo |
| `/ig-plan` | la semana: qué, en qué formato, cuándo, y con quién interactuar |
| `/ig-human` | el humanizador: dos scripts que corren |
| `/ig-comment` | comentarios en posts ajenos, nueve tipos |
| `/ig-reply` | los comentarios del propio post, clasificados antes de responder |
| `/ig-dm` | entrega por palabra clave, primer mensaje, colaboración, dos seguimientos |
| `/ig-repurpose` | un material largo a una semana de reels y carruseles |
| `/ig-audit` | qué funcionó de lo publicado, por múltiplo y envíos, no por vistas |

## Instalar

En Claude Code, dos comandos:

```
/plugin marketplace add critec553/instagram-es
/plugin install instagram-agent-es@instagram-agent-es
```

O a mano, copiando las carpetas:

```bash
git clone https://github.com/critec553/instagram-es
cp -r instagram-es/skills/ig-* ~/.claude/skills/
```

Después crea una carpeta por cuenta y llena su voz:

```bash
mkdir -p ~/.claude/instagram/NOMBRE-DE-LA-CUENTA
cp templates/voice.md ~/.claude/instagram/NOMBRE-DE-LA-CUENTA/voice.md
```

## Las herramientas

Sin dependencias y sin red: corren en la máquina, sobre el texto.

```bash
python3 skills/ig-reel/hookscore.py ganchos.txt
python3 skills/ig-reel/beats.py guion.txt --target 30
python3 skills/ig-caption/caption.py texto.txt --keywords "carreras online"
python3 skills/ig-human/humanize.py borrador.txt --report
python3 skills/ig-human/detect.py antes.txt despues.txt
python3 skills/ig-viral/swipe.py capturados.tsv
```

## Comprobar que funciona

```bash
python3 pruebas/probar.py
```

30 comprobaciones: que no se rompe con tildes ni con `$1.800.000`, que pilla
saludos, preámbulos y relleno, que no toca links, y que las 26 fórmulas se
reconocen a sí mismas.

## Licencia

MIT, como el original. El aviso de copyright de Jake Schincariol está en
`LICENSE` y se mantiene.
