import sympy as sp
import pytest

from app.mathcore.parser import parse_expression
from app.mathcore.geometry import tangent_plane_and_normal


# paraboloide z = x^2 + y^2 en (1, 2): fx=2, fy=4, f=5 -> z = 2x + 4y - 5
def test_tangent_plane_paraboloid():
    expr = parse_expression("x^2 + y^2")
    x, y = sp.symbols("x y")
    _, fx, fy, plane, line = tangent_plane_and_normal(expr, {"x": "1", "y": "2"})
    assert (fx, fy) == (2, 4)
    assert sp.expand(plane - (2*x + 4*y - 5)) == 0
    # la recta normal pasa por (1, 2, 5) con direccion (2, 4, -1)
    assert list(line.subs(sp.Symbol("t"), 0)) == [1, 2, 5]


# solo funciones de dos variables
def test_tangent_plane_needs_two_variables():
    with pytest.raises(ValueError):
        tangent_plane_and_normal(parse_expression("x^2"), {"x": "1"})


# punto fuera del dominio: 1/x en x=0
def test_tangent_plane_outside_domain():
    with pytest.raises(ValueError):
        tangent_plane_and_normal(parse_expression("1/x + y"), {"x": "0", "y": "1"})
