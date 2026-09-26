// ====================================================
// elementos del html
// ====================================================

const operation = document.getElementById("operation");

const limitPanel = document.getElementById("limit-panel");
const derivativePanel = document.getElementById("derivative-panel");

const functionInput = document.getElementById("function");

const variablesFeedback = document.getElementById("variables-feedback");
const variablesFeedbackLabel = document.getElementById("variables-feedback-label");
const variablesMath = document.getElementById("variables-math");

const limitPointInputs = document.getElementById("limit-point-inputs");
const derivativePointInputs = document.getElementById("derivative-point-inputs");
const derivativeVariableSelect = document.getElementById("derivative-variable");

const calculateButton = document.getElementById("calculate");

const resultField = document.getElementById("result-field");
const resultPlaceholder = document.getElementById("result-placeholder");

// variables detectadas (nombres planos, usados como claves) y su version
// latex en paralelo (solo para mostrar), por nombre
let currentVariables = [];
let currentVariablesLatex = {};


// ====================================================
// cambio de operacion (limite / derivada)
// ====================================================

operation.addEventListener("change", () => {

    if (operation.value === "limit") {
        limitPanel.hidden = false;
        derivativePanel.hidden = true;
    } else {
        limitPanel.hidden = true;
        derivativePanel.hidden = false;
    }

    renderDynamicInputs(currentVariables);

});


// ====================================================
// deteccion dinamica de variables
// ====================================================

let debounceTimer = null;

functionInput.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(detectVariables, 400);
});


async function detectVariables() {

    const latex = functionInput.getValue("latex").trim();

    if (!latex) {
        currentVariables = [];
        currentVariablesLatex = {};
        setFeedback("", false);
        renderDynamicInputs([]);
        return;
    }

    try {
        console.log("LaTeX enviado:", JSON.stringify(latex));
        const response = await fetch("/api/variables", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ latex })
        });

        const data = await response.json();

        if (data.success) {

            currentVariables = data.variables;

            // armamos el mapa {nombre_plano: latex} para usarlo al renderizar
            // etiquetas en otras partes de la interfaz
            currentVariablesLatex = {};
            data.variables.forEach((name, i) => {
                currentVariablesLatex[name] = data.variables_latex[i];
            });

            if (currentVariables.length > 0) {
                // mostramos "Variables detectadas:" + los simbolos en notacion matematica real
                setFeedback("Variables detectadas:", false, currentVariables.map(v => currentVariablesLatex[v]).join(", "));
            } else {
                setFeedback("La expresión no tiene variables (es una constante).", false);
            }

            renderDynamicInputs(currentVariables);

        } else {

            currentVariables = [];
            currentVariablesLatex = {};
            setFeedback(data.error, true);
            renderDynamicInputs([]);

        }

    } catch (error) {
        console.error(error);
        setFeedback("No se pudo conectar con el servidor.", true);
    }

}


// actualiza el feedback de variables. si se pasa mathLatex, se muestra
// tambien el campo matematico de solo lectura con esa notacion
function setFeedback(text, isError, mathLatex) {

    if (!text) {
        variablesFeedback.hidden = true;
        return;
    }

    variablesFeedback.hidden = false;
    variablesFeedbackLabel.textContent = text;
    variablesFeedbackLabel.classList.toggle("error", isError);

    if (mathLatex) {
        variablesMath.hidden = false;
        variablesMath.value = mathLatex;
    } else {
        variablesMath.hidden = true;
    }

}


// crea una etiqueta <label> que muestra el simbolo de la variable en
// notacion matematica real (via un math-field de solo lectura), en vez
// de texto plano — asi se ve bien incluso con letras griegas o subindices
function createVariableLabel(forId, variableName) {

    const label = document.createElement("label");
    label.setAttribute("for", forId);

    const symbol = document.createElement("math-field");
    symbol.className = "inline-math";
    symbol.setAttribute("read-only", "");
    symbol.tabIndex = -1;
    symbol.value = currentVariablesLatex[variableName] || variableName;

    label.appendChild(symbol);
    label.appendChild(document.createTextNode(" →"));

    return label;
}


function renderDynamicInputs(variables) {

    // -------- panel de limites --------
    limitPointInputs.innerHTML = "";

    if (variables.length === 0) {
        limitPointInputs.innerHTML =
            '<p class="empty-hint">Escribe una función para continuar.</p>';
    } else {

        variables.forEach((variable) => {

            const group = document.createElement("div");
            group.className = "input-group";

            const inputId = `point-${variable}`;
            group.appendChild(createVariableLabel(inputId, variable));

            const input = document.createElement("input");
            input.type = "number";
            input.id = inputId;
            input.className = "point-input";
            input.dataset.variable = variable;
            input.placeholder = "0";
            input.step = "any";

            group.appendChild(input);
            limitPointInputs.appendChild(group);

        });
    }

    // -------- panel de derivadas --------
    derivativePointInputs.innerHTML = "";
    derivativeVariableSelect.innerHTML = "";

    if (variables.length === 0) {

        const placeholder = document.createElement("option");
        placeholder.value = "";
        placeholder.textContent = "Escribe una función primero";
        derivativeVariableSelect.appendChild(placeholder);

        derivativePointInputs.innerHTML =
            '<p class="empty-hint">Escribe una función para continuar.</p>';

    } else {

        variables.forEach((variable) => {

            // nota: un <select> nativo no puede renderizar math-field dentro
            // de sus <option>, asi que aqui se queda como texto plano
            const option = document.createElement("option");
            option.value = variable;
            option.textContent = variable;
            derivativeVariableSelect.appendChild(option);

            const group = document.createElement("div");
            group.className = "input-group";

            const inputId = `deriv-point-${variable}`;
            group.appendChild(createVariableLabel(inputId, variable));

            const input = document.createElement("input");
            input.type = "number";
            input.id = inputId;
            input.className = "point-input";
            input.dataset.variable = variable;
            input.placeholder = "opcional";
            input.step = "any";

            group.appendChild(input);
            derivativePointInputs.appendChild(group);

        });
    }

}


function readPoint(container, requireAll) {

    const inputs = container.querySelectorAll(".point-input");
    const point = {};

    for (const input of inputs) {

        const value = input.value.trim();

        if (value === "") {
            if (requireAll) return null;
            continue;
        }

        point[input.dataset.variable] = value;
    }

    return point;
}


// ====================================================
// mostrar el resultado (exito: math-field. error: texto plano)
// ====================================================

function showResult(data) {

    if (data.success) {
        resultPlaceholder.hidden = true;
        resultField.hidden = false;
        resultField.value = data.result_latex;
    } else {
        resultField.hidden = true;
        resultPlaceholder.hidden = false;
        resultPlaceholder.textContent = data.error;
        resultPlaceholder.classList.add("error");
    }

}


function showResultLoading() {
    resultField.hidden = true;
    resultPlaceholder.hidden = false;
    resultPlaceholder.classList.remove("error");
    resultPlaceholder.textContent = "Calculando...";
}


// ====================================================
// calcular
// ====================================================

calculateButton.addEventListener("click", async () => {

    const latex = functionInput.getValue("latex").trim();

    if (!latex) {
        showResult({ success: false, error: "Escribe una función." });
        return;
    }

    if (currentVariables.length === 0) {
        showResult({ success: false, error: "No se detectaron variables válidas. Revisa la función." });
        return;
    }

    calculateButton.disabled = true;
    showResultLoading();

    try {

        let response;

        if (operation.value === "limit") {

            const point = readPoint(limitPointInputs, true);

            if (point === null) {
                showResult({ success: false, error: "Completa el punto para todas las variables." });
                return;
            }

            response = await fetch("/api/limit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ latex, point })
            });

        } else {

            const variable = derivativeVariableSelect.value;

            if (!variable) {
                showResult({ success: false, error: "Selecciona respecto a qué variable derivar." });
                return;
            }

            const point = readPoint(derivativePointInputs, false);
            const hasPoint = Object.keys(point).length > 0;

            response = await fetch("/api/derivative", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    latex,
                    variable,
                    point: hasPoint ? point : null
                })
            });

        }

        const data = await response.json();
        showResult(data);

        // graficamos la funcion actual, tanto si el calculo tuvo exito como si no
        renderPlot();

    } catch (error) {
        console.error(error);
        showResult({ success: false, error: "Error al comunicarse con el servidor." });

    } finally {
        calculateButton.disabled = false;
    }

});

// ====================================================
// grafica (plotly)
// ====================================================

const plotContainer = document.getElementById("plot-container");
const canvasPlaceholder = document.querySelector(".canvas-placeholder");


// pide los datos de la grafica al backend y la dibuja con plotly.
// se llama despues de cada calculo, exitoso o no, usando la funcion actual
async function renderPlot() {

    const latex = functionInput.getValue("latex").trim();

    // solo tiene sentido graficar con 1 o 2 variables (linea o superficie)
    if (!latex || currentVariables.length === 0 || currentVariables.length > 2) {
        showPlotMessage("La gráfica aparecerá aquí (solo para funciones de 1 o 2 variables)");
        return;
    }

    try {

        const response = await fetch("/api/plot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ latex })
        });

        const data = await response.json();

        if (!data.success) {
            showPlotMessage(data.error);
            return;
        }

        drawPlot(data);

    } catch (error) {
        console.error(error);
        showPlotMessage("Error al generar la gráfica.");
    }

}


// muestra un mensaje de texto en vez de la grafica (placeholder o error)
function showPlotMessage(text) {

    // si plotly ya dibujo algo antes, lo limpiamos
    if (plotContainer.dataset.hasPlot === "true") {
        Plotly.purge(plotContainer);
        plotContainer.dataset.hasPlot = "false";
    }

    plotContainer.innerHTML = `<span class="canvas-placeholder">${text}</span>`;

}


// dibuja la grafica con plotly: linea 2d o superficie 3d, segun el tipo
function drawPlot(data) {

    plotContainer.innerHTML = "";
    plotContainer.dataset.hasPlot = "true";

    if (data.type === "2d") {

        Plotly.newPlot(plotContainer, [{
            x: data.x,
            y: data.y,
            type: "scatter",
            mode: "lines",
            line: { color: "#e48aae", width: 2.5 } // sakura
        }], plotLayout(), plotConfig());

    } else if (data.type === "3d") {

        Plotly.newPlot(plotContainer, [{
            x: data.x,
            y: data.y,
            z: data.z,
            type: "surface",
            colorscale: [
                [0, "#fbf3ef"],
                [0.5, "#f0a8c2"],
                [1, "#c9718b"]
            ],
            showscale: false
        }], plotLayout(data.variable_names), plotConfig());

    }

}


// layout compartido: combina con la paleta clara actual de la interfaz
function plotLayout(variableNames) {

    const base = {
        paper_bgcolor: "#ffffff",
        plot_bgcolor: "#ffffff",
        font: { color: "#8c7377", family: "Inter, sans-serif" },
        margin: { l: 30, r: 20, t: 20, b: 30 },
    };

    if (variableNames) {
        return {
            ...base,
            scene: {
                xaxis: { title: variableNames[0], color: "#8c7377", gridcolor: "#f6d9e4" },
                yaxis: { title: variableNames[1], color: "#8c7377", gridcolor: "#f6d9e4" },
                zaxis: { color: "#8c7377", gridcolor: "#f6d9e4" },
            },
        };
    }
    return {
        ...base,
        xaxis: { gridcolor: "#f6d9e4", zerolinecolor: "#f6d9e4" },
        yaxis: { gridcolor: "#f6d9e4", zerolinecolor: "#f6d9e4" },
    };

}

// configuracion de plotly: quitamos la barra de herramientas flotante
// para que se vea mas integrado y menos "libreria generica"
function plotConfig() {
    return {
        displayModeBar: false,
        responsive: true,
    };
}
