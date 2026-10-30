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


# constantes que el usuario escribe como letras o simbolos de MathLive.
# sin esto, "e" y "\pi" entran como variables libres y rompen deteccion,
# limites, graficas y puntos de evaluacion.
CONSTANT_NAMES = {
    "e": sp.E,
    "E": sp.E,
    "pi": sp.pi,
    "Pi": sp.pi,
    "π": sp.pi,
    "exponentialE": sp.E,
}


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
    "e": sp.E,
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


def replace_constants(expr):
    """Sustituye e, pi y equivalentes de MathLive por las constantes de SymPy."""

    if not hasattr(expr, "free_symbols"):
        return expr

    replacements = {}

    for symbol in expr.free_symbols:
        constant = CONSTANT_NAMES.get(str(symbol))
        if constant is not None:
            replacements[symbol] = constant

    return expr.subs(replacements) if replacements else expr


def is_constant_name(name):
    return str(name) in CONSTANT_NAMES


def _normalize_latex(latex_string):
    # MathLive a veces escribe el numero e con comandos propios
    return (
        latex_string
        .replace(r"\exponentialE", "e")
        .replace(r"\mathrm{e}", "e")
        .replace(r"\operatorname{e}", "e")
    )


# parser de texto plano (ej. "x^2 + y^2", "sqrt(x)+sin(y)").
# cualquier identificador que el usuario escriba y que no este en
# ALLOWED_FUNCTIONS se convierte automaticamente en una variable simbolica nueva.
def parse_expression(expression):

    expr = parse_expr(
        expression,
        local_dict=ALLOWED_FUNCTIONS,
        global_dict=GLOBAL_DICT,
        transformations=TRANSFORMATIONS,
    )

    return replace_constants(expr)


# parser de notacion LaTeX (usado por el math-field de MathLive).
# devuelve directamente un objeto sympy, igual que parse_expression.
def latex_to_expr(latex_string):

    try:
        expr = parse_latex(_normalize_latex(latex_string))
        return replace_constants(expr)

    # normalizamos cualquier error interno de parse_latex a ValueError,
    # para que routes.py lo maneje igual que los errores del parser de texto
    except Exception as e:
        raise ValueError(f"No se pudo interpretar la notación matemática: {e}")


# convierte el texto de un valor numerico (ej. "0", "1/2", "pi") en un
# objeto sympy. pasa por el parser controlado en vez de sympify, para no
# evaluar texto arbitrario que llegue a la api
def parse_value(text):

    try:
        value = parse_expression(str(text))
    except Exception:
        raise ValueError(f"Valor no válido: '{text}'")

    # un valor de punto debe ser un numero, no una expresion con variables
    if value.free_symbols:
        raise ValueError(f"Valor no válido: '{text}'")

    return value
