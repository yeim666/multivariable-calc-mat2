import sympy as sp

from app.mathcore.common import (
    get_variables,
    make_result,
    step,
    substitution_from_point,
    to_latex,
)
from app.mathcore.parser import parse_value
from app.mathcore.registry import register


PROCEDURE_NOTE = (
    "Los procedimientos describen operaciones simbólicas y no constituyen un tutor universal."
)


def _point_steps(variables, point):
    if not point:
        return []

    subs = substitution_from_point(variables, point)
    return [
        step(
            "Punto de evaluación",
            latex=",\\; ".join(
                f"{to_latex(var)} = {to_latex(subs[var])}"
                for var in variables
                if var in subs
            ),
        )
    ]


def partial_derivative(expr, variable_name, point=None):

    variables = get_variables(expr)
    by_name = {str(v): v for v in variables}

    if variable_name not in by_name:
        raise ValueError(f"La variable '{variable_name}' no aparece en la expresión.")

    result = sp.diff(expr, by_name[variable_name])

    if point:
        result = result.subs(substitution_from_point(variables, point))

    return result


def gradient(expr, point=None):

    variables = get_variables(expr)
    components = [sp.diff(expr, v) for v in variables]

    if point:
        subs_point = substitution_from_point(variables, point)
        components = [c.subs(subs_point) for c in components]

    return sp.Matrix(components)


def parse_direction(variables, direction):

    if not direction:
        raise ValueError("Indica un vector dirección.")

    components = []

    for variable in variables:
        name = str(variable)
        if name not in direction:
            raise ValueError(f"Falta la componente de '{name}' en la dirección.")
        components.append(parse_value(direction[name]))

    vector = sp.Matrix(components)

    if vector.norm() == 0:
        raise ValueError("El vector dirección no puede ser nulo.")

    return vector


@register("derivative")
def derivative_operation(expr, params):

    variable = params.get("variable")

    if not variable:
        raise ValueError("No se proporcionó la variable respecto a la cual derivar.")

    variables = get_variables(expr)
    symbolic = partial_derivative(expr, variable)
    result = partial_derivative(expr, variable, params.get("point"))

    procedure = [
        step("Función", latex=to_latex(expr)),
        step(f"Derivada parcial respecto de {variable}", latex=to_latex(symbolic)),
        *_point_steps(variables, params.get("point")),
        step("Alcance", text=PROCEDURE_NOTE),
    ]

    if params.get("point"):
        procedure.insert(-1, step("Evaluación", latex=to_latex(result)))

    return make_result(result, procedure=procedure)


@register("gradient")
def gradient_operation(expr, params):

    variables = get_variables(expr)

    if not variables:
        raise ValueError("Una constante no tiene gradiente no trivial.")

    symbolic = gradient(expr)
    result = gradient(expr, params.get("point"))

    procedure = [
        step("Función", latex=to_latex(expr)),
        step("Variables", latex=to_latex(sp.Matrix([variables]).T)),
    ]

    for variable, component in zip(variables, symbolic):
        procedure.append(
            step(
                title_latex=rf"\frac{{\partial f}}{{\partial {to_latex(variable)}}}",
                latex=to_latex(component),
            )
        )

        procedure.append(step(title_latex=r"\nabla f", latex=to_latex(symbolic)))
    procedure.extend(_point_steps(variables, params.get("point")))

    if params.get("point"):
        procedure.append(step("Gradiente en el punto", title_latex=r"\nabla f", latex=to_latex(result)))

    procedure.append(step("Alcance", text=PROCEDURE_NOTE))

    return make_result(result, procedure=procedure)


def higher_order_derivative(expr, variable_names, point=None):

    variables = get_variables(expr)
    by_name = {str(v): v for v in variables}

    if not variable_names:
        raise ValueError("Indica al menos una variable para derivar.")

    for name in variable_names:
        if name not in by_name:
            raise ValueError(f"La variable '{name}' no aparece en la expresión.")

    result = sp.diff(expr, *[by_name[name] for name in variable_names])

    if point:
        result = result.subs(substitution_from_point(variables, point))

    return result


def schwarz_check(expr, name_a, name_b):

    f_ab = higher_order_derivative(expr, [name_a, name_b])
    f_ba = higher_order_derivative(expr, [name_b, name_a])
    equal = sp.simplify(f_ab - f_ba) == 0

    return f_ab, f_ba, equal


@register("higher_derivative")
def higher_derivative_operation(expr, params):

    variables = params.get("variables")

    if not variables or not isinstance(variables, list):
        raise ValueError("Indica la lista de variables a derivar, en orden.")

    order = ", ".join(variables)
    symbolic = higher_order_derivative(expr, variables)
    result = higher_order_derivative(expr, variables, params.get("point"))
    free = get_variables(expr)

    procedure = [
        step("Función", latex=to_latex(expr)),
        step("Orden de derivación", text=order),
        step("Derivada", latex=to_latex(symbolic)),
        *_point_steps(free, params.get("point")),
        step("Alcance", text=PROCEDURE_NOTE),
    ]

    if params.get("point"):
        procedure.insert(-1, step("Evaluación", latex=to_latex(result)))

    return make_result(result, procedure=procedure)


@register("schwarz")
def schwarz_operation(expr, params):

    variables = params.get("variables")

    if not isinstance(variables, list) or len(variables) != 2:
        raise ValueError("Indica exactamente dos variables para comparar las derivadas mixtas.")

    f_ab, f_ba, equal = schwarz_check(expr, variables[0], variables[1])
    a, b = variables
    latex = (
        f"f_{{{a}{b}}} = {sp.latex(f_ab)}"
        f"\\;,\\quad f_{{{b}{a}}} = {sp.latex(f_ba)}"
    )

    procedure = [
        step("Función", latex=to_latex(expr)),
        step(title_latex=rf"f_{{{a}{b}}}", latex=to_latex(f_ab)),
        step(title_latex=rf"f_{{{b}{a}}}", latex=to_latex(f_ba)),
        step(
            "Comparación",
            text="Las derivadas mixtas coinciden." if equal else "Las derivadas mixtas no coinciden.",
        ),
        step("Alcance", text=PROCEDURE_NOTE),
    ]

    return {
        "result": f"f_{a}{b} = {f_ab}, f_{b}{a} = {f_ba}",
        "result_latex": latex,
        "equal": equal,
        "procedure": procedure,
    }


@register("hessian")
def hessian_operation(expr, params):

    variables = get_variables(expr)

    if len(variables) < 1:
        raise ValueError("La hessiana requiere al menos una variable.")

    matrix = sp.hessian(expr, variables)
    procedure = [
        step("Función", latex=to_latex(expr)),
        step("Variables", latex=to_latex(sp.Matrix([variables]).T)),
    ]

    for i, vi in enumerate(variables):
        for j, vj in enumerate(variables):
            if j < i:
                continue
            second = sp.diff(expr, vi, vj)
            procedure.append(
                step(
                    title_latex=rf"f_{{{to_latex(vi)}{to_latex(vj)}}}",
                    latex=to_latex(second),
                )
            )

    procedure.append(step("Matriz hessiana", latex=to_latex(matrix)))
    procedure.extend(_point_steps(variables, params.get("point")))

    result = matrix
    if params.get("point"):
        result = matrix.subs(substitution_from_point(variables, params["point"]))
        procedure.append(step("Hessiana en el punto", latex=to_latex(result)))

    procedure.append(step("Alcance", text=PROCEDURE_NOTE))

    return make_result(result, procedure=procedure)


@register("directional")
def directional_operation(expr, params):

    variables = get_variables(expr)

    if not variables:
        raise ValueError("Indica una función con variables.")

    vector = parse_direction(variables, params.get("direction"))
    unit = sp.simplify(vector / vector.norm())
    grad = gradient(expr)
    symbolic = sp.simplify((grad.T * unit)[0])
    result = symbolic

    procedure = [
        step("Función", latex=to_latex(expr)),
        step(title_latex=r"\nabla f", latex=to_latex(grad)),
        step(title_latex=r"\vec{u}", latex=to_latex(vector)),
        step(title_latex=r"\hat{u} = \vec{u}/\|\vec{u}\|", latex=to_latex(unit)),
        step(title_latex=r"D_{\hat{u}} f = \nabla f \cdot \hat{u}", latex=to_latex(symbolic)),
        *_point_steps(variables, params.get("point")),
    ]

    if params.get("point"):
        result = symbolic.subs(substitution_from_point(variables, params["point"]))
        procedure.append(step("Evaluación", latex=to_latex(result)))

    procedure.append(step("Alcance", text=PROCEDURE_NOTE))

    return make_result(result, procedure=procedure)
