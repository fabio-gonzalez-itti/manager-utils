from . import utils
from logging import Logger
from argparse import Namespace


def run(logger: Logger, args: Namespace) -> None:
    """
    Escribe en archivo de log.
    Parameters:
        logger: Logger de programa.
        args: Parámetros de línea de comandos procesados.
    """
    # Control - mensaje a escribir.
    msg = utils.read_required_cmd_arg(logger, args, "msg", "Se esperaba el parámetro mensaje (especificar con --msg).")
    logger.info(msg)
