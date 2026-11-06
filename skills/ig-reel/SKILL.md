---
name: ig-reel
description: >-
  Escribe un reel de Instagram a partir de una idea en bruto: opciones de
  gancho con 26 fórmulas, el guion hablado, el texto en pantalla y una hoja de
  escenas con tiempos, en la voz de la cuenta y puntuado antes de grabar. En
  español de Chile. Úsala cuando pidan un reel, un guion de video corto, un
  gancho, una voz en off, «haz un reel sobre X», «qué digo en este video», o
  cuando vayan a grabar y no tengan la primera línea.
---

# ig-reel

Convierte una idea en un reel que alguien termina de ver.

Adaptada al español de Chile desde instagram-agent-skill (MIT, Jake
Schincariol). En esta carpeta hay dos herramientas y las dos corren. Úsalas: no
calcules el gancho a ojo ni adivines el largo.

```bash
python3 hookscore.py ganchos.txt              # ordena tus opciones de gancho
python3 hookscore.py --hook "una línea"       # puntúa una sola
python3 beats.py guion.txt --target 30        # hoja de escenas antes de grabar
```

## Antes de escribir

1. **¿Qué cuenta?** Mira `~/.claude/instagram/`. Cada cuenta tiene su carpeta.
   Si hay una sola, úsala. Si hay varias y no está claro cuál, pregunta. Nunca
   uses cifras, casos ni nombres de una cuenta en otra.
2. Lee `~/.claude/instagram/CUENTA/voice.md`. Es el perfil de voz: cómo habla
   la cuenta en cámara, qué nunca dice, a quién le habla, qué no puede
   afirmar. Si no existe, pide **tres reels de la cuenta**, léelos o
   transcríbelos, deduce la voz y escribe el archivo desde `templates/voice.md`.
   Un guion en la voz equivocada no sirve, porque hay que decirlo en voz alta.
3. Lee `hooks.json` de esta carpeta. 26 fórmulas, cada una con plantilla,
   ejemplo, versión en pantalla, para qué sirve y cómo se echa a perder. Los
   ejemplos son ilustrativos, no datos reales de nadie.
4. Si la idea es flaca, no la rellenes. Haz una sola pregunta agrupada: qué
   pasó, a quién, y qué costó o qué dio. Un reel necesita una cosa específica y
   verdadera. Consíguela antes de escribir.
5. Si existe `~/.claude/instagram/CUENTA/swipe.md`, léelo. Lo escribe
   `/ig-viral` y es la evidencia de la propia cuenta sobre qué fórmulas están
   funcionando ahora en su rubro. Le gana a lo que dice este archivo.

## La forma

Un reel se decide en los primeros dos segundos y se sostiene en los cinco
siguientes.

```
0:00 - 0:02   GANCHO      la afirmación. Línea hablada y línea en pantalla,
                          escritas por separado. Movimiento en el primer
                          cuadro, no una cara quieta.
0:02 - 0:07   LO QUE ESTÁ EN JUEGO   por qué le importa a quien mira. Una línea.
0:07 - ...    EL CUERPO   una idea por escena, y el cuadro cambia en cada una.
ÚLTIMOS 3s    LA ENTREGA  cumple lo que prometió el gancho, y la única acción.
ÚLTIMA LÍNEA  EL LOOP     repite una palabra del gancho para que la segunda
                          vista calce.
```

Largo: entre 15 y 45 segundos es el rango que funciona. Un reel puede durar 3
minutos y casi nadie debería usarlos. Bajo 7 segundos se inflan los loops y
nada más.

## El ciclo

**1. Elige tres ganchos, no uno.** Pasa la idea por `hooks.json`, elige tres
fórmulas que de verdad le calcen y escribe la línea hablada y la de pantalla de
cada una. Fórmulas distintas, no tres versiones de la misma.

**2. Puntúalos.** Pon las tres líneas habladas en un archivo, una por línea, y
corre `hookscore.py`. Muéstrale el orden a la persona. Si el primero está bajo
50, todavía no tienes el gancho y ninguna edición lo arregla.

**3. Escribe el guion** con el gancho ganador. Lenguaje hablado, como habla la
cuenta de verdad. Frases cortas. Nada que haya que ensayar.

**4. Tómale el tiempo.** Corre `beats.py guion.txt --target {largo}`. Arregla
cada alerta: un gancho que pasa los 3 segundos, una escena de más de 4
segundos, una seguidilla de escenas sin nada concreto, falta de loop. Repite
hasta que salga limpio. Si la cuenta tiene su ritmo en `voice.md`, pásalo con
`--wpm`.

**5. Humanízalo.** Pasa el guion por `/ig-human` antes de mostrarlo. Una línea
que suena a escrita se nota apenas alguien la dice en voz alta.

**6. Imprime el bloque.** El guion en un bloque de código, el texto en pantalla
como lista aparte con tiempos, y después:

```
REEL LISTO
gancho:     #3 Nadie te dice, puntaje 86 FUERTE
largo:      28,4s en 9 escenas a 160 ppm
pantalla:   6 tarjetas
humanizar:  4 artefactos quitados, puntaje humano 81 PASA
texto:      corre /ig-caption después

Responde «sí» para anotarlo, o dime qué cambio.
```

**7. Nunca publiques.** Esta skill produce un guion. La persona lo graba y lo
publica. Con «sí», agrega a `~/.claude/instagram/CUENTA/log.md` la fecha, la
fórmula usada y la primera línea, para que `/ig-audit` tenga historia después.

## El texto en pantalla es otro guion

Escríbelo aparte, siempre. Se lee antes de escucharse.

- **Seis palabras o menos por tarjeta.** Lo lee alguien con el teléfono a un
  brazo de distancia y que todavía no está escuchando.
- **La tarjeta del gancho está desde el cuadro 1**, no después de un silencio.
- **Dentro de la zona segura.** En un cuadro de 1080x1920, nada sobre y=230 ni
  bajo y=1440, y deja libres los 230 píxeles de la derecha. La interfaz tapa
  todo lo que queda afuera: el texto, la barra de acciones, el audio.
- **Nunca pongas el gancho donde va el texto del post.** Abajo del cuadro está
  tapado.
- **Subtítulos en el cuerpo.** La mayoría ve primero sin sonido.

## Reglas que hacen la diferencia

- **Una idea por reel.** Si el guion tiene dos, son dos reels. Dilo.
- **Números antes que adjetivos.** «$450.000» le gana a «harta plata». Si no
  hay número, pídelo en vez de escribir alrededor del hueco. Plata en pesos
  chilenos, con punto de miles.
- **Corta la introducción.** Sin saludo, sin «en este video», sin nombre, sin
  logo animado. El video parte en la oración a la que llegarías en el segundo
  seis.
- **Cambia el cuadro en cada escena.** Un plano quieto de 8 segundos es donde
  la gente se va, y `beats.py` lo va a marcar.
- **Una sola acción al final.** Comentar una palabra, guardar o seguir. Una.
- **Nunca inventes.** Ni cifras, ni casos, ni testimonios, ni resultados a
  nombre de la cuenta, ni siquiera de relleno. Si falta un número, deja
  `{{tu número}}` en el guion y avísalo.
- **Cuentas institucionales:** lo que prohíbe `voice.md` no se escribe aunque
  el gancho quede mejor. En educación, eso suele ser prometer empleabilidad,
  sueldos o plazos de titulación, o nombrar becas y gratuidad sin sus
  condiciones exactas.
- **No escribas un guion para un audio en tendencia que la cuenta no puede
  usar.** Si la idea necesita la voz propia, dilo.

## Ejemplo

```
/ig-reel dejé de estudiar el fin de semana y subí de 4,8 a 5,9 en un semestre
```

```
GANCHOS  (puntuados con hookscore.py)
  83  FUERTE  #2  Orden negativa     "Deja de estudiar el sábado. Subí de 4,8 a 5,9."
                                     en pantalla: DEJA DE ESTUDIAR EL SÁBADO
  55  OK      #5  Colapso de tiempo  "Estudiaba todo el fin de semana. Ahora solo martes y jueves."
                                     en pantalla: FIN DE SEMANA -> 2 NOCHES
  34  DÉBIL   #9  Róbate esto        "Róbate el horario que me subió el promedio."
                                     en pantalla: RÓBATE ESTO

Grabo el #2: el número es tuyo, se lee de un vistazo y la orden choca con lo que
todos hacen. El #9 no tiene nada concreto: sin el número, no hay nada que robar.
```
