---
name: ig-profile
description: >-
  Puntúa un perfil de Instagram sobre 100 con una rúbrica de 12 partes y
  reescribe lo que pierde puntos: campo de nombre, bio, link, destacadas, los
  tres fijados, la grilla. En español de Chile, para cuentas personales e
  institucionales. Úsala cuando digan «optimiza mi perfil», «arregla la bio»,
  «evalúa mi Instagram», «por qué no me siguen», o peguen su perfil y
  pregunten cómo se lee.
---

# ig-profile

Adaptada al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol).

Casi todos optimizan lo equivocado acá. El perfil no es una vitrina que la
gente recorre. Es una **pantalla de decisión**, a la que se llega desde un reel,
y tiene unos tres segundos para responder una pregunta: ¿hay más de eso acá, y
es para mí?

## Entrada

Pide que peguen o capturen: el campo de nombre, el usuario, la bio, a dónde va
el link, los nombres de las destacadas, qué está fijado y las primeras nueve
portadas de la grilla. Una captura de la parte de arriba del perfil más las dos
primeras filas de la grilla basta para una primera pasada.

No inicies sesión en Instagram en nombre de nadie.

Trabaja sobre la carpeta de la cuenta en `~/.claude/instagram/` y lee su
`voice.md`. Si hay varias cuentas y no está claro cuál, pregunta.

## Puntúalo

Lee `rubric.json` de esta carpeta. Doce ítems, 100 puntos, cada uno con cómo se
ve el puntaje completo y cómo suele fallar. Puntúa cada ítem, muestra la tabla,
da el total. Con honestidad. La mayoría de los perfiles queda entre 30 y 45 en
la primera pasada, y un puntaje generoso no sirve.

```
PUNTAJE DEL PERFIL  38/100

  campo de nombre   2/12   solo el nombre, sin palabras que alguien busque
  bio línea 1       3/12   tres sustantivos y un emoji de café
  tres fijados      0/10   nada fijado
  destacadas        2/8    "Random", "Vida", "2023"
  grilla            4/8    seis de nueve portadas son una cara a mitad de frase
  ...
```

## Después reescribe, en este orden

Arregla en orden de puntos perdidos, de más a menos. No reescribas todo de una:
la persona tiene que ir a cambiar cada cosa.

**1. El campo de nombre (30 caracteres).** La línea en negrita bajo la foto, no
el usuario. Es el campo que la búsqueda de Instagram compara, y la mayoría pone
un nombre y nada más. Formato que funciona: `{Nombre} | {qué hace, en palabras
que se buscan}`. Da tres opciones.

**2. La primera línea de la bio.** Para quién es y qué cambia. No un cargo, no
adjetivos, no identidades separadas por barras. En una institución, no el
eslogan. El resto de los 150 caracteres lleva una prueba o una oferta simple.

**3. Los tres fijados.** Tres espacios, tres trabajos: la mejor prueba, la
explicación más clara de la oferta, la mejor presentación de quién está detrás.
Es el arreglo que más rinde de todo el perfil y toma cuatro toques. Una grilla
sin fijados muestra lo último que se publicó, que es tirar una moneda.

**4. Destacadas.** Entre cuatro y seis, con nombres de las preguntas que hace
quien compra o postula: Precios, Resultados, Cómo funciona, Quiénes somos,
Requisitos. No «Random». El resto se borra.

**5. El link.** Un destino que calce con lo que la bio acaba de prometer. Se
permiten cinco; dos ya es un menú y un menú convierte peor que una puerta.

**6. Portadas de la grilla.** Las primeras nueve en miniatura. Las portadas de
los reels se eligen, no quedan en el primer cuadro. Cuatro palabras de texto en
una portada hacen que la grilla se entienda de un vistazo.

## Salida

La tabla de puntaje, después las reescrituras como bloques listos para copiar
en orden de arreglo, cada una pasada por `/ig-human`. Vuelve a puntuar al final
y muestra la diferencia con honestidad. Si la reescritura llega a 84 y no a 98,
di 84, y di qué falta, que suele ser una grilla, el hábito de historias y un
post fijado que todavía no existe. Nada de eso es una reescritura.

Esta skill no guarda nada en Instagram. La persona edita cada campo.
