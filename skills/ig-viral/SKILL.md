---
name: ig-viral
description: >-
  Busca los reels que de verdad están funcionando ahora en el rubro de la
  cuenta, los ordena según cuánto le ganaron a su propia cuenta, nombra la
  fórmula de gancho de cada uno y arma un archivo de referencias para grabar.
  En español de Chile. Úsala cuando digan «busca videos virales», «qué está
  funcionando», «qué publica la competencia», «analiza esta cuenta», «arma
  referencias», «por qué le fue tan bien a este reel», o pregunten qué hacer
  después sin evidencia para responder.
---

# ig-viral

La skill de investigación. Todo lo demás del paquete escribe; esta sale a
mirar. Córrela una vez al mes, no todos los días: las fórmulas duran una
temporada.

Adaptada al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol). En esta carpeta hay una herramienta y corre:

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/CUENTA/swipe.md
```

## La única idea que hace que valga la pena

**Las vistas brutas no son evidencia.** Una cuenta de dos millones de
seguidores con 400.000 vistas tuvo un martes tranquilo. Una de cuatro mil con
400.000 vistas encontró algo, y ese algo se puede copiar.

Por eso todo acá se ordena por el **múltiplo**: vistas divididas por la mediana
reciente de esa misma cuenta. Sobre 3x es señal. Bajo 1,5x es un día normal de
esa cuenta y no enseña nada, por grande que se vea el número.

Junta cuentas **hasta unas 10 veces el tamaño de la propia**. Una fórmula que
funciona con 2 millones de seguidores muchas veces funciona porque tiene 2
millones.

## Paso 0: la cuenta

Mira `~/.claude/instagram/` y decide para qué cuenta es la investigación. El
archivo de referencias va en su carpeta. Si hay varias cuentas y no está claro,
pregunta.

## Paso 1: elige las cuentas

Pide entre 6 y 12 cuentas, o propónlas y pide aprobación:

- **4 directas**: mismo rubro, misma oferta, un poco más adelante.
- **4 vecinas**: otro rubro, misma audiencia. De acá se sacan formatos antes de
  que alguien del rubro los tenga. Para una audiencia adulta que trabaja y
  estudia: cuentas de finanzas personales, de productividad, de cambio de
  carrera.
- **2 a 4 grandes**: mucho más grandes, solo para ver formato, nunca para
  frecuencia ni tono.

Pide también que abra su colección de **Guardados**. Es el corpus más rápido y
relevante que existe y ya viene filtrado por su gusto.

## Paso 2: sal a mirar

Usa la herramienta de navegación que esta sesión tenga de verdad: un navegador
integrado, una extensión conectada al Chrome de la persona, o control del
computador. No hay API para esto y no hace falta, porque el volumen es chico.

**Reglas que no se negocian:**

- **Nunca inicies sesión en Instagram en nombre de la persona ni pidas una
  contraseña.** Si una página pide login, la sesión abierta es la de la persona.
  Maneja su navegador con ella presente, o pídele que pegue los datos.
- **Esto es leer, no raspar.** Diez cuentas, una docena de reels cada una, a
  velocidad humana. Recolectar en volumen de forma automática viola las
  Condiciones de Uso de Instagram y bloquea cuentas. No armes un crawler, no uses
  un servicio de scraping, no lo dejes corriendo de fondo.
- **Copia la fórmula, nunca el video.** La forma del gancho, la estructura, el
  largo, el patrón de cortes. No su guion, no su voz, no su edición. Atribuye
  cada fila del archivo a la cuenta de donde salió.

**Qué anotar de cada reel**, con las palabras del creador:

| campo | notas |
| --- | --- |
| cuenta | usuario |
| seguidores | del perfil |
| mediana | mira los últimos 12 reels y toma las vistas del medio |
| vistas | de este reel |
| gancho | la primera línea, hablada o en pantalla, textual, con errores y todo |
| pantalla | la primera tarjeta de texto, si es distinta |
| largo | segundos |
| acción | qué pidió al final |

La mediana es la importante. Sin ella vuelves a ordenar por seguidores, que es
justo lo que esta skill existe para evitar.

**Cuando Instagram no muestra suficiente:** la misma gramática de ganchos corre
en YouTube Shorts, donde las vistas y las transcripciones son públicas y no hay
login. Es un segundo corpus legítimo:

```bash
# vistas de los shorts de un canal
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@CANAL/shorts" > canal.json

# la primera línea hablada de un short, desde sus subtítulos automáticos
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "es.*" \
  --sub-format json3 -o gancho "https://www.youtube.com/watch?v=ID_DEL_VIDEO"
```

Toma cada palabra de los subtítulos con marca de tiempo bajo 3,0 segundos. Ese
es el gancho, como se dijo, no como se escribió.

Para formatos de anuncios pagados, la **Biblioteca de Anuncios de Meta** es
pública y no pide login. Sirve para ver qué piezas mantiene activas la
competencia hace semanas, que es la mejor señal de que les rinden.

## Paso 3: ordénalo

Llena un archivo separado por tabulaciones, con encabezado, y corre el script.
Acepta las columnas en español o en inglés:

```
cuenta	seguidores	mediana	vistas	gancho
@alguien	48000	11000	412000	nadie te dice que el primer semestre es el peor
```

```bash
python3 swipe.py capturados.tsv --out ~/.claude/instagram/CUENTA/swipe.md
```

Calcula el múltiplo, nombra la fórmula del gancho con las mismas 26 que usa
`/ig-reel`, puntúa cada gancho con `hookscore.py` e imprime qué separa al tercio
de arriba del de abajo.

## Paso 4: di qué significa, con cuidado

Informa tres cosas y nada más:

1. **Qué fórmulas se repiten** en el tercio de arriba, con conteos. Dos fórmulas
   que aparecen cuatro veces cada una en seis cuentas es un hallazgo. Una que
   aparece dos veces no.
2. **Qué tiene en común el tercio de arriba** que el de abajo no: largo del
   gancho, si la entrega es visual, si el primer cuadro se mueve, dónde está la
   acción.
3. **Las filas sin clasificar.** Cada gancho que el clasificador no pudo nombrar
   es ruido o una fórmula que todavía no está en `hooks.json`. Léelas a mano. Es
   la columna más valiosa de la salida, y por eso el script imprime el conteo.
   El clasificador en español se probó con pocos ganchos: espera más filas sin
   clasificar que en el original.

Después di el tamaño de la muestra y la confianza en palabras simples. Cuarenta
reels de seis cuentas sostienen una afirmación. Doce no, y decirlo es la
diferencia entre investigar y leer el horóscopo.

## Paso 5: conviértelo en algo para grabar

Para las tres fórmulas de arriba, escribe **la versión de la cuenta**: su propia
historia, su propio número, con la forma que está funcionando. Pásale cada una a
`/ig-reel` con el número de fórmula ya elegido.

Nunca entregues «haz un reel como este». Entrega una línea de gancho que se
pueda decir mañana.

## Salida

```
REFERENCIAS  ·  38 reels  ·  7 cuentas  ·  base: mediana de la cuenta

SOBRE 3x
  38,4x  gancho 86  #3  Nadie te dice        @cuenta_a    412.000  (mediana 10.700)
  11,2x  gancho 79  #9  Róbate esto          @cuenta_c    180.000  (mediana 16.100)
  ...

QUÉ SE REPITE
  #3 Nadie te dice      x5 en el tercio de arriba, 0 abajo
  #2 Orden negativa     x4
  largo mediano         8 palabras arriba, 19 abajo

SIN CLASIFICAR (6)
  Dos tienen la misma forma y no está en hooks.json: un gancho que parte
  leyendo en voz alta el comentario de otra persona. Vale la pena agregarla.

TU VERSIÓN
  #3  "Nadie te dice que el primer semestre online es el más difícil."
  ...
```

(Los números de este ejemplo son ilustrativos.)

Escribe el archivo en `~/.claude/instagram/CUENTA/swipe.md`. `/ig-reel` e
`/ig-plan` lo leen, que es la idea: después de correr esto una vez, el resto del
paquete trabaja con la evidencia propia y no con valores por defecto.

Esta skill no publica, no sigue, no da like ni manda mensajes. Lee.
