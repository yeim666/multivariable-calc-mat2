from flask import Blueprint, render_template, request, jsonify

from app.mathcore import (
    OPERATIONS,
    run,
    parse_expression,
    latex_to_expr,
    get_variables,
    generate_plot_data,
    to_latex,
)


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


# respuesta de error uniforme para toda la api
def error_response(message, status=400):
    return jsonify({"success": False, "error": message}), status


# decide que parser usar segun lo que mande el frontend
def get_expr_from_request(data):

    if data.get("latex"):
        return latex_to_expr(data["latex"])

    elif data.get("expression"):
        return parse_expression(data["expression"])

    else:
        raise ValueError("No se proporcionó una expresión ni notación LaTeX.")


# ejecuta una funcion de la api con el manejo de errores comun:
# ValueError = problema de entrada (mensaje claro al usuario),
# cualquier otra excepcion = error interno (mensaje generico, detalle en consola)
def handle_api(action, label, fallback_message):

    data = request.get_json(silent=True)

    if not data:
        return error_response("No se recibieron datos.")

    try:
        return jsonify({"success": True, **action(data)})

    except ValueError as e:
        return error_response(str(e))

    except Exception as e:
        print(f"[{label}] error: {e}")
        return error_response(fallback_message)


# api de variables: /api/variables
@main.route("/api/variables", methods=["POST"])
def variables():

    def action(data):
        found = get_variables(get_expr_from_request(data))
        return {
            "variables": [str(v) for v in found],
            "variables_latex": [to_latex(v) for v in found],
        }

    return handle_api(action, "/api/variables", "No se pudo interpretar la expresión.")


# api de graficas: /api/plot
@main.route("/api/plot", methods=["POST"])
def plot():

    def action(data):
        expr = get_expr_from_request(data)

        # rango de graficado opcional, con valores por defecto razonables
        x_range = tuple(data.get("x_range", (-10, 10)))
        y_range = tuple(data.get("y_range", (-10, 10)))

        return generate_plot_data(
            expr,
            x_range=x_range,
            y_range=y_range,
            point=data.get("point"),
            overlay=data.get("overlay"),
        )

    return handle_api(action, "/api/plot", "No se pudo generar la gráfica.")


# endpoint generico de operaciones: /api/limit, /api/derivative, /api/gradient...
# cualquier operacion registrada en mathcore queda disponible aqui sin tocar este archivo
@main.route("/api/<operation>", methods=["POST"])
def operation_endpoint(operation):

    if operation not in OPERATIONS:
        return error_response(f"Operación desconocida: {operation}", 404)

    def action(data):
        return run(operation, get_expr_from_request(data), data)

    return handle_api(action, f"/api/{operation}", "No se pudo calcular el resultado.")
