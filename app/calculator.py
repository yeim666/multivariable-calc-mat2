import sympy as sp

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)

#definicion de transformaciones con sympy
transformations = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)

# parser sencillo, un parser basicamente convierte el input del usuario
# en una expresion de sympy
def parse_expression(expression):

    x, y, z = sp.symbols("x y z")

    variables = {
        "x": x,
        "y": y,
        "z": z
    }
    # parse_expr interpreta la expresión escrita
    # por el usuario.
  
    return parse_expr(
        expression,
        local_dict=variables,
        transformations=transformations
    )

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