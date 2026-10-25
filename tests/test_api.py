import pytest

from app import create_app


@pytest.fixture
def client():
    return create_app().test_client()


# la operacion "limit" responde con el formato comun
def test_limit_endpoint(client):
    res = client.post("/api/limit", json={"expression": "x^2 + y^2", "point": {"x": "1", "y": "2"}})
    data = res.get_json()
    assert res.status_code == 200
    assert data["success"] is True
    assert data["result"] == "5"
    assert "result_latex" in data


# la operacion "derivative" exige la variable
def test_derivative_requires_variable(client):
    res = client.post("/api/derivative", json={"expression": "x^2"})
    assert res.status_code == 400
    assert res.get_json()["success"] is False


# las operaciones nuevas quedan disponibles solo con registrarlas
def test_gradient_endpoint(client):
    res = client.post("/api/gradient", json={"expression": "x^2 + y^2"})
    assert res.get_json()["success"] is True


# una operacion que no existe da 404
def test_unknown_operation(client):
    res = client.post("/api/inexistente", json={"expression": "x"})
    assert res.status_code == 404


# detectar variables sigue funcionando
def test_variables_endpoint(client):
    res = client.post("/api/variables", json={"expression": "x*y + z"})
    assert res.get_json()["variables"] == ["x", "y", "z"]


# la grafica 3d devuelve la malla
def test_plot_endpoint(client):
    res = client.post("/api/plot", json={"expression": "x^2 + y^2"})
    data = res.get_json()
    assert data["success"] is True and data["type"] == "3d"


# texto con codigo python no se ejecuta como valor del punto
def test_point_does_not_execute_code(client):
    res = client.post("/api/limit", json={"expression": "x", "point": {"x": "__import__('os')"}})
    assert res.status_code == 400


# schwarz responde con el indicador de igualdad
def test_schwarz_endpoint(client):
    res = client.post("/api/schwarz", json={"expression": "x^2*y", "variables": ["x", "y"]})
    data = res.get_json()
    assert data["success"] is True and data["equal"] is True


# plano tangente por la api
def test_tangent_plane_endpoint(client):
    res = client.post("/api/tangent_plane", json={"expression": "x^2 + y^2", "point": {"x": "1", "y": "2"}})
    assert res.get_json()["success"] is True
