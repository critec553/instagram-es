---
name: ig-reply
description: >-
  Maneja los comentarios bajo los reels y posts de la propia cuenta: redacta
  respuestas para los que vale la pena contestar, ordenados según cuáles son.
  En español de Chile. Úsala cuando peguen sus comentarios, digan «responde
  estos», «maneja mis comentarios», «alguien dijo X en mi reel», o estén
  lidiando con una crítica, un troll o un interesado en los comentarios.
---

# ig-reply

Adaptada al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol).

El hilo de comentarios bajo tu propio post es donde se decide el alcance. Cada
respuesta es otra interacción en el post, las respuestas de la primera hora
hacen casi todo el trabajo, y en Instagram una respuesta también puede ser un
reel, que es la jugada más subutilizada de la plataforma.

Pero no todos los comentarios valen lo mismo, así que esta skill ordena antes de
escribir.

## Entrada

Pegan los comentarios, idealmente con los usuarios. Las capturas sirven. No
raspes el hilo con un navegador.

Trabaja sobre la carpeta de la cuenta en `~/.claude/instagram/` y lee su
`voice.md`. Si hay varias cuentas y no está claro cuál, pregunta.

## Primero, clasifica

Pon cada comentario en uno de seis grupos y di los conteos en voz alta:

| grupo | qué es | qué recibe |
| --- | --- | --- |
| **PALABRA CLAVE** | la palabra que pediste comentar | lo prometido, a mano o con tu herramienta aprobada |
| **INTERESADO** | alguien que describe el problema que resuelves | una respuesta de verdad en público, y después una puerta |
| **APORTE** | suma datos, discrepa, extiende | la respuesta más larga del hilo |
| **PREGUNTA** | una pregunta que tiene mucha gente | esta se convierte en reel, no solo en respuesta |
| **APOYO** | «🔥», «buenísimo», una etiqueta | un like, y de 3 a 8 palabras como mucho |
| **RUIDO** | venta, spam, mala fe, carnada | nada, o una línea y fuera |

Escribe en ese orden y para cuando se acaba el valor.

## La jugada que casi nadie hace

Si una pregunta de los comentarios la tienen otras treinta personas,
**respóndela con un reel**. Instagram pega el comentario al video nuevo como
sticker, a quien preguntó le llega aviso, y una pregunta con demanda real se
convierte en un post con el gancho ya escrito. Marca cada PREGUNTA que califica y
pásasela a `/ig-reel` como fórmula #16.

## Cómo responder

- **Responde la pregunta de verdad.** Si alguien pregunta cómo, dile cómo, en la
  respuesta. No lo mandes al DM a escuchar una respuesta que podía tener ahí.
- **Usa su nombre una vez**, al principio, sin signo de exclamación.
- **Mide su largo.** A un comentario de cuatro palabras no le toca una respuesta
  de cuatro líneas.
- **A una crítica:** concede primero lo que es verdad, con sus palabras, y
  después sostén tu postura. Nunca borres, nunca te pongas a la defensiva, nunca
  respondas dos veces en el mismo hilo.
- **A un troll:** nada. Una respuesta es alcance, y el alcance es a lo que vino.
  Oculta el comentario si es ofensivo. Los controles de comentarios de Instagram
  existen y usarlos no es perder.
- **A un interesado:** responde completo en público. La puerta es una oración al
  final y es una oferta de ayuda, no una venta. La respuesta pública es lo que
  hace que la siguiente persona escriba por DM.
- **Datos personales fuera del hilo.** Si alguien comenta su RUT, su teléfono o
  su situación financiera, no los repitas en público: responde que le escribes
  por interno.

## Comentarios con palabra clave

Si el post pidió comentar una palabra, esos comentarios son todo el sentido del
post. Cada uno es una persona que levantó la mano. Respóndele a cada uno y manda
lo prometido. Si la cuenta tiene automatización con las herramientas de
Instagram, un partner aprobado o el CRM conectado, dilo y déjala correr; si no,
las respuestas son a mano y a este volumen está bien. Nunca mandes DMs masivos a
quien no comentó.

**Reglas de Instagram para la respuesta privada a un comentario** (verificadas
en la integración del CRM con Zernio, septiembre de 2026; revísalas si pasó
tiempo): hay **un solo mensaje privado por comentario**, dentro de **7 días**, y
desde fines de agosto de 2026 **no admite botones ni adjuntos**, solo texto. Si
el primer privado sale mal, no hay segundo intento: por eso se redacta con
cuidado y lo revisa una persona.

## Salida

Un bloque, agrupado por grupo, cada respuesta lista para copiar y ya humanizada:

```
RESPUESTAS  ·  84 comentarios  ·  41 PALABRA CLAVE, 2 INTERESADO, 3 APORTE, 2 PREGUNTA, 34 APOYO, 2 RUIDO

PALABRA CLAVE  (41)  manda la planilla. Una línea cada uno, mismo tono, no copiar y pegar.

INTERESADO
@usuario - "yo trabajo de noche, ¿igual se puede?"
> Sí. Con turnos de noche lo que mejor funciona es fijar horas por semana y no
> días. Te escribo por interno con un ejemplo.

PREGUNTA -> REEL
@usuario - "¿y si me atraso con una entrega qué pasa?"
  34 likes en este comentario. Eso es un reel, no una respuesta. Fórmula #16.

RUIDO  (2)  omitidos. Responderles les da alcance.
```

Después la barrera: no se publica nada hasta que la persona diga sí. Ella pega
las respuestas.
