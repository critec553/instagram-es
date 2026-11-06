---
name: ig-dm
description: >-
  Escribe DMs de Instagram que reciben respuesta: la entrega por palabra
  clave, el primer mensaje a alguien que interactuó, la propuesta de
  colaboración, y los dos seguimientos. En español de Chile. Úsala cuando
  digan «escríbele a esta persona», «qué le mando», «mensaje de contacto»,
  «cómo hago el seguimiento», «propónle una colaboración a esta cuenta», o
  vayan a contactar a alguien específico.
---

# ig-dm

Adaptada al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol).

Los DMs de Instagram son el único lugar de la plataforma donde de verdad pasa
algo (una venta, una postulación, una alianza), y también donde la mayoría de
las cuentas quema la buena voluntad que se ganó con su contenido. La diferencia
es completamente quién se movió primero.

## Antes: la cuenta

Trabaja sobre la carpeta de la cuenta en `~/.claude/instagram/` y lee su
`voice.md`. Si hay varias cuentas y no está claro cuál, pregunta. Si la cuenta
tiene un CRM o una herramienta que responde DMs, lo que redactes acá es lo que
esa persona o herramienta va a mandar: respeta sus reglas.

## Los tres tipos de DM que vale la pena escribir

**1. La respuesta a una mano levantada.** Comentó la palabra clave, respondió la
encuesta, contestó una historia, o guardó y preguntó. Se movió primero. Es el
90% de los DMs que vale la pena mandar, y convierte porque no es prospección.

**2. El acercamiento tibio.** Alguien cuyos posts la cuenta lleva semanas
comentando de verdad. Ya hay un hilo de conversación.

**3. La propuesta de colaboración.** Una idea concreta a una cuenta concreta,
con una razón por la que es ella.

Todo lo demás es mandarle DMs en frío a desconocidos, que es lo que hace todo el
mundo, y por eso las tasas de respuesta están donde están. Si piden una
secuencia en frío, di claramente que es lo que menos rinde con esa misma hora, y
ofrece la alternativa: comentar en esas diez cuentas durante dos semanas
primero. Después escríbela si todavía la quieren.

## Antes de escribir, consigue lo específico

Pregunta en una sola pregunta agrupada:

1. **Quién**: usuario, qué hace, y qué publicó o hizo que empezó esto.
2. **El motivo**: la razón real para escribir hoy. Una palabra que comentó, una
   historia que respondió, un post que publicó. No «calza con el perfil».
3. **Qué quiere la cuenta**: una conversación, una venta, una postulación, una
   colaboración, un referido. Con honestidad interna, aunque el mensaje no parta
   por ahí.

Si no hay motivo, no hay mensaje. Dilo.

## La entrega por palabra clave

El DM más común del paquete y el más fácil de arruinar. Comentó una palabra.
Espera lo prometido. Entonces:

```
{su nombre}, acá está: {lo prometido, o cómo acceder}.

{una línea sobre cómo usarlo}

{una pregunta que se pueda responder en cuatro palabras}
```

Manda lo prometido **primero**, en el mensaje uno, sin condiciones. Un post con
palabra clave que responde «antes de mandártelo, ¿me cuentas a qué te dedicas?»
es cambiar las reglas a mitad de camino, y se recuerda. La pregunta del final es
la que empieza la conversación, y es opcional para la persona.

**Si responde a un comentario con la respuesta privada de Instagram:** hay un
solo mensaje por comentario, dentro de 7 días, y desde fines de agosto de 2026
**sin botones ni adjuntos** (verificado en la integración del CRM con Zernio,
septiembre de 2026). O sea: nada de «toca el botón» ni de mandar un PDF en ese
primer mensaje. Lo prometido va como texto, o como la invitación a seguir
conversando para mandarlo ahí.

Las respuestas automáticas por palabra clave son una función permitida para
cuentas profesionales, con las herramientas de Instagram o de un partner
aprobado. Usarlas está bien. Mandar DMs masivos no solicitados no, y es el camino
más rápido a una cuenta restringida.

## El primer mensaje a alguien tibio

- **De dos a cuatro oraciones.** Una pantalla de texto se borra.
- **Nombra lo específico.** El comentario, el post, la respuesta. Con sus
  palabras.
- **Da antes de pedir.** Un número, una plantilla, un nombre, una respuesta.
- **Una sola petición, chica.** «¿Te sirve que lo conversemos 10 minutos?» le
  gana a «déjame mostrarte todo lo que ofrecemos».
- **Sin link ni agenda en el mensaje uno.** Se lee como embudo porque lo es.
- **Sin audio a un desconocido.** Es una gran herramienta para quien ya conoce
  la voz de la cuenta.
- **Sin datos sensibles.** No pidas RUT, dirección ni datos bancarios por
  Instagram. Si hacen falta, van por el canal formal.

## La propuesta de colaboración

Cuatro líneas, en este orden: qué le has visto hacer, la idea concreta, qué gana,
qué necesitas de ella. Un post en colaboración aparece en las dos grillas y llega
a las dos audiencias, que es el mecanismo de crecimiento más fuerte de Instagram
sin pagarle a nadie. Propónlo así, y deja claro quién hace qué.

## Seguimientos

Dos. Ese es el número.

- **+4 días**: suma algo nuevo. Nunca «solo te escribo para saber si viste mi
  mensaje». Si no hay nada nuevo, no hay seguimiento.
- **+10 días**: el mensaje de cierre. Di que no vas a volver a escribir, y
  cúmplelo. Este se lleva una parte sorprendente de las respuestas, porque quita
  la presión.

Después para. Un tercero no convierte a nadie y le cuesta la relación a la
cuenta.

## Nunca

- Nunca automatices DMs de prospección, ni uses una herramienta que mande en
  horario a gente que no interactuó. Viola las Condiciones de Uso de Instagram y
  restringe la cuenta.
- Nunca inventes haber visto algo, un contacto en común ni nada compartido.
- Nunca partas con «¡Hola! Una consulta rápida» y después no hagas ninguna
  pregunta.
- Nunca mandes la propuesta en el mismo mensaje que el halago.

## Salida

El mensaje, el conteo de caracteres, y los dos seguimientos con el día en que
sale cada uno, todo pasado por `/ig-human`. La persona manda cada uno a mano, o
con su propia automatización aprobada solo para respuestas por palabra clave.
