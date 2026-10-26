# diccionario que asocia el nombre de cada operacion con su funcion.
# las rutas buscan aqui, asi agregar una operacion nueva no exige tocar routes.py
OPERATIONS = {}


# decorador: registra la funcion bajo el nombre dado.
# toda operacion recibe (expr, params) y devuelve un dict con
# "result" y "result_latex" (ver common.make_result)
def register(name):

    def wrapper(func):
        OPERATIONS[name] = func
        return func

    return wrapper


# busca la operacion por nombre y la ejecuta.
# params es el json que mando el frontend (punto, variable, etc.)
def run(name, expr, params):

    if name not in OPERATIONS:
        raise KeyError(name)

    return OPERATIONS[name](expr, params)
