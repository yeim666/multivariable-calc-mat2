# Calculadora Multivariable

Aplicación web desarrollada con **Flask** y **SymPy** para calcular límites de funciones multivariables.

El proyecto está pensado como una herramienta sencilla para trabajar con funciones de varias variables desde una interfaz web.

Actualmente el proyecto se encuentra en desarrollo.

## Características

* Cálculo de límites multivariables.
* Interfaz web sencilla.
* Backend desarrollado con Flask.
* Cálculos simbólicos utilizando SymPy.
* Preparado para añadir derivadas parciales y otras operaciones en el futuro.

---

# Requisitos

Necesitas tener instalado:

* Python 3
* pip
* Git

Puedes comprobar que están instalados con:

```bash
python --version
pip --version
git --version
```

En algunos sistemas el comando de Python puede ser:

```bash
python3 --version
```

---

# Instalación

Primero clona el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
```

Entra en la carpeta:

```bash
cd calculadora-web
```

Se recomienda utilizar un entorno virtual para evitar instalar las dependencias globalmente.

## Linux

Crear el entorno virtual:

```bash
python3 -m venv venv
```

Activarlo:

```bash
source venv/bin/activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

---

## macOS

Crear el entorno virtual:

```bash
python3 -m venv venv
```

Activarlo:

```bash
source venv/bin/activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Dependiendo de la instalación de Python, también puede funcionar:

```bash
python -m venv venv
```

---

## Windows

Crear el entorno virtual:

```powershell
python -m venv venv
```

Si utilizas PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Si utilizas CMD:

```cmd
venv\Scripts\activate
```

Después instala las dependencias:

```powershell
pip install -r requirements.txt
```

Si PowerShell impide ejecutar el script de activación, puedes utilizar CMD o cambiar temporalmente la política de ejecución para la sesión actual.

---

# Ejecutar el programa

Primero asegúrate de tener el entorno virtual activado.

Luego ejecuta Flask desde la carpeta principal del proyecto:

```bash
flask --app 'app:create_app' --debug run
```

En Windows CMD, si las comillas simples causan problemas, utiliza:

```cmd
flask --app app:create_app --debug run
```

Flask debería mostrar una dirección similar a:

```text
http://127.0.0.1:5000
```

Abre esa dirección en tu navegador.

Para detener el servidor utiliza:

```text
Ctrl + C
```

---

# Cómo usar la calculadora

1. Abre la aplicación en el navegador.

2. Selecciona la operación que deseas realizar.

3. Para calcular un límite, escribe una función utilizando las variables `x` y `y`.

Por ejemplo:

```text
x^2 + y^2
```

4. Introduce el punto al que deben aproximarse las variables.

Por ejemplo:

```text
x → 0
y → 0
```

5. Presiona el botón **Calcular**.

El resultado aparecerá en la parte inferior de la calculadora.

Ejemplo:

```text
Función:

x^2 + y^2

Punto:

(0, 0)

Resultado:

0
```

Actualmente algunas expresiones o límites multivariables complejos pueden no ser evaluados correctamente, ya que el sistema de cálculo todavía está en desarrollo.

---

# Estructura del proyecto

```text
calculadora-web/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── calculator.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       │
│       └── js/
│           └── main.js
│
├── tests/
│   └── test_calculator.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Archivos principales

### `app/__init__.py`

Inicializa la aplicación Flask y registra las rutas.

### `app/routes.py`

Contiene las rutas de Flask y los endpoints de la API.

Por ejemplo:

```text
/
```

muestra la página principal.

Mientras que:

```text
/api/limit
```

recibe los datos enviados desde JavaScript y solicita el cálculo del límite.

### `app/calculator.py`

Contiene la lógica matemática de la aplicación.

Aquí se utiliza SymPy para interpretar expresiones y realizar los cálculos.

### `app/templates/index.html`

Contiene la estructura de la interfaz.

### `app/static/css/style.css`

Contiene los estilos de la página.

### `app/static/js/main.js`

Controla la interacción de la interfaz y la comunicación con el backend mediante `fetch()`.

---

# Contribuir

Las contribuciones son bienvenidas.

Para trabajar en el proyecto sin destruir accidentalmente la rama principal, sigue este flujo.

## 1. Clonar el repositorio

```bash
git clone https://github.com/yeim666/multivariable-calc-mat2/
```

Después:

```bash
cd calculadora-web
```

Instala las dependencias siguiendo las instrucciones anteriores.

---

## 2. Crear una nueva rama

No trabajes directamente sobre `main`.

Crea una rama para tu cambio:

```bash
git switch -c nombre-de-la-rama
```

Por ejemplo:

```bash
git switch -c feat-derivadas-parciales
```

También puedes utilizar:

```bash
git checkout -b feat-derivadas-parciales
```

---

## 3. Realizar los cambios

Modifica únicamente lo necesario para la funcionalidad en la que estés trabajando.

Antes de hacer un commit puedes revisar los archivos modificados con:

```bash
git status
```

---

## 4. Añadir los cambios

```bash
git add .
```

---

## 5. Crear un commit

Intentamos utilizar mensajes de commit claros.

Formato recomendado:

```text
tipo: descripción
```

Algunos tipos:

```text
feat: nueva funcionalidad

fix: corrección de un error

docs: cambios en documentación

style: cambios visuales o de formato

refactor: reorganización del código

test: cambios relacionados con pruebas

chore: configuración o mantenimiento
```

Ejemplos:

```bash
git commit -m "feat: add partial derivative support"
```

```bash
git commit -m "fix: validate empty function input"
```

```bash
git commit -m "docs: update installation guide"
```

---

## 6. Subir la rama

```bash
git push -u origin nombre-de-la-rama
```

Por ejemplo:

```bash
git push -u origin feat-derivadas-parciales
```

---

## 7. Crear un Pull Request

Desde GitHub, crea un **Pull Request** desde tu rama hacia `main`.

En la descripción explica brevemente:

* Qué cambiaste.
* Por qué lo cambiaste.
* Cómo se puede probar.

Después el código puede revisarse antes de integrarlo a la rama principal.

---

# Recomendaciones para contribuir

Antes de enviar cambios:

* Comprueba que el programa siga ejecutándose.
* Prueba manualmente la funcionalidad modificada.
* No subas el entorno virtual `venv/`.
* No subas archivos temporales.
* Evita modificar archivos que no estén relacionados con tu cambio.
* Intenta mantener el código legible.
* Añade comentarios cuando una parte del código no sea evidente.
* Haz commits pequeños y relacionados con un único cambio.

---

# Flujo general de la aplicación

```text
Usuario
   │
   ▼
HTML
   │
   ▼
JavaScript
   │
   │ fetch()
   ▼
API de Flask
   │
   ▼
calculator.py
   │
   ▼
SymPy
   │
   ▼
Flask devuelve JSON
   │
   ▼
JavaScript
   │
   ▼
Resultado mostrado en HTML
```

---

# Estado del proyecto

Actualmente se está trabajando principalmente en:

* Límites multivariables.
* Interpretación de expresiones matemáticas.
* Validación de datos.
* Mejora de la precisión de los cálculos.

Entre las funcionalidades previstas se encuentran:

* Derivadas parciales.
* Mejor representación matemática de los resultados.
* Soporte para más tipos de expresiones.
* Mejor manejo de errores.
* Pruebas automatizadas.

---

# Tecnologías utilizadas

* Python
* Flask
* SymPy
* HTML
* CSS
* JavaScript

