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
