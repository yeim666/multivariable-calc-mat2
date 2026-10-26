import sympy as sp


# obtiene las variables libres de una expresion, ordenadas alfabeticamente
def get_variables(expression):
    return sorted(expression.free_symbols, key=str)


# convierte un objeto sympy a LaTeX, para que el frontend lo renderice
# como notacion matematica real (no como texto plano estilo python)
def to_latex(expr):
    return sp.latex(expr)


# empaqueta un resultado sympy en el formato comun que devuelven todas
# las operaciones: texto plano + latex. el frontend solo conoce este formato
def make_result(value):
    return {
        "result": str(value),
        "result_latex": to_latex(value),
    }
