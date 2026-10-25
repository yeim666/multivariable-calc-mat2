import sympy as sp
import pytest

from app.mathcore.parser import parse_expression
from app.mathcore.limits import multivariable_limit


# limite de un polinomio: sustitucion directa
def test_polynomial_limit():
    expr = parse_expression("x^2 + y^2")
    assert multivariable_limit(expr, {"x": "1", "y": "2"}) == 5


# forma indeterminada que obliga a usar sp.limit
def test_indeterminate_limit():
    expr = parse_expression("sin(x)/x")
    assert multivariable_limit(expr, {"x": "0"}) == 1


# el punto acepta fracciones y constantes, no solo enteros
def test_point_accepts_fraction():
    expr = parse_expression("2*x")
    assert multivariable_limit(expr, {"x": "1/2"}) == 1


# si falta una variable del punto debe avisar con ValueError
def test_missing_point_variable():
    expr = parse_expression("x + y")
    with pytest.raises(ValueError):
        multivariable_limit(expr, {"x": "0"})


# un valor con texto no numerico se rechaza
def test_invalid_point_value():
    expr = parse_expression("x")
    with pytest.raises(ValueError):
        multivariable_limit(expr, {"x": "y"})
