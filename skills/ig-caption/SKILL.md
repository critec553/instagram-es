---
name: ig-caption
description: >-
  Escribe el texto de un post de Instagram (la línea que sobrevive al corte de
  «... más», el cuerpo, la única acción, los términos de búsqueda y los
  hashtags) y lo revisa antes de publicar. En español de Chile. Úsala cuando
  pidan «escribe el texto», «el copy», «la descripción», «el caption», tengan un
  reel o carrusel listo y les falte el texto, o pregunten por hashtags.
---

# ig-caption

Adaptada al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol). En esta carpeta hay una herramienta y corre:

```bash
python3 caption.py texto.txt
python3 caption.py texto.txt --keywords "carreras online,estudiar trabajando"
```

Imprime el texto como lo imprime el feed: los primeros 125 caracteres en una
caja y el resto detrás del toque. Lee esa caja antes que cualquier otra cosa
que hayas escrito.

## Antes: la cuenta

Mira `~/.claude/instagram/` y trabaja sobre la carpeta de la cuenta que
corresponde. Lee su `voice.md`: el tuteo o el usted, los emojis, lo que no se
puede afirmar. Si hay varias cuentas y no está claro cuál, pregunta.

## Primero, decide qué trabajo tiene este texto

Esta es la decisión que arruina los textos cuando se salta.

**Trabajo A: el video ya enganchó.** Un reel trae su propio gancho en los
primeros dos segundos, hablado y en pantalla. El texto no es un segundo gancho,
y competir con el video es la forma de perder los dos. Su trabajo es la acción,
el contexto que hace que la acción tenga sentido, y las palabras que la gente
busca.

**Trabajo B: el texto es el contenido.** Una foto, una imagen sola, la portada
de un carrusel que abre una pregunta. Acá la primera línea es el gancho y
funciona igual que el gancho de un reel: concreta, corta, y cortada en suspenso,
no a mitad de frase.

Pregunta cuál estás escribiendo. Si hay un reel con un buen gancho, escribe A y
di por qué.

## La forma

```
Línea 1     125 caracteres visibles. Trabajo A: la acción, directa.
            Trabajo B: el gancho.
            Nunca un saludo, nunca un hashtag, nunca un emoji como primer carácter.
Cuerpo      párrafos cortos, una línea en blanco entre cada uno. De dos a
            seis. Acá viven los términos de búsqueda.
La acción   una. Comentar una palabra, guardar, o escribir por DM. Una.
Hashtags    hasta cinco, en su propia línea al final, o ninguno.
```

El límite es 2.200 caracteres y casi nada los necesita. Un texto que se gana el
toque y entrega 600 caracteres le gana a uno que entrega 1.800.

## Hashtags, en serio

Los hashtags ya no son una palanca de alcance, y la plataforma lo dijo con un
cambio de producto: **Instagram puso un tope de cinco hashtags por post el 18
de diciembre de 2025**, antes eran treinta, explicando que usar pocos y
específicos rinde más que muchos genéricos.

Entonces: hasta cinco, específicos, como etiquetas de tema. Si hay un bloque de
veinte guardado en las notas del teléfono, ese bloque ya es peso muerto y la
revisión lo va a reprobar.

`#viral`, `#fyp`, `#parati`, `#explorar`, `#chile` no describen nada. Fuera.

## Los términos de búsqueda importan más que los hashtags

La búsqueda de Instagram lee el texto. La frase por la que la cuenta quiere
aparecer va en el texto como la escribiría una persona, en una oración normal.
«Carreras online» como palabras en la línea tres, no «#carrerasonline» en un
bloque al final.

Pide dos o tres términos y pásaselos a la revisión:

```bash
python3 caption.py borrador.txt --keywords "carreras online,estudiar trabajando"
```

## Reglas

- **Sin link en el texto.** El texto no es clicable. Una URL en el cuerpo es
  texto muerto que dice «no uso esta plataforma». Bio o DM.
- **Una acción.** Dos acciones es lo mismo que ninguna. `caption.py` las
  cuenta.
- **La palabra clave tiene que poder escribirse.** Una palabra, sin espacios,
  sin emoji, en MAYÚSCULAS, y dicha en voz alta en el video también.
  `Comenta BECA` funciona. `Comenta "quiero la guía de becas"` no.
- **Si hay link, escribe el primer comentario aparte.** Dilo en el resumen.
- **Emojis como puntuación, no como decoración.** La revisión marca más de 4
  cada 100 caracteres.
- **El texto alternativo vale 20 segundos.** En carruseles y fotos, escríbelo.
  Lo leen los lectores de pantalla y lo lee Instagram.
- **Cuentas institucionales:** nada que `voice.md` marque como fuera de
  límites, aunque sea «solo el texto».

## El ciclo

1. Decide Trabajo A o B y di cuál.
2. Escribe el borrador.
3. Pásalo por `/ig-human`. Los textos son cortos, así que el relleno se nota
   más acá que en cualquier otra parte del paquete.
4. Corre `caption.py` con los términos de búsqueda. Arregla cada FALLA.
   Decide en voz alta cada OJO, no en silencio.
5. Imprime el bloque listo para copiar y después el resumen:

```
TEXTO LISTO
trabajo:    A - el reel trae el gancho
visible:    118 de 125 caracteres usados antes del corte
acción:     una, comentar BECA
hashtags:   3
búsqueda:   "carreras online" en la línea 3, "estudiar trabajando" en la línea 5
revisión:   LISTO
```

No se publica nada. La persona lo pega.
