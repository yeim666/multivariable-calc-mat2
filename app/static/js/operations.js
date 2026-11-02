// ====================================================
// catalogo de operaciones
//
// cada operacion declara su unidad y grupo (para el selector), su endpoint
// y los campos que pide la interfaz.
// para agregar una operacion nueva basta con sumar una entrada aqui
// (y registrar su funcion en el backend); main.js dibuja el resto.
//
// tipos de campo disponibles:
//   point         valores numericos, uno por variable detectada
//                 (required: true obliga a llenar todas)
//   variable      lista desplegable con una variable
//   variableList  texto con variables separadas por coma, ej. "x, y, x"
//   variablePair  dos listas desplegables (par de variables)
//   direction     componentes del vector direccion, una por variable
//   math          math-field (restriccion u otra expresion)
//
// note(data) es opcional: devuelve un texto breve que se muestra
// debajo del resultado (ej. si se cumplio una verificacion)
//
// requires es opcional: cantidad de variables que necesita la operacion
// ({ min, max, message }). si la funcion no lo cumple, la interfaz lo avisa
// y bloquea el boton Calcular en vez de esperar al error del servidor
//
// overlay es opcional: capa extra que la grafica dibuja sobre la superficie
// en el punto de evaluacion ("tangent_plane", "gradient" o "directional")
// ====================================================

const OPERATIONS = {

    limit: {
        label: "Límite multivariable",
        unit: "Unidad 1",
        group: "Límites",
        endpoint: "/api/limit",
        fields: [
            { type: "point", title: "Punto de aproximación", hint: "variable → valor", required: true },
        ],
        note: (data) => {
            if (data.paths_agree === true) {
                return "Las cinco trayectorias coinciden. Coincidir en trayectorias no demuestra existencia.";
            }
            if (data.paths_agree === false) {
                return "Las trayectorias no coinciden: el límite multivariable no existe.";
            }
            return "";
        },
    },

    domain: {
        label: "Dominio (análisis parcial)",
        unit: "Unidad 1",
        group: "Límites",
        endpoint: "/api/domain",
        fields: [],
        note: () => "El dominio se analiza por variable y puede requerir análisis conjunto.",
    },

    derivative: {
        label: "Derivada parcial",
        unit: "Unidad 1",
        group: "Derivadas",
        endpoint: "/api/derivative",
        fields: [
            { type: "variable", key: "variable", title: "Derivar respecto a" },
            { type: "point", title: "Punto de evaluación", hint: "opcional", required: false },
        ],
    },

    higher_derivative: {
        label: "Derivada de orden superior",
        unit: "Unidad 1",
        group: "Derivadas",
        endpoint: "/api/higher_derivative",
        fields: [
            {
                type: "variableList",
                key: "variables",
                title: "Orden de derivación",
                hint: "de izquierda a derecha",
                placeholder: "x, y",
            },
            { type: "point", title: "Punto de evaluación", hint: "opcional", required: false },
        ],
    },

    schwarz: {
        label: "Teorema de Schwarz",
        unit: "Unidad 1",
        group: "Derivadas",
        endpoint: "/api/schwarz",
        requires: { min: 2, message: "El teorema de Schwarz necesita una función de al menos 2 variables." },
        fields: [
            { type: "variablePair", key: "variables", title: "Derivadas mixtas a comparar" },
        ],
        note: (data) => data.equal
            ? "Las derivadas mixtas son iguales: se cumple el teorema."
            : "Las derivadas mixtas son distintas.",
    },

    gradient: {
        label: "Gradiente",
        unit: "Unidad 1",
        group: "Gradiente y geometría",
        endpoint: "/api/gradient",
        overlay: "gradient",
        fields: [
            { type: "point", title: "Punto de evaluación", hint: "opcional", required: false },
        ],
    },

    hessian: {
        label: "Hessiana",
        unit: "Unidad 1",
        group: "Gradiente y geometría",
        endpoint: "/api/hessian",
        fields: [
            { type: "point", title: "Punto de evaluación", hint: "opcional", required: false },
        ],
    },

    directional: {
        label: "Derivada direccional",
        unit: "Unidad 1",
        group: "Gradiente y geometría",
        endpoint: "/api/directional",
        overlay: "directional",
        fields: [
            { type: "direction", title: "Vector dirección", hint: "se normaliza", required: true },
            { type: "point", title: "Punto de evaluación", hint: "opcional", required: false },
        ],
    },

    tangent_plane: {
        label: "Plano tangente y recta normal",
        unit: "Unidad 1",
        group: "Gradiente y geometría",
        endpoint: "/api/tangent_plane",
        overlay: "tangent_plane",
        requires: { min: 2, max: 2, message: "El plano tangente requiere una función de exactamente 2 variables." },
        fields: [
            { type: "point", title: "Punto de tangencia", hint: "(a, b)", required: true },
        ],
    },

    critical: {
        label: "Candidatos críticos",
        unit: "Unidad 1",
        group: "Extremos",
        endpoint: "/api/critical",
        fields: [],
        note: () => "Los candidatos de extremos requieren clasificación y revisión del dominio.",
    },

    lagrange: {
        label: "Candidatos de Lagrange",
        unit: "Unidad 1",
        group: "Extremos",
        endpoint: "/api/lagrange",
        requires: { min: 2, message: "Lagrange necesita una función de al menos 2 variables." },
        fields: [
            {
                type: "math",
                key: "constraint",
                title: "Restricción g = 0",
                hint: "o una ecuación, p. ej. x^2+y^2=1",
                required: true,
            },
        ],
        note: () => "Los candidatos de extremos requieren clasificación y revisión del dominio.",
    },

    double_integral: {
        label: "Integral doble cartesiana",
        unit: "Unidad 2",
        group: "Integrales dobles",
        endpoint: "/api/double_integral",
        allowConstant: true,
        requires: { min: 2, max: 2, message: "La integral doble requiere una función de 2 variables." },
        fields: [{ type: "bounds", title: "Límites de integración", variables: ["x", "y"] }],
    },

    surface_area: {
        label: "Área de superficie z = f(x,y)",
        unit: "Unidad 2",
        group: "Aplicaciones geométricas",
        endpoint: "/api/surface_area",
        allowConstant: true,
        requires: { min: 2, max: 2, message: "El área de superficie requiere una función de 2 variables." },
        fields: [{ type: "bounds", title: "Región de integración (x, y)", variables: ["x", "y"] }],
    },

    mass_properties: {
        label: "Masa, centro y momentos",
        unit: "Unidad 2",
        group: "Aplicaciones físicas",
        endpoint: "/api/mass_properties",
        allowConstant: true,
        requires: { min: 2, max: 2, message: "Las propiedades de una lámina requieren una densidad de 2 variables." },
        fields: [{ type: "bounds", title: "Región de integración (x, y)", variables: ["x", "y"] }],
    },

    double_polar: {
        label: "Integral doble polar",
        unit: "Unidad 2",
        group: "Integrales dobles",
        endpoint: "/api/double_polar",
        allowConstant: true,
        requires: { min: 2, max: 2, message: "La integral polar requiere una función de 2 variables x, y." },
        fields: [{ type: "bounds", title: "Límites en orden r, θ", variables: ["r", "theta"] }],
    },

    triple_integral: {
        label: "Integral triple cartesiana",
        unit: "Unidad 2",
        group: "Integrales triples",
        endpoint: "/api/triple_integral",
        allowConstant: true,
        requires: { min: 3, max: 3, message: "La integral triple requiere una función de 3 variables." },
        fields: [{ type: "bounds", title: "Límites de integración", variables: ["x", "y", "z"] }],
    },

    triple_cylindrical: {
        label: "Integral triple cilíndrica",
        unit: "Unidad 2",
        group: "Integrales triples",
        endpoint: "/api/triple_cylindrical",
        allowConstant: true,
        requires: { min: 3, max: 3, message: "La integral cilíndrica requiere una función de 3 variables x, y, z." },
        fields: [{ type: "bounds", title: "Límites en orden r, θ, z", variables: ["r", "theta", "z"] }],
    },

    triple_spherical: {
        label: "Integral triple esférica",
        unit: "Unidad 2",
        group: "Integrales triples",
        endpoint: "/api/triple_spherical",
        allowConstant: true,
        requires: { min: 3, max: 3, message: "La integral esférica requiere una función de 3 variables x, y, z." },
        fields: [{ type: "bounds", title: "Límites en orden ρ, φ, θ", variables: ["rho", "phi", "theta"] }],
    },

    divergence: {
        label: "Divergencia",
        unit: "Unidad 3",
        group: "Campos vectoriales",
        endpoint: "/api/divergence",
        noFunction: true,
        fields: [{ type: "expressionList", key: "components", title: "Componentes del campo F", count: 2, dynamicDimension: true }],
    },

    curl: {
        label: "Rotacional (plano o espacio)",
        unit: "Unidad 3",
        group: "Campos vectoriales",
        endpoint: "/api/curl",
        noFunction: true,
        fields: [{ type: "expressionList", key: "components", title: "Componentes del campo F", count: 2, dynamicDimension: true }],
    },

    laplacian: {
        label: "Laplaciano",
        unit: "Unidad 3",
        group: "Campos escalares",
        endpoint: "/api/laplacian",
        fields: [],
    },

    conservative: {
        label: "Campo conservativo y potencial",
        unit: "Unidad 3",
        group: "Campos vectoriales",
        endpoint: "/api/conservative",
        noFunction: true,
        fields: [{ type: "expressionList", key: "components", title: "Componentes P, Q", count: 2 }],
        note: (data) => data.note || "",
    },

    line_integral: {
        label: "Integral de línea parametrizada",
        unit: "Unidad 3",
        group: "Integrales curvilíneas",
        endpoint: "/api/line_integral",
        noFunction: true,
        allowConstant: true,
        fields: [
            { type: "select", key: "kind", title: "Tipo de integral", options: [["second", "Segundo tipo: P dx + Q dy"], ["first", "Primer tipo: f ds"]] },
            { type: "expressionList", key: "components", title: "Componentes P, Q", count: 2, visibleWhen: { key: "kind", value: "second" } },
            { type: "curve", title: "Curva y límites del parámetro" },
        ],
    },

    green: {
        label: "Teorema de Green",
        unit: "Unidad 3",
        group: "Teorema de Green",
        endpoint: "/api/green",
        noFunction: true,
        fields: [
            { type: "expressionList", key: "components", title: "Componentes P, Q", count: 2 },
            { type: "greenBounds", title: "Límites de la región" },
        ],
    },

    vector_curve: {
        label: "Función vectorial: límite, derivada o integral",
        unit: "Unidad 3",
        group: "Funciones vectoriales",
        endpoint: "/api/vector_curve",
        noFunction: true,
        fields: [
            { type: "select", key: "mode", title: "Operación", options: [["limit", "Límite"], ["derivative", "Derivada"], ["integral", "Integral"]] },
            { type: "expressionList", key: "components", title: "Componentes r(t)", count: 2, dynamicDimension: true },
            { type: "scalar", key: "parameter", title: "Valor del parámetro" },
            { type: "scalar", key: "lower", title: "Límite inferior de integración" },
        ],
    },

};


const EXAMPLES = [
    {
        label: "Paraboloide x² + y²",
        latex: "x^2+y^2",
        operation: "gradient",
        point: { x: "1", y: "2" },
    },
    {
        label: "Límite xy/(x²+y²) en el origen",
        latex: "\\frac{xy}{x^2+y^2}",
        operation: "limit",
        point: { x: "0", y: "0" },
    },
    {
        label: "e^{x} + π y",
        latex: "e^{x}+\\pi y",
        operation: "derivative",
        fields: { "field-variable": "x" },
    },
    {
        label: "Dominio ln(x) + √y",
        latex: "\\ln(x)+\\sqrt{y}",
        operation: "domain",
    },
    {
        label: "Hessiana de x³ − 3xy + y³",
        latex: "x^3-3xy+y^3",
        operation: "critical",
    },
    {
        label: "Lagrange: xy en x+y=1",
        latex: "xy",
        operation: "lagrange",
        constraint: "x+y-1",
    },
    {
        label: "Direccional de x²+y² hacia (1,1)",
        latex: "x^2+y^2",
        operation: "directional",
        direction: { x: "1", y: "1" },
        point: { x: "1", y: "0" },
    },
];


const PRACTICE = {
    title: "Práctica guiada",
    prompt: "Estudia el límite de xy/(x²+y²) cuando (x, y) → (0, 0) con las cinco trayectorias. ¿Existe el límite?",
    latex: "\\frac{xy}{x^2+y^2}",
    operation: "limit",
    point: { x: "0", y: "0" },
    hint: "Compara al menos y = 0 (eje x) con y = x. Si dos trayectorias dan valores distintos, el límite no existe. Coincidir en cinco caminos tampoco demostraría existencia.",
    note: "La práctica incluye un ejercicio con pista. El procedimiento describe operaciones simbólicas; no es un tutor universal.",
};
