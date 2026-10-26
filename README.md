# NekoCalc — Calculadora Multivariable

Aplicación web desarrollada con **Flask** y **SymPy** para trabajar con funciones de varias variables: límites, derivadas parciales, gradiente, plano tangente y más, con gráficas 2D/3D interactivas.

El proyecto nace como Proyecto Integrador de Matemática II (cálculo diferencial, integral y vectorial de funciones multivariables) y está pensado para crecer unidad por unidad.

Actualmente el proyecto se encuentra en desarrollo. Consulta el [CHANGELOG](CHANGELOG.md) para ver qué cambió en cada versión.

## Características

* Escritura de funciones en notación matemática (MathLive) con detección automática de variables.
* Selector de operaciones por unidad y tema; las que no aplican a la función escrita se atenúan y explican el motivo.
* Gráfica en vivo de funciones de 1 o 2 variables, con rango de ejes editable, vista de superficie o curvas de nivel y descarga como PNG.
* La gráfica marca el punto de evaluación y dibuja la capa de cada operación (plano tangente, flecha del gradiente).
* Resultado en notación matemática, con botones para copiarlo como LaTeX o texto.
* Puntos de evaluación con fracciones y constantes (`1/2`, `pi/2`, `sqrt(2)`).
* Enter para calcular desde cualquier campo.
* Funciona sin internet una vez descargadas las librerías del navegador (ver [Modo sin internet](#modo-sin-internet)).
* API REST sencilla y extensible: agregar una operación nueva no requiere tocar las rutas.

## Operaciones disponibles

| Unidad | Operación | Qué hace |
| --- | --- | --- |
| 1 | Límite multivariable | Límite iterado variable por variable en un punto |
| 1 | Derivada parcial | Respecto a una variable, simbólica o evaluada en un punto |
| 1 | Derivada de orden superior | Derivadas sucesivas y mixtas (`x, y, x`), simbólicas o evaluadas |
| 1 | Teorema de Schwarz | Calcula `f_xy` y `f_yx` y verifica si son iguales |
| 1 | Gradiente | Vector gradiente, simbólico o evaluado en un punto |
| 1 | Plano tangente y recta normal | A `z = f(x, y)` en un punto |

> **Nota sobre los límites:** el cálculo itera el límite variable por variable (límite iterado). Esto **no** equivale al límite multivariable riguroso, que exige obtener el mismo valor por cualquier trayectoria. Un límite iterado puede existir aunque el límite doble no exista.

### Hoja de ruta

- [x] Límites, derivadas parciales, orden superior, Schwarz, gradiente, plano tangente
- [ ] Dominio, rango, curvas y superficies de nivel; continuidad
- [ ] Diferencial total, diferencial exacta y función potencial
- [ ] Regla de la cadena, derivación implícita y Jacobiano
- [ ] Derivada direccional, extremos (Hessiano) y multiplicadores de Lagrange
- [ ] Unidad 2: integrales dobles y triples, áreas, volúmenes, masa y momentos
- [ ] Unidad 3: funciones vectoriales, campos, divergencia, rotacional, integrales de línea y Green

---

# Requisitos

Necesitas tener instalado:

* Python 3.11 o superior
* pip
* Git
* npm (opcional, solo para el [modo sin internet](#modo-sin-internet))

Puedes comprobar que están instalados con:

```bash
python --version
pip --version
git --version
```

En algunos sistemas el comando de Python puede ser:

```bash
python3 --version
```

---

# Instalación

Primero clona el repositorio:

```bash
git clone https://github.com/yeim666/multivariable-calc-mat2.git
```

Entra en la carpeta:

```bash
cd multivariable-calc-mat2
```

Se recomienda utilizar un entorno virtual para evitar instalar las dependencias globalmente.

## Linux y macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Windows

PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

CMD:

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Si PowerShell impide ejecutar el script de activación, puedes utilizar CMD o cambiar temporalmente la política de ejecución para la sesión actual.

---

# Ejecutar el programa

Primero asegúrate de tener el entorno virtual activado.

Luego ejecuta Flask desde la carpeta principal del proyecto:

```bash
flask --app 'app:create_app' --debug run
```

En Windows CMD, si las comillas simples causan problemas, utiliza:

```cmd
flask --app app:create_app --debug run
```

También puedes usar el script incluido (añade `FLASK_DEBUG=1` para el modo de desarrollo):

```bash
python run.py
```

Flask debería mostrar una dirección similar a:

```text
http://127.0.0.1:5000
```

Abre esa dirección en tu navegador. Para detener el servidor utiliza `Ctrl + C`.

## Modo sin internet

La interfaz usa dos librerías del navegador, MathLive (entrada matemática) y Plotly (gráficas), que por defecto se cargan desde un CDN. Para trabajar sin conexión, descárgalas una vez (requiere npm):

```bash
python scripts/vendor.py
```

Los archivos quedan en `app/static/vendor/` y la plantilla los usa automáticamente cuando existen; si borras esa carpeta, vuelve a usar el CDN. La carpeta está en `.gitignore`: si quieres versionarla para desplegar sin npm, quita esa línea.

Las fuentes de Google siguen cargándose en línea; sin conexión se usan las fuentes del sistema.

---

# Cómo usar la calculadora

1. Escribe una función en el campo **Función**, por ejemplo `x^2 + y^2`. Las variables se detectan solas y la gráfica se dibuja en vivo.
2. Elige una **operación** en el panel (por unidad y tema).
3. Completa los campos que pide: un punto, la variable a derivar, el orden de derivación, etc. Los puntos aceptan fracciones como `1/2` o constantes como `pi`.
4. Pulsa **Calcular** (o presiona Enter).
5. El resultado aparece en el panel, con botones para copiarlo. La gráfica marca el punto y dibuja la capa de la operación.

Ejemplo:

```text
Función:     x^2 + y^2
Operación:   Plano tangente y recta normal
Punto:       x = 1, y = 2

Resultado:   z = 2x + 4y − 5
             r(t) = (1 + 2t, 2 + 4t, 5 − t)
```

---

# API

Todas las rutas reciben y devuelven JSON. La función se envía como `latex` (lo que produce MathLive) o como `expression` (texto, por ejemplo `x^2*y`).

Las operaciones responden con:

```json
{ "success": true, "result": "5", "result_latex": "5" }
```

Y los errores con:

```json
{ "success": false, "error": "mensaje para el usuario" }
```

| Ruta | Parámetros además de la función | Respuesta extra |
| --- | --- | --- |
| `POST /api/variables` | — | `variables`, `variables_latex` |
| `POST /api/limit` | `point` (obligatorio) | — |
| `POST /api/derivative` | `variable` (obligatorio), `point` | — |
| `POST /api/higher_derivative` | `variables` (lista, en orden), `point` | — |
| `POST /api/schwarz` | `variables` (exactamente 2) | `equal` |
| `POST /api/gradient` | `point` | — |
| `POST /api/tangent_plane` | `point` (obligatorio, 2 variables) | — |
| `POST /api/plot` | `x_range`, `y_range`, `point`, `overlay` (`tangent_plane` o `gradient`) | `type`, `x`, `y`, `z`, `marker`, `plane_z`, `gradient_arrow` |

`point` es un objeto `{ "x": "1", "y": "1/2" }` con un valor por variable.

Ejemplo:

```bash
curl -X POST http://127.0.0.1:5000/api/limit \
  -H "Content-Type: application/json" \
  -d '{"expression": "x^2 + y^2", "point": {"x": "1", "y": "2"}}'
```

---

# Cómo agregar una operación

1. **Backend.** Escribe la función en el módulo que corresponda de `app/mathcore/` y regístrala. Recibe la expresión de SymPy y los parámetros del JSON, y devuelve `make_result(...)`:

   ```python
   # app/mathcore/derivatives.py
   from app.mathcore.common import make_result
   from app.mathcore.registry import register

   @register("mi_operacion")
   def mi_operacion(expr, params):
       # ...calcula con sympy...
       return make_result(resultado)
   ```

   Si creas un módulo nuevo, impórtalo en `app/mathcore/__init__.py` para que el decorador se ejecute. La ruta `/api/mi_operacion` queda disponible sin tocar `routes.py`.

2. **Frontend.** Agrega una entrada en `app/static/js/operations.js` con su unidad, grupo, endpoint y campos (`point`, `variable`, `variableList` o `variablePair`). Opcionalmente `requires` (cantidad de variables), `overlay` (capa en la gráfica) y `note` (texto bajo el resultado).

3. **Pruebas.** Agrega tests en `tests/`.

---

# Pruebas

```bash
pip install -r requirements-dev.txt
python -m pytest
```

---

# Estructura del proyecto

```text
multivariable-calc-mat2/
├── app/
│   ├── __init__.py            # fábrica de la app (create_app)
│   ├── routes.py              # rutas: /, /api/variables, /api/plot y /api/<operación>
│   ├── mathcore/
│   │   ├── common.py          # variables, LaTeX y formato de resultados
│   │   ├── registry.py        # registro de operaciones (@register)
│   │   ├── parser.py          # texto/LaTeX → expresión de SymPy
│   │   ├── limits.py          # límites
│   │   ├── derivatives.py     # derivadas, orden superior, Schwarz, gradiente
│   │   ├── geometry.py        # plano tangente y recta normal
│   │   └── plotting.py        # datos de gráficas 2D/3D, marcador y capas
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/
│   │       ├── operations.js  # catálogo de operaciones de la interfaz
│   │       └── main.js        # lógica de la interfaz
│   └── templates/index.html
├── scripts/vendor.py          # descarga MathLive y Plotly para uso sin internet
├── tests/
├── run.py
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── CHANGELOG.md
└── README.md
```
