# Diamond Adventure: notas técnicas de la traducción

## El original

- Cinta CAS con un programa en MSX-BASIC tokenizado que se carga con `CLOAD`. Se llama `Adv` y empieza en &H8001.
- Los textos están en katakana y hiragana del juego de caracteres japonés de MSX.
- Salida de texto: SCREEN 2 a través de `OPEN "grp:"` (`PRINT #1`, 32 columnas, zona de mensajes entre y=152 e y=200) y SCREEN 1 para las pantallas de texto (unos 28 caracteres útiles).

### Analizador de órdenes

- Pide un verbo («QUE HACES ?») y, si hace falta, un objeto («QUE OBJETO ?»).
- Solo compara las **3 primeras letras**: `A$=LEFT$(A$+"  ",3)`.
- El vocabulario está escondido en `DATA` en hexadecimal (líneas 3120 a 3160) y se lee en `A$(0..18)` (verbos) y `B$(0..16)` (objetos) con `CHR$(VAL("&h"+X$))`. La línea 3170 son datos sin usar.

### Variables principales

| Variable | Uso |
| --- | --- |
| `SC` | Escena: 0 calle, 1 pasillo, 2 a 7 habitaciones, 8 cuarto secreto, 9 armario, 10 detrás de la librería, 11 caja fuerte |
| `ST` | Piso |
| `C(0..6)` | Los 7 escondites, donde se reparten al azar 4 objetos |
| `PC$` | Código de 5 cifras de la caja fuerte |
| `B3`, `B4` | Libros correctos del puzle de la biblioteca |
| `DA` | Diamante conseguido |

### Caracteres

En el juego japonés, los códigos `01h`+`41h..4Fh` son kanji (月火水木金土日年円時分秒百千万) y el texto los usaba, por ejemplo `1千万` (10 millones) y `時`. Los códigos `01h`+`50h..5Fh`, usados para las cajas, son iguales en los juegos de caracteres japonés e internacional.

## Cambios de la traducción

- Todos los textos traducidos, **en mayúsculas, sin tildes ni Ñ**, para que se vean bien en MSX japonés y europeo.
- Se mantienen «\*\*DIAMOND ADVENTURE\*\*», «GAME START» y «GAME OVER».
- Vocabulario nuevo, con prefijos de 3 letras distintos y codificado en hexadecimal igual que el original:
  - Verbos `A$(0..18)`: AYUDA, MOVER, COGER, MIRAR, SUBIR, BAJAR, DERECHA, IZQUIERDA, ADELANTE, ABRIR, USAR, ENCENDER, ATRAS, BUSCAR, CONECTAR, APAGAR, FIN, ABRIR (repetido también en el original: ｱｹﾙ) y ENTRAR.
  - Objetos `B$(0..16)`: PUERTA, BUZON, LLAVE, SILLA, MESA, ARMARIO, LIBRO, JARRON, TELE, DIAMANTE, VENTANA, CAJA, VELA, CERILLAS, CUADRO, BOLIGRAFO, NOTA.
- ﾂｹﾙ (encender fuego) es **ENCENDER** e ｲﾚﾙ (accionar el interruptor) es **CONECTAR**.
- Línea nueva 1285: `IFC$>="a"ANDC$<="z"THENC$=CHR$(ASC(C$)-32)`, que pasa a mayúsculas lo tecleado.
- La línea 1460 escribe `"PISO";ST` en vez de `ST;" F"`, y la etiqueta POST de la línea 1470 pasa a ser BUZON (en x=198).

### Rarezas del original que se mantienen

- `GOSUB 2340` sin `RETURN` (espera dos teclas).
- `GOSUBGOSUB2430` en la línea 2500.
- `PRINT` sin `#1` en la línea 1190.
- FIN hace `NEW`.
- La tecla de retroceso no borra en pantalla.

## Cómo se hizo

1. Un detokenizador y tokenizador de MSX-BASIC propio que reproduce el original **byte a byte**: tablas de tokens normales y con prefijo `FFh`, enteros `11h..1Ah`, `0Fh` y `1Ch`, números de línea `0Eh`, doble precisión `1Fh`, `ELSE` como `3A A1` y el apóstrofo como `3A 8F E6`.
2. Las líneas se editaron sobre un listado escapado (`{XX}` para cada byte no ASCII) y se volvió a tokenizar, recalculando los punteros de enlace desde &H8001.
3. El CAS se genera con la cabecera `1F A6 DE BA CC 13 7D 74`, 10 bytes `D3` y el nombre de 6 caracteres; después otra cabecera, el programa y 7 bytes a cero de relleno.
4. Verificación con un intérprete mínimo de MSX-BASIC, con gráficos y sonido simulados y un jugador automático: la partida completa en castellano se gana, y la misma partida con el original japonés sigue exactamente el mismo camino (63 467 pasos iguales, sin contar el bucle que lee las teclas). También se comprobaron las muertes: CONECTAR TELE, subir al piso 4, ABRIR PUERTA en los pisos 1 o 2 y el código equivocado.

Como el programa traducido cambia de longitud y se recalculan todos los enlaces entre líneas, el parche IPS cubre casi todo el programa.
