---
name: ig-audit
description: >-
  Análisis de lo que la cuenta ya publicó: qué reels funcionaron de verdad, por
  qué, y qué dejar de hacer. En español de Chile. Úsala cuando peguen
  estadísticas de Instagram o posts anteriores y pregunten «qué está
  funcionando», «por qué le fue mal a este», «lee mis estadísticas», «audita mi
  contenido», o quieran saber qué hacer más.
---

# ig-audit

Adaptada al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol).

La única fuente honesta de qué funciona para una cuenta es esa cuenta. Cada regla
de cada guía de Instagram, incluidas las de este paquete, es una suposición
previa. Los últimos 30 posts de la cuenta son la evidencia.

## Entrada

Decide la cuenta: mira `~/.claude/instagram/` y trabaja sobre su carpeta. Si hay
varias y no está claro cuál, pregunta.

Pide lo que haya:

- Estadísticas por post: vistas, alcance, interacciones, tiempo de
  reproducción, guardados, compartidos, seguidores ganados, y la parte del
  alcance que viene de gente que no sigue la cuenta. Las capturas sirven.
- O el gráfico de retención del mejor y el peor reel reciente. Esa captura vale
  más que todo lo demás junto.
- O solo los posts y sus vistas, que alcanza para una primera pasada.

Lee también `~/.claude/instagram/CUENTA/log.md` si existe, porque anota qué
fórmula de gancho usó cada post.

**Si la cuenta tiene una herramienta de métricas conectada** (Porter, Zernio, la
API de Instagram), úsala en vez de pedir capturas, pero revisa primero que
apunte a **la cuenta correcta**. Una organización puede tener dos cuentas, y una
herramienta midiendo la cuenta vieja devuelve cero publicaciones recientes que
parecen una caída. Y ojo: las métricas únicas de Meta (alcance, visitas al
perfil) muchas veces solo cuadran agregadas y devuelven cero desglosadas por
día; las impresiones de una cuenta con anuncios activos incluyen entrega pagada,
así que no son orgánico.

## Qué medir de verdad

Las vistas brutas son el número menos útil de la página, porque dependen sobre
todo de cuánta gente ya sigue la cuenta. Calcula esto en su lugar y muestra el
cálculo:

| métrica | cómo | qué dice |
| --- | --- | --- |
| **Múltiplo** | vistas / mediana de vistas de la propia cuenta | si fue un acierto real o un día normal |
| **Alcance de no seguidores** | % del alcance de gente que no sigue | si viajó o no |
| **Retención a los 3s** | quienes siguen a los 3s / quienes empezaron | si funcionó el gancho. Es la nota del gancho. |
| **Tiempo promedio** | directo de las estadísticas | si funcionó la mitad |
| **Envíos por alcance** | compartidos / alcance | la señal más fuerte que se puede ganar. Mandar algo es poner tu nombre encima. |
| **Seguidores por alcance** | seguidores ganados / alcance | si el perfil convirtió la atención |

Ordena por múltiplo y envíos por alcance, no por vistas. Un reel con 4.000 vistas
y 90 envíos le ganó al de 60.000 vistas y 11.

## Después, busca el patrón

Con los cinco de arriba y los cinco de abajo lado a lado, busca qué los separa, y
atrévete a concluir algo que a la cuenta no le va a gustar:

- **Retención a los 3 segundos.** Si arriba y abajo difieren acá, es el gancho y
  nada más, y todo lo que viene después es distracción.
- **Fórmula de gancho.** ¿Qué números de `ig-reel/hooks.json` están arriba?
- **Formato.** Reel, carrusel, imagen sola.
- **Largo.** Agrupa en menos de 15s, 15 a 30s, 30 a 60s, más de 60s.
- **Tema.**
- **Si la cuenta respondió comentarios en la primera hora.**
- **Día y hora.** Revísalo **al final** y solo si lo demás no muestra nada. Casi
  nunca es la causa y es donde la gente quiere que esté.

Di el hallazgo como afirmación con la evidencia al lado, y di cuánta confianza
tiene. Con 30 posts se ve un patrón. Con 6 no, y decirlo es mejor que inventar
uno.

## La distinción que ahorra meses

**Un reel con vistas y sin seguidores nuevos no es un reel fallido, es un
problema de perfil.** Un reel sin vistas es un problema de gancho. Separa los dos
antes de recomendar nada. Si el alcance de no seguidores es alto y los
seguidores por alcance son bajos, deja de reescribir ganchos y pasa a
`/ig-profile`.

## Salida

```
AUDITORÍA  ·  31 posts  ·  12 jun - 5 sep  ·  mediana 4.100 vistas

5 DE ARRIBA POR MÚLTIPLO
  18,2x  #3  Nadie te dice        74.600 vistas  62% no seguidores  retención@3s 71%  128 envíos
   6,4x  #1  Confesión de costo   26.300 vistas  48% no seguidores  retención@3s 64%   71 envíos
  ...

5 DE ABAJO
   0,3x  #11 Lista                 1.200 vistas   9% no seguidores  retención@3s 31%    2 envíos
  ...

QUÉ DICEN LOS DATOS
1. La retención a los 3 segundos es toda la historia. Arriba promedian 66%,
   abajo 33%. Todo lo demás que te preocupa depende de los primeros dos segundos.
2. Los posts donde la cuenta queda vulnerable: promedio 8,1x contra 0,9x del
   resto. n=5. La señal más fuerte acá, y no es ni cerca.
3. Las listas de herramientas tienen vistas y nada más. Mucho alcance, sin
   envíos ni seguidores. Tres de los cinco de abajo.
4. El día de la semana no muestra nada. Martes y viernes están dentro del ruido.
   Deja de optimizarlo.

DEJAR: listas.
HACER MÁS: los que tienen un costo real y un número al lado.
```

(Los números de este ejemplo son ilustrativos.)

Después pásale las conclusiones a `/ig-plan` para que la semana siguiente se arme
con la evidencia propia y no con valores por defecto, y a `/ig-viral` para que
las referencias se filtren a las fórmulas que le funcionan a esta cuenta.
