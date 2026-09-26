from flask import Blueprint, render_template, request, jsonify

from app.mathcore import (
    parse_expression,
    latex_to_expr,
    multivariable_limit,
    partial_derivative,
    get_variables,
    generate_plot_data,
    to_latex,
)


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


# decide que parser usar segun lo que mande el frontend.
def get_expr_from_request(data):

    if data.get("latex"):
        return latex_to_expr(data["latex"])

    elif data.get("expression"):
        return parse_expression(data["expression"])

    else:
        raise ValueError("No se proporcionó una expresión ni notación LaTeX.")


# api de variables
#
# /api/variables
@main.route("/api/variables", methods=["POST"])
def variables():

    data = request.get_json()

    if not data:
        return jsonify({ 
            "success": False,
            "error": "No se recibieron datos."
        }), 400

    try:
        expr = get_expr_from_request(data)
        vars_found = get_variables(expr)

        return jsonify({
            "success": True,
            "variables": [str(v) for v in vars_found],
            "variables_latex": [to_latex(v) for v in vars_found],
        })

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"[/api/variables] error: {e}")
        return jsonify({
            "success": False,
            "error": "No se pudo interpretar la expresión."
        }), 400


# api de limites
#
# /api/limit
@main.route("/api/limit", methods=["POST"])
def limit():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No se recibieron datos."
        }), 400

    point = data.get("point")

    if not point:
        return jsonify({
            "success": False,
            "error": "No se proporcionó el punto."
        }), 400

    try:
        expr = get_expr_from_request(data)
        result = multivariable_limit(expr, point)

        return jsonify({
            "success": True,
            "result": str(result),
            "result_latex": to_latex(result),
        })

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"[/api/limit] error: {e}")
        return jsonify({
            "success": False,
            "error": "No se pudo calcular el límite."
        }), 400


# api de derivadas parciales
#
# /api/derivative
@main.route("/api/derivative", methods=["POST"])
def derivative():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No se recibieron datos."
        }), 400

    variable = data.get("variable")
    point = data.get("point")  # opcional

    if not variable:
        return jsonify({
            "success": False,
            "error": "No se proporcionó la variable respecto a la cual derivar."
        }), 400

    try:
        expr = get_expr_from_request(data)
        result = partial_derivative(expr, variable, point)

        return jsonify({
            "success": True,
            "result": str(result),
            "result_latex": to_latex(result),
        })

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"[/api/derivative] error: {e}")
        return jsonify({
            "success": False,
            "error": "No se pudo calcular la derivada."
        }), 400


# api de graficas
#
# /api/plot
@main.route("/api/plot", methods=["POST"])
def plot():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No se recibieron datos."
        }), 400

    try:
        expr = get_expr_from_request(data)

        # rango de graficado opcional, con valores por defecto razonables
        x_range = tuple(data.get("x_range", (-10, 10)))
        y_range = tuple(data.get("y_range", (-10, 10)))

        plot_data = generate_plot_data(expr, x_range=x_range, y_range=y_range)

        return jsonify({
            "success": True,
            **plot_data
        })

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        print(f"[/api/plot] error: {e}")
        return jsonify({
            "success": False,
            "error": "No se pudo generar la gráfica."
        }), 400
