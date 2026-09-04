// elementos del html

// selector donde el usuario elige la operacion a realizar
const operation = document.getElementById("operation");


// panel que contiene todos los elementos relacionados a limites
const limitPanel = document.getElementById("limit-panel");


// panel que contiene todos los elemetnos relacionados a derivadas parciales
const derivativePanel = document.getElementById("derivative-panel");


// boton d calcular
const calculateButton = document.getElementById("calculate");


// input de la expresion
const functionInput = document.getElementById("function");


// input de la coordenada del punto del limite
const pointX = document.getElementById("point-x");
const pointY = document.getElementById("point-y");


// resultado para el html
const result = document.getElementById("result");


// comprobamos la operacion que escoge el usuario
operation.addEventListener("change", () => {


  // si selecciona limite: mostramos el panel de limites y ocultamos el de derivadas
    if (operation.value === "limit") {
        limitPanel.hidden = false;

        derivativePanel.hidden = true;

    }


    // lo mismo pero al reves
    else if (operation.value === "derivative"){
        limitPanel.hidden = true;

        derivativePanel.hidden = false;
    }

});


// calcular limite
// esperamos a que el usuario 
calculateButton.addEventListener("click", async () => {
    // obtenemos el texto del input, con trim elminamos los espacios innecesarios
    const expression = functionInput.value.trim();
    // obtenemos el punto
    const x = pointX.value;
    const y = pointY.value;


    // comprobamos que no hayan campos vacios
    if (!expression || x === "" || y === "") {

        // mensaje para el usuario jeje
        result.textContent = "Completa todos los campos.";

        return;
    }


    // nomas muestra un mensaje mientras carga
    result.textContent = "Calculando...";

    // peticion al servidor
    try {

        // estamos haciendo una peticion POST a /api/limit. fetch permite comunicarnos con nuestro server flask
        const response = await fetch("/api/limit", {

            // indicamos el metodo HTTP.
            method: "POST",

            // indicamos que los datos que estamos enviando tienen formato json.
            headers: {
                "Content-Type": "application/json"
            },


            // convertimos nuestro objeto js en json para enviarlo al servidor.
            body: JSON.stringify({

                // enviamos la funcion
                expression: expression,

                // enviamos el punto
                point: {
                    x: x,
                    y: y
                }
            })

        });


        // convertimos la respuesta de json a un objeto de js
        const data = await response.json();


        // mostrar el resultado

        // si todo funca como deberia
        if (data.success) {

            // mostramos el resultado
            result.textContent = data.result;

        }

        // error handling
        else {

            // mostramos el mensaje de error
            result.textContent = data.error;
        }


    }

    // error handling: si no nos comunicamos con flask
    catch (error) {

        // mostramos el error en la consola
        console.error(error);
        // mensaje al usuario
        result.textContent =
            "Error al comunicarse con el servidor.";

    }

});
