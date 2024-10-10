from . import utils
import logging
import argparse
import docker


def resolve_docker_context_socket() -> str:
    """
    Obtiene el nombre de socket para el contexto docker actualmente activo.
    """
    try:
        # Determinar nombre de contexto actual.
        ret, output = utils.simple_exec(["docker", "context", "show"])
        if ret == 0 and output != "":
            context = output.strip()
            # Determinar socket para contexto.
            ret, output = utils.simple_exec(["docker", "context", "ls"])
            if context in output:
                lines = output.splitlines()
                line = list(filter(lambda line: context in line, lines))
                _, socket = line[0].strip().split("unix:///")
                return f"unix://{socket}"
    except Exception:
        return ""


def run(logger: logging.Logger, args: argparse.Namespace):
    """
    Verifica si una imagen Docker existe, inicialmente, en el repositorio local.
    Parameters:
        logger: Logger de programa.
        args: Parámetros de línea de comandos procesados.
    """
    # Control - imagen a verificar.
    image_name = utils.read_required_cmd_arg(logger, args, "image_name", "Se esperaba el parámetro nombre de imagen Docker (especificar con --image-name).")

    # Log level actual.
    # NOTE: Se desactivan los logs ya que el sdk Docker emite logs innecesarios.
    log_level = logger.getEffectiveLevel()
    logging.disable(logging.CRITICAL)

    try:
        # Buscar imagen puntual.
        docker_socket = resolve_docker_context_socket()
        client = docker.DockerClient(base_url=docker_socket)
        try:
            client.images.get(image_name)
        except docker.errors.ImageNotFound:
            raise RuntimeWarning("Imagen no encontrada.")
    except Exception as ex:
        logging.disable(log_level)
        logger.error("Ocurrió un error verificando si imagen existe.")
        logger.exception(ex)
        exit(1)
    finally:
        logging.disable(log_level)
