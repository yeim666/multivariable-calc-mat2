// ====================================================
// elementos del html
// ====================================================

const operationSelect = document.getElementById("operation");
const operationFields = document.getElementById("operation-fields");

const functionInput = document.getElementById("function");

const variablesFeedback = document.getElementById("variables-feedback");
const variablesFeedbackLabel = document.getElementById("variables-feedback-label");
const variablesMath = document.getElementById("variables-math");

const calculateButton = document.getElementById("calculate");

const resultField = document.getElementById("result-field");
const resultPlaceholder = document.getElementById("result-placeholder");
const resultNote = document.getElementById("result-note");

// variables detectadas (nombres planos, usados como claves) y su version
// latex en paralelo (solo para mostrar), por nombre
let currentVariables = [];
let currentVariablesLatex = {};


// ====================================================
// selector de operaciones (se llena desde operations.js)
// ====================================================

function buildOperationSelect() {

    // agrupamos por unidad para que la lista siga ordenada al crecer
    const groups = {};

    for (const [name, op] of Object.entries(OPERATIONS)) {

        if (!groups[op.unit]) {
            const group = document.createElement("optgroup");
            group.label = op.unit;
            groups[op.unit] = group;
            operationSelect.appendChild(group);
        }

        const option = document.createElement("option");
        option.value = name;
        option.textContent = op.label;
        groups[op.unit].appendChild(option);
    }
}

operationSelect.addEventListener("change", () => {
    clearResult();
    renderFields();
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
        renderFields();
        return;
    }

    try {
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

            renderFields();

        } else {

            currentVariables = [];
            currentVariablesLatex = {};
            setFeedback(data.error, true);
            renderFields();

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


// ====================================================
// campos de cada operacion
//
// cada tipo de campo sabe dibujarse (render) y leerse (read).
// read devuelve { payload: {...} } con lo que se envia al backend,
// o { error: "mensaje" } si falta algo
// ====================================================

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


// <select> con las variables detectadas. un <select> nativo no puede
// mostrar math-field dentro de sus <option>, asi que va en texto plano
function createVariableSelect(id) {

    const select = document.createElement("select");
    select.id = id;

    currentVariables.forEach((variable) => {
        const option = document.createElement("option");
        option.value = variable;
        option.textContent = variable;
        select.appendChild(option);
    });

    return select;
}


const FIELD_TYPES = {

    // un input numerico por variable. el id es compartido entre operaciones
    // para que el punto escrito se conserve al cambiar de operacion
    point: {

        render(field, container) {

            const grid = document.createElement("div");
            grid.className = "point-inputs";

            currentVariables.forEach((variable) => {

                const group = document.createElement("div");
                group.className = "input-group";

                const inputId = `point-${variable}`;
                group.appendChild(createVariableLabel(inputId, variable));

                const input = document.createElement("input");
                input.type = "number";
                input.id = inputId;
                input.className = "point-input";
                input.dataset.variable = variable;
                input.placeholder = field.required ? "0" : "opcional";
                input.step = "any";

                group.appendChild(input);
                grid.appendChild(group);
            });

            container.appendChild(grid);
        },

        read(field, container) {

            const point = {};

            for (const input of container.querySelectorAll(".point-input")) {

                const value = input.value.trim();

                if (value === "") {
                    if (field.required) {
                        return { error: "Completa el punto para todas las variables." };
                    }
                    continue;
                }

                point[input.dataset.variable] = value;
            }

            // si el punto es opcional y esta vacio, no se envia
            if (Object.keys(point).length === 0) {
                return { payload: {} };
            }

            return { payload: { point } };
        },
    },

    // una sola variable
    variable: {

        render(field, container) {
            container.appendChild(createVariableSelect(`field-${field.key}`));
        },

        read(field, container) {

            const value = container.querySelector("select").value;

            if (!value) {
                return { error: "Selecciona una variable." };
            }

            return { payload: { [field.key]: value } };
        },
    },

    // texto libre con variables separadas por coma o espacio, ej. "x, y, x"
    variableList: {

        render(field, container) {

            const input = document.createElement("input");
            input.type = "text";
            input.id = `field-${field.key}`;
            input.placeholder = field.placeholder || "";
            input.autocomplete = "off";
            container.appendChild(input);
        },

        read(field, container) {

            const names = container.querySelector("input").value
                .split(/[\s,]+/)
                .filter(Boolean);

            if (names.length === 0) {
                return { error: "Escribe las variables a derivar, por ejemplo: x, y." };
            }

            const unknown = names.find((name) => !currentVariables.includes(name));

            if (unknown) {
                return { error: `La variable '${unknown}' no aparece en la función.` };
            }

            return { payload: { [field.key]: names } };
        },
    },

    // dos listas desplegables, para comparar o relacionar un par de variables
    variablePair: {

        render(field, container) {

            const row = document.createElement("div");
            row.className = "point-inputs";

            const first = createVariableSelect(`field-${field.key}-0`);
            const second = createVariableSelect(`field-${field.key}-1`);

            // por defecto proponemos dos variables distintas
            if (currentVariables.length > 1) {
                second.value = currentVariables[1];
            }

            row.appendChild(first);
            row.appendChild(second);
            container.appendChild(row);
        },

        read(field, container) {

            const [first, second] = container.querySelectorAll("select");

            if (!first.value || !second.value || first.value === second.value) {
                return { error: "Elige dos variables distintas." };
            }

            return { payload: { [field.key]: [first.value, second.value] } };
        },
    },

};


// memoria de lo escrito en los campos, por id. se actualiza antes de cada
// redibujado y nunca se borra, asi un valor sobrevive aunque pasemos por una
// operacion que no tiene ese campo (ej. punto -> schwarz -> plano tangente)
const fieldMemory = {};


// lee los valores actuales de los campos visibles, por id
function snapshotFieldValues() {

    const saved = {};

    operationFields.querySelectorAll("input[id], select[id]").forEach((el) => {
        saved[el.id] = el.value;
    });

    return saved;
}


// vuelve a poner en los campos recien dibujados lo que la memoria recuerda
function restoreFieldValues() {

    for (const [id, value] of Object.entries(fieldMemory)) {

        const el = document.getElementById(id);

        if (!el) continue;

        // en un <select> solo restauramos si la opcion sigue existiendo
        if (el.tagName === "SELECT" && ![...el.options].some((o) => o.value === value)) {
            continue;
        }

        el.value = value;
    }
}


// dibuja los campos de la operacion elegida segun las variables detectadas
function renderFields() {

    Object.assign(fieldMemory, snapshotFieldValues());
    const op = OPERATIONS[operationSelect.value];

    operationFields.innerHTML = "";

    if (currentVariables.length === 0) {
        operationFields.innerHTML =
            '<p class="empty-hint">Escribe una función para continuar.</p>';
        return;
    }

    op.fields.forEach((field, index) => {

        const block = document.createElement("section");
        block.className = "field-block";
        block.dataset.fieldIndex = index;

        const title = document.createElement("div");
        title.className = "section-title";

        const heading = document.createElement("h2");
        heading.textContent = field.title;
        title.appendChild(heading);

        if (field.hint) {
            const hint = document.createElement("span");
            hint.textContent = field.hint;
            title.appendChild(hint);
        }

        block.appendChild(title);
        FIELD_TYPES[field.type].render(field, block);
        operationFields.appendChild(block);
    });

    restoreFieldValues();
}


// lee todos los campos de la operacion y arma lo que se envia al backend.
// devuelve { payload } o { error }
function collectPayload(op) {

    const payload = {};
    const blocks = operationFields.querySelectorAll(".field-block");

    for (let i = 0; i < op.fields.length; i++) {

        const field = op.fields[i];
        const result = FIELD_TYPES[field.type].read(field, blocks[i]);

        if (result.error) {
            return { error: result.error };
        }

        Object.assign(payload, result.payload);
    }

    return { payload };
}


// ====================================================
// mostrar el resultado (exito: math-field. error: texto plano)
// ====================================================

function showResult(data, op) {

    if (data.success) {
        resultPlaceholder.hidden = true;
        resultField.hidden = false;
        resultField.value = data.result_latex;

        // nota opcional de la operacion (ej. "se cumple el teorema")
        const note = op && op.note ? op.note(data) : "";
        resultNote.textContent = note;
        resultNote.hidden = !note;
    } else {
        resultField.hidden = true;
        resultNote.hidden = true;
        resultPlaceholder.hidden = false;
        resultPlaceholder.textContent = data.error;
        resultPlaceholder.classList.add("error");
    }

}


function showResultLoading() {
    resultField.hidden = true;
    resultNote.hidden = true;
    resultPlaceholder.hidden = false;
    resultPlaceholder.classList.remove("error");
    resultPlaceholder.textContent = "Calculando...";
}


// vuelve el panel de resultado a su estado inicial
function clearResult() {
    resultField.hidden = true;
    resultNote.hidden = true;
    resultPlaceholder.hidden = false;
    resultPlaceholder.classList.remove("error");
    resultPlaceholder.textContent = "El resultado aparecerá aquí";
}


// ====================================================
// calcular
// ====================================================

calculateButton.addEventListener("click", async () => {

    const latex = functionInput.getValue("latex").trim();
    const op = OPERATIONS[operationSelect.value];

    if (!latex) {
        showResult({ success: false, error: "Escribe una función." });
        return;
    }

    if (currentVariables.length === 0) {
        showResult({ success: false, error: "No se detectaron variables válidas. Revisa la función." });
        return;
    }

    // validamos los campos antes de bloquear el boton
    const collected = collectPayload(op);

    if (collected.error) {
        showResult({ success: false, error: collected.error });
        return;
    }

    calculateButton.disabled = true;
    showResultLoading();

    try {

        const response = await fetch(op.endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ latex, ...collected.payload })
        });

        const data = await response.json();
        showResult(data, op);

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

    const message = document.createElement("span");
    message.className = "canvas-placeholder";
    message.textContent = text;

    plotContainer.innerHTML = "";
    plotContainer.appendChild(message);

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


// ====================================================
// arranque
// ====================================================

buildOperationSelect();
renderFields();
