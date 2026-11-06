---
name: ig-carousel
description: >-
  Arma un carrusel de Instagram: la portada que se gana el deslizar, el texto
  lámina por lámina y los archivos de 1080x1350 para subir. En español de
  Chile. Úsala cuando digan «carrusel», «láminas», «post para deslizar»,
  «convierte esto en carrusel», o tengan una idea con forma de lista o de pasos
  que moriría como imagen sola.
---

# ig-carousel

Adaptada al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol).

Los carruseles son el formato de la grilla donde más tiempo se queda la gente,
porque deslizar es una interacción y pasar de largo no. Además tienen segunda
oportunidad: Instagram puede volver a mostrar un carrusel desde una lámina
posterior a quien no interactuó la primera vez, así que la lámina dos también
tiene que sostenerse sola.

El formato premia una idea partida en pasos. Castiga un texto cortado en
pedazos.

## Antes: la cuenta

Trabaja sobre la carpeta de la cuenta en `~/.claude/instagram/` y lee su
`voice.md`. Si hay varias cuentas y no está claro cuál, pregunta. Si la cuenta
tiene manual de marca o sistema de diseño, se usa ese, no uno inventado.

## Cuándo usarlo en vez de un reel

Usa carrusel cuando la idea tiene **secuencia y hay que releerla**: pasos, un
esquema con partes, un antes y después, una lista que vale una captura. Usa
reel cuando la idea tiene movimiento, una cara, o una entrega que hay que ver
pasar.

Si la idea es una sola afirmación, no es ninguno de los dos. Pásasela a
`/ig-reel` y dilo.

## Estructura

De 6 a 10 láminas. El tope es 20 y 20 casi siempre es un libro que nadie
termina. Con menos de 5 el deslizar nunca empieza.

```
1         PORTADA   el gancho. 6 palabras o menos, a un tamaño que se lea en la
                    grilla en miniatura. Una línea de promesa abajo.
2         LO QUE ESTÁ EN JUEGO   por qué importa, en una oración. Esta lámina
                    también es una segunda portada, así que no puede ser relleno.
3 a N     UNA IDEA POR LÁMINA. Un título de 3 a 7 palabras y como mucho 25
                    palabras abajo. Si una lámina necesita un párrafo, son dos.
N+1       RESUMEN   todo como lista. Esta es la lámina de la captura.
ÚLTIMA    ACCIÓN    una. Guardar, comentar una palabra o seguir. Una.
```

## Reglas del texto

- **La portada es el 80% del resultado.** Seis palabras. Grande. Nada del resto
  salva una portada que nadie desliza.
- **Diseña para el recorte de la grilla.** La grilla del perfil recorta a un
  rectángulo vertical, y la proporción exacta ha cambiado más de una vez. Arma
  en 1080x1350 y deja el texto de la portada bien al centro, lejos de los 120
  píxeles de cada borde, y el recorte deja de importar.
- **Numera las láminas** (3/8). Más gente llega al final cuando ve dónde está.
- **Ninguna lámina es un párrafo.** Si no cabe en 25 palabras, se parte.
- **La lámina de resumen es la que se captura y se manda.** Los envíos son la
  señal más fuerte que se puede ganar. Que se entienda sola, sin contexto.
- **El usuario en cada lámina**, chico, en una esquina de abajo. Las capturas
  viajan sin ti.
- **Texto alternativo al menos en la portada.** Lo leen los lectores de pantalla
  y lo lee Instagram.
- **Nada inventado.** Una estadística en una lámina lleva su fuente, y lo que
  `voice.md` marca como fuera de límites no entra.

## Armar los archivos

Instagram pide 1080x1350 (4:5), JPEG o PNG, hasta 20 elementos. Ármalo como HTML
e imprime cada lámina:

```bash
# un <section> por lámina, 1080x1350, page-break-after: always
# después Chrome sin interfaz --print-to-pdf, o el conversor HTML a imagen que ya uses
```

Escribe el HTML con `width:1080px; height:1350px`, un solo color de acento y
letra de 32px como mínimo, porque se lee en un teléfono a un tercio del tamaño
real. Tildes y eñes: fuente que las tenga todas, y revisa que no aparezcan
cuadraditos.

## Salida

Primero el texto lámina por lámina, como lista numerada que se lea en diez
segundos y se pueda corregir antes de armar nada. Después el **texto del post**,
que para un carrusel es el Trabajo B de `/ig-caption`: el texto trabaja, porque
la portada ya gastó sus seis palabras.

Pasa los dos por `/ig-human`. Arma los archivos solo cuando la persona apruebe
el texto.

```
CARRUSEL  ·  8 láminas

1  PORTADA   EL HORARIO QUE ME SUBIÓ EL PROMEDIO
             Dos noches a la semana. Nada más.
2  EN JUEGO  Estudiaba todos los fines de semana y seguía atrasada.
3            MARTES Y JUEVES
             21:00 a 23:00, sin excepción.
...
7  RESUMEN   Los cuatro pasos, en orden.
8  ACCIÓN    Comenta HORARIO y te mando la planilla.

Texto: Trabajo B, gancho en la línea 1, una acción, 3 hashtags.
```

No se sube nada. La persona lo publica.
