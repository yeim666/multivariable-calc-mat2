import sympy as sp
import pytest

from app.mathcore.parser import parse_expression
from app.mathcore.derivatives import (
    partial_derivative, gradient, higher_order_derivative, schwarz_check,
)


# derivada parcial simbolica
def test_partial_symbolic():
    expr = parse_expression("x^2*y")
    x, y = sp.symbols("x y")
    assert partial_derivative(expr, "x") == 2*x*y


# derivada parcial evaluada en un punto
def test_partial_at_point():
    expr = parse_expression("x^2*y")
    assert partial_derivative(expr, "x", {"x": "1", "y": "3"}) == 6


# variable que no esta en la expresion
def test_partial_unknown_variable():
    expr = parse_expression("x^2")
    with pytest.raises(ValueError):
        partial_derivative(expr, "z")


# gradiente en un punto: vector con una componente por variable
def test_gradient_at_point():
    expr = parse_expression("x^2 + y^2")
    assert list(gradient(expr, {"x": "1", "y": "2"})) == [2, 4]


# segunda derivada respecto a x
def test_second_derivative():
    expr = parse_expression("x^3*y")
    x, y = sp.symbols("x y")
    assert higher_order_derivative(expr, ["x", "x"]) == 6*x*y


# derivada mixta evaluada en un punto
def test_mixed_derivative_at_point():
    expr = parse_expression("x^2*y^3")
    assert higher_order_derivative(expr, ["x", "y"], {"x": "1", "y": "1"}) == 6


# Schwarz se cumple en una funcion suave
def test_schwarz_smooth():
    expr = parse_expression("x^2*sin(y) + exp(x*y)")
    _, _, equal = schwarz_check(expr, "x", "y")
    assert equal is True


# variable inexistente en orden superior
def test_higher_unknown_variable():
    expr = parse_expression("x^2")
    with pytest.raises(ValueError):
        higher_order_derivative(expr, ["x", "z"])
