from app.mathcore.parser import latex_to_expr, parse_expression, parse_value
from app.mathcore.common import get_variables
import sympy as sp


def test_e_is_euler_constant():
    expr = parse_expression("e^x + y")
    assert expr.free_symbols == {sp.Symbol("x"), sp.Symbol("y")}
    assert get_variables(expr) == [sp.Symbol("x"), sp.Symbol("y")]
    assert expr.subs({sp.Symbol("x"): 0, sp.Symbol("y"): 0}) == 1


def test_pi_is_constant_in_text():
    expr = parse_expression("sin(pi*x) + y")
    assert get_variables(expr) == [sp.Symbol("x"), sp.Symbol("y")]


def test_latex_pi_is_not_a_variable():
    expr = latex_to_expr(r"\pi x + y")
    assert expr.has(sp.pi)
    assert get_variables(expr) == [sp.Symbol("x"), sp.Symbol("y")]


def test_latex_e_is_not_a_variable():
    expr = latex_to_expr(r"e^{x}+y")
    names = {str(v) for v in get_variables(expr)}
    assert names == {"x", "y"}
    assert expr.subs({sp.Symbol("x"): 0, sp.Symbol("y"): 0}) == 1


def test_constants_work_in_mixed_text_and_latex_forms():
    text_expr = parse_expression("e^x + pi*y")
    latex_expr = latex_to_expr(r"e^{x}+\pi y")

    assert get_variables(text_expr) == [sp.Symbol("x"), sp.Symbol("y")]
    assert get_variables(latex_expr) == [sp.Symbol("x"), sp.Symbol("y")]
    assert text_expr.subs({sp.Symbol("x"): 0, sp.Symbol("y"): 0}) == 1
    assert latex_expr.subs({sp.Symbol("x"): 0, sp.Symbol("y"): 0}) == 1


def test_parse_value_accepts_e_and_pi():
    assert parse_value("e") == sp.E
    assert parse_value("pi") == sp.pi
    assert parse_value("pi/2") == sp.pi / 2
