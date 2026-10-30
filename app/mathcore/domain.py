import sympy as sp
from sympy.calculus.util import continuous_domain

from app.mathcore.common import get_variables, make_result, step, to_latex
from app.mathcore.registry import register


PROCEDURE_NOTE = (
    "Los procedimientos describen operaciones simbólicas y no constituyen un tutor universal."
)

DOMAIN_CAVEAT = (
    "El dominio se analiza por variable y puede requerir análisis conjunto."
)


@register("domain")
def domain_operation(expr, params):

    variables = get_variables(expr)

    procedure = [
        step("Función", latex=to_latex(expr)),
        step(
            "Enfoque",
            text=(
                "Se recorta el dominio real variable por variable, tratando las demás "
                "como parámetros. Las condiciones cruzadas (por ejemplo x + y > 0) "
                "pueden quedar incompletas."
            ),
        ),
    ]

    if not variables:
        procedure.append(step("Conclusión", text="La expresión es constante: no hay variables que restringir."))
        procedure.append(step("Alcance", text=PROCEDURE_NOTE))
        return make_result(
            "constante (sin variables)",
            procedure=procedure,
            caveats=[DOMAIN_CAVEAT, PROCEDURE_NOTE],
            result_latex=r"\mathbb{R}",
        )

    latex_parts = []
    text_parts = []

    for variable in variables:
        try:
            domain = continuous_domain(expr, variable, sp.S.Reals)
            latex_parts.append(rf"{to_latex(variable)} \in {to_latex(domain)}")
            text_parts.append(f"{variable} ∈ {domain}")
            procedure.append(
                step(
                    f"Recorte respecto de {variable}",
                    latex=rf"{to_latex(variable)} \in {to_latex(domain)}",
                    text="Las otras variables se tratan como parámetros reales.",
                )
            )
        except Exception:
            latex_parts.append(
                rf"{to_latex(variable)}:\ \text{{requiere análisis conjunto}}"
            )
            text_parts.append(f"{variable}: requiere análisis conjunto")
            procedure.append(
                step(
                    f"Recorte respecto de {variable}",
                    text="No se pudo cerrar este recorte; hace falta un análisis conjunto.",
                )
            )

    procedure.append(step("Advertencia", text=DOMAIN_CAVEAT))
    procedure.append(step("Alcance", text=PROCEDURE_NOTE))

    return make_result(
        "; ".join(text_parts),
        procedure=procedure,
        caveats=[DOMAIN_CAVEAT, PROCEDURE_NOTE],
        result_latex="\\;,\\quad ".join(latex_parts),
    )
