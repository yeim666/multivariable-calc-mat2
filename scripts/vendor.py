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
        try:
            # filtro "data": rechaza rutas peligrosas dentro del tar (python 3.12+)
            tar.extractall(target, filter="data")
        except TypeError:
            tar.extractall(target)

    return target / "package"


# busca un archivo dentro del paquete sin asumir la estructura: segun la
# version, los archivos estan en la raiz o dentro de dist/
def find_file(package_dir, filename):

    matches = sorted(package_dir.rglob(filename), key=lambda p: len(p.parts))

    if not matches:
        sys.exit(f"No se encontró {filename} en el paquete descargado ({package_dir}).")

    return matches[0]


def main():

    if shutil.which("npm") is None:
        sys.exit("No se encontró npm. Instálalo o descarga las librerías a mano (ver README).")

    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)

        # mathlive: se copia la carpeta que contiene mathlive.min.js completa,
        # porque la libreria busca sus fuentes (fonts/) junto a ese archivo
        print("Descargando mathlive...")
        mathlive = fetch_package("mathlive", workdir)
        mathlive_src = find_file(mathlive, "mathlive.min.js").parent
        mathlive_dest = VENDOR / "mathlive"
        shutil.rmtree(mathlive_dest, ignore_errors=True)
        shutil.copytree(
            mathlive_src,
            mathlive_dest,
            ignore=shutil.ignore_patterns("*.map", "*.d.ts", "types", "node_modules"),
        )

        # plotly: bundle minificado de un solo archivo
        print("Descargando plotly...")
        plotly = fetch_package("plotly.js-dist-min", workdir)
        plotly_dest = VENDOR / "plotly"
        plotly_dest.mkdir(parents=True, exist_ok=True)
        shutil.copy(find_file(plotly, "plotly.min.js"), plotly_dest / "plotly.min.js")

    # si algo salio mal, mejor avisar que dejar la app apuntando a un archivo roto
    if not (VENDOR / "mathlive" / "mathlive.min.js").exists() or not (VENDOR / "plotly" / "plotly.min.js").exists():
        sys.exit("La descarga no dejó los archivos esperados en " + str(VENDOR))

    print(f"Listo: {VENDOR}")


if __name__ == "__main__":
    main()
