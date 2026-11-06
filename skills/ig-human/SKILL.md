---
name: ig-human
description: >-
  Quita la huella de máquina de cualquier borrador en español (rayas, palabras
  de relleno de IA, caracteres invisibles) y lo puntúa con un panel de cinco
  chequeos antes de publicar. Úsala siempre que un texto tenga que sonar
  humano, cuando digan «humaniza esto», «¿suena a IA?», «saca las rayas»,
  «esto suena a ChatGPT», o antes de mostrar cualquier texto, guion,
  comentario, respuesta o DM.
---

# ig-human

Adaptada al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol). En esta carpeta hay dos herramientas y las dos corren. Úsalas: no
lo hagas a ojo.

```bash
python3 humanize.py borrador.txt --report        # limpia y muestra qué cambió
python3 detect.py borrador.txt                    # puntúa, cinco chequeos
python3 detect.py antes.txt despues.txt           # demuestra la diferencia
```

Las dos leen `slop.json`: unas 160 palabras y frases de relleno en español con
reemplazos simples, 18 tipos de caracteres invisibles, 13 cambios tipográficos
y 18 señales estructurales. El último bloque de frases es de Instagram. Está
hecho para editarse: si la cuenta usa siempre una palabra que el léxico cambia,
sácala del archivo.

## Qué cambió respecto del original en inglés

- **Letras con tilde y eñe** cuentan como letras. En el original, «también» se
  partía en dos palabras.
- **El chequeo de VOZ ya no cuenta contracciones**, porque el español no las
  tiene. Cuenta marcas de oralidad: preguntas y exclamaciones con su signo de
  apertura, y muletillas de conversación («igual», «ojo», «harto», «la verdad»).
- **Las comillas angulares («»)** cuentan como huella tipográfica igual que las
  curvas.
- **La raya (—)** sigue marcándose. En español impreso es tipografía correcta,
  pero nadie la escribe desde el teléfono en un post y los modelos la ponen en
  cada párrafo. Si la cuenta la usa de verdad, sácala de `slop.json`.
- **El léxico es propio del español**, no una traducción: «cabe destacar»,
  «potenciar», «en el mundo actual», «un antes y un después», «tu futuro empieza
  hoy», «no te lo pierdas», «síguenos para más». Los reemplazos que cambiaban
  de género («integral» → «completo») se sacaron para no romper la
  concordancia.

## Por qué importa más en Instagram de lo que parece

Los textos son cortos y los guiones se dicen en voz alta. Una línea que suena a
escrita pesa más en un texto de 600 caracteres que en un ensayo, y una voz en
off que nadie diría natural se nota en la primera toma. La señal acá no es que
un detector marque el post: es alguien que pasa de largo porque se lee como
folleto, o alguien que se tropieza con su propio guion.

## Lo que se arregla solo

**1. Caracteres invisibles.** Espacios de ancho cero, unidores, guiones
blandos, BOM, caracteres de etiqueta Unicode, separadores invisibles, espacios
duros y angostos. Un teclado no los produce, sobreviven al copiar y pegar, y
son lo más mecánico de un texto generado. `humanize.py` los borra todos.

**2. Tipografía.** Raya a coma, guion medio a guion, comillas curvas y
angulares a rectas, puntos suspensivos de un carácter a tres puntos, viñeta a
guion. Después limpia la puntuación doble y los puntos huérfanos que eso deja.

**3. El léxico de relleno.** Cada entrada se cambia por una palabra simple o se
borra, respetando mayúsculas y sin tocar los links. Después de borrar, limpia
los signos que quedan vacíos («¡!») y las conjunciones colgando al final
(«contenido y.»).

## Lo que NO se arregla solo

Las señales estructurales se **marcan, no se reescriben**, porque cambiar la
forma de una oración pide criterio:

- «No es solo X, es Y» y «no solo X, sino también Y»
- «No se trata de X. Se trata de Y.»
- Tríadas de tres
- Preguntas retóricas solas en una línea: «¿El resultado?»
- El preámbulo de video: «en este video te voy a mostrar»
- La apertura «Imagina que...»
- Listas con emojis como viñetas
- Tres o más palabras gritadas seguidas, y exclamaciones dobles
- Muros de hashtags
- Carnada por reflejo: «síguenos para más», «etiqueta a alguien», «comenta si»

Esa lista es tu trabajo. Reescribe cada línea marcada a mano, manteniendo el
sentido, y vuelve a correr `detect.py`. Esa es la parte que mueve el puntaje de
REVISAR a PASA, y es la que un script no puede hacer.

## Los cinco chequeos

`detect.py` puntúa cinco señales de 0 a 100, más alto es más humano:

| chequeo | qué mide | una máquina se ve así |
| --- | --- | --- |
| VARIACIÓN | variación del largo de las oraciones | todas del mismo largo |
| CONCRECIÓN | números, nombres, cosas concretas cada 100 palabras | sustantivos abstractos, sin cifras |
| RELLENO | palabras del léxico cada 100 palabras | vocabulario de folleto |
| HUELLA | invisibles, rayas, comillas tipográficas cada 1.000 caracteres | tipografía perfecta |
| VOZ | oralidad, persona, señales estructurales | sin preguntas, sin «tú», revelaciones montadas |

El veredicto pondera el promedio al 60% y **el chequeo más débil** al 40%,
porque con una señal basta. PASA pide 70 o más en total y ningún chequeo bajo
55.

## Dilo con honestidad

Son cinco heurísticas locales basadas en las señales que miran los detectores
públicos. Corren enteras en la máquina y no se sube nada. **No** son GPTZero,
Originality, Copyleaks, Winston ni Turnitin, no llaman a sus APIs y no pueden
prometer su veredicto. Arreglar lo que miden suele mover esos números, porque
miden lo mismo de fondo. Esa es la afirmación. No hagas una más grande en
nombre de nadie, y nunca digas que un texto es indetectable.

Y una más: esta versión en español no se ha calibrado contra un corpus propio.
Los umbrales vienen del original en inglés. Si un texto claramente humano sale
marcado, anota el caso: es información para ajustar.

## Orden de trabajo

1. `humanize.py borrador.txt -o limpio.txt --report`
2. Lee las señales estructurales. Reescribe esas líneas tú.
3. `detect.py borrador.txt limpio.txt` para mostrar el antes y el después.
4. Si el veredicto no es PASA, arregla el chequeo más débil que indica la
   salida y repite. Dos vueltas es normal. Cinco significa que el borrador se
   escribió con fórmula, y el arreglo es otro borrador, no más vueltas.
5. Muestra el texto limpio y el puntaje. Nunca el puntaje solo.
