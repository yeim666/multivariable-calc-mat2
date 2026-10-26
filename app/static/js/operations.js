// ====================================================
// catalogo de operaciones
//
// cada operacion declara su endpoint y los campos que pide la interfaz.
// para agregar una operacion nueva basta con sumar una entrada aqui
// (y registrar su funcion en el backend); main.js dibuja el resto.
//
// tipos de campo disponibles:
//   point         valores numericos, uno por variable detectada
//                 (required: true obliga a llenar todas)
//   variable      lista desplegable con una variable
//   variableList  texto con variables separadas por coma, ej. "x, y, x"
//   variablePair  dos listas desplegables (par de variables)
//
// note(data) es opcional: devuelve un texto breve que se muestra
// debajo del resultado (ej. si se cumplio una verificacion)
//
// requires es opcional: cantidad de variables que necesita la operacion
// ({ min, max, message }). si la funcion no lo cumple, la interfaz lo avisa
// y bloquea el boton Calcular en vez de esperar al error del servidor
//
// overlay es opcional: capa extra que la grafica dibuja sobre la superficie
// en el punto de evaluacion ("tangent_plane" o "gradient")
// ====================================================

const OPERATIONS = {

    limit: {
        label: "Límite multivariable",
        unit: "Unidad 1",
        endpoint: "/api/limit",
        fields: [
            { type: "point", title: "Punto de aproximación", hint: "variable → valor", required: true },
        ],
    },

    derivative: {
        label: "Derivada parcial",
        unit: "Unidad 1",
        endpoint: "/api/derivative",
        fields: [
            { type: "variable", key: "variable", title: "Derivar respecto a" },
            { type: "point", title: "Punto de evaluación", hint: "opcional", required: false },
        ],
    },

    higher_derivative: {
        label: "Derivada de orden superior",
        unit: "Unidad 1",
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
        endpoint: "/api/gradient",
        overlay: "gradient",
        fields: [
            { type: "point", title: "Punto de evaluación", hint: "opcional", required: false },
        ],
    },

    tangent_plane: {
        label: "Plano tangente y recta normal",
        unit: "Unidad 1",
        endpoint: "/api/tangent_plane",
        overlay: "tangent_plane",
        requires: { min: 2, max: 2, message: "El plano tangente requiere una función de exactamente 2 variables." },
        fields: [
            { type: "point", title: "Punto de tangencia", hint: "(a, b)", required: true },
        ],
    },

};
