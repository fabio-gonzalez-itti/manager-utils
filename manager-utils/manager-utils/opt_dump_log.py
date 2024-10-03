from . import utils
from logging import Logger
from argparse import Namespace


def run(logger: Logger, args: Namespace) -> None:
    """
    Vuelva el contenido del archivo de log a la salida estandar.
    Parameters:
        logger: Logger de programa.
        args: Parámetros de línea de comandos procesados.
    """
    try:
        with open("/tmp/manager.log", "r") as logfile:
            for line in logfile:
                print(line.strip())
    except Exception:
        pass
