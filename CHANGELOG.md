# Changelog

Todos los cambios importantes del proyecto se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el
proyecto usa [versionado semántico](https://semver.org/lang/es/).

## [Unreleased]

### Añadido

- Procedimientos simbólicos por operación para límites, derivadas, gradiente, Hessiana,
  derivada direccional, geometría y candidatos críticos o de Lagrange. La interfaz aclara
  que no es un tutor universal.
- Comparación de cinco trayectorias para límites de dos o más variables, junto con el límite
  iterado. Se advierte que coincidir en esas trayectorias no demuestra la existencia del
  límite multivariable.
- Análisis real del dominio por variable, con advertencia de que restricciones conjuntas
  pueden requerir análisis adicional.
- Clasificación Hessiana cuando es concluyente para candidatos críticos y advertencias para
  revisar el dominio y clasificar los candidatos de extremos.
- Marcador de evaluación y capas de plano tangente, gradiente o dirección en las gráficas;
  valores no reales o fuera del dominio quedan como huecos.
- Ejemplos, una práctica guiada con pista, historial limitado al almacenamiento local del
  navegador y presentación para imprimir o guardar como PDF desde el navegador.

### Cambiado

- La tabla de operaciones, la hoja de ruta, la API y la estructura del README describen las
  capacidades actuales.
- Los símbolos `e` y `pi` se reconocen como constantes en expresiones y puntos de evaluación,
  y no se cuentan como variables.

### Corregido

- Las familias de puntos críticos con variables libres ya no provocan un error al formatear
  candidatos; se identifican como pendientes de clasificación.
- Las soluciones de Lagrange sin multiplicador determinado ya no generan una expresión vacía
  en el resultado.

### Eliminado

- Copias antiguas y no utilizadas de código, recursos y pruebas que estaban anidadas en
  `app/templates/` y `tests/`, además del test vacío `tests/test_calculator.py`.

## [0.2.0] - 2026-10-25

Primera entrega de la Unidad 1 (cálculo diferencial) y rediseño completo de la interfaz.

### Añadido

- Operaciones nuevas: derivadas de orden superior y mixtas, verificación del teorema de
  Schwarz, gradiente, y plano tangente con recta normal a `z = f(x, y)`.
- API genérica `POST /api/<operacion>`: cualquier operación registrada en `mathcore` queda
  disponible sin tocar `routes.py` (ver "Cómo agregar una operación" en el README).
- Catálogo de operaciones en el frontend (`operations.js`): cada operación declara sus campos,
  su grupo y los requisitos de variables; la interfaz se dibuja a partir de él.
- Selector de operaciones con pestañas por unidad y chips agrupados por tema. Las operaciones
  que no aplican a la función escrita se atenúan e indican el motivo.
- Aviso previo cuando la operación necesita otra cantidad de variables, con el botón Calcular
  bloqueado en lugar de esperar al error del servidor.
- Gráfica en vivo mientras se escribe la función.
- Marcador del punto de evaluación sobre la gráfica y capas por operación: plano tangente
  semitransparente y flecha de máximo ascenso para el gradiente.
- Controles de la gráfica: rango editable de cada eje, vista de superficie o curvas de nivel
  y descarga como PNG.
- Botones para copiar el resultado como LaTeX o como texto.
- Los puntos de evaluación aceptan fracciones y constantes (`1/2`, `pi/2`, `sqrt(2)`).
- Enter en la función o en cualquier campo calcula el resultado.
- Modo sin internet: `python scripts/vendor.py` descarga MathLive y Plotly a
  `app/static/vendor/` y la plantilla los usa automáticamente cuando existen.
- `run.py`, `.gitignore`, `pytest.ini`, `requirements-dev.txt` y este changelog.
- Suite de pruebas por módulo (`test_limits`, `test_derivatives`, `test_geometry`, `test_api`).

### Cambiado

- La interfaz pasa a dos columnas: a la izquierda el flujo completo (función, operación,
  parámetros, calcular y resultado) y a la derecha la gráfica a toda la altura. Se elimina la
  barra de función inferior y la cabecera es más compacta.
- El módulo `operations.py` se divide en `common.py`, `registry.py`, `limits.py`,
  `derivatives.py` y `geometry.py`.
- Todas las operaciones devuelven el mismo formato (`result`, `result_latex`).
- El rango de la gráfica se valida en el servidor y en la interfaz.
- La vista 3D usa menos márgenes, una cámara más cercana y una proporción más ancha.
- `requirements.txt` incluye `antlr4-python3-runtime`, que necesita el lector de LaTeX de SymPy.

### Corregido

- Los valores del punto ya no se evalúan con `sympify`: pasan por el parser controlado y se
  rechaza cualquier texto que no sea un número.
- Las funciones con huecos en el dominio (por ejemplo `log(x) + y`) generaban JSON inválido
  (`NaN`) y la gráfica fallaba; ahora esos puntos quedan como huecos.
- En pantallas estrechas la página quedaba recortada sin posibilidad de desplazarse.
- En pantallas bajas no se podía llegar al resultado.
- El contenedor de la gráfica usaba la clase `plot-container`, que Plotly usa internamente, y
  sus estilos se aplicaban también al elemento interno de Plotly.
- La gráfica no se reajustaba cuando el recuadro cambiaba de tamaño sin cambiar la ventana.
- Los valores escritos en los campos se perdían al cambiar de operación o al detectar variables.
- Errata `oveflow` en `style.css`.

### Eliminado

- `app/mathcore/operations.py` (sustituido por los módulos nuevos).
- `app/static/js/theme.js`, que no se cargaba y apuntaba a un botón inexistente.
- `tests/test_calculator.py` (estaba vacío) y `repomix-output.xml` (no debe versionarse).

## [0.1.0]

Versión inicial.

### Añadido

- Calculadora web con Flask y SymPy: límites multivariables (límite iterado variable por
  variable) y derivada parcial.
- Entrada de funciones en notación matemática con MathLive y detección dinámica de variables.
- Gráfica 2D y 3D con Plotly.
