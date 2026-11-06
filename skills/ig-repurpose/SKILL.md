---
name: ig-repurpose
description: >-
  Convierte un material largo (un video de YouTube, un podcast, un live, un
  newsletter, un artículo, una charla o una clase) en una semana de reels y
  carruseles. En español de Chile. Úsala cuando digan «reutiliza esto», «saca
  reels de esto», «tengo un video / podcast / transcripción», «córtalo», o
  peguen algo largo y lo quieran en Instagram.
---

# ig-repurpose

Adaptada al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol).

Un buen material largo trae entre cuatro y seis posts adentro. La mayoría saca
uno y bota el resto.

## Entrada

Una transcripción, un artículo, un newsletter, un guion, el resumen de una
charla, un live, una clase grabada. Si dan una URL y la sesión tiene una
herramienta de transcripción, úsala; si no, pide que peguen el texto. Lee todo
antes de extraer nada.

Si el material es un video de la propia cuenta, pide también el archivo. Un reel
armado con el material real le gana a uno armado con las mismas palabras leídas
de nuevo.

Trabaja sobre la carpeta de la cuenta en `~/.claude/instagram/` y lee su
`voice.md`. **Permisos:** si en el material aparecen estudiantes, docentes o
clientes, su cara y su voz solo se usan con autorización. Si no está claro, se
pregunta antes de proponer ese corte.

## Extrae, no resumas

El resumen de un video no es un reel. Nadie quiere el resumen. Recorre el
material y saca lo que se sostiene solo:

| extraer | qué es |
| --- | --- |
| **Afirmaciones** | cada oración que empezaría una discusión |
| **Números** | cada cifra, costo, duración, porcentaje |
| **Historias** | cada momento con una persona, una escena y un costo |
| **Mecanismos** | cada «la forma en que esto funciona de verdad es...» |
| **Errores** | cada reconocimiento de algo que salió mal |
| **Frases** | cada oración que ya se puede citar tal cual |

Haz la lista de lo que encontraste, con conteos, antes de escribir nada. Si el
material da menos de cuatro cosas, es flaco, y cuatro posts exprimidos de ahí
también van a ser flacos. Dilo.

## Después, elige formato por extracto

No todo es reel.

- **Afirmación, error, historia** a reel. Necesitan voz y cara.
- **Mecanismo, lista numerada** a carrusel. Hay que releerlos.
- **Una frase citable** a un cuadro de historia, no a un post.

## Después, arma la semana

Cada extracto es un post y cada post se sostiene completamente solo. Quien mira
no vio el material original y nunca lo va a ver. Nunca escribas «como dije en mi
último video». El post es la cosa.

Asigna una fórmula de gancho de `ig-reel/hooks.json` a cada uno y varíalas. Cinco
posts de una misma fuente con la misma forma de gancho se leen como fábrica de
contenido, porque lo son.

Si el material es un video de la cuenta, **usa el material real**. El clip donde
se dijo la cosa, con la reacción real adentro, le gana siempre a volver a
grabar. Corta en la oración, no en la respiración.

Ordena la semana para que la afirmación más fuerte vaya primero, la historia a
mitad de semana, y el mecanismo al final, cuando quienes vieron los anteriores
lo están esperando.

## Salida

```
MATERIAL: "Cómo organizar la semana si trabajas y estudias" (charla de 42 min, 8.900 palabras)

ENCONTRÉ  5 afirmaciones, 9 números, 3 historias, 4 mecanismos, 2 errores, 7 frases citables

SEMANA
MAR  REEL      #2  Orden negativa     Deja de estudiar el fin de semana
                                      usa el clip del 14:20, se ríe al final
MIÉ  CARRUSEL  Trabajo B              El horario de 4 pasos
VIE  REEL      #21 Mitad de frase     "...y ahí fue cuando me di cuenta de que iba atrasada"
DOM  REEL      #5  Colapso de tiempo  De 10 horas el fin de semana a 4 horas en dos noches

Di «escribe el martes» y lo redacto.
```

Después redacta cuando lo pidan, de a uno, cada uno por `/ig-reel` y
`/ig-human`. No sueltes cuatro guiones terminados de una: van a sonar iguales y
la persona no va a grabar ninguno.
