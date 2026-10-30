import sympy as sp

from app.mathcore.parser import is_constant_name, parse_value


# obtiene las variables libres de una expresion, ordenadas alfabeticamente.
# e y pi no cuentan: son constantes, aunque el parser las haya visto como letras.
def get_variables(expression):
    symbols = [
        symbol
        for symbol in expression.free_symbols
        if not is_constant_name(symbol)
    ]
    return sorted(symbols, key=str)


# convierte un objeto sympy a LaTeX, para que el frontend lo renderice
# como notacion matematica real (no como texto plano estilo python)
def to_latex(expr):
    return sp.latex(expr)


def substitution_from_point(variables, point):
    if not point:
        return {}

    return {
        variable: parse_value(point[str(variable)])
        for variable in variables
        if str(variable) in point
    }


def require_point(variables, point, label="punto"):
    if not point:
        raise ValueError(f"No se proporcionó el {label}.")

    missing = [str(variable) for variable in variables if str(variable) not in point]
    if missing:
        raise ValueError(f"Falta el valor de '{missing[0]}' en el {label}.")

    return substitution_from_point(variables, point)


def step(title=None, latex=None, text=None, title_latex=None):
    item = {}
    if title:
        item["title"] = title
    if title_latex:
        item["title_latex"] = title_latex
    if latex:
        item["latex"] = latex
    if text:
        item["text"] = text
    return item


# empaqueta un resultado sympy en el formato comun que devuelven todas
# las operaciones: texto plano + latex. el frontend solo conoce este formato
def make_result(value, procedure=None, caveats=None, **extra):
    payload = {
        "result": str(value),
        "result_latex": to_latex(value),
    }

    if procedure:
        payload["procedure"] = procedure

    if caveats:
        payload["caveats"] = caveats

    payload.update(extra)
    return payload
