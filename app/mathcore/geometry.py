import sympy as sp

from app.mathcore.common import get_variables, require_point, step, to_latex
from app.mathcore.registry import register


PROCEDURE_NOTE = (
    "Los procedimientos describen operaciones simbólicas y no constituyen un tutor universal."
)


def tangent_plane_and_normal(expr, point):

    variables = get_variables(expr)

    if len(variables) != 2:
        raise ValueError("El plano tangente requiere una función de exactamente 2 variables.")

    x, y = variables
    at_point = require_point(variables, point, "punto de tangencia")
    a, b = at_point[x], at_point[y]

    z0 = expr.subs(at_point)

    if not z0.is_finite:
        raise ValueError("La función no está definida en ese punto.")

    fx = sp.diff(expr, x).subs(at_point)
    fy = sp.diff(expr, y).subs(at_point)

    if not (fx.is_finite and fy.is_finite):
        raise ValueError("Las derivadas parciales no existen en ese punto.")

    plane = sp.expand(z0 + fx * (x - a) + fy * (y - b))

    t = sp.Symbol("t")
    line = sp.Matrix([a + fx * t, b + fy * t, z0 - t])

    return z0, fx, fy, plane, line


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

    procedure = [
        step("Función", latex=to_latex(expr)),
        step("Altura", title_latex=r"z_0 = f(a, b)", latex=to_latex(z0)),
        step(title_latex=r"f_x(a, b)", latex=to_latex(fx)),
        step(title_latex=r"f_y(a, b)", latex=to_latex(fy)),
        step("Plano tangente", latex=rf"z = {to_latex(plane)}"),
        step("Recta normal", latex=rf"\vec{{r}}(t) = {to_latex(line)}"),
        step("Alcance", text=PROCEDURE_NOTE),
    ]

    return {
        "result": f"plano: z = {plane}; recta normal: r(t) = {list(line)}",
        "result_latex": latex,
        "procedure": procedure,
    }
