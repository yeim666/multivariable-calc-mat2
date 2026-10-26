import os

from flask import Flask, url_for


def create_app():
    app = Flask(__name__)

    from app.routes import main
    app.register_blueprint(main)

    # ayuda para las plantillas: devuelve la copia local de una libreria
    # (static/vendor/...) si existe, y si no, su direccion en un cdn.
    # asi la app funciona sin internet una vez ejecutado scripts/vendor.py,
    # y sigue funcionando con cdn mientras tanto
    @app.context_processor
    def vendor_helpers():

        def vendor_url(local_path, cdn_url):
            local_file = os.path.join(app.static_folder, "vendor", local_path)

            if os.path.exists(local_file):
                return url_for("static", filename=f"vendor/{local_path}")

            return cdn_url

        return {"vendor_url": vendor_url}

    return app
