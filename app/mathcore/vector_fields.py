import sympy as sp

from app.mathcore.common import make_result, step, to_latex
from app.mathcore.parser import parse_expression
from app.mathcore.registry import register


def _components(params, expected):
    values = params.get("components")
    if not isinstance(values, list) or len(values) != expected:
        raise ValueError(f"Se requieren {expected} componentes del campo vectorial.")
    return [parse_expression(str(value)) for value in values]


@register("divergence")
def divergence(expr, params):
    components = _components(params, len(params.get("components", [])))
    if len(components) not in (2, 3):
        raise ValueError("La divergencia requiere un campo de 2 o 3 componentes.")
    # Las componentes se interpretan en el orden fijo x, y, z.
    variables = sp.symbols("x y z")[:len(components)]
    value = sp.simplify(sum(sp.diff(component, variable) for component, variable in zip(components, variables)))
    return make_result(value, procedure=[
        step("Campo", latex=r"\vec{F} = " + sp.latex(sp.Matrix(components))),
        step(title_latex=r"\nabla \cdot \vec{F}", latex=to_latex(value)),
        step("Interpretación", text="La divergencia mide la densidad local de flujo neto del campo."),
    ])


@register("curl")
def curl(expr, params):
    components = _components(params, len(params.get("components", [])))
    if len(components) not in (2, 3):
        raise ValueError("El rotacional requiere un campo de 2 o 3 componentes.")
    variables = sp.symbols("x y z")[:len(components)]
    if len(variables) == 2:
        x, y = variables
        # En el plano, el rotacional se devuelve como su componente perpendicular.
        value = sp.simplify(sp.diff(components[1], x) - sp.diff(components[0], y))
    else:
        x, y, z = variables
        p, q, r = components
        value = sp.Matrix([
            sp.diff(r, y) - sp.diff(q, z),
            sp.diff(p, z) - sp.diff(r, x),
            sp.diff(q, x) - sp.diff(p, y),
        ]).applyfunc(sp.simplify)
    return make_result(value, procedure=[
        step("Campo", latex=r"\vec{F} = " + sp.latex(sp.Matrix(components))),
        step(title_latex=r"\nabla \times \vec{F}", latex=to_latex(value)),
        step("Interpretación", text="El rotacional describe la tendencia local de giro del campo."),
    ])


@register("laplacian")
def laplacian(expr, params):
    variables = sorted(expr.free_symbols, key=str)
    if len(variables) not in (1, 2, 3):
        raise ValueError("El Laplaciano requiere una función de 1, 2 o 3 variables.")
    value = sp.simplify(sum(sp.diff(expr, variable, 2) for variable in variables))
    return make_result(value, procedure=[
        step("Campo escalar", latex=to_latex(expr)),
        step(title_latex=r"\nabla^2 f", latex=to_latex(value)),
        step("Interpretación", text="El Laplaciano mide la variación neta local de un campo escalar."),
    ])


@register("conservative")
def conservative(expr, params):
    components = _components(params, 2)
    x, y = sp.symbols("x y")
    p, q = components
    curl_value = sp.simplify(sp.diff(q, x) - sp.diff(p, y))
    # Integra P respecto a x y completa el potencial con la parte restante de Q.
    potential = sp.integrate(p, x) + sp.integrate(q - sp.diff(sp.integrate(p, x), y), y)
    residual = sp.simplify(sp.diff(potential, x) - p) + sp.simplify(sp.diff(potential, y) - q)
    is_conservative = curl_value == 0 and residual == 0
    note = (
        "En un dominio simplemente conexo, rotacional nulo implica independencia de trayectoria."
        if is_conservative
        else "El criterio de rotacional nulo o la reconstrucción del potencial no se cumple."
    )
    return make_result(
        potential if is_conservative else curl_value,
        procedure=[
            step("Campo", latex=r"\vec{F} = " + sp.latex(sp.Matrix([p, q]))),
            step(title_latex=r"Q_x - P_y", latex=to_latex(curl_value)),
            step("Potencial", latex=to_latex(potential)),
            step("Conclusión", text=note),
        ],
        conservative=is_conservative,
        potential_latex=to_latex(potential) if is_conservative else None,
        note=note,
    )


@register("vector_curve")
def vector_curve(expr, params):
    components = _components(params, len(params.get("components", [])))
    if len(components) not in (2, 3):
        raise ValueError("La función vectorial debe tener 2 o 3 componentes.")
    t = sp.Symbol("t")
    parameter = parse_expression(str(params.get("parameter", "0")))
    if parameter.free_symbols:
        raise ValueError("El parámetro de evaluación debe ser un valor constante.")

    mode = params.get("mode", "derivative")
    results = []
    # Limite, derivada e integral vectoriales se calculan componente por componente.
    for component in components:
        if mode == "limit":
            target = sp.limit(component, t, parameter)
        elif mode == "integral":
            lower = parse_expression(str(params.get("lower", "0")))
            target = sp.integrate(component, (t, lower, parameter))
        elif mode == "derivative":
            target = sp.diff(component, t).subs(t, parameter)
        else:
            raise ValueError("Elige límite, derivada o integral para la función vectorial.")
        results.append(sp.simplify(target))

    vector = sp.Matrix(results)
    title = {"limit": "Límite vectorial", "integral": "Integral vectorial", "derivative": "Derivada vectorial"}[mode]
    return make_result(vector, procedure=[
        step("Función vectorial", latex=r"\vec{r}(t) = " + sp.latex(sp.Matrix(components))),
        step(title, latex=to_latex(vector)),
    ])