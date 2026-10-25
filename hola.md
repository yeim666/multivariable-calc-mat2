Project Path: multivariable-calc-mat2

Source Tree:

```txt
multivariable-calc-mat2
├── README.md
├── app
│   ├── __init__.py
│   ├── mathcore
│   │   ├── __init__.py
│   │   ├── operations.py
│   │   ├── parser.py
│   │   └── plotting.py
│   ├── routes.py
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── js
│   │       ├── main.js
│   │       └── theme.js
│   └── templates
│       └── index.html
├── repomix-output.xml
├── requirements.txt
└── tests
    └── test_calculator.py

```

`README.md`:

```md
# Calculadora Multivariable

Aplicación web desarrollada con **Flask** y **SymPy** para calcular límites de funciones multivariables.

El proyecto está pensado como una herramienta sencilla para trabajar con funciones de varias variables desde una interfaz web.

Actualmente el proyecto se encuentra en desarrollo.

## Características

* Cálculo de límites multivariables.
* Interfaz web sencilla.
* Backend desarrollado con Flask.
* Cálculos simbólicos utilizando SymPy.
* Preparado para añadir derivadas parciales y otras operaciones en el futuro.

---

# Requisitos

Necesitas tener instalado:

* Python 3
* pip
* Git

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
git clone https://github.com/yeim666/multivariable-calc-mat2/
```

Entra en la carpeta:

```bash
cd calculadora-web
```

Se recomienda utilizar un entorno virtual para evitar instalar las dependencias globalmente.

## Linux

Crear el entorno virtual:

```bash
python3 -m venv venv
```

Activarlo:

```bash
source venv/bin/activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

---

## macOS

Crear el entorno virtual:

```bash
python3 -m venv venv
```

Activarlo:

```bash
source venv/bin/activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Dependiendo de la instalación de Python, también puede funcionar:

```bash
python -m venv venv
```

---

## Windows

Crear el entorno virtual:

```powershell
python -m venv venv
```

Si utilizas PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Si utilizas CMD:

```cmd
venv\Scripts\activate
```

Después instala las dependencias:

```powershell
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

Flask debería mostrar una dirección similar a:

```text
http://127.0.0.1:5000
```

Abre esa dirección en tu navegador.

Para detener el servidor utiliza:

```text
Ctrl + C
```

---

# Cómo usar la calculadora

1. Abre la aplicación en el navegador.

2. Selecciona la operación que deseas realizar.

3. Para calcular un límite, escribe una función utilizando las variables `x` y `y`.

Por ejemplo:

```text
x^2 + y^2
```

4. Introduce el punto al que deben aproximarse las variables.

Por ejemplo:

```text
x → 0
y → 0
```

5. Presiona el botón **Calcular**.

El resultado aparecerá en la parte inferior de la calculadora.

Ejemplo:

```text
Función:

x^2 + y^2

Punto:

(0, 0)

Resultado:

0
```

Actualmente algunas expresiones o límites multivariables complejos pueden no ser evaluados correctamente, ya que el sistema de cálculo todavía está en desarrollo.

---

# Estructura del proyecto

```text
calculadora-web/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── calculator.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       │
│       └── js/
│           └── main.js
│
├── tests/
│   └── test_calculator.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Archivos principales

### `app/__init__.py`

Inicializa la aplicación Flask y registra las rutas.

### `app/routes.py`

Contiene las rutas de Flask y los endpoints de la API.

Por ejemplo:

```text
/
```

muestra la página principal.

Mientras que:

```text
/api/limit
```

recibe los datos enviados desde JavaScript y solicita el cálculo del límite.

### `app/calculator.py`

Contiene la lógica matemática de la aplicación.

Aquí se utiliza SymPy para interpretar expresiones y realizar los cálculos.

### `app/templates/index.html`

Contiene la estructura de la interfaz.

### `app/static/css/style.css`

Contiene los estilos de la página.

### `app/static/js/main.js`

Controla la interacción de la interfaz y la comunicación con el backend mediante `fetch()`.

---

# Contribuir

Las contribuciones son bienvenidas.

Para trabajar en el proyecto sin destruir accidentalmente la rama principal, sigue este flujo.

## 1. Clonar el repositorio

```bash
git clone https://github.com/yeim666/multivariable-calc-mat2/
```

Después:

```bash
cd calculadora-web
```

Instala las dependencias siguiendo las instrucciones anteriores.

---

## 2. Crear una nueva rama

No trabajes directamente sobre `main`.

Crea una rama para tu cambio:

```bash
git switch -c nombre-de-la-rama
```

Por ejemplo:

```bash
git switch -c feat-derivadas-parciales
```

También puedes utilizar:

```bash
git checkout -b feat-derivadas-parciales
```

---

## 3. Realizar los cambios

Modifica únicamente lo necesario para la funcionalidad en la que estés trabajando.

Antes de hacer un commit puedes revisar los archivos modificados con:

```bash
git status
```

---

## 4. Añadir los cambios

```bash
git add .
```

---

## 5. Crear un commit

Intentamos utilizar mensajes de commit claros.

Formato recomendado:

```text
tipo: descripción
```

Algunos tipos:

```text
feat: nueva funcionalidad

fix: corrección de un error

docs: cambios en documentación

style: cambios visuales o de formato

refactor: reorganización del código

test: cambios relacionados con pruebas

chore: configuración o mantenimiento
```

Ejemplos:

```bash
git commit -m "feat: add partial derivative support"
```

```bash
git commit -m "fix: validate empty function input"
```

```bash
git commit -m "docs: update installation guide"
```

---

## 6. Subir la rama

```bash
git push -u origin nombre-de-la-rama
```

Por ejemplo:

```bash
git push -u origin feat-derivadas-parciales
```

---

## 7. Crear un Pull Request

Desde GitHub, crea un **Pull Request** desde tu rama hacia `main`.

En la descripción explica brevemente:

* Qué cambiaste.
* Por qué lo cambiaste.
* Cómo se puede probar.

Después el código puede revisarse antes de integrarlo a la rama principal.

---

# Recomendaciones para contribuir

Antes de enviar cambios:

* Comprueba que el programa siga ejecutándose.
* Prueba manualmente la funcionalidad modificada.
* No subas el entorno virtual `venv/`.
* No subas archivos temporales.
* Evita modificar archivos que no estén relacionados con tu cambio.
* Intenta mantener el código legible.
* Añade comentarios cuando una parte del código no sea evidente.
* Haz commits pequeños y relacionados con un único cambio.

---

# Flujo general de la aplicación

```text
Usuario
   │
   ▼
HTML
   │
   ▼
JavaScript
   │
   │ fetch()
   ▼
API de Flask
   │
   ▼
calculator.py
   │
   ▼
SymPy
   │
   ▼
Flask devuelve JSON
   │
   ▼
JavaScript
   │
   ▼
Resultado mostrado en HTML
```

---

# Estado del proyecto

Actualmente se está trabajando principalmente en:

* Límites multivariables.
* Interpretación de expresiones matemáticas.
* Validación de datos.
* Mejora de la precisión de los cálculos.

Entre las funcionalidades previstas se encuentran:

* Derivadas parciales.
* Mejor representación matemática de los resultados.
* Soporte para más tipos de expresiones.
* Mejor manejo de errores.
* Pruebas automatizadas.

---

# Tecnologías utilizadas

* Python
* Flask
* SymPy
* HTML
* CSS
* JavaScript


```
`app/__init__.py`:

```py
from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes import main
    app.register_blueprint(main)

    return app

```
`app/mathcore/__init__.py`:

```py
from app.mathcore.parser import parse_expression, latex_to_expr
from app.mathcore.operations import (
    get_variables,
    multivariable_limit,
    partial_derivative,
    gradient,
    to_latex,
)
from app.mathcore.plotting import generate_plot_data

```
`app/mathcore/operations.py`:

```py
import sympy as sp


# obtiene las variables libres de una expresion, ordenadas alfabeticamente
def get_variables(expression):
    return sorted(expression.free_symbols, key=str)


# limite multivariable: itera el limite variable por variable.
# nota: esto es un limite iterado, no el limite multivariable riguroso
# (que exige que el resultado sea el mismo por cualquier trayectoria).
def multivariable_limit(expr, point):

    variables = get_variables(expr)

    # si no hay variables, la expresion es una constante: el limite es ella misma
    if not variables:
        return expr

    result = expr

    for variable in variables:
        value = point[str(variable)]

        # intento rapido: sustitucion directa, evita el costo de sp.limit
        # cuando el punto no es una indeterminacion
        try:
            substituted = result.subs(variable, value)

            if substituted.is_finite is not False and not substituted.has(sp.nan, sp.zoo):
                result = substituted
                continue

        except Exception:
            pass

        # fallback: calculo simbolico real del limite (mas lento, pero necesario
        # para formas indeterminadas)
        result = sp.limit(result, variable, value)

    return result


# derivada parcial respecto a una variable. point es opcional: si se da,
# la derivada se evalua ahi; si no, se devuelve la forma simbolica
def partial_derivative(expr, variable_name, point=None):

    variables = {str(v): v for v in get_variables(expr)}

    if variable_name not in variables:
        raise ValueError(f"La variable '{variable_name}' no aparece en la expresión.")

    variable = variables[variable_name]
    result = sp.diff(expr, variable)

    if point:
        subs_point = {variables[k]: v for k, v in point.items() if k in variables}
        result = result.subs(subs_point)

    return result


# gradiente completo: diccionario {variable: derivada parcial}.
# util para analisis y para la grafica (direccion de maximo crecimiento)
def gradient(expr, point=None):

    variables = get_variables(expr)
    grad = {}

    for variable in variables:
        deriv = sp.diff(expr, variable)

        if point:
            subs_point = {v: point[str(v)] for v in variables if str(v) in point}
            deriv = deriv.subs(subs_point)

        grad[str(variable)] = deriv

    return grad

# convierte un objeto sympy a su representación en LaTeX, para que el
# frontend pueda renderizarlo como notación matemática real (no como
# texto plano estilo python/sympy)
def to_latex(expr):
    return sp.latex(expr)

```
`app/mathcore/parser.py`:

```py
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)
from sympy.parsing.latex import parse_latex


# transformaciones para el parser de texto plano:
# - implicit_multiplication_application: permite "2x" -> "2*x", "xy" -> "x*y"
# - convert_xor: convierte "^" en potencia (**) en vez de xor bit a bit
TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


# funciones matematicas permitidas explicitamente en el parser de texto plano.
# cualquier identificador que NO este aqui, sympy lo trata como variable nueva
# automaticamente. esto es lo que permite funciones de cualquier nombre de variable.
ALLOWED_FUNCTIONS = {
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "sinh": sp.sinh,
    "cosh": sp.cosh,
    "tanh": sp.tanh,
    "exp": sp.exp,
    "log": sp.log,
    "ln": sp.log,
    "sqrt": sp.sqrt,
    "Abs": sp.Abs,
    "pi": sp.pi,
    "E": sp.E,
}


# espacio de evaluacion controlado para parse_expr. sin __builtins__, para
# que el usuario no pueda ejecutar codigo python arbitrario (ej. __import__).
# Symbol, Integer y Float estan aqui porque las transformaciones de sympy
# generan codigo interno que los necesita para crear variables/numeros nuevos.
GLOBAL_DICT = {
    "Symbol": sp.Symbol,
    "Integer": sp.Integer,
    "Float": sp.Float,
    "__builtins__": {},
}


# parser de texto plano (ej. "x^2 + y^2", "sqrt(x)+sin(y)").
# cualquier identificador que el usuario escriba y que no este en
# ALLOWED_FUNCTIONS se convierte automaticamente en una variable simbolica nueva.
def parse_expression(expression):

    return parse_expr(
        expression,
        local_dict=ALLOWED_FUNCTIONS,
        global_dict=GLOBAL_DICT,
        transformations=TRANSFORMATIONS,
    )


# parser de notacion LaTeX (usado por el math-field de MathLive).
# devuelve directamente un objeto sympy, igual que parse_expression.
def latex_to_expr(latex_string):

    try:
        return parse_latex(latex_string)

    # normalizamos cualquier error interno de parse_latex a ValueError,
    # para que routes.py lo maneje igual que los errores del parser de texto
    except Exception as e:
        raise ValueError(f"No se pudo interpretar la notación matemática: {e}")

```
`app/mathcore/plotting.py`:

```py
import sympy as sp
import numpy as np

from app.mathcore.operations import get_variables


# genera los puntos numericos para graficar una funcion de 1 o 2 variables.
# x_range/y_range son tuplas (minimo, maximo). resolution es cuantos puntos
# por eje (mas resolucion = superficie mas suave, pero mas lento).
def generate_plot_data(expr, x_range=(-10, 10), y_range=(-10, 10), resolution=60):

    variables = get_variables(expr)

    if len(variables) == 0:
        raise ValueError("La expresión es una constante, no se puede graficar.")

    if len(variables) > 2:
        raise ValueError("Solo se pueden graficar funciones de 1 o 2 variables.")

    if len(variables) == 1:
        return _plot_2d(expr, variables[0], x_range, resolution)

    return _plot_3d(expr, variables[0], variables[1], x_range, y_range, resolution)


# caso de una sola variable: linea 2D, y = f(x)
def _plot_2d(expr, var, x_range, resolution):

    # lambdify convierte la expresion simbolica en una funcion de numpy,
    # mucho mas rapida que evaluar sympy punto por punto
    f = sp.lambdify(var, expr, modules=["numpy"])

    x_vals = np.linspace(x_range[0], x_range[1], resolution)

    # evaluamos la funcion en todos los puntos de una vez (vectorizado)
    y_vals = f(x_vals)

    return {
        "type": "2d",
        "x": x_vals.tolist(),
        "y": np.real(y_vals).tolist(),  # descartamos parte imaginaria si aparece
    }


# caso de dos variables: superficie 3D, z = f(x, y)
def _plot_3d(expr, var1, var2, x_range, y_range, resolution):

    f = sp.lambdify((var1, var2), expr, modules=["numpy"])

    x_vals = np.linspace(x_range[0], x_range[1], resolution)
    y_vals = np.linspace(y_range[0], y_range[1], resolution)

    # meshgrid arma la malla 2D de combinaciones (x, y) sobre la que evaluamos
    x_grid, y_grid = np.meshgrid(x_vals, y_vals)

    z_grid = f(x_grid, y_grid)

    # si la funcion es constante en una de las variables, numpy puede devolver
    # un solo numero en vez de una malla completa. la expandimos manualmente.
    if np.isscalar(z_grid):
        z_grid = np.full_like(x_grid, z_grid, dtype=float)

    return {
        "type": "3d",
        "x": x_vals.tolist(),
        "y": y_vals.tolist(),
        "z": np.real(z_grid).tolist(),
        "variable_names": [str(var1), str(var2)],
    }

```
`app/routes.py`:

```py
from flask import Blueprint, render_template, request, jsonify

from app.mathcore import (
    parse_expression,
    latex_to_expr,
    multivariable_limit,
    partial_derivative,
    get_variables,
    generate_plot_data,
    to_latex,
)


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


# decide que parser usar segun lo que mande el frontend.
def get_expr_from_request(data):

    if data.get("latex"):
        return latex_to_expr(data["latex"])

    elif data.get("expression"):
        return parse_expression(data["expression"])

    else:
        raise ValueError("No se proporcionó una expresión ni notación LaTeX.")


# api de variables
#
# /api/variables
@main.route("/api/variables", methods=["POST"])
def variables():

    data = request.get_json()

    if not data:
        return jsonify({ 
            "success": False,
            "error": "No se recibieron datos."
        }), 400

    try:
        expr = get_expr_from_request(data)
        vars_found = get_variables(expr)

        return jsonify({
            "success": True,
            "variables": [str(v) for v in vars_found],
            "variables_latex": [to_latex(v) for v in vars_found],
        })

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"[/api/variables] error: {e}")
        return jsonify({
            "success": False,
            "error": "No se pudo interpretar la expresión."
        }), 400


# api de limites
#
# /api/limit
@main.route("/api/limit", methods=["POST"])
def limit():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No se recibieron datos."
        }), 400

    point = data.get("point")

    if not point:
        return jsonify({
            "success": False,
            "error": "No se proporcionó el punto."
        }), 400

    try:
        expr = get_expr_from_request(data)
        result = multivariable_limit(expr, point)

        return jsonify({
            "success": True,
            "result": str(result),
            "result_latex": to_latex(result),
        })

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"[/api/limit] error: {e}")
        return jsonify({
            "success": False,
            "error": "No se pudo calcular el límite."
        }), 400


# api de derivadas parciales
#
# /api/derivative
@main.route("/api/derivative", methods=["POST"])
def derivative():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No se recibieron datos."
        }), 400

    variable = data.get("variable")
    point = data.get("point")  # opcional

    if not variable:
        return jsonify({
            "success": False,
            "error": "No se proporcionó la variable respecto a la cual derivar."
        }), 400

    try:
        expr = get_expr_from_request(data)
        result = partial_derivative(expr, variable, point)

        return jsonify({
            "success": True,
            "result": str(result),
            "result_latex": to_latex(result),
        })

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"[/api/derivative] error: {e}")
        return jsonify({
            "success": False,
            "error": "No se pudo calcular la derivada."
        }), 400


# api de graficas
#
# /api/plot
@main.route("/api/plot", methods=["POST"])
def plot():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No se recibieron datos."
        }), 400

    try:
        expr = get_expr_from_request(data)

        # rango de graficado opcional, con valores por defecto razonables
        x_range = tuple(data.get("x_range", (-10, 10)))
        y_range = tuple(data.get("y_range", (-10, 10)))

        plot_data = generate_plot_data(expr, x_range=x_range, y_range=y_range)

        return jsonify({
            "success": True,
            **plot_data
        })

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"[/api/plot] error: {e}")
        return jsonify({
            "success": False,
            "error": "No se pudo generar la gráfica."
        }), 400

```
`app/static/css/style.css`:

```css
/* ====================================================
   TOKENS DE DISEÑO — paleta inspirada en Nekopara, sutil
   ==================================================== */

* {
    box-sizing: border-box;
}


:root {
    --cream: #fbf3ef;        /* fondo general */
    --panel: #ffffff;        /* superficies (panel, inputs) */
    --blush: #f6d9e4;        /* bordes y rellenos suaves */
    --sakura: #e48aae;       /* acento primario: botones, foco, "Nyan" del logo */
    --highlight: #c9718b;    /* acento secundario: borde del resultado */
    --cocoa: #3e2a2e;        /* texto principal, "delbrot" del logo */
    --cocoa-muted: #8c7377;  /* texto secundario */
    --error: #b3475b;        /* mensajes de error */

    --font-logo: "Fredoka", sans-serif;
    --font-heading: "Plus Jakarta Sans", sans-serif;
    --font-body: "Inter", sans-serif;

    --radius: 8px;
    --transition: 0.15s ease;
}


@media (prefers-reduced-motion: reduce) {
    * {
        transition: none !important;
    }
} 


/* ====================================================
   BASE
   ==================================================== */

html, body {
    margin: 0;
    min-height: 100vh;

    background: var(--cream);
    color: var(--cocoa);

    font-family: var(--font-body);
    font-size: 15px;
    line-height: 1.5;
}



.app {
    position: relative;

    display: grid;
    grid-template-areas:
        "topbar topbar"
        "sidebar canvas"
        "function function";
    grid-template-columns: 340px 1fr;
    grid-template-rows: auto minmax(0, 1fr) auto;

    height: 100vh;
    oveflow: hidden;
}


.app::before {
    content: "";
    position: fixed;
    inset: 0;

    z-index: -1;

    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'%3E%3Cg fill='%23e48aae'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3Ccircle cx='22' cy='22' r='2.2'/%3E%3Ccircle cx='38' cy='22' r='2.2'/%3E%3Ccircle cx='22' cy='38' r='2.2'/%3E%3Ccircle cx='38' cy='38' r='2.2'/%3E%3Ccircle cx='90' cy='80' r='4'/%3E%3Ccircle cx='82' cy='72' r='2.2'/%3E%3Ccircle cx='98' cy='72' r='2.2'/%3E%3Ccircle cx='82' cy='88' r='2.2'/%3E%3Ccircle cx='98' cy='88' r='2.2'/%3E%3C/g%3E%3C/svg%3E");
    background-size: 160px 160px;
    opacity: 0.06;
}


/* enfoque visible por teclado */
button:focus-visible,
select:focus-visible,
input:focus-visible,
math-field:focus-within {
    outline: 2px solid var(--sakura);
    outline-offset: 2px;
}


/* ====================================================
   LOGO Y BARRA SUPERIOR
   ==================================================== */

.topbar {
    grid-area: topbar;

    padding: 1.4rem 1.75rem 1rem;

    border-bottom: 1px solid var(--blush);
    background: var(--panel);
}


.logo {
    margin: 0;

    font-family: var(--font-logo);
    font-size: 1.9rem;
    font-weight: 600;
    letter-spacing: -0.01em;
}


.logo-nyan {
    color: var(--sakura);
}


.logo-delbrot {
    color: var(--cocoa);
}


.topbar-subtitle {
    margin: 0.25rem 0 0;

    color: var(--cocoa-muted);

    font-family: var(--font-body);
    font-size: 0.85rem;
}


/* ====================================================
   PANEL DE CONTROL
   ==================================================== */

.control-panel {
    grid-area: sidebar;

    padding: 1.6rem;

    border-right: 1px solid var(--blush);
    background: var(--panel);

    overflow-y: auto;
}


/* ====================================================
   LIENZO — mas grande, es el foco visual principal
   ==================================================== */

.canvas {
    grid-area: canvas;

    display: flex;

    padding: 1.6rem;

    min-height: 0;
}


.plot-container {
    width: 100%;
    height: 100%;

    display: flex;
    align-items: center;
    justify-content: center;

    border: 1px solid var(--blush);
    border-radius: var(--radius);

    background: var(--panel);

    overflow: hidden;
}


.canvas-placeholder {
    color: var(--cocoa-muted);

    font-family: var(--font-body);
    font-size: 0.9rem;
}


/* ====================================================
   BARRA DE FUNCION (abajo, ancho completo)
   ==================================================== */

.function-bar {
    grid-area: function;
    margin: 0;
    padding: 0.85rem 1.75rem;

    border-top: 1px solid var(--blush);
    background: var(--panel);
}


.function-bar-inner {
    max-width: 900px;
    margin: 0 auto;
}


/* ====================================================
   RESPONSIVE
   ==================================================== */

@media (max-width: 900px) {

    .app {
        grid-template-areas:
            "topbar"
            "sidebar"
            "canvas"
            "function";
        grid-template-columns: 1fr;
    }

    .control-panel {
        border-right: none;
        border-bottom: 1px solid var(--blush);
    }

    .canvas {
        min-height: 45vh;
    }

}


/* ====================================================
   SECCIONES Y TITULOS
   ==================================================== */

section {
    margin-bottom: 1.5rem;
}


.section-title {
    display: flex;
    align-items: baseline;
    justify-content: space-between;

    margin-bottom: 0.6rem;
}


.section-title h2 {
    margin: 0;

    font-family: var(--font-heading);
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--cocoa);
}


.section-title span {
    color: var(--cocoa-muted);

    font-size: 0.78rem;
}


label {
    display: block;

    margin-bottom: 0.5rem;

    display: flex;
    align-items: center;
    gap: 0.3rem;

    color: var(--cocoa-muted);

    font-size: 0.82rem;
}


/* ====================================================
   INPUTS
   ==================================================== */

input,
select {
    width: 100%;

    padding: 0.7rem 0.85rem;

    border: 1px solid var(--blush);
    border-radius: var(--radius);

    outline: none;

    background: var(--cream);
    color: var(--cocoa);

    font-family: var(--font-body);
    font-size: 0.9rem;

    transition: border-color var(--transition);
}


input:focus,
select:focus {
    border-color: var(--sakura);
}


input::placeholder {
    color: var(--cocoa-muted);
    opacity: 0.6;
}


select {
    cursor: pointer;
}


/* campo matematico principal (funcion) */
.function-input {
    display: block;
    width: 100%;

    padding: 0.6rem 0.8rem;

    border: 1px solid var(--blush);
    border-radius: var(--radius);

    background: var(--cream);

    font-size: 1.1rem;

    transition: border-color var(--transition);

    --primary-color: var(--sakura);
    --text-color: var(--cocoa);
    --background-color: var(--cream);
    --caret-color: var(--sakura);
}


.function-input:focus-within {
    border-color: var(--sakura);
}


/* campos matematicos de solo lectura (variables detectadas, resultado):
   sin borde ni fondo propio, se insertan dentro de otro contenedor */
.inline-math,
.result-field {
    border: none;
    background: transparent;
    padding: 0;

    --primary-color: var(--cocoa);
    --text-color: var(--cocoa);
    --background-color: transparent;
}


.inline-math {
    display: inline-block;
    font-size: 0.85rem;
}


.result-field {
    font-size: 1.15rem;
}


.variables-feedback {
    display: flex;
    align-items: center;
    gap: 0.4rem;

    margin-top: 0.55rem;
    margin-bottom: 0;

    min-height: 1.1rem;
}


.feedback-label {
    color: var(--sakura);

    font-size: 0.78rem;
}


.feedback-label.error {
    color: var(--error);
}


.empty-hint {
    grid-column: 1 / -1;

    margin: 0;
    padding: 0.85rem;

    color: var(--cocoa-muted);

    font-size: 0.82rem;

    border: 1px dashed var(--blush);
    border-radius: var(--radius);
}


.point-inputs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.85rem;
}


/* ====================================================
   BOTON DE CALCULAR
   ==================================================== */

.calculate-button {
    width: 100%;

    padding: 0.8rem 1rem;
    margin-bottom: 1.6rem;

    border: 1px solid var(--sakura);
    border-radius: var(--radius);

    background: var(--sakura);
    color: #ffffff;

    font-family: var(--font-heading);
    font-size: 0.9rem;
    font-weight: 600;

    cursor: pointer;

    transition: opacity var(--transition), transform 0.1s ease;
}


.calculate-button:hover {
    opacity: 0.9;
}


.calculate-button:active {
    transform: translateY(1px);
}


.calculate-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}


/* ====================================================
   RESULTADO
   ==================================================== */

.result {
    min-height: 60px;

    display: flex;
    align-items: center;

    padding: 0.9rem 1rem;

    border: 1px solid var(--blush);
    border-left: 3px solid var(--highlight);
    border-radius: var(--radius);

    background: var(--cream);
}


.result-placeholder {
    color: var(--cocoa-muted);

    font-size: 0.85rem;
}


.result-placeholder.error {
    color: var(--error);
}

```
`app/static/js/main.js`:

```js
// ====================================================
// elementos del html
// ====================================================

const operation = document.getElementById("operation");

const limitPanel = document.getElementById("limit-panel");
const derivativePanel = document.getElementById("derivative-panel");

const functionInput = document.getElementById("function");

const variablesFeedback = document.getElementById("variables-feedback");
const variablesFeedbackLabel = document.getElementById("variables-feedback-label");
const variablesMath = document.getElementById("variables-math");

const limitPointInputs = document.getElementById("limit-point-inputs");
const derivativePointInputs = document.getElementById("derivative-point-inputs");
const derivativeVariableSelect = document.getElementById("derivative-variable");

const calculateButton = document.getElementById("calculate");

const resultField = document.getElementById("result-field");
const resultPlaceholder = document.getElementById("result-placeholder");

// variables detectadas (nombres planos, usados como claves) y su version
// latex en paralelo (solo para mostrar), por nombre
let currentVariables = [];
let currentVariablesLatex = {};


// ====================================================
// cambio de operacion (limite / derivada)
// ====================================================

operation.addEventListener("change", () => {

    if (operation.value === "limit") {
        limitPanel.hidden = false;
        derivativePanel.hidden = true;
    } else {
        limitPanel.hidden = true;
        derivativePanel.hidden = false;
    }

    renderDynamicInputs(currentVariables);

});


// ====================================================
// deteccion dinamica de variables
// ====================================================

let debounceTimer = null;

functionInput.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(detectVariables, 400);
});


async function detectVariables() {

    const latex = functionInput.getValue("latex").trim();

    if (!latex) {
        currentVariables = [];
        currentVariablesLatex = {};
        setFeedback("", false);
        renderDynamicInputs([]);
        return;
    }

    try {
        console.log("LaTeX enviado:", JSON.stringify(latex));
        const response = await fetch("/api/variables", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ latex })
        });

        const data = await response.json();

        if (data.success) {

            currentVariables = data.variables;

            // armamos el mapa {nombre_plano: latex} para usarlo al renderizar
            // etiquetas en otras partes de la interfaz
            currentVariablesLatex = {};
            data.variables.forEach((name, i) => {
                currentVariablesLatex[name] = data.variables_latex[i];
            });

            if (currentVariables.length > 0) {
                // mostramos "Variables detectadas:" + los simbolos en notacion matematica real
                setFeedback("Variables detectadas:", false, currentVariables.map(v => currentVariablesLatex[v]).join(", "));
            } else {
                setFeedback("La expresión no tiene variables (es una constante).", false);
            }

            renderDynamicInputs(currentVariables);

        } else {

            currentVariables = [];
            currentVariablesLatex = {};
            setFeedback(data.error, true);
            renderDynamicInputs([]);

        }

    } catch (error) {
        console.error(error);
        setFeedback("No se pudo conectar con el servidor.", true);
    }

}


// actualiza el feedback de variables. si se pasa mathLatex, se muestra
// tambien el campo matematico de solo lectura con esa notacion
function setFeedback(text, isError, mathLatex) {

    if (!text) {
        variablesFeedback.hidden = true;
        return;
    }

    variablesFeedback.hidden = false;
    variablesFeedbackLabel.textContent = text;
    variablesFeedbackLabel.classList.toggle("error", isError);

    if (mathLatex) {
        variablesMath.hidden = false;
        variablesMath.value = mathLatex;
    } else {
        variablesMath.hidden = true;
    }

}


// crea una etiqueta <label> que muestra el simbolo de la variable en
// notacion matematica real (via un math-field de solo lectura), en vez
// de texto plano — asi se ve bien incluso con letras griegas o subindices
function createVariableLabel(forId, variableName) {

    const label = document.createElement("label");
    label.setAttribute("for", forId);

    const symbol = document.createElement("math-field");
    symbol.className = "inline-math";
    symbol.setAttribute("read-only", "");
    symbol.tabIndex = -1;
    symbol.value = currentVariablesLatex[variableName] || variableName;

    label.appendChild(symbol);
    label.appendChild(document.createTextNode(" →"));

    return label;
}


function renderDynamicInputs(variables) {

    // -------- panel de limites --------
    limitPointInputs.innerHTML = "";

    if (variables.length === 0) {
        limitPointInputs.innerHTML =
            '<p class="empty-hint">Escribe una función para continuar.</p>';
    } else {

        variables.forEach((variable) => {

            const group = document.createElement("div");
            group.className = "input-group";

            const inputId = `point-${variable}`;
            group.appendChild(createVariableLabel(inputId, variable));

            const input = document.createElement("input");
            input.type = "number";
            input.id = inputId;
            input.className = "point-input";
            input.dataset.variable = variable;
            input.placeholder = "0";
            input.step = "any";

            group.appendChild(input);
            limitPointInputs.appendChild(group);

        });
    }

    // -------- panel de derivadas --------
    derivativePointInputs.innerHTML = "";
    derivativeVariableSelect.innerHTML = "";

    if (variables.length === 0) {

        const placeholder = document.createElement("option");
        placeholder.value = "";
        placeholder.textContent = "Escribe una función primero";
        derivativeVariableSelect.appendChild(placeholder);

        derivativePointInputs.innerHTML =
            '<p class="empty-hint">Escribe una función para continuar.</p>';

    } else {

        variables.forEach((variable) => {

            // nota: un <select> nativo no puede renderizar math-field dentro
            // de sus <option>, asi que aqui se queda como texto plano
            const option = document.createElement("option");
            option.value = variable;
            option.textContent = variable;
            derivativeVariableSelect.appendChild(option);

            const group = document.createElement("div");
            group.className = "input-group";

            const inputId = `deriv-point-${variable}`;
            group.appendChild(createVariableLabel(inputId, variable));

            const input = document.createElement("input");
            input.type = "number";
            input.id = inputId;
            input.className = "point-input";
            input.dataset.variable = variable;
            input.placeholder = "opcional";
            input.step = "any";

            group.appendChild(input);
            derivativePointInputs.appendChild(group);

        });
    }

}


function readPoint(container, requireAll) {

    const inputs = container.querySelectorAll(".point-input");
    const point = {};

    for (const input of inputs) {

        const value = input.value.trim();

        if (value === "") {
            if (requireAll) return null;
            continue;
        }

        point[input.dataset.variable] = value;
    }

    return point;
}


// ====================================================
// mostrar el resultado (exito: math-field. error: texto plano)
// ====================================================

function showResult(data) {

    if (data.success) {
        resultPlaceholder.hidden = true;
        resultField.hidden = false;
        resultField.value = data.result_latex;
    } else {
        resultField.hidden = true;
        resultPlaceholder.hidden = false;
        resultPlaceholder.textContent = data.error;
        resultPlaceholder.classList.add("error");
    }

}


function showResultLoading() {
    resultField.hidden = true;
    resultPlaceholder.hidden = false;
    resultPlaceholder.classList.remove("error");
    resultPlaceholder.textContent = "Calculando...";
}


// ====================================================
// calcular
// ====================================================

calculateButton.addEventListener("click", async () => {

    const latex = functionInput.getValue("latex").trim();

    if (!latex) {
        showResult({ success: false, error: "Escribe una función." });
        return;
    }

    if (currentVariables.length === 0) {
        showResult({ success: false, error: "No se detectaron variables válidas. Revisa la función." });
        return;
    }

    calculateButton.disabled = true;
    showResultLoading();

    try {

        let response;

        if (operation.value === "limit") {

            const point = readPoint(limitPointInputs, true);

            if (point === null) {
                showResult({ success: false, error: "Completa el punto para todas las variables." });
                return;
            }

            response = await fetch("/api/limit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ latex, point })
            });

        } else {

            const variable = derivativeVariableSelect.value;

            if (!variable) {
                showResult({ success: false, error: "Selecciona respecto a qué variable derivar." });
                return;
            }

            const point = readPoint(derivativePointInputs, false);
            const hasPoint = Object.keys(point).length > 0;

            response = await fetch("/api/derivative", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    latex,
                    variable,
                    point: hasPoint ? point : null
                })
            });

        }

        const data = await response.json();
        showResult(data);

        // graficamos la funcion actual, tanto si el calculo tuvo exito como si no
        renderPlot();

    } catch (error) {
        console.error(error);
        showResult({ success: false, error: "Error al comunicarse con el servidor." });

    } finally {
        calculateButton.disabled = false;
    }

});

// ====================================================
// grafica (plotly)
// ====================================================

const plotContainer = document.getElementById("plot-container");
const canvasPlaceholder = document.querySelector(".canvas-placeholder");


// pide los datos de la grafica al backend y la dibuja con plotly.
// se llama despues de cada calculo, exitoso o no, usando la funcion actual
async function renderPlot() {

    const latex = functionInput.getValue("latex").trim();

    // solo tiene sentido graficar con 1 o 2 variables (linea o superficie)
    if (!latex || currentVariables.length === 0 || currentVariables.length > 2) {
        showPlotMessage("La gráfica aparecerá aquí (solo para funciones de 1 o 2 variables)");
        return;
    }

    try {

        const response = await fetch("/api/plot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ latex })
        });

        const data = await response.json();

        if (!data.success) {
            showPlotMessage(data.error);
            return;
        }

        drawPlot(data);

    } catch (error) {
        console.error(error);
        showPlotMessage("Error al generar la gráfica.");
    }

}


// muestra un mensaje de texto en vez de la grafica (placeholder o error)
function showPlotMessage(text) {

    // si plotly ya dibujo algo antes, lo limpiamos
    if (plotContainer.dataset.hasPlot === "true") {
        Plotly.purge(plotContainer);
        plotContainer.dataset.hasPlot = "false";
    }

    plotContainer.innerHTML = `<span class="canvas-placeholder">${text}</span>`;

}


// dibuja la grafica con plotly: linea 2d o superficie 3d, segun el tipo
function drawPlot(data) {

    plotContainer.innerHTML = "";
    plotContainer.dataset.hasPlot = "true";

    if (data.type === "2d") {

        Plotly.newPlot(plotContainer, [{
            x: data.x,
            y: data.y,
            type: "scatter",
            mode: "lines",
            line: { color: "#e48aae", width: 2.5 } // sakura
        }], plotLayout(), plotConfig());

    } else if (data.type === "3d") {

        Plotly.newPlot(plotContainer, [{
            x: data.x,
            y: data.y,
            z: data.z,
            type: "surface",
            colorscale: [
                [0, "#fbf3ef"],
                [0.5, "#f0a8c2"],
                [1, "#c9718b"]
            ],
            showscale: false
        }], plotLayout(data.variable_names), plotConfig());

    }

}


// layout compartido: combina con la paleta clara actual de la interfaz
function plotLayout(variableNames) {

    const base = {
        paper_bgcolor: "#ffffff",
        plot_bgcolor: "#ffffff",
        font: { color: "#8c7377", family: "Inter, sans-serif" },
        margin: { l: 30, r: 20, t: 20, b: 30 },
    };

    if (variableNames) {
        return {
            ...base,
            scene: {
                xaxis: { title: variableNames[0], color: "#8c7377", gridcolor: "#f6d9e4" },
                yaxis: { title: variableNames[1], color: "#8c7377", gridcolor: "#f6d9e4" },
                zaxis: { color: "#8c7377", gridcolor: "#f6d9e4" },
            },
        };
    }
    return {
        ...base,
        xaxis: { gridcolor: "#f6d9e4", zerolinecolor: "#f6d9e4" },
        yaxis: { gridcolor: "#f6d9e4", zerolinecolor: "#f6d9e4" },
    };

}

// configuracion de plotly: quitamos la barra de herramientas flotante
// para que se vea mas integrado y menos "libreria generica"
function plotConfig() {
    return {
        displayModeBar: false,
        responsive: true,
    };
}

```
`app/static/js/theme.js`:

```js
// controla el boton de alternar tema. la aplicacion INICIAL del tema ya
// ocurrio en un script inline dentro de <head> (para evitar parpadeo);
// aqui solo manejamos el click para cambiarlo despues.

const themeToggle = document.getElementById("theme-toggle");


themeToggle.addEventListener("click", () => {

    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";

    document.documentElement.setAttribute("data-theme", next);

    // guardamos la preferencia para que persista entre visitas
    localStorage.setItem("theme", next);

});

```
`app/templates/index.html`:

```html
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>NekoCalc — Calculadora Multivariable</title>

    <!-- Fredoka: logo. Plus Jakarta Sans: titulos de seccion. Inter: interfaz general -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@600&family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@500;600;700&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">

    <script defer src="https://cdn.jsdelivr.net/npm/mathlive"></script>
    <script defer src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
</head>

<body>

    <div class="app">

        <!-- ==================== -->
        <!-- BARRA SUPERIOR / LOGO  -->
        <!-- ==================== -->

        <header class="topbar">

            <h1 class="logo">
                <span class="logo-nyan">Neko</span><span class="logo-delbrot">Calc</span>
            </h1>

            <p class="topbar-subtitle">Límites y derivadas de funciones multivariables</p>

        </header>


        <!-- ==================== -->
        <!-- PANEL DE CONTROL       -->
        <!-- ==================== -->

        <aside class="control-panel">

            <section class="operation-section">

                <label for="operation">Operación</label>

                <select id="operation">
                    <option value="limit">Límite multivariable</option>
                    <option value="derivative">Derivada parcial</option>
                </select>

            </section>


            <section id="limit-panel">

                <div class="section-title">
                    <h2>Punto de aproximación</h2>
                    <span>variable → valor</span>
                </div>

                <div id="limit-point-inputs" class="point-inputs">
                    <p class="empty-hint">Escribe una función para continuar.</p>
                </div>

            </section>


            <section id="derivative-panel" hidden>

                <div class="section-title">
                    <h2>Derivar respecto a</h2>
                </div>

                <!-- nota: un <select> nativo no puede renderizar latex dentro de
                     sus opciones, asi que esta lista se queda como texto plano -->
                <select id="derivative-variable" class="variable-select">
                    <option value="">Escribe una función primero</option>
                </select>

                <div class="section-title">
                    <h2>Punto de evaluación</h2>
                    <span>opcional</span>
                </div>

                <div id="derivative-point-inputs" class="point-inputs">
                    <p class="empty-hint">Escribe una función para continuar.</p>
                </div>

            </section>


            <button id="calculate" class="calculate-button" type="button">
                Calcular
            </button>


            <section class="result-section">

                <div class="section-title">
                    <h2>Resultado</h2>
                </div>

                <div id="result" class="result">

                    <!-- campo matematico de solo lectura: aqui se renderiza
                         el resultado real en notacion matematica -->
                    <math-field
                        id="result-field"
                        class="result-field"
                        read-only
                        tabindex="-1"
                        hidden
                    >
                    </math-field>

                    <span id="result-placeholder" class="result-placeholder">
                        El resultado aparecerá aquí
                    </span>

                </div>

            </section>

        </aside>


        <!-- ==================== -->
        <!-- LIENZO (grafica)       -->
        <!-- ==================== -->

        <main class="canvas">

            <div id="plot-container" class="plot-container">
                <span class="canvas-placeholder">La gráfica aparecerá aquí</span>
            </div>

        </main>


        <!-- ==================== -->
        <!-- BARRA DE FUNCION       -->
        <!-- ==================== -->

        <section class="function-bar">

            <div class="function-bar-inner">

                <div class="section-title">
                    <h2>Función</h2>
                    <span id="function-hint">f(x, y, ...)</span>
                </div>

                <math-field
                    id="function"
                    class="function-input"
                    virtual-keyboard-mode="onfocus"
                >
                </math-field>

                <p id="variables-feedback" class="variables-feedback" hidden>
                    <span id="variables-feedback-label" class="feedback-label"></span>
                    <math-field
                        id="variables-math"
                        class="inline-math"
                        read-only
                        tabindex="-1"
                        hidden
                    >
                    </math-field>
                </p>

            </div>

        </section>

    </div>


    <script src="{{ url_for('static', filename='js/main.js') }}"></script>

</body>

</html>

```
`repomix-output.xml`:

```xml
This file is a merged representation of the entire codebase, combined into a single document by Repomix.

<file_summary>
This section contains a summary of this file.

<purpose>
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.
</purpose>

<file_format>
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  - File path as an attribute
  - Full contents of the file
</file_format>

<usage_guidelines>
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.
</usage_guidelines>

<notes>
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)
</notes>

</file_summary>

<directory_structure>
app/
  mathcore/
    __init__.py
    operations.py
    parser.py
    plotting.py
  static/
    css/
      style.css
    js/
      main.js
      theme.js
  templates/
    index.html
  __init__.py
  routes.py
tests/
  test_calculator.py
.gitignore
README.md
requirements.txt
</directory_structure>

<files>
This section contains the contents of the repository's files.

<file path="app/mathcore/__init__.py">
from app.mathcore.parser import parse_expression, latex_to_expr
from app.mathcore.operations import (
    get_variables,
    multivariable_limit,
    partial_derivative,
    gradient,
    to_latex,
)
from app.mathcore.plotting import generate_plot_data
</file>

<file path="app/mathcore/operations.py">
import sympy as sp


# obtiene las variables libres de una expresion, ordenadas alfabeticamente
def get_variables(expression):
    return sorted(expression.free_symbols, key=str)


# limite multivariable: itera el limite variable por variable.
# nota: esto es un limite iterado, no el limite multivariable riguroso
# (que exige que el resultado sea el mismo por cualquier trayectoria).
def multivariable_limit(expr, point):

    variables = get_variables(expr)

    # si no hay variables, la expresion es una constante: el limite es ella misma
    if not variables:
        return expr

    result = expr

    for variable in variables:
        value = point[str(variable)]

        # intento rapido: sustitucion directa, evita el costo de sp.limit
        # cuando el punto no es una indeterminacion
        try:
            substituted = result.subs(variable, value)

            if substituted.is_finite is not False and not substituted.has(sp.nan, sp.zoo):
                result = substituted
                continue

        except Exception:
            pass

        # fallback: calculo simbolico real del limite (mas lento, pero necesario
        # para formas indeterminadas)
        result = sp.limit(result, variable, value)

    return result


# derivada parcial respecto a una variable. point es opcional: si se da,
# la derivada se evalua ahi; si no, se devuelve la forma simbolica
def partial_derivative(expr, variable_name, point=None):

    variables = {str(v): v for v in get_variables(expr)}

    if variable_name not in variables:
        raise ValueError(f"La variable '{variable_name}' no aparece en la expresión.")

    variable = variables[variable_name]
    result = sp.diff(expr, variable)

    if point:
        subs_point = {variables[k]: v for k, v in point.items() if k in variables}
        result = result.subs(subs_point)

    return result


# gradiente completo: diccionario {variable: derivada parcial}.
# util para analisis y para la grafica (direccion de maximo crecimiento)
def gradient(expr, point=None):

    variables = get_variables(expr)
    grad = {}

    for variable in variables:
        deriv = sp.diff(expr, variable)

        if point:
            subs_point = {v: point[str(v)] for v in variables if str(v) in point}
            deriv = deriv.subs(subs_point)

        grad[str(variable)] = deriv

    return grad

# convierte un objeto sympy a su representación en LaTeX, para que el
# frontend pueda renderizarlo como notación matemática real (no como
# texto plano estilo python/sympy)
def to_latex(expr):
    return sp.latex(expr)
</file>

<file path="app/mathcore/parser.py">
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)
from sympy.parsing.latex import parse_latex


# transformaciones para el parser de texto plano:
# - implicit_multiplication_application: permite "2x" -> "2*x", "xy" -> "x*y"
# - convert_xor: convierte "^" en potencia (**) en vez de xor bit a bit
TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


# funciones matematicas permitidas explicitamente en el parser de texto plano.
# cualquier identificador que NO este aqui, sympy lo trata como variable nueva
# automaticamente. esto es lo que permite funciones de cualquier nombre de variable.
ALLOWED_FUNCTIONS = {
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "sinh": sp.sinh,
    "cosh": sp.cosh,
    "tanh": sp.tanh,
    "exp": sp.exp,
    "log": sp.log,
    "ln": sp.log,
    "sqrt": sp.sqrt,
    "Abs": sp.Abs,
    "pi": sp.pi,
    "E": sp.E,
}


# espacio de evaluacion controlado para parse_expr. sin __builtins__, para
# que el usuario no pueda ejecutar codigo python arbitrario (ej. __import__).
# Symbol, Integer y Float estan aqui porque las transformaciones de sympy
# generan codigo interno que los necesita para crear variables/numeros nuevos.
GLOBAL_DICT = {
    "Symbol": sp.Symbol,
    "Integer": sp.Integer,
    "Float": sp.Float,
    "__builtins__": {},
}


# parser de texto plano (ej. "x^2 + y^2", "sqrt(x)+sin(y)").
# cualquier identificador que el usuario escriba y que no este en
# ALLOWED_FUNCTIONS se convierte automaticamente en una variable simbolica nueva.
def parse_expression(expression):

    return parse_expr(
        expression,
        local_dict=ALLOWED_FUNCTIONS,
        global_dict=GLOBAL_DICT,
        transformations=TRANSFORMATIONS,
    )


# parser de notacion LaTeX (usado por el math-field de MathLive).
# devuelve directamente un objeto sympy, igual que parse_expression.
def latex_to_expr(latex_string):

    try:
        return parse_latex(latex_string)

    # normalizamos cualquier error interno de parse_latex a ValueError,
    # para que routes.py lo maneje igual que los errores del parser de texto
    except Exception as e:
        raise ValueError(f"No se pudo interpretar la notación matemática: {e}")
</file>

<file path="app/mathcore/plotting.py">
import sympy as sp
import numpy as np

from app.mathcore.operations import get_variables


# genera los puntos numericos para graficar una funcion de 1 o 2 variables.
# x_range/y_range son tuplas (minimo, maximo). resolution es cuantos puntos
# por eje (mas resolucion = superficie mas suave, pero mas lento).
def generate_plot_data(expr, x_range=(-10, 10), y_range=(-10, 10), resolution=60):

    variables = get_variables(expr)

    if len(variables) == 0:
        raise ValueError("La expresión es una constante, no se puede graficar.")

    if len(variables) > 2:
        raise ValueError("Solo se pueden graficar funciones de 1 o 2 variables.")

    if len(variables) == 1:
        return _plot_2d(expr, variables[0], x_range, resolution)

    return _plot_3d(expr, variables[0], variables[1], x_range, y_range, resolution)


# caso de una sola variable: linea 2D, y = f(x)
def _plot_2d(expr, var, x_range, resolution):

    # lambdify convierte la expresion simbolica en una funcion de numpy,
    # mucho mas rapida que evaluar sympy punto por punto
    f = sp.lambdify(var, expr, modules=["numpy"])

    x_vals = np.linspace(x_range[0], x_range[1], resolution)

    # evaluamos la funcion en todos los puntos de una vez (vectorizado)
    y_vals = f(x_vals)

    return {
        "type": "2d",
        "x": x_vals.tolist(),
        "y": np.real(y_vals).tolist(),  # descartamos parte imaginaria si aparece
    }


# caso de dos variables: superficie 3D, z = f(x, y)
def _plot_3d(expr, var1, var2, x_range, y_range, resolution):

    f = sp.lambdify((var1, var2), expr, modules=["numpy"])

    x_vals = np.linspace(x_range[0], x_range[1], resolution)
    y_vals = np.linspace(y_range[0], y_range[1], resolution)

    # meshgrid arma la malla 2D de combinaciones (x, y) sobre la que evaluamos
    x_grid, y_grid = np.meshgrid(x_vals, y_vals)

    z_grid = f(x_grid, y_grid)

    # si la funcion es constante en una de las variables, numpy puede devolver
    # un solo numero en vez de una malla completa. la expandimos manualmente.
    if np.isscalar(z_grid):
        z_grid = np.full_like(x_grid, z_grid, dtype=float)

    return {
        "type": "3d",
        "x": x_vals.tolist(),
        "y": y_vals.tolist(),
        "z": np.real(z_grid).tolist(),
        "variable_names": [str(var1), str(var2)],
    }
</file>

<file path="app/static/js/theme.js">
// controla el boton de alternar tema. la aplicacion INICIAL del tema ya
// ocurrio en un script inline dentro de <head> (para evitar parpadeo);
// aqui solo manejamos el click para cambiarlo despues.

const themeToggle = document.getElementById("theme-toggle");


themeToggle.addEventListener("click", () => {

    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";

    document.documentElement.setAttribute("data-theme", next);

    // guardamos la preferencia para que persista entre visitas
    localStorage.setItem("theme", next);

});
</file>

<file path="tests/test_calculator.py">

</file>

<file path="app/__init__.py">
from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes import main
    app.register_blueprint(main)

    return app
</file>

<file path=".gitignore">
__pycache__/ 
*.py[cod]
.venv
venv/
.env
.pytest_cache/
.idea/
.vscode/
</file>

<file path="requirements.txt">
blinker==1.9.0
click==8.5.0
Flask==3.1.3
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
mpmath==1.3.0
sympy==1.14.0
Werkzeug==3.1.8
numpy==2.5.0
</file>

<file path="app/static/css/style.css">
/* ====================================================
   TOKENS DE DISEÑO — paleta inspirada en Nekopara, sutil
   ==================================================== */

* {
    box-sizing: border-box;
}


:root {
    --cream: #fbf3ef;        /* fondo general */
    --panel: #ffffff;        /* superficies (panel, inputs) */
    --blush: #f6d9e4;        /* bordes y rellenos suaves */
    --sakura: #e48aae;       /* acento primario: botones, foco, "Nyan" del logo */
    --highlight: #c9718b;    /* acento secundario: borde del resultado */
    --cocoa: #3e2a2e;        /* texto principal, "delbrot" del logo */
    --cocoa-muted: #8c7377;  /* texto secundario */
    --error: #b3475b;        /* mensajes de error */

    --font-logo: "Fredoka", sans-serif;
    --font-heading: "Plus Jakarta Sans", sans-serif;
    --font-body: "Inter", sans-serif;

    --radius: 8px;
    --transition: 0.15s ease;
}


@media (prefers-reduced-motion: reduce) {
    * {
        transition: none !important;
    }
} 


/* ====================================================
   BASE
   ==================================================== */

html, body {
    margin: 0;
    min-height: 100vh;

    background: var(--cream);
    color: var(--cocoa);

    font-family: var(--font-body);
    font-size: 15px;
    line-height: 1.5;
}



.app {
    position: relative;

    display: grid;
    grid-template-areas:
        "topbar topbar"
        "sidebar canvas"
        "function function";
    grid-template-columns: 340px 1fr;
    grid-template-rows: auto minmax(0, 1fr) auto;

    height: 100vh;
    oveflow: hidden;
}


.app::before {
    content: "";
    position: fixed;
    inset: 0;

    z-index: -1;

    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'%3E%3Cg fill='%23e48aae'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3Ccircle cx='22' cy='22' r='2.2'/%3E%3Ccircle cx='38' cy='22' r='2.2'/%3E%3Ccircle cx='22' cy='38' r='2.2'/%3E%3Ccircle cx='38' cy='38' r='2.2'/%3E%3Ccircle cx='90' cy='80' r='4'/%3E%3Ccircle cx='82' cy='72' r='2.2'/%3E%3Ccircle cx='98' cy='72' r='2.2'/%3E%3Ccircle cx='82' cy='88' r='2.2'/%3E%3Ccircle cx='98' cy='88' r='2.2'/%3E%3C/g%3E%3C/svg%3E");
    background-size: 160px 160px;
    opacity: 0.06;
}


/* enfoque visible por teclado */
button:focus-visible,
select:focus-visible,
input:focus-visible,
math-field:focus-within {
    outline: 2px solid var(--sakura);
    outline-offset: 2px;
}


/* ====================================================
   LOGO Y BARRA SUPERIOR
   ==================================================== */

.topbar {
    grid-area: topbar;

    padding: 1.4rem 1.75rem 1rem;

    border-bottom: 1px solid var(--blush);
    background: var(--panel);
}


.logo {
    margin: 0;

    font-family: var(--font-logo);
    font-size: 1.9rem;
    font-weight: 600;
    letter-spacing: -0.01em;
}


.logo-nyan {
    color: var(--sakura);
}


.logo-delbrot {
    color: var(--cocoa);
}


.topbar-subtitle {
    margin: 0.25rem 0 0;

    color: var(--cocoa-muted);

    font-family: var(--font-body);
    font-size: 0.85rem;
}


/* ====================================================
   PANEL DE CONTROL
   ==================================================== */

.control-panel {
    grid-area: sidebar;

    padding: 1.6rem;

    border-right: 1px solid var(--blush);
    background: var(--panel);

    overflow-y: auto;
}


/* ====================================================
   LIENZO — mas grande, es el foco visual principal
   ==================================================== */

.canvas {
    grid-area: canvas;

    display: flex;

    padding: 1.6rem;

    min-height: 0;
}


.plot-container {
    width: 100%;
    height: 100%;

    display: flex;
    align-items: center;
    justify-content: center;

    border: 1px solid var(--blush);
    border-radius: var(--radius);

    background: var(--panel);

    overflow: hidden;
}


.canvas-placeholder {
    color: var(--cocoa-muted);

    font-family: var(--font-body);
    font-size: 0.9rem;
}


/* ====================================================
   BARRA DE FUNCION (abajo, ancho completo)
   ==================================================== */

.function-bar {
    grid-area: function;
    margin: 0;
    padding: 0.85rem 1.75rem;

    border-top: 1px solid var(--blush);
    background: var(--panel);
}


.function-bar-inner {
    max-width: 900px;
    margin: 0 auto;
}


/* ====================================================
   RESPONSIVE
   ==================================================== */

@media (max-width: 900px) {

    .app {
        grid-template-areas:
            "topbar"
            "sidebar"
            "canvas"
            "function";
        grid-template-columns: 1fr;
    }

    .control-panel {
        border-right: none;
        border-bottom: 1px solid var(--blush);
    }

    .canvas {
        min-height: 45vh;
    }

}


/* ====================================================
   SECCIONES Y TITULOS
   ==================================================== */

section {
    margin-bottom: 1.5rem;
}


.section-title {
    display: flex;
    align-items: baseline;
    justify-content: space-between;

    margin-bottom: 0.6rem;
}


.section-title h2 {
    margin: 0;

    font-family: var(--font-heading);
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--cocoa);
}


.section-title span {
    color: var(--cocoa-muted);

    font-size: 0.78rem;
}


label {
    display: block;

    margin-bottom: 0.5rem;

    display: flex;
    align-items: center;
    gap: 0.3rem;

    color: var(--cocoa-muted);

    font-size: 0.82rem;
}


/* ====================================================
   INPUTS
   ==================================================== */

input,
select {
    width: 100%;

    padding: 0.7rem 0.85rem;

    border: 1px solid var(--blush);
    border-radius: var(--radius);

    outline: none;

    background: var(--cream);
    color: var(--cocoa);

    font-family: var(--font-body);
    font-size: 0.9rem;

    transition: border-color var(--transition);
}


input:focus,
select:focus {
    border-color: var(--sakura);
}


input::placeholder {
    color: var(--cocoa-muted);
    opacity: 0.6;
}


select {
    cursor: pointer;
}


/* campo matematico principal (funcion) */
.function-input {
    display: block;
    width: 100%;

    padding: 0.6rem 0.8rem;

    border: 1px solid var(--blush);
    border-radius: var(--radius);

    background: var(--cream);

    font-size: 1.1rem;

    transition: border-color var(--transition);

    --primary-color: var(--sakura);
    --text-color: var(--cocoa);
    --background-color: var(--cream);
    --caret-color: var(--sakura);
}


.function-input:focus-within {
    border-color: var(--sakura);
}


/* campos matematicos de solo lectura (variables detectadas, resultado):
   sin borde ni fondo propio, se insertan dentro de otro contenedor */
.inline-math,
.result-field {
    border: none;
    background: transparent;
    padding: 0;

    --primary-color: var(--cocoa);
    --text-color: var(--cocoa);
    --background-color: transparent;
}


.inline-math {
    display: inline-block;
    font-size: 0.85rem;
}


.result-field {
    font-size: 1.15rem;
}


.variables-feedback {
    display: flex;
    align-items: center;
    gap: 0.4rem;

    margin-top: 0.55rem;
    margin-bottom: 0;

    min-height: 1.1rem;
}


.feedback-label {
    color: var(--sakura);

    font-size: 0.78rem;
}


.feedback-label.error {
    color: var(--error);
}


.empty-hint {
    grid-column: 1 / -1;

    margin: 0;
    padding: 0.85rem;

    color: var(--cocoa-muted);

    font-size: 0.82rem;

    border: 1px dashed var(--blush);
    border-radius: var(--radius);
}


.point-inputs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.85rem;
}


/* ====================================================
   BOTON DE CALCULAR
   ==================================================== */

.calculate-button {
    width: 100%;

    padding: 0.8rem 1rem;
    margin-bottom: 1.6rem;

    border: 1px solid var(--sakura);
    border-radius: var(--radius);

    background: var(--sakura);
    color: #ffffff;

    font-family: var(--font-heading);
    font-size: 0.9rem;
    font-weight: 600;

    cursor: pointer;

    transition: opacity var(--transition), transform 0.1s ease;
}


.calculate-button:hover {
    opacity: 0.9;
}


.calculate-button:active {
    transform: translateY(1px);
}


.calculate-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}


/* ====================================================
   RESULTADO
   ==================================================== */

.result {
    min-height: 60px;

    display: flex;
    align-items: center;

    padding: 0.9rem 1rem;

    border: 1px solid var(--blush);
    border-left: 3px solid var(--highlight);
    border-radius: var(--radius);

    background: var(--cream);
}


.result-placeholder {
    color: var(--cocoa-muted);

    font-size: 0.85rem;
}


.result-placeholder.error {
    color: var(--error);
}
</file>

<file path="app/static/js/main.js">
// ====================================================
// elementos del html
// ====================================================

const operation = document.getElementById("operation");

const limitPanel = document.getElementById("limit-panel");
const derivativePanel = document.getElementById("derivative-panel");

const functionInput = document.getElementById("function");

const variablesFeedback = document.getElementById("variables-feedback");
const variablesFeedbackLabel = document.getElementById("variables-feedback-label");
const variablesMath = document.getElementById("variables-math");

const limitPointInputs = document.getElementById("limit-point-inputs");
const derivativePointInputs = document.getElementById("derivative-point-inputs");
const derivativeVariableSelect = document.getElementById("derivative-variable");

const calculateButton = document.getElementById("calculate");

const resultField = document.getElementById("result-field");
const resultPlaceholder = document.getElementById("result-placeholder");

// variables detectadas (nombres planos, usados como claves) y su version
// latex en paralelo (solo para mostrar), por nombre
let currentVariables = [];
let currentVariablesLatex = {};


// ====================================================
// cambio de operacion (limite / derivada)
// ====================================================

operation.addEventListener("change", () => {

    if (operation.value === "limit") {
        limitPanel.hidden = false;
        derivativePanel.hidden = true;
    } else {
        limitPanel.hidden = true;
        derivativePanel.hidden = false;
    }

    renderDynamicInputs(currentVariables);

});


// ====================================================
// deteccion dinamica de variables
// ====================================================

let debounceTimer = null;

functionInput.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(detectVariables, 400);
});


async function detectVariables() {

    const latex = functionInput.getValue("latex").trim();

    if (!latex) {
        currentVariables = [];
        currentVariablesLatex = {};
        setFeedback("", false);
        renderDynamicInputs([]);
        return;
    }

    try {
        console.log("LaTeX enviado:", JSON.stringify(latex));
        const response = await fetch("/api/variables", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ latex })
        });

        const data = await response.json();

        if (data.success) {

            currentVariables = data.variables;

            // armamos el mapa {nombre_plano: latex} para usarlo al renderizar
            // etiquetas en otras partes de la interfaz
            currentVariablesLatex = {};
            data.variables.forEach((name, i) => {
                currentVariablesLatex[name] = data.variables_latex[i];
            });

            if (currentVariables.length > 0) {
                // mostramos "Variables detectadas:" + los simbolos en notacion matematica real
                setFeedback("Variables detectadas:", false, currentVariables.map(v => currentVariablesLatex[v]).join(", "));
            } else {
                setFeedback("La expresión no tiene variables (es una constante).", false);
            }

            renderDynamicInputs(currentVariables);

        } else {

            currentVariables = [];
            currentVariablesLatex = {};
            setFeedback(data.error, true);
            renderDynamicInputs([]);

        }

    } catch (error) {
        console.error(error);
        setFeedback("No se pudo conectar con el servidor.", true);
    }

}


// actualiza el feedback de variables. si se pasa mathLatex, se muestra
// tambien el campo matematico de solo lectura con esa notacion
function setFeedback(text, isError, mathLatex) {

    if (!text) {
        variablesFeedback.hidden = true;
        return;
    }

    variablesFeedback.hidden = false;
    variablesFeedbackLabel.textContent = text;
    variablesFeedbackLabel.classList.toggle("error", isError);

    if (mathLatex) {
        variablesMath.hidden = false;
        variablesMath.value = mathLatex;
    } else {
        variablesMath.hidden = true;
    }

}


// crea una etiqueta <label> que muestra el simbolo de la variable en
// notacion matematica real (via un math-field de solo lectura), en vez
// de texto plano — asi se ve bien incluso con letras griegas o subindices
function createVariableLabel(forId, variableName) {

    const label = document.createElement("label");
    label.setAttribute("for", forId);

    const symbol = document.createElement("math-field");
    symbol.className = "inline-math";
    symbol.setAttribute("read-only", "");
    symbol.tabIndex = -1;
    symbol.value = currentVariablesLatex[variableName] || variableName;

    label.appendChild(symbol);
    label.appendChild(document.createTextNode(" →"));

    return label;
}


function renderDynamicInputs(variables) {

    // -------- panel de limites --------
    limitPointInputs.innerHTML = "";

    if (variables.length === 0) {
        limitPointInputs.innerHTML =
            '<p class="empty-hint">Escribe una función para continuar.</p>';
    } else {

        variables.forEach((variable) => {

            const group = document.createElement("div");
            group.className = "input-group";

            const inputId = `point-${variable}`;
            group.appendChild(createVariableLabel(inputId, variable));

            const input = document.createElement("input");
            input.type = "number";
            input.id = inputId;
            input.className = "point-input";
            input.dataset.variable = variable;
            input.placeholder = "0";
            input.step = "any";

            group.appendChild(input);
            limitPointInputs.appendChild(group);

        });
    }

    // -------- panel de derivadas --------
    derivativePointInputs.innerHTML = "";
    derivativeVariableSelect.innerHTML = "";

    if (variables.length === 0) {

        const placeholder = document.createElement("option");
        placeholder.value = "";
        placeholder.textContent = "Escribe una función primero";
        derivativeVariableSelect.appendChild(placeholder);

        derivativePointInputs.innerHTML =
            '<p class="empty-hint">Escribe una función para continuar.</p>';

    } else {

        variables.forEach((variable) => {

            // nota: un <select> nativo no puede renderizar math-field dentro
            // de sus <option>, asi que aqui se queda como texto plano
            const option = document.createElement("option");
            option.value = variable;
            option.textContent = variable;
            derivativeVariableSelect.appendChild(option);

            const group = document.createElement("div");
            group.className = "input-group";

            const inputId = `deriv-point-${variable}`;
            group.appendChild(createVariableLabel(inputId, variable));

            const input = document.createElement("input");
            input.type = "number";
            input.id = inputId;
            input.className = "point-input";
            input.dataset.variable = variable;
            input.placeholder = "opcional";
            input.step = "any";

            group.appendChild(input);
            derivativePointInputs.appendChild(group);

        });
    }

}


function readPoint(container, requireAll) {

    const inputs = container.querySelectorAll(".point-input");
    const point = {};

    for (const input of inputs) {

        const value = input.value.trim();

        if (value === "") {
            if (requireAll) return null;
            continue;
        }

        point[input.dataset.variable] = value;
    }

    return point;
}


// ====================================================
// mostrar el resultado (exito: math-field. error: texto plano)
// ====================================================

function showResult(data) {

    if (data.success) {
        resultPlaceholder.hidden = true;
        resultField.hidden = false;
        resultField.value = data.result_latex;
    } else {
        resultField.hidden = true;
        resultPlaceholder.hidden = false;
        resultPlaceholder.textContent = data.error;
        resultPlaceholder.classList.add("error");
    }

}


function showResultLoading() {
    resultField.hidden = true;
    resultPlaceholder.hidden = false;
    resultPlaceholder.classList.remove("error");
    resultPlaceholder.textContent = "Calculando...";
}


// ====================================================
// calcular
// ====================================================

calculateButton.addEventListener("click", async () => {

    const latex = functionInput.getValue("latex").trim();

    if (!latex) {
        showResult({ success: false, error: "Escribe una función." });
        return;
    }

    if (currentVariables.length === 0) {
        showResult({ success: false, error: "No se detectaron variables válidas. Revisa la función." });
        return;
    }

    calculateButton.disabled = true;
    showResultLoading();

    try {

        let response;

        if (operation.value === "limit") {

            const point = readPoint(limitPointInputs, true);

            if (point === null) {
                showResult({ success: false, error: "Completa el punto para todas las variables." });
                return;
            }

            response = await fetch("/api/limit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ latex, point })
            });

        } else {

            const variable = derivativeVariableSelect.value;

            if (!variable) {
                showResult({ success: false, error: "Selecciona respecto a qué variable derivar." });
                return;
            }

            const point = readPoint(derivativePointInputs, false);
            const hasPoint = Object.keys(point).length > 0;

            response = await fetch("/api/derivative", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    latex,
                    variable,
                    point: hasPoint ? point : null
                })
            });

        }

        const data = await response.json();
        showResult(data);

        // graficamos la funcion actual, tanto si el calculo tuvo exito como si no
        renderPlot();

    } catch (error) {
        console.error(error);
        showResult({ success: false, error: "Error al comunicarse con el servidor." });

    } finally {
        calculateButton.disabled = false;
    }

});

// ====================================================
// grafica (plotly)
// ====================================================

const plotContainer = document.getElementById("plot-container");
const canvasPlaceholder = document.querySelector(".canvas-placeholder");


// pide los datos de la grafica al backend y la dibuja con plotly.
// se llama despues de cada calculo, exitoso o no, usando la funcion actual
async function renderPlot() {

    const latex = functionInput.getValue("latex").trim();

    // solo tiene sentido graficar con 1 o 2 variables (linea o superficie)
    if (!latex || currentVariables.length === 0 || currentVariables.length > 2) {
        showPlotMessage("La gráfica aparecerá aquí (solo para funciones de 1 o 2 variables)");
        return;
    }

    try {

        const response = await fetch("/api/plot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ latex })
        });

        const data = await response.json();

        if (!data.success) {
            showPlotMessage(data.error);
            return;
        }

        drawPlot(data);

    } catch (error) {
        console.error(error);
        showPlotMessage("Error al generar la gráfica.");
    }

}


// muestra un mensaje de texto en vez de la grafica (placeholder o error)
function showPlotMessage(text) {

    // si plotly ya dibujo algo antes, lo limpiamos
    if (plotContainer.dataset.hasPlot === "true") {
        Plotly.purge(plotContainer);
        plotContainer.dataset.hasPlot = "false";
    }

    plotContainer.innerHTML = `<span class="canvas-placeholder">${text}</span>`;

}


// dibuja la grafica con plotly: linea 2d o superficie 3d, segun el tipo
function drawPlot(data) {

    plotContainer.innerHTML = "";
    plotContainer.dataset.hasPlot = "true";

    if (data.type === "2d") {

        Plotly.newPlot(plotContainer, [{
            x: data.x,
            y: data.y,
            type: "scatter",
            mode: "lines",
            line: { color: "#e48aae", width: 2.5 } // sakura
        }], plotLayout(), plotConfig());

    } else if (data.type === "3d") {

        Plotly.newPlot(plotContainer, [{
            x: data.x,
            y: data.y,
            z: data.z,
            type: "surface",
            colorscale: [
                [0, "#fbf3ef"],
                [0.5, "#f0a8c2"],
                [1, "#c9718b"]
            ],
            showscale: false
        }], plotLayout(data.variable_names), plotConfig());

    }

}


// layout compartido: combina con la paleta clara actual de la interfaz
function plotLayout(variableNames) {

    const base = {
        paper_bgcolor: "#ffffff",
        plot_bgcolor: "#ffffff",
        font: { color: "#8c7377", family: "Inter, sans-serif" },
        margin: { l: 30, r: 20, t: 20, b: 30 },
    };

    if (variableNames) {
        return {
            ...base,
            scene: {
                xaxis: { title: variableNames[0], color: "#8c7377", gridcolor: "#f6d9e4" },
                yaxis: { title: variableNames[1], color: "#8c7377", gridcolor: "#f6d9e4" },
                zaxis: { color: "#8c7377", gridcolor: "#f6d9e4" },
            },
        };
    }
    return {
        ...base,
        xaxis: { gridcolor: "#f6d9e4", zerolinecolor: "#f6d9e4" },
        yaxis: { gridcolor: "#f6d9e4", zerolinecolor: "#f6d9e4" },
    };

}

// configuracion de plotly: quitamos la barra de herramientas flotante
// para que se vea mas integrado y menos "libreria generica"
function plotConfig() {
    return {
        displayModeBar: false,
        responsive: true,
    };
}
</file>

<file path="app/templates/index.html">
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>NekoCalc — Calculadora Multivariable</title>

    <!-- Fredoka: logo. Plus Jakarta Sans: titulos de seccion. Inter: interfaz general -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@600&family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@500;600;700&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">

    <script defer src="https://cdn.jsdelivr.net/npm/mathlive"></script>
    <script defer src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
</head>

<body>

    <div class="app">

        <!-- ==================== -->
        <!-- BARRA SUPERIOR / LOGO  -->
        <!-- ==================== -->

        <header class="topbar">

            <h1 class="logo">
                <span class="logo-nyan">Neko</span><span class="logo-delbrot">Calc</span>
            </h1>

            <p class="topbar-subtitle">Límites y derivadas de funciones multivariables</p>

        </header>


        <!-- ==================== -->
        <!-- PANEL DE CONTROL       -->
        <!-- ==================== -->

        <aside class="control-panel">

            <section class="operation-section">

                <label for="operation">Operación</label>

                <select id="operation">
                    <option value="limit">Límite multivariable</option>
                    <option value="derivative">Derivada parcial</option>
                </select>

            </section>


            <section id="limit-panel">

                <div class="section-title">
                    <h2>Punto de aproximación</h2>
                    <span>variable → valor</span>
                </div>

                <div id="limit-point-inputs" class="point-inputs">
                    <p class="empty-hint">Escribe una función para continuar.</p>
                </div>

            </section>


            <section id="derivative-panel" hidden>

                <div class="section-title">
                    <h2>Derivar respecto a</h2>
                </div>

                <!-- nota: un <select> nativo no puede renderizar latex dentro de
                     sus opciones, asi que esta lista se queda como texto plano -->
                <select id="derivative-variable" class="variable-select">
                    <option value="">Escribe una función primero</option>
                </select>

                <div class="section-title">
                    <h2>Punto de evaluación</h2>
                    <span>opcional</span>
                </div>

                <div id="derivative-point-inputs" class="point-inputs">
                    <p class="empty-hint">Escribe una función para continuar.</p>
                </div>

            </section>


            <button id="calculate" class="calculate-button" type="button">
                Calcular
            </button>


            <section class="result-section">

                <div class="section-title">
                    <h2>Resultado</h2>
                </div>

                <div id="result" class="result">

                    <!-- campo matematico de solo lectura: aqui se renderiza
                         el resultado real en notacion matematica -->
                    <math-field
                        id="result-field"
                        class="result-field"
                        read-only
                        tabindex="-1"
                        hidden
                    >
                    </math-field>

                    <span id="result-placeholder" class="result-placeholder">
                        El resultado aparecerá aquí
                    </span>

                </div>

            </section>

        </aside>


        <!-- ==================== -->
        <!-- LIENZO (grafica)       -->
        <!-- ==================== -->

        <main class="canvas">

            <div id="plot-container" class="plot-container">
                <span class="canvas-placeholder">La gráfica aparecerá aquí</span>
            </div>

        </main>


        <!-- ==================== -->
        <!-- BARRA DE FUNCION       -->
        <!-- ==================== -->

        <section class="function-bar">

            <div class="function-bar-inner">

                <div class="section-title">
                    <h2>Función</h2>
                    <span id="function-hint">f(x, y, ...)</span>
                </div>

                <math-field
                    id="function"
                    class="function-input"
                    virtual-keyboard-mode="onfocus"
                >
                </math-field>

                <p id="variables-feedback" class="variables-feedback" hidden>
                    <span id="variables-feedback-label" class="feedback-label"></span>
                    <math-field
                        id="variables-math"
                        class="inline-math"
                        read-only
                        tabindex="-1"
                        hidden
                    >
                    </math-field>
                </p>

            </div>

        </section>

    </div>


    <script src="{{ url_for('static', filename='js/main.js') }}"></script>

</body>

</html>
</file>

<file path="app/routes.py">
from flask import Blueprint, render_template, request, jsonify

from app.mathcore import (
    parse_expression,
    latex_to_expr,
    multivariable_limit,
    partial_derivative,
    get_variables,
    generate_plot_data,
    to_latex,
)


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


# decide que parser usar segun lo que mande el frontend.
def get_expr_from_request(data):

    if data.get("latex"):
        return latex_to_expr(data["latex"])

    elif data.get("expression"):
        return parse_expression(data["expression"])

    else:
        raise ValueError("No se proporcionó una expresión ni notación LaTeX.")


# api de variables
#
# /api/variables
@main.route("/api/variables", methods=["POST"])
def variables():

    data = request.get_json()

    if not data:
        return jsonify({ 
            "success": False,
            "error": "No se recibieron datos."
        }), 400

    try:
        expr = get_expr_from_request(data)
        vars_found = get_variables(expr)

        return jsonify({
            "success": True,
            "variables": [str(v) for v in vars_found],
            "variables_latex": [to_latex(v) for v in vars_found],
        })

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"[/api/variables] error: {e}")
        return jsonify({
            "success": False,
            "error": "No se pudo interpretar la expresión."
        }), 400


# api de limites
#
# /api/limit
@main.route("/api/limit", methods=["POST"])
def limit():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No se recibieron datos."
        }), 400

    point = data.get("point")

    if not point:
        return jsonify({
            "success": False,
            "error": "No se proporcionó el punto."
        }), 400

    try:
        expr = get_expr_from_request(data)
        result = multivariable_limit(expr, point)

        return jsonify({
            "success": True,
            "result": str(result),
            "result_latex": to_latex(result),
        })

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"[/api/limit] error: {e}")
        return jsonify({
            "success": False,
            "error": "No se pudo calcular el límite."
        }), 400


# api de derivadas parciales
#
# /api/derivative
@main.route("/api/derivative", methods=["POST"])
def derivative():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No se recibieron datos."
        }), 400

    variable = data.get("variable")
    point = data.get("point")  # opcional

    if not variable:
        return jsonify({
            "success": False,
            "error": "No se proporcionó la variable respecto a la cual derivar."
        }), 400

    try:
        expr = get_expr_from_request(data)
        result = partial_derivative(expr, variable, point)

        return jsonify({
            "success": True,
            "result": str(result),
            "result_latex": to_latex(result),
        })

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"[/api/derivative] error: {e}")
        return jsonify({
            "success": False,
            "error": "No se pudo calcular la derivada."
        }), 400


# api de graficas
#
# /api/plot
@main.route("/api/plot", methods=["POST"])
def plot():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No se recibieron datos."
        }), 400

    try:
        expr = get_expr_from_request(data)

        # rango de graficado opcional, con valores por defecto razonables
        x_range = tuple(data.get("x_range", (-10, 10)))
        y_range = tuple(data.get("y_range", (-10, 10)))

        plot_data = generate_plot_data(expr, x_range=x_range, y_range=y_range)

        return jsonify({
            "success": True,
            **plot_data
        })

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"[/api/plot] error: {e}")
        return jsonify({
            "success": False,
            "error": "No se pudo generar la gráfica."
        }), 400
</file>

<file path="README.md">
# Calculadora Multivariable

Aplicación web desarrollada con **Flask** y **SymPy** para calcular límites de funciones multivariables.

El proyecto está pensado como una herramienta sencilla para trabajar con funciones de varias variables desde una interfaz web.

Actualmente el proyecto se encuentra en desarrollo.

## Características

* Cálculo de límites multivariables.
* Interfaz web sencilla.
* Backend desarrollado con Flask.
* Cálculos simbólicos utilizando SymPy.
* Preparado para añadir derivadas parciales y otras operaciones en el futuro.

---

# Requisitos

Necesitas tener instalado:

* Python 3
* pip
* Git

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
git clone https://github.com/yeim666/multivariable-calc-mat2/
```

Entra en la carpeta:

```bash
cd calculadora-web
```

Se recomienda utilizar un entorno virtual para evitar instalar las dependencias globalmente.

## Linux

Crear el entorno virtual:

```bash
python3 -m venv venv
```

Activarlo:

```bash
source venv/bin/activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

---

## macOS

Crear el entorno virtual:

```bash
python3 -m venv venv
```

Activarlo:

```bash
source venv/bin/activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Dependiendo de la instalación de Python, también puede funcionar:

```bash
python -m venv venv
```

---

## Windows

Crear el entorno virtual:

```powershell
python -m venv venv
```

Si utilizas PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Si utilizas CMD:

```cmd
venv\Scripts\activate
```

Después instala las dependencias:

```powershell
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

Flask debería mostrar una dirección similar a:

```text
http://127.0.0.1:5000
```

Abre esa dirección en tu navegador.

Para detener el servidor utiliza:

```text
Ctrl + C
```

---

# Cómo usar la calculadora

1. Abre la aplicación en el navegador.

2. Selecciona la operación que deseas realizar.

3. Para calcular un límite, escribe una función utilizando las variables `x` y `y`.

Por ejemplo:

```text
x^2 + y^2
```

4. Introduce el punto al que deben aproximarse las variables.

Por ejemplo:

```text
x → 0
y → 0
```

5. Presiona el botón **Calcular**.

El resultado aparecerá en la parte inferior de la calculadora.

Ejemplo:

```text
Función:

x^2 + y^2

Punto:

(0, 0)

Resultado:

0
```

Actualmente algunas expresiones o límites multivariables complejos pueden no ser evaluados correctamente, ya que el sistema de cálculo todavía está en desarrollo.

---

# Estructura del proyecto

```text
calculadora-web/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── calculator.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       │
│       └── js/
│           └── main.js
│
├── tests/
│   └── test_calculator.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Archivos principales

### `app/__init__.py`

Inicializa la aplicación Flask y registra las rutas.

### `app/routes.py`

Contiene las rutas de Flask y los endpoints de la API.

Por ejemplo:

```text
/
```

muestra la página principal.

Mientras que:

```text
/api/limit
```

recibe los datos enviados desde JavaScript y solicita el cálculo del límite.

### `app/calculator.py`

Contiene la lógica matemática de la aplicación.

Aquí se utiliza SymPy para interpretar expresiones y realizar los cálculos.

### `app/templates/index.html`

Contiene la estructura de la interfaz.

### `app/static/css/style.css`

Contiene los estilos de la página.

### `app/static/js/main.js`

Controla la interacción de la interfaz y la comunicación con el backend mediante `fetch()`.

---

# Contribuir

Las contribuciones son bienvenidas.

Para trabajar en el proyecto sin destruir accidentalmente la rama principal, sigue este flujo.

## 1. Clonar el repositorio

```bash
git clone https://github.com/yeim666/multivariable-calc-mat2/
```

Después:

```bash
cd calculadora-web
```

Instala las dependencias siguiendo las instrucciones anteriores.

---

## 2. Crear una nueva rama

No trabajes directamente sobre `main`.

Crea una rama para tu cambio:

```bash
git switch -c nombre-de-la-rama
```

Por ejemplo:

```bash
git switch -c feat-derivadas-parciales
```

También puedes utilizar:

```bash
git checkout -b feat-derivadas-parciales
```

---

## 3. Realizar los cambios

Modifica únicamente lo necesario para la funcionalidad en la que estés trabajando.

Antes de hacer un commit puedes revisar los archivos modificados con:

```bash
git status
```

---

## 4. Añadir los cambios

```bash
git add .
```

---

## 5. Crear un commit

Intentamos utilizar mensajes de commit claros.

Formato recomendado:

```text
tipo: descripción
```

Algunos tipos:

```text
feat: nueva funcionalidad

fix: corrección de un error

docs: cambios en documentación

style: cambios visuales o de formato

refactor: reorganización del código

test: cambios relacionados con pruebas

chore: configuración o mantenimiento
```

Ejemplos:

```bash
git commit -m "feat: add partial derivative support"
```

```bash
git commit -m "fix: validate empty function input"
```

```bash
git commit -m "docs: update installation guide"
```

---

## 6. Subir la rama

```bash
git push -u origin nombre-de-la-rama
```

Por ejemplo:

```bash
git push -u origin feat-derivadas-parciales
```

---

## 7. Crear un Pull Request

Desde GitHub, crea un **Pull Request** desde tu rama hacia `main`.

En la descripción explica brevemente:

* Qué cambiaste.
* Por qué lo cambiaste.
* Cómo se puede probar.

Después el código puede revisarse antes de integrarlo a la rama principal.

---

# Recomendaciones para contribuir

Antes de enviar cambios:

* Comprueba que el programa siga ejecutándose.
* Prueba manualmente la funcionalidad modificada.
* No subas el entorno virtual `venv/`.
* No subas archivos temporales.
* Evita modificar archivos que no estén relacionados con tu cambio.
* Intenta mantener el código legible.
* Añade comentarios cuando una parte del código no sea evidente.
* Haz commits pequeños y relacionados con un único cambio.

---

# Flujo general de la aplicación

```text
Usuario
   │
   ▼
HTML
   │
   ▼
JavaScript
   │
   │ fetch()
   ▼
API de Flask
   │
   ▼
calculator.py
   │
   ▼
SymPy
   │
   ▼
Flask devuelve JSON
   │
   ▼
JavaScript
   │
   ▼
Resultado mostrado en HTML
```

---

# Estado del proyecto

Actualmente se está trabajando principalmente en:

* Límites multivariables.
* Interpretación de expresiones matemáticas.
* Validación de datos.
* Mejora de la precisión de los cálculos.

Entre las funcionalidades previstas se encuentran:

* Derivadas parciales.
* Mejor representación matemática de los resultados.
* Soporte para más tipos de expresiones.
* Mejor manejo de errores.
* Pruebas automatizadas.

---

# Tecnologías utilizadas

* Python
* Flask
* SymPy
* HTML
* CSS
* JavaScript
</file>

</files>

```
`requirements.txt`:

```txt
blinker==1.9.0
click==8.5.0
Flask==3.1.3
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
mpmath==1.3.0
sympy==1.14.0
Werkzeug==3.1.8
numpy==2.5.0

```