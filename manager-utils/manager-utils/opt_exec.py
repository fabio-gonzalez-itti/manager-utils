from . import utils
from logging import Logger
from argparse import Namespace
import subprocess
import os
import uuid


def run(logger: Logger, args: Namespace) -> None:
    """
    Ejecuta un comando arbitrario.
    Parameters:
        logger: Logger de programa.
        args: Parámetros de línea de comandos procesados.
    """
    # Control - directorio de trabajo.
    cwd = utils.read_optional_cmd_arg(args, "cwd", ".")

    # Control - parámetros de comando concreto.
    extras = args.extras
    if extras == None or len(extras) == 0 or extras[0] != "--":
        utils.exit_log_message(logger, "Error: Se esperaban parámetros de exec (especificar con -- <args>).")

    # Ejecutar comando.
    tempfile = None
    try:
        with open(f"/tmp/{str(uuid.uuid4())}", "w") as tempfile:
            proc = subprocess.run(
                extras[1:],
                env=os.environ.copy(),
                cwd=cwd,
                stderr=tempfile,
                stdout=tempfile
            )
            ret = proc.returncode
            logger.info(f"Exec return code: {ret}")
            utils.exit_return_code_unexpected(ret)
    except Exception as ex:
        logger.error("Ocurrió un error ejecutando acción.")
        logger.exception(ex)
        exit(1)
    finally:
        utils.delete_file(tempfile)
