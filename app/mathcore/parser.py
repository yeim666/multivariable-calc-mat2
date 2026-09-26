import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)
from sympy.parsing.latex import parse_latex


# transformaciones para el parser de texto plano:
# - implicit_multiplication_application: permite "2x" -> "2*x", "xy" -> "x*y"
# - convert_xor: convierte "^" en potencia (**) en vez de xor bit a bit
TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


# funciones matematicas permitidas explicitamente en el parser de texto plano.
# cualquier identificador que NO este aqui, sympy lo trata como variable nueva
# automaticamente. esto es lo que permite funciones de cualquier nombre de variable.
ALLOWED_FUNCTIONS = {
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "sinh": sp.sinh,
    "cosh": sp.cosh,
    "tanh": sp.tanh,
    "exp": sp.exp,
    "log": sp.log,
    "ln": sp.log,
    "sqrt": sp.sqrt,
    "Abs": sp.Abs,
    "pi": sp.pi,
    "E": sp.E,
}


# espacio de evaluacion controlado para parse_expr. sin __builtins__, para
# que el usuario no pueda ejecutar codigo python arbitrario (ej. __import__).
# Symbol, Integer y Float estan aqui porque las transformaciones de sympy
# generan codigo interno que los necesita para crear variables/numeros nuevos.
GLOBAL_DICT = {
    "Symbol": sp.Symbol,
    "Integer": sp.Integer,
    "Float": sp.Float,
    "__builtins__": {},
}


# parser de texto plano (ej. "x^2 + y^2", "sqrt(x)+sin(y)").
# cualquier identificador que el usuario escriba y que no este en
# ALLOWED_FUNCTIONS se convierte automaticamente en una variable simbolica nueva.
def parse_expression(expression):

    return parse_expr(
        expression,
        local_dict=ALLOWED_FUNCTIONS,
        global_dict=GLOBAL_DICT,
        transformations=TRANSFORMATIONS,
    )


# parser de notacion LaTeX (usado por el math-field de MathLive).
# devuelve directamente un objeto sympy, igual que parse_expression.
def latex_to_expr(latex_string):

    try:
        return parse_latex(latex_string)

    # normalizamos cualquier error interno de parse_latex a ValueError,
    # para que routes.py lo maneje igual que los errores del parser de texto
    except Exception as e:
        raise ValueError(f"No se pudo interpretar la notación matemática: {e}")
