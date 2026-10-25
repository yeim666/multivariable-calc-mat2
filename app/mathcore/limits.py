import sympy as sp

from app.mathcore.common import get_variables, make_result
from app.mathcore.parser import parse_value
from app.mathcore.registry import register


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

        if str(variable) not in point:
            raise ValueError(f"Falta el valor de '{variable}' en el punto.")

        value = parse_value(point[str(variable)])

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


# operacion "limit" de la api
@register("limit")
def limit_operation(expr, params):

    point = params.get("point")

    if not point:
        raise ValueError("No se proporcionó el punto.")

    return make_result(multivariable_limit(expr, point))
