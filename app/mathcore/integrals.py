import sympy as sp

from app.mathcore.common import make_result, step, to_latex
from app.mathcore.parser import parse_expression
from app.mathcore.registry import register


COORDINATES = {
    # El orden de cada tupla es el mismo que espera SymPy: variable interior primero.
    "double_integral": ("x", "y"),
    "double_polar": ("r", "theta"),
    "triple_integral": ("x", "y", "z"),
    "triple_cylindrical": ("r", "theta", "z"),
    "triple_spherical": ("rho", "phi", "theta"),
}


def _bounds(params, names):
    bounds = params.get("bounds")
    if not isinstance(bounds, list) or len(bounds) != len(names):
        raise ValueError(f"Se requieren {len(names)} pares de límites de integración.")

    symbols = {name: sp.Symbol(name) for name in names}
    parsed = []
    for index, (name, pair) in enumerate(zip(names, bounds)):
        if not isinstance(pair, dict) or not pair.get("lower") or not pair.get("upper"):
            raise ValueError(f"Completa los límites de {name}.")
        lower = parse_expression(str(pair["lower"]))
        upper = parse_expression(str(pair["upper"]))
        # Un limite interior puede depender de variables exteriores, no al reves.
        allowed = {symbols[outer] for outer in names[index + 1:]}
        for value in (lower, upper):
            if value.free_symbols - allowed:
                raise ValueError(f"Los límites de {name} solo pueden depender de variables exteriores.")
        parsed.append((symbols[name], lower, upper))
    return parsed, symbols


def _integrate(expr, params, operation):
    names = COORDINATES[operation]
    bounds, symbols = _bounds(params, names)

    # La funcion se escribe en cartesianas; aqui se transforma antes de integrar.
    cartesian_names = ("x", "y") if len(names) == 2 else ("x", "y", "z")
    unexpected = expr.free_symbols - {sp.Symbol(name) for name in cartesian_names}
    if unexpected:
        raise ValueError(f"La función debe estar escrita en coordenadas cartesianas {', '.join(cartesian_names)}.")

    if operation == "double_polar":
        x, y = sp.symbols("x y")
        r, theta = symbols["r"], symbols["theta"]
        # El factor r es el jacobiano del cambio a coordenadas polares.
        integrand = expr.subs({x: r * sp.cos(theta), y: r * sp.sin(theta)}) * r
    elif operation == "triple_cylindrical":
        x, y, z = sp.symbols("x y z")
        r, theta, axial = symbols["r"], symbols["theta"], symbols["z"]
        # En coordenadas cilíndricas, el jacobiano también aporta un factor r.
        integrand = expr.subs({x: r * sp.cos(theta), y: r * sp.sin(theta), z: axial}) * r
    elif operation == "triple_spherical":
        x, y, z = sp.symbols("x y z")
        rho, phi, theta = symbols["rho"], symbols["phi"], symbols["theta"]
        # En esfericas, el jacobiano es rho^2 sin(phi).
        integrand = expr.subs({
            x: rho * sp.sin(phi) * sp.cos(theta),
            y: rho * sp.sin(phi) * sp.sin(theta),
            z: rho * sp.cos(phi),
        }) * rho**2 * sp.sin(phi)
    else:
        integrand = expr

    result = sp.integrate(integrand, *bounds)
    procedure = [
        step("Integrando con jacobiano", latex=to_latex(integrand)),
        step("Integral definida", latex=sp.latex(sp.Integral(integrand, *bounds))),
        step("Resultado", latex=to_latex(result)),
    ]
    return make_result(result, procedure=procedure, coordinate_system=operation)


@register("double_integral")
def double_integral(expr, params):
    return _integrate(expr, params, "double_integral")


@register("double_polar")
def double_polar(expr, params):
    return _integrate(expr, params, "double_polar")


@register("triple_integral")
def triple_integral(expr, params):
    return _integrate(expr, params, "triple_integral")


@register("triple_cylindrical")
def triple_cylindrical(expr, params):
    return _integrate(expr, params, "triple_cylindrical")


@register("triple_spherical")
def triple_spherical(expr, params):
    return _integrate(expr, params, "triple_spherical")


@register("line_integral")
def line_integral(expr, params):
    t = sp.Symbol("t")
    try:
        lower = parse_expression(str(params["lower"]))
        upper = parse_expression(str(params["upper"]))
        x_curve = parse_expression(str(params["x_curve"]))
        y_curve = parse_expression(str(params["y_curve"]))
    except (KeyError, TypeError):
        raise ValueError("Completa la parametrización de la curva y los límites de t.")
    if (lower.free_symbols | upper.free_symbols | x_curve.free_symbols | y_curve.free_symbols) - {t}:
        raise ValueError("La curva y sus límites solo pueden depender del parámetro t.")

    kind = params.get("kind", "second")
    x, y = sp.symbols("x y")
    if kind == "first":
        # Primer tipo: el campo escalar se multiplica por la rapidez de la curva.
        integrand = expr.subs({x: x_curve, y: y_curve}) * sp.sqrt(sp.diff(x_curve, t)**2 + sp.diff(y_curve, t)**2)
    else:
        components = params.get("components")
        if not isinstance(components, list) or len(components) != 2:
            raise ValueError("La integral de segundo tipo requiere las componentes P y Q.")
        p, q = (parse_expression(str(value)) for value in components)
        # Segundo tipo: sustituye la curva en P,Q y aplica dx=x'(t)dt, dy=y'(t)dt.
        integrand = p.subs({x: x_curve, y: y_curve}) * sp.diff(x_curve, t) + q.subs({x: x_curve, y: y_curve}) * sp.diff(y_curve, t)
    result = sp.integrate(integrand, (t, lower, upper))
    return make_result(result, procedure=[
        step("Curva parametrizada", latex=rf"x(t)={to_latex(x_curve)},\quad y(t)={to_latex(y_curve)}"),
        step("Integrando", latex=to_latex(integrand)),
        step("Integral de línea", latex=sp.latex(sp.Integral(integrand, (t, lower, upper)))),
    ])


@register("green")
def green_theorem(expr, params):
    components = params.get("components")
    if not isinstance(components, list) or len(components) != 2:
        raise ValueError("El teorema de Green requiere las componentes P y Q.")
    p, q = (parse_expression(str(value)) for value in components)
    x, y = sp.symbols("x y")
    unexpected = (p.free_symbols | q.free_symbols) - {x, y}
    if unexpected:
        raise ValueError("Las componentes del campo deben depender solo de x e y.")

    order = params.get("integration_order", "dxdy")
    variable_order = {"dxdy": ("x", "y"), "dydx": ("y", "x")}
    if order not in variable_order:
        raise ValueError("El orden de integración debe ser 'dxdy' o 'dydx'.")
    # Green convierte la circulacion del borde en la integral de Q_x - P_y.
    # El orden elegido tambien determina que limites pueden depender de cual variable.
    bounds, _ = _bounds(params, variable_order[order])
    integrand = sp.diff(q, x) - sp.diff(p, y)
    value = sp.integrate(integrand, *bounds)
    return make_result(value, procedure=[
        step("Circulación según Green", title_latex=r"Q_x - P_y", latex=to_latex(integrand)),
        step("Integral doble sobre la región", latex=sp.latex(sp.Integral(integrand, *bounds))),
        step("Integral sobre la curva cerrada con orientación positiva", latex=to_latex(value)),
    ], integration_order=order)


@register("surface_area")
def surface_area(expr, params):
    bounds, _ = _bounds(params, ("x", "y"))
    x, y = sp.symbols("x y")
    integrand = sp.sqrt(1 + sp.diff(expr, x)**2 + sp.diff(expr, y)**2)
    area = sp.integrate(integrand, *bounds)
    return make_result(area, procedure=[
        step("Elemento de área", title_latex=r"dS = \sqrt{1+f_x^2+f_y^2}\,dx\,dy", latex=to_latex(integrand)),
        step("Área de la superficie", latex=sp.latex(sp.Integral(integrand, *bounds))),
        step("Resultado", latex=to_latex(area)),
    ])


@register("mass_properties")
def mass_properties(expr, params):
    bounds, _ = _bounds(params, ("x", "y"))
    x, y = sp.symbols("x y")
    mass = sp.integrate(expr, *bounds)
    if mass == 0:
        raise ValueError("La masa total es cero; no se puede calcular el centro de masa.")
    x_moment = sp.integrate(x * expr, *bounds)
    y_moment = sp.integrate(y * expr, *bounds)
    x_center = sp.simplify(x_moment / mass)
    y_center = sp.simplify(y_moment / mass)
    # Ix usa la distancia al eje x (y^2); Iy usa la distancia al eje y (x^2).
    inertia_x = sp.integrate(y**2 * expr, *bounds)
    inertia_y = sp.integrate(x**2 * expr, *bounds)
    polar_moment = sp.simplify(inertia_x + inertia_y)
    latex = (
        rf"m={to_latex(mass)},\quad (\bar x,\bar y)=({to_latex(x_center)},{to_latex(y_center)}),"
        rf"\quad (I_x,I_y,I_O)=({to_latex(inertia_x)},{to_latex(inertia_y)},{to_latex(polar_moment)})"
    )
    return {
        "result": f"m={mass}; centro=({x_center}, {y_center}); Ix={inertia_x}; Iy={inertia_y}; I0={polar_moment}",
        "result_latex": latex,
        "mass": str(mass),
        "center_of_mass": {"x": str(x_center), "y": str(y_center)},
        "moments_of_inertia": {"x": str(inertia_x), "y": str(inertia_y), "polar": str(polar_moment)},
        "procedure": [
            step("Densidad", latex=to_latex(expr)),
            step("Masa", latex=to_latex(mass)),
            step("Centro de masa", latex=rf"(\bar x,\bar y)=({to_latex(x_center)},{to_latex(y_center)})"),
            step("Momentos de inercia", latex=rf"I_x={to_latex(inertia_x)},\quad I_y={to_latex(inertia_y)},\quad I_O={to_latex(polar_moment)}"),
        ],
    }