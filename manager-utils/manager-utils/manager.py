import argparse
from . import utils
from . import opt_log
from . import opt_clear_log
from . import opt_dump_log
from . import opt_exec
from . import opt_publish_image_ecr
from . import opt_check_image_exists

def main() -> None:
    """
    Implementa la lógica central de la herramienta.
    """
    # Configuración de parámetros de línea de comandos.
    parser = argparse.ArgumentParser(prog="manager", description="Gestión remota")
    parser.add_argument("--action", type=str, required=True, choices=["log", "clear-log", "dump-log", "exec", "check-image-exists", "publish-image-ecr"], help="Acción a realizar.")
    parser.add_argument("--cwd", type=str, required=False, help="Carpeta de trabajo para ciertas acciones que lo requieran.")
    parser.add_argument("--msg", type=str, required=False, help="Texto arbitrario para ciertas acciones que lo requieran.")
    parser.add_argument("--image-name", type=str, required=False, help="Nombre de imagen, dependiendo de la accióna a realizar puede incluir la versión de la misma.")
    parser.add_argument("--aws-profile", type=str, required=False, help="Nombre de perfil de identificación contra AWS.")
    parser.add_argument("--aws-region", type=str, required=False, help="Nombre de región de preferencia para AWS.")
    parser.add_argument("--aws-ecr-repository", type=str, required=False, help="Host de repositorio AWS ECR.")
    parser.add_argument("extras", nargs=argparse.REMAINDER, help="Valores consumidos tal cual por ciertas acciones de programa.")
    args = parser.parse_args()

    # Configuración de logger.
    logger = utils.configure_logger("manager", "/tmp/manager.log")

    if args.action == "log":
        opt_log.run(logger, args)
        return

    if args.action == "clear-log":
        opt_clear_log.run(logger, args)
        return

    if args.action == "dump-log":
        opt_dump_log.run(logger, args)
        return

    if args.action == "exec":
        opt_exec.run(logger, args)
        return

    if args.action == "check-image-exists":
        opt_check_image_exists.run(logger, args)
        return

    if args.action == "publish-image-ecr":
        opt_publish_image_ecr.run(logger, args)
        return

    raise RuntimeError("No debe ocurrir - IllegalState")
