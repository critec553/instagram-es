---
name: ig-story
description: >-
  Escribe las historias de Instagram del día: la secuencia cuadro por cuadro,
  qué sticker usar dónde, y el que lleva a la gente a escribir por DM. En
  español de Chile. Úsala cuando digan «historias», «qué subo a historias»,
  «secuencia de historias», «idea de encuesta», «no tengo nada que subir», o
  quieran vender algo sin hacer un post al respecto.
---

# ig-story

Adaptada al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol).

Las historias no son un feed chico. El feed es como te encuentran
desconocidos. Las historias son donde quienes ya te siguen deciden si vale la
pena comprarte, postular o escribirte, y son la única superficie de Instagram
donde un toque se convierte en conversación de un paso.

Fuera de tus seguidores nadie las ve, así que el trabajo es otro:
profundidad, no alcance.

## Antes: la cuenta

Trabaja sobre la carpeta de la cuenta en `~/.claude/instagram/` y lee su
`voice.md`. Si hay varias cuentas y no está claro cuál, pregunta.

## La forma del día

Entre tres y siete cuadros al día. Pasados unos siete, sube la tasa de gente
que adelanta y los últimos cuadros se muestran a nadie, que es justo donde se
suele poner la acción.

```
1       LA APERTURA  algo que pasa hoy, con una cara o una mano.
2-3     EL MEDIO     el contenido de verdad: el proceso, el resultado, el error.
4       LA ACCIÓN    un sticker. Encuesta, caja de preguntas, quiz o link.
5       EL CIERRE    la respuesta, el resultado, o lo que viene mañana.
```

Pon la acción en el cuadro 4, no en el 7. La gente se va con cada toque y la
acción la tiene que ver quien sigue ahí.

## Los stickers, y para qué sirve cada uno

| sticker | trabajo | cuándo |
| --- | --- | --- |
| **Encuesta** | el toque más barato que hay | quieres volumen de respuestas, no información |
| **Caja de preguntas** | juntar las palabras exactas que usa la gente | necesitas ideas de contenido u objeciones, textuales |
| **Quiz** | enseñar dejando que se equivoquen | hay un error común en el rubro |
| **Deslizador** | medir el ánimo | nada importante. Entretenido, poco valor |
| **Link** | la única superficie clicable además de la bio | hay un lugar real a donde ir |
| **Cuenta regresiva** | una fecha límite a la que se pueden suscribir | un lanzamiento, un live, un cierre de postulación |
| **Agrega el tuyo** | alcance fuera de los seguidores, a veces | la consigna la puede responder cualquiera del rubro |

La caja de preguntas es la más subestimada de la lista. Cada respuesta es un
texto, un gancho de reel o una apertura de DM escrita con las palabras de la
audiencia. Pásaselas a `/ig-reel` como fórmula #16.

## Reglas

- **Una cara o una mano en el primer cuadro.** Texto sobre fondo de color se
  adelanta, y el primer cuadro decide si se ve el resto.
- **Una idea por cuadro.** Nadie lee un párrafo en una historia.
- **El texto al centro.** En 1080x1920, nada sobre y=250 ni bajo y=1600. Arriba
  va la fila del perfil y abajo la barra para responder.
- **Háblale a una persona.** «Tú», en singular (o el trato que diga `voice.md`).
  Las historias son lo más parecido a un DM sin serlo.
- **No resubas tu propio post a historias sin decir nada.** Es el cuadro más
  ignorado de la plataforma. Si apuntas a un post, di qué pasó en los
  comentarios y por qué vale la pena volver.
- **Vende en historias, no en posts.** Tres cuadros de contexto, uno de oferta,
  uno de prueba. Esa secuencia vende más que un post sobre lo mismo y no te
  cuesta alcance.
- **Plazos y condiciones exactos.** Si un cuadro nombra una fecha de cierre, un
  descuento o una beca, va con la condición real. Si no la tienes, `{{dato}}` y
  avisa.

## El embudo a DM, hecho con honestidad

La secuencia que funciona: una historia que nombra un problema, una caja de
preguntas o una encuesta que deja decir «esa soy yo», y después una respuesta a
cada persona que contestó. La conversación empieza porque ella habló primero.

Las respuestas automáticas por palabra clave son una función real y permitida
para cuentas profesionales, con las herramientas de Instagram o de partners
aprobados. Mandar DMs masivos a gente que no interactuó no lo es, y es lo que
restringe cuentas. La regla es simple: **primero actúan, después respondes.**

## Salida

Los cuadros en orden, cada uno con qué se ve, qué se dice y qué sticker, más qué
hacer con las respuestas:

```
HISTORIAS  ·  martes  ·  5 cuadros

1  [selfie, caminando]      "Tercera vez esta semana que me preguntan lo mismo."
2  [grabación de pantalla]  el requisito, destacado
3  [a cámara]               "Si trabajas por turnos, esto te sirve."
4  [encuesta]               "¿Trabajas por turnos?"  Sí / No
5  [texto sobre foto]       "Responde y te mando el detalle."

Después: todos los que votaron Sí reciben respuesta. Ese es el embudo entero.
```

No se publica nada. La persona lo sube.
