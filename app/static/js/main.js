// ====================================================
// elementos del html
// ====================================================

const unitTabs = document.getElementById("unit-tabs");
const operationChips = document.getElementById("operation-chips");
const operationFields = document.getElementById("operation-fields");

const functionInput = document.getElementById("function");

const variablesFeedback = document.getElementById("variables-feedback");
const variablesFeedbackLabel = document.getElementById("variables-feedback-label");
const variablesMath = document.getElementById("variables-math");

const calculateButton = document.getElementById("calculate");

const resultField = document.getElementById("result-field");
const resultPlaceholder = document.getElementById("result-placeholder");
const resultNote = document.getElementById("result-note");

const copyLatexButton = document.getElementById("copy-latex");
const copyTextButton = document.getElementById("copy-text");

// controles de la grafica
const plotToolbar = document.getElementById("plot-toolbar");
const xMinInput = document.getElementById("x-min");
const xMaxInput = document.getElementById("x-max");
const yMinInput = document.getElementById("y-min");
const yMaxInput = document.getElementById("y-max");
const xRangeLabel = document.getElementById("x-range-label");
const yRangeLabel = document.getElementById("y-range-label");
const yRangeGroup = document.getElementById("y-range-group");
const viewToggle = document.getElementById("view-toggle");
const downloadButton = document.getElementById("download-plot");

// variables detectadas (nombres planos, usados como claves) y su version
// latex en paralelo (solo para mostrar), por nombre
let currentVariables = [];
let currentVariablesLatex = {};

// ultimo resultado exitoso, para los botones de copiar
let lastResult = null;

// el boton Calcular se bloquea mientras se calcula o si la operacion
// elegida no aplica a la funcion escrita (ver requires en operations.js)
let calculating = false;
let blockedByRequirement = false;

function refreshCalculateButton() {
    calculateButton.disabled = calculating || blockedByRequirement;
}


// ====================================================
// selector de operaciones: pestañas por unidad + chips por grupo
// (se genera desde operations.js)
// ====================================================

// operacion y unidad elegidas. por defecto, la primera del catalogo
let currentOperation = Object.keys(OPERATIONS)[0];
let currentUnit = OPERATIONS[currentOperation].unit;


// unidades que existen en el catalogo, en orden de aparicion
function listUnits() {
    return [...new Set(Object.values(OPERATIONS).map((op) => op.unit))];
}


// dibuja las pestañas de unidad. con una sola unidad no hacen falta
function renderUnitTabs() {

    const units = listUnits();

    unitTabs.innerHTML = "";
    unitTabs.hidden = units.length < 2;

    units.forEach((unit) => {

        const tab = document.createElement("button");
        tab.type = "button";
        tab.className = "unit-tab";
        tab.textContent = unit;
        tab.setAttribute("role", "tab");
        tab.setAttribute("aria-selected", String(unit === currentUnit));

        tab.addEventListener("click", () => {

            currentUnit = unit;
            renderUnitTabs();
            renderChips();

            // si la operacion actual no es de esta unidad, pasamos a la primera de ella
            if (OPERATIONS[currentOperation].unit !== unit) {
                const first = Object.keys(OPERATIONS).find((name) => OPERATIONS[name].unit === unit);
                setOperation(first);
            }
        });

        unitTabs.appendChild(tab);
    });
}


// dibuja los chips de la unidad actual, agrupados por tema
function renderChips() {

    operationChips.innerHTML = "";

    const groups = {};

    for (const [name, op] of Object.entries(OPERATIONS)) {

        if (op.unit !== currentUnit) continue;

        if (!groups[op.group]) {

            const wrapper = document.createElement("div");
            wrapper.className = "chip-group";

            const title = document.createElement("p");
            title.className = "chip-group-title";
            title.textContent = op.group;

            const chips = document.createElement("div");
            chips.className = "chips";

            wrapper.appendChild(title);
            wrapper.appendChild(chips);
            operationChips.appendChild(wrapper);

            groups[op.group] = chips;
        }

        const chip = document.createElement("button");
        chip.type = "button";
        chip.className = "chip";
        chip.dataset.op = name;
        chip.textContent = op.label;

        chip.addEventListener("click", () => setOperation(name));

        groups[op.group].appendChild(chip);
    }

    refreshChips();
}


// marca la operacion activa y atenua las que no aplican a la funcion
// actual (con el motivo como tooltip). siguen siendo elegibles: al elegirlas,
// el panel explica por que no se pueden calcular
function refreshChips() {

    operationChips.querySelectorAll(".chip").forEach((chip) => {

        const op = OPERATIONS[chip.dataset.op];
        const message = currentVariables.length === 0 ? null : checkRequirements(op);

        chip.setAttribute("aria-pressed", String(chip.dataset.op === currentOperation));
        chip.classList.toggle("unavailable", Boolean(message));

        if (message) {
            chip.title = message;
        } else {
            chip.removeAttribute("title");
        }
    });
}


// cambia la operacion activa y redibuja lo que depende de ella
function setOperation(name) {

    currentOperation = name;
    currentUnit = OPERATIONS[name].unit;

    refreshChips();
    clearResult();
    renderFields();

    // quitamos las capas de la operacion anterior (marcador, plano...)
    renderPlot();
}


// ====================================================
// deteccion dinamica de variables
// ====================================================

let debounceTimer = null;

// true mientras hay una deteccion programada que aun no se ejecuto
// (el usuario escribio hace menos de 400 ms)
let detectPending = false;

functionInput.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    detectPending = true;
    debounceTimer = setTimeout(detectVariables, 400);
});


async function detectVariables() {

    detectPending = false;

    const latex = functionInput.getValue("latex").trim();

    if (!latex) {
        currentVariables = [];
        currentVariablesLatex = {};
        setFeedback("", false);
        renderFields();
        renderPlot();
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

            // la grafica se actualiza en vivo al escribir la funcion
            renderPlot();

        } else {

            currentVariables = [];
            currentVariablesLatex = {};
            setFeedback(data.error, true);
            renderFields();
            renderPlot();

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

                // texto y no numerico, para poder escribir 1/2, pi/2, sqrt(2)...
                const input = document.createElement("input");
                input.type = "text";
                input.id = inputId;
                input.className = "point-input";
                input.dataset.variable = variable;
                input.placeholder = field.required ? "0" : "opcional";
                input.autocomplete = "off";
                input.spellcheck = false;

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


// devuelve un mensaje si la cantidad de variables de la funcion no sirve
// para la operacion, o null si todo esta bien
function checkRequirements(op) {

    const req = op.requires;

    if (!req) return null;

    const n = currentVariables.length;

    if ((req.min && n < req.min) || (req.max && n > req.max)) {
        return `${req.message} (la función actual tiene ${n} variable${n === 1 ? "" : "s"}).`;
    }

    return null;
}


// dibuja los campos de la operacion elegida segun las variables detectadas
function renderFields() {

    Object.assign(fieldMemory, snapshotFieldValues());
    const op = OPERATIONS[currentOperation];

    // las variables pudieron cambiar: actualizamos cuales operaciones aplican
    refreshChips();

    operationFields.innerHTML = "";

    // si la operacion necesita otra cantidad de variables, se avisa aqui
    // y se bloquea el boton, en vez de esperar al error del servidor
    const requirementMessage = currentVariables.length === 0 ? null : checkRequirements(op);
    blockedByRequirement = Boolean(requirementMessage);
    refreshCalculateButton();

    if (currentVariables.length === 0) {
        operationFields.innerHTML =
            '<p class="empty-hint">Escribe una función para continuar.</p>';
        return;
    }

    if (requirementMessage) {
        const warning = document.createElement("p");
        warning.className = "field-warning";
        warning.textContent = requirementMessage;
        operationFields.appendChild(warning);
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

        lastResult = { latex: data.result_latex, text: data.result };
        setCopyEnabled(true);

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

        lastResult = null;
        setCopyEnabled(false);
    }

}


// habilita o deshabilita los botones de copiar segun haya resultado
function setCopyEnabled(enabled) {
    copyLatexButton.disabled = !enabled;
    copyTextButton.disabled = !enabled;
}


// copia texto al portapapeles. navigator.clipboard solo existe en contextos
// seguros (https o localhost); si falla, se usa el metodo antiguo con un
// <textarea> temporal, que funciona tambien al abrir la app desde otra ip
async function copyToClipboard(text) {

    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (error) {
        // seguimos con el metodo alternativo
    }

    const area = document.createElement("textarea");
    area.value = text;
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();

    let copied = false;

    try {
        copied = document.execCommand("copy");
    } catch (error) {
        copied = false;
    }

    area.remove();
    return copied;
}


// conecta un boton para copiar lo que devuelve getText y avisa en el propio boton
function wireCopyButton(button, getText) {

    button.dataset.label = button.textContent;

    button.addEventListener("click", async () => {

        const text = getText();

        if (!text) return;

        const copied = await copyToClipboard(text);

        button.textContent = copied ? "¡Copiado!" : "No se pudo copiar";

        setTimeout(() => {
            button.textContent = button.dataset.label;
        }, 1200);
    });
}

wireCopyButton(copyLatexButton, () => lastResult && lastResult.latex);
wireCopyButton(copyTextButton, () => lastResult && lastResult.text);


function showResultLoading() {
    resultField.hidden = true;
    resultNote.hidden = true;
    resultPlaceholder.hidden = false;
    resultPlaceholder.classList.remove("error");
    resultPlaceholder.textContent = "Calculando...";
    lastResult = null;
    setCopyEnabled(false);
}


// vuelve el panel de resultado a su estado inicial
function clearResult() {
    resultField.hidden = true;
    resultNote.hidden = true;
    resultPlaceholder.hidden = false;
    resultPlaceholder.classList.remove("error");
    resultPlaceholder.textContent = "El resultado aparecerá aquí";
    lastResult = null;
    setCopyEnabled(false);
}


// ====================================================
// calcular
// ====================================================

// enter en la funcion o en cualquier campo de la operacion calcula
function calculateOnEnter(event) {

    if (event.key !== "Enter") return;

    event.preventDefault();

    if (!calculateButton.disabled) {
        calculateButton.click();
    }
}

functionInput.addEventListener("keydown", calculateOnEnter);

operationFields.addEventListener("keydown", (event) => {
    if (event.target.matches("input")) {
        calculateOnEnter(event);
    }
});


calculateButton.addEventListener("click", async () => {

    // si el usuario acaba de escribir (p. ej. escribio y presiono enter),
    // las variables detectadas pueden estar desactualizadas: las
    // actualizamos antes de calcular
    if (detectPending) {
        clearTimeout(debounceTimer);
        await detectVariables();
    }

    const latex = functionInput.getValue("latex").trim();
    const op = OPERATIONS[currentOperation];

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

    calculating = true;
    refreshCalculateButton();
    showResultLoading();

    try {

        const response = await fetch(op.endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ latex, ...collected.payload })
        });

        const data = await response.json();
        showResult(data, op);

        // graficamos la funcion actual. si el calculo tuvo exito, se marca
        // el punto y se agrega la capa de la operacion (plano tangente...)
        if (data.success) {
            renderPlot({ point: collected.payload.point, overlay: op.overlay });
        } else {
            renderPlot();
        }

    } catch (error) {
        console.error(error);
        showResult({ success: false, error: "Error al comunicarse con el servidor." });

    } finally {
        calculating = false;
        refreshCalculateButton();
    }

});


// ====================================================
// grafica (plotly)
// ====================================================

const plotContainer = document.getElementById("plot-container");

const PLOT_PLACEHOLDER = "La gráfica aparecerá aquí (solo para funciones de 1 o 2 variables)";

// plotly solo reajusta su tamaño cuando cambia la ventana, pero el recuadro
// tambien cambia cuando aparece la barra de controles o el resultado: lo
// observamos y le pedimos a plotly que se ajuste
if (typeof ResizeObserver !== "undefined") {

    let resizeFrame = null;

    new ResizeObserver(() => {

        if (plotContainer.dataset.hasPlot !== "true") return;

        cancelAnimationFrame(resizeFrame);
        resizeFrame = requestAnimationFrame(() => Plotly.Plots.resize(plotContainer));
    }).observe(plotContainer);
}


// contador para ignorar respuestas viejas: si el usuario sigue escribiendo,
// solo la ultima peticion puede dibujar
let plotRequestId = 0;

// vista de las funciones de 2 variables: "surface" o "contour" (curvas de nivel)
let plotMode = "surface";

// punto y capa de la ultima operacion calculada; se reutilizan al cambiar
// el rango, para que el marcador y el plano no desaparezcan
let currentPlotOptions = {};

// datos de la ultima grafica dibujada, para cambiar de vista sin pedirlos otra vez
let lastPlot = null;


// muestra u oculta los controles segun la funcion: el rango de y y el
// interruptor de vista solo tienen sentido con 2 variables
function updateToolbar() {

    const n = currentVariables.length;

    plotToolbar.hidden = !(n === 1 || n === 2);

    if (plotToolbar.hidden) return;

    xRangeLabel.textContent = `${currentVariables[0]} ∈`;

    yRangeGroup.hidden = n < 2;
    viewToggle.hidden = n < 2;

    if (n === 2) {
        yRangeLabel.textContent = `${currentVariables[1]} ∈`;
    }
}


// lee un par de inputs de rango. devuelve [minimo, maximo] o null si no
// son numeros o el minimo no es menor que el maximo (y marca los campos)
function readRange(minInput, maxInput) {

    const low = parseFloat(minInput.value);
    const high = parseFloat(maxInput.value);

    const valid = Number.isFinite(low) && Number.isFinite(high) && low < high;

    minInput.setAttribute("aria-invalid", String(!valid));
    maxInput.setAttribute("aria-invalid", String(!valid));

    return valid ? [low, high] : null;
}


// pide los datos de la grafica al backend y la dibuja con plotly.
// options.point y options.overlay agregan el marcador y la capa de la
// operacion (plano tangente, gradiente)
async function renderPlot(options = {}) {

    const requestId = ++plotRequestId;
    currentPlotOptions = options;

    const latex = functionInput.getValue("latex").trim();

    updateToolbar();

    // solo tiene sentido graficar con 1 o 2 variables (linea o superficie)
    if (!latex || currentVariables.length === 0 || currentVariables.length > 2) {
        showPlotMessage(PLOT_PLACEHOLDER);
        return;
    }

    // si un rango no es valido se conserva la grafica anterior
    const xRange = readRange(xMinInput, xMaxInput);
    const yRange = currentVariables.length > 1 ? readRange(yMinInput, yMaxInput) : [-10, 10];

    if (!xRange || !yRange) return;

    try {

        const response = await fetch("/api/plot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                latex,
                x_range: xRange,
                y_range: yRange,
                point: options.point || null,
                overlay: options.overlay || null,
            })
        });

        const data = await response.json();

        if (requestId !== plotRequestId) return;

        if (!data.success) {
            showPlotMessage(data.error);
            return;
        }

        drawPlot(data, latex);

    } catch (error) {
        if (requestId !== plotRequestId) return;
        console.error(error);
        showPlotMessage("Error al generar la gráfica.");
    }

}


// los rangos se aplican al terminar de editar un campo (change)
[xMinInput, xMaxInput, yMinInput, yMaxInput].forEach((input) => {
    input.addEventListener("change", () => renderPlot(currentPlotOptions));
});


// interruptor superficie / curvas de nivel: reutiliza los datos ya pedidos
viewToggle.addEventListener("click", (event) => {

    const button = event.target.closest("button[data-mode]");

    if (!button) return;

    plotMode = button.dataset.mode;

    viewToggle.querySelectorAll("button").forEach((b) => {
        b.classList.toggle("active", b === button);
    });

    if (lastPlot) {
        drawPlot(lastPlot.data, lastPlot.latex);
    }
});


// descarga la grafica actual como imagen
downloadButton.addEventListener("click", () => {

    if (plotContainer.dataset.hasPlot !== "true") return;

    Promise.resolve(
        Plotly.downloadImage(plotContainer, {
            format: "png",
            filename: "nekocalc",
            width: 1200,
            height: 800,
            scale: 2,
        })
    ).catch((error) => console.error(error));
});


// muestra un mensaje de texto en vez de la grafica (placeholder o error)
function showPlotMessage(text) {

    // si plotly ya dibujo algo antes, lo limpiamos
    if (plotContainer.dataset.hasPlot === "true") {
        Plotly.purge(plotContainer);
        plotContainer.dataset.hasPlot = "false";
    }

    lastPlot = null;
    downloadButton.disabled = true;

    const message = document.createElement("span");
    message.className = "canvas-placeholder";
    message.textContent = text;

    plotContainer.innerHTML = "";
    plotContainer.appendChild(message);

}


// colores compartidos de la superficie y las curvas de nivel
const SURFACE_COLORSCALE = [
    [0, "#fbf3ef"],
    [0.5, "#f0a8c2"],
    [1, "#c9718b"]
];


// arma las trazas de plotly segun lo que devolvio el backend:
// la funcion, mas el marcador, el plano tangente y la flecha si vienen.
// kind es "2d", "surface" o "contour"
function buildTraces(data, kind) {

    if (kind === "2d") {
        return buildLineTraces(data);
    }

    if (kind === "contour") {
        return buildContourTraces(data);
    }

    return buildSurfaceTraces(data);
}


// funcion de una variable: linea y marcador
function buildLineTraces(data) {

    const traces = [{
        x: data.x,
        y: data.y,
        type: "scatter",
        mode: "lines",
        line: { color: "#e48aae", width: 2.5 } // sakura
    }];

    if (data.marker) {
        traces.push({
            x: [data.marker.x],
            y: [data.marker.y],
            type: "scatter",
            mode: "markers",
            marker: { color: "#3e2a2e", size: 9 },
            hoverinfo: "skip"
        });
    }

    return traces;
}


// superficie 3d, con el plano tangente, la flecha del gradiente y el marcador
function buildSurfaceTraces(data) {

    const traces = [{
        x: data.x,
        y: data.y,
        z: data.z,
        type: "surface",
        colorscale: SURFACE_COLORSCALE,
        showscale: false
    }];

    // plano tangente: superficie semitransparente de un solo color
    if (data.plane_z) {
        traces.push({
            x: data.x,
            y: data.y,
            z: data.plane_z,
            type: "surface",
            colorscale: [[0, "#3e2a2e"], [1, "#3e2a2e"]],
            opacity: 0.45,
            showscale: false,
            hoverinfo: "skip"
        });
    }

    // flecha del gradiente: linea con un punto grande en la punta
    if (data.gradient_arrow) {
        traces.push({
            ...data.gradient_arrow,
            type: "scatter3d",
            mode: "lines+markers",
            line: { color: "#3e2a2e", width: 6 },
            marker: { color: "#3e2a2e", size: [0, 6] },
            hoverinfo: "skip"
        });
    }

    if (data.marker) {
        traces.push({
            x: [data.marker.x],
            y: [data.marker.y],
            z: [data.marker.z],
            type: "scatter3d",
            mode: "markers",
            marker: { color: "#3e2a2e", size: 5 },
            hoverinfo: "skip"
        });
    }

    return traces;
}


// curvas de nivel (vista desde arriba). el plano tangente se dibuja como
// sus propias curvas de nivel (rectas) y el gradiente como flecha: se ve
// que es perpendicular a la curva de nivel que pasa por el punto
function buildContourTraces(data) {

    const traces = [{
        x: data.x,
        y: data.y,
        z: data.z,
        type: "contour",
        colorscale: SURFACE_COLORSCALE,
        showscale: false,
        line: { color: "#8c7377", width: 0.6 }
    }];

    if (data.plane_z) {
        traces.push({
            x: data.x,
            y: data.y,
            z: data.plane_z,
            type: "contour",
            contours: { coloring: "none" },
            line: { color: "#3e2a2e", width: 1.2, dash: "dash" },
            showscale: false,
            hoverinfo: "skip"
        });
    }

    if (data.gradient_arrow) {
        traces.push({
            x: data.gradient_arrow.x,
            y: data.gradient_arrow.y,
            type: "scatter",
            mode: "lines+markers",
            line: { color: "#3e2a2e", width: 3 },
            marker: { color: "#3e2a2e", size: [0, 8] },
            hoverinfo: "skip"
        });
    }

    if (data.marker) {
        traces.push({
            x: [data.marker.x],
            y: [data.marker.y],
            type: "scatter",
            mode: "markers",
            marker: { color: "#3e2a2e", size: 9 },
            hoverinfo: "skip"
        });
    }

    return traces;
}


// dibuja la grafica con plotly. si ya habia una del mismo tipo se usa
// react, que conserva la camara 3d y el zoom mientras no cambie la funcion,
// la vista o el rango; uirevision es lo que le dice a plotly cuando reiniciarlos
function drawPlot(data, latex) {

    const kind = data.type === "2d" ? "2d" : plotMode;

    const revision = [
        latex,
        kind,
        data.x[0],
        data.x[data.x.length - 1],
        data.type === "3d" ? data.y[0] : "",
        data.type === "3d" ? data.y[data.y.length - 1] : "",
    ].join("|");

    const layout = {
        ...plotLayout(kind, data.variable_names),
        uirevision: revision,
    };

    const sameType = plotContainer.dataset.hasPlot === "true"
        && plotContainer.dataset.plotType === kind;

    if (!sameType) {
        plotContainer.innerHTML = "";
    }

    plotContainer.dataset.hasPlot = "true";
    plotContainer.dataset.plotType = kind;

    lastPlot = { data, latex };
    downloadButton.disabled = false;

    const traces = buildTraces(data, kind);

    if (sameType) {
        Plotly.react(plotContainer, traces, layout, plotConfig());
    } else {
        Plotly.newPlot(plotContainer, traces, layout, plotConfig());
    }

}


// layout compartido: combina con la paleta clara actual de la interfaz.
// kind es "2d", "surface" o "contour"
function plotLayout(kind, variableNames) {

    const base = {
        paper_bgcolor: "#ffffff",
        plot_bgcolor: "#ffffff",
        font: { color: "#8c7377", family: "Inter, sans-serif" },
        margin: { l: 30, r: 20, t: 20, b: 30 },
    };

    const axis = { gridcolor: "#f6d9e4", zerolinecolor: "#f6d9e4" };

    if (kind === "surface") {
        return {
            ...base,
            margin: { l: 0, r: 0, t: 0, b: 0 },
            scene: {
                xaxis: { title: variableNames[0], color: "#8c7377", gridcolor: "#f6d9e4" },
                yaxis: { title: variableNames[1], color: "#8c7377", gridcolor: "#f6d9e4" },
                zaxis: { color: "#8c7377", gridcolor: "#f6d9e4" },

                // proporcion mas ancha que alta y camara mas cercana: la
                // superficie llena mejor un recuadro apaisado
                aspectmode: "manual",
                aspectratio: { x: 1.5, y: 1.5, z: 1 },
                camera: { eye: { x: 1.35, y: 1.35, z: 0.9 } },
            },
        };
    }

    if (kind === "contour") {
        return {
            ...base,
            margin: { l: 45, r: 20, t: 20, b: 40 },
            xaxis: { ...axis, title: variableNames[0] },
            // misma escala en ambos ejes, para que las perpendiculares se vean perpendiculares
            yaxis: { ...axis, title: variableNames[1], scaleanchor: "x" },
        };
    }

    return {
        ...base,
        margin: { l: 45, r: 20, t: 20, b: 40 },
        xaxis: { ...axis, title: variableNames[0] },
        yaxis: axis,
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

renderUnitTabs();
renderChips();
renderFields();
