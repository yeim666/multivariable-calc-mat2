import sympy as sp


# parser sencillo, un parser basicamente convierte el input del usuario
# en una expresion de sympy
def parse_expression(expression):

    # simbolos permitidos
    x, y, z = sp.symbols("x y z")

    # diccionario asignando el valor correspondiente a cada letra
    variables = {
        "x": x,
        "y": y,
        "z": z
    }

    # sympify convierte el string del input en una expresion de sympy
    return sp.sympify(expression, locals=variables)


# obtiene las variables de la expresion
def get_variables(expression):
    # no hay mucho que decir de esto xd
    return sorted(expression.free_symbols, key=str)


# funcion del limite
def multivariable_limit(expression, point):

    # llamamos al parser para que convierta el input del usuario y este se guarde en expr
    expr = parse_expression(expression)

    # encontramos las variables que contiene la expresion
    variables = get_variables(expr)

    # en el caso de que no haya una variable y la expresion exista
    # asumimos que hay una constante, y el limite de la expresion es la misma constante
    if not variables:
        return expr

    # guardamos la expresion en result
    result = expr

    # calculamos el límite respecto a cada variable.
    for variable in variables:

        # obtenemos el valor que le corresponde a la variable actual
        value = point[str(variable)]

        # calculamos el límite respecto a esa variable.
        result = sp.limit(
            result,
            variable,
            value
        )

    # devuelve el resutado yya
    return result
