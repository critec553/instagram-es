---
name: ig-comment
description: >-
  Escribe comentarios en posts y reels de otras cuentas de Instagram que se
  lean como una persona con opinión, no como un bot. En español de Chile.
  Úsala cuando peguen un post o un reel y quieran un comentario, digan
  «comenta esto», «interactúa con esto», «qué pongo acá», o quieran un lote
  para la ronda diaria de interacción.
---

# ig-comment

Adaptada al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol).

Comentar son los veinte minutos que más rinden en Instagram y los más fáciles
de hacer mal. Un comentario arriba de un reel con 40.000 vistas lo ve más gente
que la mayoría de los posts de una cuenta, y es el único lugar donde un
desconocido puede tocar directo hacia un perfil.

Un comentario genérico es peor que ninguno. Gasta un toque que no lleva a
ninguna parte y marca la cuenta como de grupos de interacción ante la única
persona cuya opinión importaba: quien creó el contenido.

## Entrada

Pegan el texto del post o reel, o una captura, con el nombre de la cuenta. Si
dan una URL que no puedes abrir, pide que la peguen. No uses un navegador para
raspar el feed y no publiques nada.

Decide desde qué cuenta se comenta: mira `~/.claude/instagram/` y lee su
`voice.md`. Una cuenta institucional comenta con la voz institucional.

## Los nueve tipos de comentario

Elige según lo que es el post. Nunca por defecto el tipo 1.

| # | tipo | cuándo | forma |
| --- | --- | --- | --- |
| 1 | **Suma un dato** | el post afirma algo que puedes respaldar con un número | «Nos pasa igual: el 40% de...» |
| 2 | **Suma el caso que falta** | el post tiene razón pero está incompleto | «Esto aplica hasta que {condición}.» |
| 3 | **Discrepa con respeto** | de verdad crees que está equivocado | di primero en qué estás de acuerdo, después dónde te separas |
| 4 | **Extiende una línea** | una línea es la buena | cítala y construye sobre ella |
| 5 | **Haz la pregunta real** | el post se saltó lo difícil | una pregunta, específica |
| 6 | **La boleta** | hiciste eso mismo que describe | qué pasó, dos oraciones |
| 7 | **La corrección** | hay un error de datos | ten razón, sé breve, amable y seguro |
| 8 | **El otro ángulo** | datos correctos, marco equivocado | «Otra forma de leerlo:» |
| 9 | **La frase corta** | el post no necesita nada, quieres estar presente | menos de 10 palabras, divertida o verdadera |

## Reglas

- **Una a tres oraciones.** Los comentarios se leen en una columna angosta bajo
  un video. Un párrafo queda escondido detrás de «más» y nadie lo toca.
- **Nunca partas con** «Buenísimo», «Me encanta», «Tal cual», «Esto 👏», «Justo
  lo que necesitaba», ni con el nombre de quien publicó y un signo de
  exclamación. Todos son invisibles.
- **Nada de comentarios de puro emoji** ni con emoji como primer carácter.
- **Nunca repitas lo que dice el reel.** Todos acaban de verlo.
- **Una idea.** Un comentario con dos puntos se lee como apropiarse del hilo.
- **Di lo específico.** Si el comentario serviría bajo cualquier post del tema,
  no es un comentario, es ruido.
- **Nunca vendas.** Ni la oferta, ni el link, ni «revisa mi perfil». Es la forma
  más rápida de que te bloquee justo la persona a la que querías llegar.
- **Temprano importa más acá que en cualquier otra parte.** Un comentario en la
  primera hora de un reel que después viaja, viaja con él.
- **Nada inventado.** Si el comentario usa un dato de la cuenta, tiene que
  estar en `voice.md`.

## Salida

Da **dos opciones de tipos distintos**, con su etiqueta, y una línea sobre cuál
publicarías y por qué. Pasa las dos por `/ig-human` primero: los comentarios son
cortos, así que una raya o una frase hecha se notan proporcionalmente más que en
un texto largo.

```
OPCIONES DE COMENTARIO  (en el reel de @cuenta sobre estudiar trabajando)

[6 · La boleta]
Hice lo de los dos bloques fijos el año pasado y lo único que me costó fue el
primer mes. Después el martes a las 21:00 ya no se negociaba.

[3 · Discrepa con respeto]
De acuerdo con los bloques fijos. Donde no me calza es con turnos rotativos:
ahí nos funcionó mejor fijar horas por semana, no días.

Publica el primero. Concede algo y tiene un detalle que se puede comprobar.
```

## Modo lote

Para una ronda de interacción, pide los 5 a 10 posts como texto pegado en un
mensaje, devuelve un comentario por cada uno en un solo bloque, y lleva una nota
en `~/.claude/instagram/CUENTA/log.md` de a quién se le comentó esta semana.
Comentar a las mismas tres cuentas todos los días se nota, y se ve exactamente
como lo que es.

## Nunca

No publiques solo, no automatices comentarios y no uses un navegador para
publicar en nombre de nadie. La interacción automatizada viola las Condiciones
de Uso de Instagram y bloquea cuentas. Esta skill escribe el comentario. La
persona lo publica.
