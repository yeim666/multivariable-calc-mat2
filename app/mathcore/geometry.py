import sympy as sp

from app.mathcore.common import get_variables
from app.mathcore.parser import parse_value
from app.mathcore.registry import register


# plano tangente y recta normal a la superficie z = f(x, y) en el punto (a, b).
# devuelve (z0, fx, fy, plano, recta) donde plano es la expresion de z
# y recta es el vector de posicion r(t) de la recta normal
def tangent_plane_and_normal(expr, point):

    variables = get_variables(expr)

    if len(variables) != 2:
        raise ValueError("El plano tangente requiere una función de exactamente 2 variables.")

    x, y = variables

    for v in variables:
        if str(v) not in point:
            raise ValueError(f"Falta el valor de '{v}' en el punto.")

    a = parse_value(point[str(x)])
    b = parse_value(point[str(y)])
    at_point = {x: a, y: b}

    z0 = expr.subs(at_point)

    # el punto debe estar en el dominio para que exista la superficie ahi
    if not z0.is_finite:
        raise ValueError("La función no está definida en ese punto.")

    fx = sp.diff(expr, x).subs(at_point)
    fy = sp.diff(expr, y).subs(at_point)

    if not (fx.is_finite and fy.is_finite):
        raise ValueError("Las derivadas parciales no existen en ese punto.")

    # z = f(a,b) + fx(a,b)(x-a) + fy(a,b)(y-b)
    plane = sp.expand(z0 + fx * (x - a) + fy * (y - b))

    # la normal a la superficie F(x,y,z) = f(x,y) - z = 0 es (fx, fy, -1)
    t = sp.Symbol("t")
    line = sp.Matrix([a + fx * t, b + fy * t, z0 - t])

    return z0, fx, fy, plane, line


# operacion "tangent_plane" de la api. espera "point": {"x": "1", "y": "2"}
@register("tangent_plane")
def tangent_plane_operation(expr, params):

    point = params.get("point")

    if not point:
        raise ValueError("No se proporcionó el punto.")

    z0, fx, fy, plane, line = tangent_plane_and_normal(expr, point)

    latex = (
        f"z = {sp.latex(plane)}"
        f"\\;,\\quad \\vec{{r}}(t) = {sp.latex(line)}"
    )

    return {
        "result": f"plano: z = {plane}; recta normal: r(t) = {list(line)}",
        "result_latex": latex,
    }
