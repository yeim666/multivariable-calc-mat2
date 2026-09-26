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
