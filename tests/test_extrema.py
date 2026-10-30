from app.mathcore.parser import parse_expression
from app.mathcore.derivatives import gradient, hessian_operation, directional_operation
from app.mathcore.extrema import critical_operation, lagrange_operation
from app.mathcore.limits import limit_operation
import sympy as sp


def test_hessian_at_origin():
    expr = parse_expression("x^2 + y^2")
    data = hessian_operation(expr, {"point": {"x": "0", "y": "0"}})
    assert "procedure" in data
    matrix = sp.Matrix([[2, 0], [0, 2]])
    assert sp.sympify(data["result"]) == matrix


def test_directional_unit_vector():
    expr = parse_expression("x^2 + y^2")
    data = directional_operation(expr, {
        "direction": {"x": "1", "y": "0"},
        "point": {"x": "1", "y": "0"},
    })
    assert sp.simplify(sp.sympify(data["result"]) - 2) == 0


def test_critical_paraboloid():
    expr = parse_expression("x^2 + y^2")
    data = critical_operation(expr, {})
    assert data["candidates"]
    assert "mínimo" in data["candidates"][0]["classification"]


def test_critical_families_do_not_crash():
    expr = parse_expression("x^2*y^2")
    data = critical_operation(expr, {})
    assert data["candidates"]
    assert any("familia" in item["classification"] for item in data["candidates"])


def test_lagrange_xy_on_line():
    expr = parse_expression("x*y")
    data = lagrange_operation(expr, {"constraint": "x+y-1", "constraint_is_latex": False})
    assert data["candidates"]
    assert "procedure" in data


def test_lagrange_singular_constraint_omits_missing_multiplier():
    expr = parse_expression("x*y")
    data = lagrange_operation(expr, {"constraint": "x^2", "constraint_is_latex": False})
    assert data["candidates"]
    assert all("lambda_latex" not in item for item in data["candidates"])
    assert r"\mathtt{\text{}}" not in data["result_latex"]


def test_limit_paths_disagree():
    expr = parse_expression("x*y/(x^2 + y^2)")
    data = limit_operation(expr, {"point": {"x": "0", "y": "0"}})
    assert data["paths_agree"] is False
    assert "no existe" in data["result"]
    assert len(data["trajectories"]) == 5


def test_limit_paths_agree_with_caveat():
    expr = parse_expression("x^2 + y^2")
    data = limit_operation(expr, {"point": {"x": "1", "y": "2"}})
    assert data["paths_agree"] is True
    assert data["result"] == "5"
    assert any("no demuestra" in caveat for caveat in data["caveats"])


def test_gradient_still_works():
    expr = parse_expression("x^2 + y^2")
    assert list(gradient(expr, {"x": "1", "y": "2"})) == [2, 4]
