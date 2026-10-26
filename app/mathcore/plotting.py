import numpy as np
import sympy as sp

from app.mathcore.common import get_variables
from app.mathcore.geometry import tangent_plane_and_normal
from app.mathcore.parser import parse_value


# genera los datos numericos para graficar una funcion de 1 o 2 variables.
# x_range/y_range son tuplas (minimo, maximo). resolution es cuantos puntos
# por eje (mas resolucion = superficie mas suave, pero mas lento).
#
# point (opcional) es el punto de evaluacion: se devuelve como "marker".
# overlay (opcional) agrega una capa segun la operacion:
#   "tangent_plane" -> malla del plano tangente en point
#   "gradient"      -> flecha en la direccion de maximo ascenso en point
def generate_plot_data(expr, x_range=(-10, 10), y_range=(-10, 10),
                       resolution=60, point=None, overlay=None):

    variables = get_variables(expr)

    if len(variables) == 0:
        raise ValueError("La expresión es una constante, no se puede graficar.")

    if len(variables) > 2:
        raise ValueError("Solo se pueden graficar funciones de 1 o 2 variables.")

    x_range = _check_range(x_range, variables[0])

    if len(variables) == 2:
        y_range = _check_range(y_range, variables[1])

    if len(variables) == 1:
        data = _plot_2d(expr, variables[0], x_range, resolution)
    else:
        data = _plot_3d(expr, variables[0], variables[1], x_range, y_range, resolution)

    # las capas extra son un adorno: si fallan (punto fuera del dominio,
    # valor mal escrito...) se omiten y la grafica base se entrega igual,
    # porque el error real ya lo muestra el resultado de la operacion
    try:
        marker = _marker(expr, variables, point)
        if marker:
            data["marker"] = marker

        if overlay and marker and len(variables) == 2:
            data.update(_overlay(expr, variables, point, overlay, data, x_range, y_range))

    except Exception:
        pass

    return data


# valida un rango (minimo, maximo): numeros finitos y minimo < maximo
def _check_range(value, variable):

    try:
        low, high = (float(v) for v in value)
    except (TypeError, ValueError):
        raise ValueError(f"El rango de {variable} no es válido.")

    if not (np.isfinite(low) and np.isfinite(high)) or low >= high:
        raise ValueError(f"El rango de {variable} no es válido: el mínimo debe ser menor que el máximo.")

    return (low, high)


# lista de numeros -> lista json valida: nan e infinitos pasan a None
# (json no tiene nan; sin esto el navegador no puede leer la respuesta)
def _clean(values):

    arr = np.real(np.asarray(values, dtype=complex)).astype(float)

    return np.where(np.isfinite(arr), arr, None).tolist()


# evalua una funcion lambdificada sobre una malla; si el resultado es
# un escalar (funcion constante) lo expande a la forma de la malla
def _eval_grid(f, x_grid, y_grid):

    z = f(x_grid, y_grid)

    if np.isscalar(z):
        z = np.full_like(x_grid, z, dtype=float)

    return z


# caso de una sola variable: linea 2D, y = f(x)
def _plot_2d(expr, var, x_range, resolution):

    # lambdify convierte la expresion simbolica en una funcion de numpy,
    # mucho mas rapida que evaluar sympy punto por punto
    f = sp.lambdify(var, expr, modules=["numpy"])

    x_vals = np.linspace(x_range[0], x_range[1], resolution)

    # evaluamos en todos los puntos de una vez (vectorizado); los avisos de
    # numpy por dominios invalidos (log de negativos, division por cero)
    # se silencian porque esos puntos salen como huecos en la grafica
    with np.errstate(all="ignore"):
        y_vals = f(x_vals)

    if np.isscalar(y_vals):
        y_vals = np.full_like(x_vals, y_vals, dtype=float)

    return {
        "type": "2d",
        "x": x_vals.tolist(),
        "y": _clean(y_vals),
        "variable_names": [str(var)],
    }


# caso de dos variables: superficie 3D, z = f(x, y)
def _plot_3d(expr, var1, var2, x_range, y_range, resolution):

    f = sp.lambdify((var1, var2), expr, modules=["numpy"])

    x_vals = np.linspace(x_range[0], x_range[1], resolution)
    y_vals = np.linspace(y_range[0], y_range[1], resolution)

    # meshgrid arma la malla 2D de combinaciones (x, y) sobre la que evaluamos
    x_grid, y_grid = np.meshgrid(x_vals, y_vals)

    with np.errstate(all="ignore"):
        z_grid = _eval_grid(f, x_grid, y_grid)

    return {
        "type": "3d",
        "x": x_vals.tolist(),
        "y": y_vals.tolist(),
        "z": _clean(z_grid),
        "variable_names": [str(var1), str(var2)],
    }


# punto de evaluacion sobre la grafica: (a, f(a)) o (a, b, f(a, b)).
# devuelve None si faltan variables en el punto o f no es real ahi
def _marker(expr, variables, point):

    if not point:
        return None

    values = []
    for v in variables:
        if str(v) not in point:
            return None
        values.append(parse_value(point[str(v)]))

    height = complex(sp.N(expr.subs(dict(zip(variables, values)))))

    if height.imag != 0 or not np.isfinite(height.real):
        return None

    coords = [float(sp.N(v)) for v in values] + [height.real]
    keys = ["x", "y"] if len(variables) == 1 else ["x", "y", "z"]

    return dict(zip(keys, coords))


# capas extra de la operacion sobre una superficie z = f(x, y)
def _overlay(expr, variables, point, overlay, data, x_range, y_range):

    x, y = variables
    a, b, z0 = (data["marker"][k] for k in ("x", "y", "z"))

    if overlay == "tangent_plane":

        _, _, _, plane, _ = tangent_plane_and_normal(expr, point)
        f_plane = sp.lambdify((x, y), plane, modules=["numpy"])

        x_grid, y_grid = np.meshgrid(data["x"], data["y"])

        return {"plane_z": _clean(_eval_grid(f_plane, x_grid, y_grid))}

    if overlay == "gradient":

        _, fx, fy, _, _ = tangent_plane_and_normal(expr, point)
        fx, fy = float(fx), float(fy)
        norm = np.hypot(fx, fy)

        # gradiente nulo (punto critico): no hay direccion que mostrar
        if norm == 0:
            return {}

        # la flecha apunta en la direccion de maximo ascenso sobre la
        # superficie: se avanza una longitud L en (fx, fy)/norma y la altura
        # sube norma * L, porque la derivada direccional maxima es |grad f|
        length = 0.2 * max(x_range[1] - x_range[0], y_range[1] - y_range[0])
        dx, dy = fx / norm * length, fy / norm * length

        return {
            "gradient_arrow": {
                "x": [a, a + dx],
                "y": [b, b + dy],
                "z": [z0, z0 + norm * length],
            }
        }

    return {}
