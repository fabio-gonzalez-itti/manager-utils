import argparse
from . import utils
from . import opt_exec
from . import opt_publish_image_ecr


def main() -> None:
    """
    Implementa la lógica central de la herramienta.
    """
    # Configuración de parámetros de línea de comandos.
    parser = argparse.ArgumentParser(prog="manager", description="Gestión remota")
    parser.add_argument("--action", type=str, required=True, choices=["exec", "publish-image-ecr"], help="Acción a realizar.")
    parser.add_argument("--cwd", type=str, required=False, help="Carpeta de trabajo para ciertas acciones que lo requieran.")
    parser.add_argument("--image-name", type=str, required=False, help="Nombre de imagen, dependiendo de la accióna a realizar puede incluir la versión de la misma.")
    parser.add_argument("--aws-profile", type=str, required=False, help="Nombre de perfil de identificación contra AWS.")
    parser.add_argument("--aws-region", type=str, required=False, help="Nombre de región de preferencia para AWS.")
    parser.add_argument("--aws-ecr-repository", type=str, required=False, help="Host de repositorio AWS ECR.")
    parser.add_argument("extras", nargs=argparse.REMAINDER, help="Valores consumidos tal cual por ciertas acciones de programa.")
    args = parser.parse_args()

    # Configuración de logger.
    logger = utils.configure_logger("manager", "/tmp/manager.log")

    if args.action == "exec":
        opt_exec.run(logger, args)
        return

    if args.action == "publish-image-ecr":
        opt_publish_image_ecr.run(args)
        return


def dump_log():
    with open("/tmp/manager.log", "r") as log:
        txt = log.read()
        print(txt)
