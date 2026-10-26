import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    # el modo debug recarga el servidor al editar el codigo; actívalo con
    # FLASK_DEBUG=1 (en Windows CMD: set FLASK_DEBUG=1)
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
