"""
Descarga mathlive y plotly a app/static/vendor/ para usar la calculadora sin internet.

Uso (desde la carpeta principal del proyecto, requiere npm):

    python scripts/vendor.py

Despues de ejecutarlo, la plantilla usa las copias locales automaticamente.
Si borras app/static/vendor/, vuelve a usar los cdn.
"""

import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENDOR = ROOT / "app" / "static" / "vendor"


# descarga un paquete de npm (npm pack) y devuelve la carpeta "package" extraida
def fetch_package(name, workdir):

    result = subprocess.run(
        ["npm", "pack", name, "--pack-destination", str(workdir)],
        capture_output=True, text=True, check=True,
    )

    # npm imprime el nombre del .tgz generado en la ultima linea
    tarball = workdir / result.stdout.strip().splitlines()[-1]
    target = workdir / name.replace("/", "_")

    with tarfile.open(tarball) as tar:
        tar.extractall(target, filter="data")

    return target / "package"


def main():

    if shutil.which("npm") is None:
        sys.exit("No se encontró npm. Instálalo o descarga las librerías a mano (ver README).")

    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)

        # mathlive: carpeta dist completa (el js y sus fuentes)
        print("Descargando mathlive...")
        mathlive = fetch_package("mathlive", workdir)
        mathlive_dest = VENDOR / "mathlive"
        shutil.rmtree(mathlive_dest, ignore_errors=True)
        shutil.copytree(mathlive / "dist", mathlive_dest)

        # plotly: bundle minificado de un solo archivo
        print("Descargando plotly...")
        plotly = fetch_package("plotly.js-dist-min", workdir)
        plotly_dest = VENDOR / "plotly"
        plotly_dest.mkdir(parents=True, exist_ok=True)
        shutil.copy(plotly / "plotly.min.js", plotly_dest / "plotly.min.js")

    print(f"Listo: {VENDOR}")


if __name__ == "__main__":
    main()
