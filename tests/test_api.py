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


# e y pi no se detectan como variables
def test_constants_are_not_variables(client):
    res = client.post("/api/variables", json={"latex": r"e^{x}+\pi y"})
    data = res.get_json()
    assert data["success"] is True
    assert data["variables"] == ["x", "y"]


def test_domain_endpoint(client):
    res = client.post("/api/domain", json={"expression": "sqrt(x)+log(y)"})
    assert res.get_json()["success"] is True


def test_hessian_endpoint(client):
    res = client.post("/api/hessian", json={"expression": "x^2 + y^2"})
    data = res.get_json()
    assert data["success"] is True
    assert any(step.get("title_latex") == "f_{xx}" for step in data["procedure"])


def test_directional_endpoint(client):
    res = client.post("/api/directional", json={
        "expression": "x^2 + y^2",
        "direction": {"x": "1", "y": "0"},
        "point": {"x": "1", "y": "0"},
    })
    data = res.get_json()
    assert data["success"] is True
    assert data["result"] == "2"


def test_critical_endpoint(client):
    res = client.post("/api/critical", json={"expression": "x^2 + y^2"})
    assert res.get_json()["success"] is True


def test_lagrange_endpoint(client):
    res = client.post("/api/lagrange", json={"expression": "x*y", "constraint": "x+y-1"})
    assert res.get_json()["success"] is True


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


def test_double_integral_endpoint(client):
    res = client.post("/api/double_integral", json={
        "expression": "x+y",
        "bounds": [{"lower": "0", "upper": "1"}, {"lower": "0", "upper": "1"}],
    })
    assert res.get_json()["result"] == "1"


def test_polar_integral_applies_jacobian(client):
    res = client.post("/api/double_polar", json={
        "expression": "x^2+y^2",
        "bounds": [{"lower": "0", "upper": "1"}, {"lower": "0", "upper": "2*pi"}],
    })
    assert res.get_json()["result"] == "pi/2"


def test_spherical_integral_applies_jacobian(client):
    res = client.post("/api/triple_spherical", json={
        "expression": "1",
        "bounds": [{"lower": "0", "upper": "1"}, {"lower": "0", "upper": "pi"}, {"lower": "0", "upper": "2*pi"}],
    })
    assert res.get_json()["result"] == "4*pi/3"


def test_divergence_and_curl_endpoints(client):
    divergence = client.post("/api/divergence", json={"components": ["x", "y"]}).get_json()
    curl = client.post("/api/curl", json={"components": ["-y", "x"]}).get_json()
    assert divergence["result"] == "2"
    assert curl["result"] == "2"


def test_line_integral_and_green_endpoints(client):
    line = client.post("/api/line_integral", json={
        "expression": "1", "kind": "first", "x_curve": "cos(t)", "y_curve": "sin(t)",
        "lower": "0", "upper": "2*pi",
    }).get_json()
    green = client.post("/api/green", json={
        "components": ["-y", "x"],
        "bounds": [{"lower": "-1", "upper": "1"}, {"lower": "-1", "upper": "1"}],
    }).get_json()
    assert line["result"] == "2*pi"
    assert green["result"] == "8"
    assert green["integration_order"] == "dxdy"


def test_green_integrates_triangular_regions_in_both_orders(client):
    components = ["-y", "x"]
    x_inner = client.post("/api/green", json={
        "components": components,
        "integration_order": "dxdy",
        "bounds": [{"lower": "0", "upper": "y"}, {"lower": "0", "upper": "1"}],
    }).get_json()
    y_inner = client.post("/api/green", json={
        "components": components,
        "integration_order": "dydx",
        "bounds": [{"lower": "0", "upper": "x"}, {"lower": "0", "upper": "1"}],
    }).get_json()
    assert x_inner["result"] == "1"
    assert y_inner["result"] == "1"


def test_green_rejects_invalid_order_and_nonplanar_fields(client):
    invalid_order = client.post("/api/green", json={
        "components": ["-y", "x"], "integration_order": "dzdy",
        "bounds": [{"lower": "0", "upper": "1"}, {"lower": "0", "upper": "1"}],
    })
    nonplanar = client.post("/api/green", json={
        "components": ["-y+z", "x"],
        "bounds": [{"lower": "0", "upper": "1"}, {"lower": "0", "upper": "1"}],
    })
    assert invalid_order.status_code == 400
    assert nonplanar.status_code == 400


def test_second_kind_line_integral_does_not_require_scalar_function(client):
    data = client.post("/api/line_integral", json={
        "kind": "second",
        "components": ["-y", "x"],
        "x_curve": "cos(t)",
        "y_curve": "sin(t)",
        "lower": "0",
        "upper": "2*pi",
    }).get_json()
    assert data["success"] is True
    assert data["result"] == "2*pi"


def test_first_kind_line_integral_requires_scalar_function(client):
    response = client.post("/api/line_integral", json={
        "kind": "first",
        "x_curve": "t",
        "y_curve": "t",
        "lower": "0",
        "upper": "1",
    })
    assert response.status_code == 400
    assert response.get_json()["error"] == "La integral de primer tipo requiere una función escalar."


def test_surface_area_and_mass_properties(client):
    bounds = [{"lower": "0", "upper": "1"}, {"lower": "0", "upper": "1"}]
    area = client.post("/api/surface_area", json={"expression": "0", "bounds": bounds}).get_json()
    mass = client.post("/api/mass_properties", json={"expression": "1", "bounds": bounds}).get_json()
    assert area["result"] == "1"
    assert mass["mass"] == "1"
    assert mass["center_of_mass"] == {"x": "1/2", "y": "1/2"}
    assert mass["moments_of_inertia"]["polar"] == "2/3"


def test_vector_curve_operations(client):
    payload = {"components": ["t^2", "sin(t)"], "parameter": "1", "lower": "0"}
    derivative = client.post("/api/vector_curve", json={**payload, "mode": "derivative"}).get_json()
    integral = client.post("/api/vector_curve", json={**payload, "mode": "integral"}).get_json()
    limit = client.post("/api/vector_curve", json={**payload, "mode": "limit"}).get_json()
    assert derivative["result"] == "Matrix([[2], [cos(1)]])"
    assert integral["result"] == "Matrix([[1/3], [1 - cos(1)]])"
    assert limit["result"] == "Matrix([[1], [sin(1)]])"


def test_cartesian_and_cylindrical_triple_integrals(client):
    cartesian = client.post("/api/triple_integral", json={
        "expression": "1",
        "bounds": [{"lower": "0", "upper": "1"}] * 3,
    }).get_json()
    cylindrical = client.post("/api/triple_cylindrical", json={
        "expression": "1",
        "bounds": [
            {"lower": "0", "upper": "1"},
            {"lower": "0", "upper": "2*pi"},
            {"lower": "0", "upper": "1"},
        ],
    }).get_json()
    assert cartesian["result"] == "1"
    assert cylindrical["result"] == "pi"


def test_conservative_field_returns_potential(client):
    data = client.post("/api/conservative", json={"components": ["2*x", "2*y"]}).get_json()
    assert data["success"] is True
    assert data["conservative"] is True
    assert data["potential_latex"] == "x^{2} + y^{2}"
