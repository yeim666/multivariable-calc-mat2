from app.mathcore.common import get_variables, to_latex
from app.mathcore.parser import parse_expression, latex_to_expr
from app.mathcore.plotting import generate_plot_data
from app.mathcore.registry import run, OPERATIONS

# importar cada modulo de operaciones ejecuta sus decoradores @register,
# que es lo que llena el diccionario OPERATIONS
from app.mathcore import limits, derivatives, geometry  # noqa: F401
