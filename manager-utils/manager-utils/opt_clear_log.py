from . import utils
from logging import Logger
from argparse import Namespace


def run(logger: Logger, args: Namespace) -> None:
    """
    Limpia el archivo de log.
    Parameters:
        logger: Logger de programa.
        args: Parámetros de línea de comandos procesados.
    """
    try:
        with open("/tmp/manager.log", "w") as logfile:
            logfile.truncate(0)
    except Exception:
        pass
