import sympy as sp

from app.mathcore.common import get_variables, make_result
from app.mathcore.parser import parse_value
from app.mathcore.registry import register


# convierte el punto recibido ({"x": "1", ...}) en un diccionario de
# sustitucion {Symbol: valor sympy}, ignorando variables que no aparecen
def _build_substitution(variables, point):

    return {
        v: parse_value(point[str(v)])
        for v in variables
        if str(v) in point
    }


# derivada parcial respecto a una variable. point es opcional: si se da,
# la derivada se evalua ahi; si no, se devuelve la forma simbolica
def partial_derivative(expr, variable_name, point=None):

    variables = get_variables(expr)
    by_name = {str(v): v for v in variables}

    if variable_name not in by_name:
        raise ValueError(f"La variable '{variable_name}' no aparece en la expresión.")

    result = sp.diff(expr, by_name[variable_name])

    if point:
        result = result.subs(_build_substitution(variables, point))

    return result


# gradiente completo: vector columna con la derivada parcial de cada
# variable. si se da point, se evalua en ese punto
def gradient(expr, point=None):

    variables = get_variables(expr)
    components = [sp.diff(expr, v) for v in variables]

    if point:
        subs_point = _build_substitution(variables, point)
        components = [c.subs(subs_point) for c in components]

    return sp.Matrix(components)


# operacion "derivative" de la api
@register("derivative")
def derivative_operation(expr, params):

    variable = params.get("variable")

    if not variable:
        raise ValueError("No se proporcionó la variable respecto a la cual derivar.")

    return make_result(partial_derivative(expr, variable, params.get("point")))


# operacion "gradient" de la api
@register("gradient")
def gradient_operation(expr, params):

    return make_result(gradient(expr, params.get("point")))


# derivada de orden superior: variables es la lista de variables a derivar,
# en orden de izquierda a derecha. ["x", "y"] = derivar primero en x y luego
# en y; ["x", "x"] = segunda derivada respecto a x
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
        result = result.subs(_build_substitution(variables, point))

    return result


# teorema de Schwarz: compara las dos derivadas mixtas de segundo orden.
# devuelve (f_ab, f_ba, son_iguales). son_iguales es True si la diferencia
# se simplifica a cero (con funciones de clase C2 siempre se cumple)
def schwarz_check(expr, name_a, name_b):

    f_ab = higher_order_derivative(expr, [name_a, name_b])
    f_ba = higher_order_derivative(expr, [name_b, name_a])

    equal = sp.simplify(f_ab - f_ba) == 0

    return f_ab, f_ba, equal


# operacion "higher_derivative" de la api. espera "variables": ["x", "y", ...]
@register("higher_derivative")
def higher_derivative_operation(expr, params):

    variables = params.get("variables")

    if not variables or not isinstance(variables, list):
        raise ValueError("Indica la lista de variables a derivar, en orden.")

    return make_result(higher_order_derivative(expr, variables, params.get("point")))


# operacion "schwarz" de la api. espera "variables": [a, b]
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

    return {
        "result": f"f_{a}{b} = {f_ab}, f_{b}{a} = {f_ba}",
        "result_latex": latex,
        "equal": equal,
    }
