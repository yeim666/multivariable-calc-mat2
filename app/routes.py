from flask import Blueprint, render_template, request, jsonify

# importamos la funcion que calcula el limite o loq sea
from app.calculator import multivariable_limit


# creamos el "blueprint" para ordenar todas las rutas relacionadas a nuestra app
main = Blueprint("main", __name__)



@main.route("/")
def index():

    # flask renderiza nuestro html :v
    return render_template("index.html")


# api de limites--
# esta ruta recibe las peticiones del js.
#
# /api/limit
#
# solo permitimos el método POST porque estamos enviando datos al servidor.
@main.route("/api/limit", methods=["POST"])
def limit():

    # obtenemos los datos del json enviados por el js
    data = request.get_json()


    # error handling: comprobamos que existan datos
    if not data:

        return jsonify({
            "success": False,
            "error": "No se recibieron datos."
        }), 400


    # extraemos la expresión matematica
    expression = data.get("expression")


    # extraemos el punto.
    point = data.get("point")


    # error handling: comprobamos que exista la expresion
    if not expression:

        return jsonify({
            "success": False,
            "error": "No se proporcionó una expresión."
        }), 400

    # error handling: comprobamos que exista el punto
    if not point:

        return jsonify({
            "success": False,
            "error": "No se proporcionó el punto."
        }), 400


    try:

        # llamamos a nuestra funcion del otro .py
        result = multivariable_limit(
            expression,
            point
        )


        # devolvemos el resultado como json y lo convertimos a string :v
        return jsonify({
            "success": True,
            "result": str(result)
        })


    # error handling: si no se logra resolver el limite
    except Exception:
        return jsonify({
            "success": False,
            "error": "No se pudo calcular el límite."
        }), 400
