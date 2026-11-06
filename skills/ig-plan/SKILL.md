---
name: ig-plan
description: >-
  Arma la semana en Instagram: qué publicar, en qué formato, cuándo, y con
  quién interactuar. En español de Chile. Úsala cuando digan «planifica mi
  semana», «qué publico», «calendario de contenido», «no tengo nada que
  publicar», o quieran una pauta de publicación y una lista de cuentas para
  interactuar.
---

# ig-plan

La sala de control. Todo lo demás del paquete ejecuta; esto decide qué se
ejecuta. Córrela una vez a la semana, el mismo día.

Adaptada al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol).

## Entrada

Decide la cuenta: mira `~/.claude/instagram/` y trabaja sobre su carpeta. Si
hay varias y no está claro cuál, pregunta.

Si existen `voice.md`, `swipe.md` y `log.md` de esa cuenta, léelos. El archivo
de referencias es la evidencia propia de `/ig-viral` sobre qué fórmulas están
funcionando ahora en el rubro, y le gana a cualquier cosa de este archivo. El
log evita que el plan repita un tema de las últimas dos semanas.

Si no existen, pide cuatro cosas y anótalas:

1. Qué ofrece la cuenta, y a quién.
2. Los tres o cuatro temas por los que quiere ser conocida.
3. Qué pasó de verdad esta semana: una conversación con alguien que postuló o
   compró, un número, un error, algo que se construyó, una discusión. De ahí
   salen los posts.
4. Diez cuentas a las que vale la pena ser visible.

## Qué publicar

Cuatro o cinco posts a la semana, y al menos tres reels. Los reels son el único
formato de Instagram que llega de forma confiable a gente que no sigue la
cuenta. Los carruseles profundizan con quienes ya siguen. Las historias son
diarias y se planifican aparte.

Mezcla en la semana, nunca dos del mismo tipo seguidos:

| tipo | cantidad | trabajo |
| --- | --- | --- |
| **Prueba** | 1 por semana | algo que pasó, con un número. Reel. |
| **Enseñar** | 1 o 2 por semana | una cosa que quien mira puede hacer hoy. Reel o carrusel. |
| **Opinión** | 1 por semana | una postura que podría costar seguidores. Reel. |
| **Historia** | 1 cada dos semanas | una escena con un costo. Reel. |
| **Oferta** | 1 cada dos semanas | lo que se ofrece, dicho directo, sin pedir perdón. Carrusel o historias. |

Para cada espacio da: el tema, el ángulo concreto de lo que pasó esta semana, el
formato y el número de fórmula de `ig-reel/hooks.json`. No un tema, un ángulo.
«Estudiar online» no es un plan. «La estudiante que dejó de estudiar los
sábados y subió el promedio» es un reel.

## Cuándo publicar

Cuando la audiencia está despierta y no trabajando. Para un público adulto que
trabaja, en Chile, eso suele ser la noche entre 20:00 y 22:00, la hora de
almuerzo, o temprano antes de entrar. Ancla las horas a la zona horaria de la
audiencia (America/Santiago), no a la de quien publica, si son distintas.

Pero dilo claro: **la hora importa mucho menos que los primeros dos segundos.**
Instagram sigue mostrando un reel durante días si rinde, y entierra uno bien
horario que no rinde. Si la cuenta está optimizando horas antes de que sus
ganchos funcionen, está puliendo lo equivocado, y hay que decirlo.

## La ronda de interacción, que no es opcional

20 minutos al día, antes de publicar, no después. Una lista de 10:

- **5 de alcance**: cuentas con la audiencia que la cuenta quiere, donde un buen
  comentario se ve. Comenta temprano, antes de que el hilo tenga 200.
- **3 pares**: mismo tamaño, mismo rubro. Es el grupo que devuelve.
- **2 potenciales**: personas o cuentas que de verdad podrían comprar, postular o
  aliarse. Comenta durante semanas antes de cualquier DM, y nunca vendas en un
  comentario.

Para cuentas institucionales la ronda la hace quien administra la cuenta, con la
voz de `voice.md`, no con la voz personal.

Pásale la lista a `/ig-comment`.

## Salida

```
SEMANA DEL 15 DE SEPTIEMBRE

LUN  solo interactuar  (20 min, lista abajo)
MAR  20:30  REEL      PRUEBA    #5  Colapso de tiempo  - del fin de semana a dos noches
MIÉ  solo historias + interactuar
JUE  20:00  CARRUSEL  ENSEÑAR   Trabajo B              - el horario de 4 pasos
VIE  20:30  REEL      OPINIÓN   #2  Orden negativa     - deja de estudiar el sábado
SÁB  -
DOM  19:00  REEL      HISTORIA  #21 Mitad de frase     - la llamada de admisión

HISTORIAS  todos los días, 3 a 5 cuadros, caja de preguntas el jueves.

INTERACTUAR  (5 alcance / 3 pares / 2 potenciales)
  ...

Di «escribe el martes» y lo redacto.
```

Escribe el plan en `~/.claude/instagram/CUENTA/plan.md` para que las otras
skills lo lean. No se agenda ni se publica nada en ninguna parte. Es un plan y
la persona lo ejecuta.
