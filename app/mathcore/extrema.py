import sympy as sp

from app.mathcore.common import get_variables, make_result, step, to_latex
from app.mathcore.parser import latex_to_expr, parse_expression
from app.mathcore.registry import register


PROCEDURE_NOTE = (
    "Los procedimientos describen operaciones simbólicas y no constituyen un tutor universal."
)

CANDIDATE_CAVEAT = (
    "Los candidatos de extremos requieren clasificación y revisión del dominio."
)


def _real_enough(value):
    if value.free_symbols:
        return True

    numeric = sp.N(value)

    if numeric.is_infinite:
        return False

    imag = getattr(numeric, "as_real_imag", lambda: (numeric, 0))()[1]
    try:
        return abs(float(imag)) < 1e-10
    except (TypeError, ValueError):
        return value.is_real is not False


def _real_solutions(equations, unknowns):
    try:
        solutions = sp.solve(equations, unknowns, dict=True)
    except Exception:
        return []

    real = []

    for solution in solutions:
        if all(_real_enough(solution[unknown]) for unknown in unknowns if unknown in solution):
            real.append(solution)

    return real


def _classify_hessian(expr, variables, solution):
    if len(variables) == 0:
        return "sin clasificar"

    if any(variable not in solution for variable in variables):
        return "familia de candidatos; clasificación pendiente"

    hessian = sp.hessian(expr, variables).subs(solution)

    try:
        hessian = sp.simplify(hessian)
    except Exception:
        return "hessiana no evaluable; clasificación pendiente"

    if len(variables) == 1:
        second = hessian[0, 0]
        if second.is_positive:
            return "mínimo local (f'' > 0)"
        if second.is_negative:
            return "máximo local (f'' < 0)"
        return "prueba de la segunda derivada inconclusa"

    if len(variables) == 2:
        d = sp.simplify(hessian.det())
        fxx = sp.simplify(hessian[0, 0])

        if d.is_negative:
            return "punto de silla (H < 0)"
        if d.is_positive and fxx.is_positive:
            return "mínimo local (H > 0 y f_xx > 0)"
        if d.is_positive and fxx.is_negative:
            return "máximo local (H > 0 y f_xx < 0)"
        return "prueba de la hessiana inconclusa (H = 0 o signo no determinado)"

    try:
        eigenvals = list(hessian.eigenvals().keys())
    except Exception:
        return "clasificación pendiente (autovalores no calculados)"

    signs = []
    for value in eigenvals:
        if value.is_positive:
            signs.append(1)
        elif value.is_negative:
            signs.append(-1)
        elif value == 0:
            signs.append(0)
        else:
            return "prueba espectral inconclusa"

    if 0 in signs:
        return "prueba espectral inconclusa (autovalor nulo)"
    if all(sign > 0 for sign in signs):
        return "mínimo local (hessiana definida positiva)"
    if all(sign < 0 for sign in signs):
        return "máximo local (hessiana definida negativa)"
    return "punto de silla (hessiana indefinida)"


def _point_latex(variables, solution):
    return r"\left(" + ", ".join(to_latex(solution.get(var, var)) for var in variables) + r"\right)"


@register("critical")
def critical_operation(expr, params):

    variables = get_variables(expr)

    if not variables:
        raise ValueError("Una constante no tiene candidatos críticos.")

    gradient = [sp.diff(expr, var) for var in variables]
    procedure = [
        step("Función", latex=to_latex(expr)),
        step(title_latex=r"\nabla f = 0", latex=to_latex(sp.Matrix(gradient))),
    ]

    solutions = _real_solutions(gradient, variables)

    if not solutions:
        procedure.append(step("Sistema", text="No se encontraron soluciones reales de ∇f = 0."))
        procedure.append(step("Advertencia", text=CANDIDATE_CAVEAT))
        procedure.append(step("Alcance", text=PROCEDURE_NOTE))
        return make_result(
            "sin candidatos críticos encontrados",
            procedure=procedure,
            caveats=[CANDIDATE_CAVEAT, PROCEDURE_NOTE],
            result_latex=r"\emptyset",
            candidates=[],
        )

    candidates = []
    latex_items = []

    for solution in solutions:
        classification = _classify_hessian(expr, variables, solution)
        point_latex = _point_latex(variables, solution)
        candidates.append({
            "point_latex": point_latex,
            "classification": classification,
        })
        latex_items.append(rf"{point_latex}\ \text{{({classification})}}")
        procedure.append(
            step(
                "Candidato",
                latex=point_latex,
                text=classification,
            )
        )

    procedure.append(step("Advertencia", text=CANDIDATE_CAVEAT))
    procedure.append(step("Alcance", text=PROCEDURE_NOTE))

    return make_result(
        "; ".join(f"{item['point_latex']}: {item['classification']}" for item in candidates),
        procedure=procedure,
        caveats=[CANDIDATE_CAVEAT, PROCEDURE_NOTE],
        result_latex="\\\\".join(latex_items),
        candidates=candidates,
    )


def _constraint_expr(params, variables):
    raw = params.get("constraint")

    if not raw:
        raise ValueError("Indica la restricción g = 0 (o una ecuación g = c).")

    try:
        if params.get("constraint_is_latex"):
            g = latex_to_expr(raw)
        else:
            try:
                g = latex_to_expr(raw)
            except Exception:
                g = parse_expression(raw)
    except Exception as error:
        raise ValueError(f"No se pudo interpretar la restricción: {error}") from error

    if isinstance(g, sp.Equality):
        g = sp.simplify(g.lhs - g.rhs)

    return sp.simplify(g)


@register("lagrange")
def lagrange_operation(expr, params):

    variables = get_variables(expr)
    g = _constraint_expr(params, variables)
    unknowns = sorted(set(variables) | set(get_variables(g)), key=str)

    if len(unknowns) < 2:
        raise ValueError("Lagrange necesita al menos dos variables en f o en g.")

    lam = sp.Symbol("lambda")
    grad_f = [sp.diff(expr, var) for var in unknowns]
    grad_g = [sp.diff(g, var) for var in unknowns]
    equations = [sp.simplify(df - lam * dg) for df, dg in zip(grad_f, grad_g)]
    equations.append(g)

    procedure = [
        step("Objetivo", latex=to_latex(expr)),
        step("Restricción g = 0", latex=to_latex(g)),
        step(title_latex=r"\nabla f = \lambda \nabla g", latex=to_latex(sp.Matrix(equations[:-1]))),
        step("Ecuaciones", text="Se resuelve el sistema de Lagrange junto con g = 0."),
    ]

    solutions = _real_solutions(equations, unknowns + [lam])

    if not solutions:
        procedure.append(step("Sistema", text="No se encontraron candidatos reales."))
        procedure.append(step("Advertencia", text=CANDIDATE_CAVEAT))
        procedure.append(step("Alcance", text=PROCEDURE_NOTE))
        return make_result(
            "sin candidatos de Lagrange encontrados",
            procedure=procedure,
            caveats=[CANDIDATE_CAVEAT, PROCEDURE_NOTE],
            result_latex=r"\emptyset",
            candidates=[],
        )

    candidates = []
    latex_items = []

    for solution in solutions:
        point_latex = _point_latex(unknowns, solution)
        lam_latex = to_latex(solution[lam]) if lam in solution else None
        value = sp.simplify(expr.subs({var: solution[var] for var in variables if var in solution}))
        classification = "candidato sobre la restricción; falta clasificar y revisar el dominio"
        candidate = {
            "point_latex": point_latex,
            "value_latex": to_latex(value),
            "classification": classification,
        }
        if lam_latex is not None:
            candidate["lambda_latex"] = lam_latex
            latex_items.append(
                rf"{point_latex},\ \lambda={lam_latex},\ f={to_latex(value)}"
            )
        else:
            latex_items.append(rf"{point_latex},\ f={to_latex(value)}")
        candidates.append(candidate)
        procedure.append(
            step(
                "Candidato",
                latex=(
                    rf"{point_latex},\ \lambda = {lam_latex},\ f = {to_latex(value)}"
                    if lam_latex is not None
                    else rf"{point_latex},\ f = {to_latex(value)}"
                ),
                text=classification,
            )
        )

    procedure.append(step("Advertencia", text=CANDIDATE_CAVEAT))
    procedure.append(step("Alcance", text=PROCEDURE_NOTE))

    return make_result(
        "; ".join(
            f"{item['point_latex']}, "
            + (f"λ={item['lambda_latex']}, " if "lambda_latex" in item else "")
            + f"f={item['value_latex']}"
            for item in candidates
        ),
        procedure=procedure,
        caveats=[CANDIDATE_CAVEAT, PROCEDURE_NOTE],
        result_latex="\\\\".join(latex_items),
        candidates=candidates,
    )
