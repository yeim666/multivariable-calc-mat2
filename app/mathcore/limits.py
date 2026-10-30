import sympy as sp

from app.mathcore.common import get_variables, make_result, require_point, step, to_latex
from app.mathcore.registry import register


PROCEDURE_NOTE = (
    "Los procedimientos describen operaciones simbólicas y no constituyen un tutor universal."
)

TRAJECTORY_CAVEAT = (
    "Coincidir en trayectorias no demuestra existencia del límite multivariable."
)


def _along_limit(expr, variable, value):
    try:
        substituted = expr.subs(variable, value)
        if substituted.is_finite is not False and not substituted.has(sp.nan, sp.zoo):
            return sp.simplify(substituted)
    except Exception:
        pass

    return sp.simplify(sp.limit(expr, variable, value))


def _is_determined(value):
    if value is None:
        return False
    if value.has(sp.nan, sp.zoo, sp.oo, -sp.oo):
        return False
    if value.free_symbols:
        return False
    return value.is_finite is not False


def _same_value(left, right):
    try:
        return sp.simplify(sp.N(left - right)) == 0 or sp.simplify(left - right) == 0
    except Exception:
        return False


def iterated_limit(expr, point):
    variables = get_variables(expr)

    if not variables:
        return expr

    result = expr
    substitutions = require_point(variables, point)

    for variable in variables:
        result = _along_limit(result, variable, substitutions[variable])

    return result


def trajectory_limits(expr, point):
    """Cinco trayectorias hacia el punto, en el plano de las dos primeras variables."""

    variables = get_variables(expr)
    substitutions = require_point(variables, point)

    if len(variables) < 2:
        return []

    x, y = variables[0], variables[1]
    a, b = substitutions[x], substitutions[y]
    t = sp.Dummy("t")

    extras = {var: substitutions[var] for var in variables[2:]}

    paths = [
        ("horizontal", rf"{to_latex(y)} = {to_latex(b)}", {x: t, y: b, **extras}, t, a),
        ("vertical", rf"{to_latex(x)} = {to_latex(a)}", {x: a, y: t, **extras}, t, b),
        ("diagonal", rf"{to_latex(y)} - ({to_latex(b)}) = {to_latex(x)} - ({to_latex(a)})",
         {x: a + t, y: b + t, **extras}, t, 0),
        ("antidiagonal", rf"{to_latex(y)} - ({to_latex(b)}) = -({to_latex(x)} - ({to_latex(a)}))",
         {x: a + t, y: b - t, **extras}, t, 0),
        ("parabolic", rf"{to_latex(y)} - ({to_latex(b)}) = ({to_latex(x)} - ({to_latex(a)}))^2",
         {x: a + t, y: b + t**2, **extras}, t, 0),
    ]

    results = []

    for name, description, mapping, param, target in paths:
        restricted = expr.subs(mapping)
        value = _along_limit(restricted, param, target)
        results.append({
            "name": name,
            "description": description,
            "restricted_latex": to_latex(restricted),
            "value": value,
            "value_latex": to_latex(value),
            "determined": _is_determined(value),
        })

    return results


def multivariable_limit(expr, point):
    variables = get_variables(expr)

    if not variables:
        return expr

    if len(variables) == 1:
        variable = variables[0]
        return _along_limit(expr, variable, require_point(variables, point)[variable])

    return iterated_limit(expr, point)


@register("limit")
def limit_operation(expr, params):

    point = params.get("point")
    variables = get_variables(expr)

    if not variables:
        return make_result(
            expr,
            procedure=[
                step("Expresión constante", latex=to_latex(expr),
                     text="El límite de una constante es la constante."),
                step("Alcance", text=PROCEDURE_NOTE),
            ],
        )

    substitutions = require_point(variables, point)
    procedure = [
        step("Función", latex=to_latex(expr)),
        step(
            "Punto",
            latex=",\\; ".join(
                f"{to_latex(var)} = {to_latex(substitutions[var])}"
                for var in variables
            ),
        ),
    ]

    if len(variables) == 1:
        value = multivariable_limit(expr, point)
        procedure.append(step("Límite en una variable", latex=to_latex(value)))
        procedure.append(step("Alcance", text=PROCEDURE_NOTE))
        return make_result(value, procedure=procedure)

    iterated = iterated_limit(expr, point)
    procedure.append(
        step(
            "Límite iterado (variable por variable)",
            latex=to_latex(iterated),
            text="Este cálculo no equivale al límite multivariable: exige el mismo valor por cualquier trayectoria.",
        )
    )

    paths = trajectory_limits(expr, point)
    determined = [item for item in paths if item["determined"]]
    values = [item["value"] for item in determined]
    all_determined = len(determined) == len(paths)
    agree = all_determined and all(_same_value(values[0], value) for value in values[1:])

    for index, item in enumerate(paths, start=1):
        procedure.append(
            step(
                f"Trayectoria {index}: {item['name']}",
                latex=(
                    f"{item['description']}"
                    f"\\;\\Longrightarrow\\; {item['restricted_latex']}"
                    f"\\;\\longrightarrow\\; {item['value_latex']}"
                ),
            )
        )

    caveats = [TRAJECTORY_CAVEAT, PROCEDURE_NOTE]

    extra = {
        "trajectories": [
            {
                "name": item["name"],
                "description": item["description"],
                "value_latex": item["value_latex"],
                "determined": item["determined"],
            }
            for item in paths
        ],
        "iterated_latex": to_latex(iterated),
        "paths_agree": agree,
    }

    if not all_determined:
        return make_result(
            "no existe (alguna trayectoria no tiene límite finito)",
            procedure=procedure,
            caveats=caveats,
            result_latex=r"\text{no existe}",
            **extra,
        )

    if not agree:
        return make_result(
            "no existe (las trayectorias no coinciden)",
            procedure=procedure,
            caveats=caveats,
            result_latex=r"\text{no existe}",
            **extra,
        )

    procedure.append(
        step(
            "Comparación",
            latex=to_latex(values[0]),
            text="Las cinco trayectorias coinciden. Eso no demuestra que el límite exista.",
        )
    )

    return make_result(
        values[0],
        procedure=procedure,
        caveats=caveats,
        **extra,
    )
