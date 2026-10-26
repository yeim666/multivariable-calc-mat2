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


# una funcion con dominio restringido no rompe el json (nan -> null)
def test_plot_domain_holes_are_valid_json(client):
    res = client.post("/api/plot", json={"expression": "log(x) + y"})
    data = res.get_json()
    assert data["success"] is True
    assert any(v is None for row in data["z"] for v in row)


# el punto de evaluacion llega como marcador sobre la superficie
def test_plot_marker(client):
    res = client.post("/api/plot", json={"expression": "x^2 + y^2", "point": {"x": "1", "y": "1/2"}})
    marker = res.get_json()["marker"]
    assert marker == {"x": 1.0, "y": 0.5, "z": 1.25}


# overlay del plano tangente: misma malla que la superficie
def test_plot_tangent_plane_overlay(client):
    res = client.post("/api/plot", json={
        "expression": "x^2 + y^2", "point": {"x": "1", "y": "2"}, "overlay": "tangent_plane"})
    data = res.get_json()
    assert len(data["plane_z"]) == len(data["z"])


# overlay del gradiente: flecha con dos puntos
def test_plot_gradient_overlay(client):
    res = client.post("/api/plot", json={
        "expression": "x^2 + y^2", "point": {"x": "1", "y": "2"}, "overlay": "gradient"})
    arrow = res.get_json()["gradient_arrow"]
    assert len(arrow["x"]) == 2 and arrow["z"][1] > arrow["z"][0]


# un punto invalido no tumba la grafica base
def test_plot_bad_point_still_plots(client):
    res = client.post("/api/plot", json={"expression": "x^2 + y^2", "point": {"x": "hola", "y": "1"}, "overlay": "tangent_plane"})
    data = res.get_json()
    assert data["success"] is True and "marker" not in data


# el rango personalizado cambia la malla devuelta
def test_plot_custom_range(client):
    res = client.post("/api/plot", json={"expression": "x^2 + y^2", "x_range": [0, 2], "y_range": [-1, 1]})
    data = res.get_json()
    assert data["x"][0] == 0 and data["x"][-1] == 2
    assert data["y"][0] == -1 and data["y"][-1] == 1


# un rango al reves o con texto se rechaza con mensaje claro
def test_plot_invalid_range(client):
    for bad in ([5, 1], [1, 1], ["a", 2], [0]):
        res = client.post("/api/plot", json={"expression": "x^2", "x_range": bad})
        assert res.status_code == 400, bad
        assert "rango" in res.get_json()["error"].lower()
