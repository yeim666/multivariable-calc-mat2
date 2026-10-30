from app.mathcore.parser import parse_expression
from app.mathcore.domain import domain_operation


def test_domain_log_and_sqrt():
    expr = parse_expression("log(x) + sqrt(y)")
    data = domain_operation(expr, {})
    assert data["success"] if "success" in data else True
    assert "procedure" in data
    assert any("análisis conjunto" in caveat for caveat in data["caveats"])
    assert "x" in data["result"]
    assert "y" in data["result"]
