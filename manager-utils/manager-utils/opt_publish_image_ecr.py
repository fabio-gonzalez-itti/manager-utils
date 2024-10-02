from . import utils


def run(logger, args):
    """
    Publica una imagen Docker a un repositorio AWS Elastic Container Registry.
    Parameters:
        logger: Logger de programa.
        args: Parámetros de línea de comandos procesados.
    """
    # Control - imagen a publicar.
    image_name = utils.read_required_cmd_arg(logger, args, "image_name", "Se esperaba el parámetro nombre de imagen Docker (especificar con --image-name).")
    if ':' not in image_name:
        utils.exit_log_message(logger, "Se debe especificar la versión para la imagen.")

    # Control - datos AWS.
    aws_profile = utils.read_required_cmd_arg(logger, args, "aws_profile", "Se esperaba el parámetro perfil AWS (especificar con --aws-profile).")
    aws_region = utils.read_required_cmd_arg(logger, args, "aws_region", "Se esperaba el parámetro región AWS (especificar con --aws-region).")
    aws_ecr_repository = utils.read_required_cmd_arg(logger, args, "aws_ecr_repository", "Se esperaba el parámetro repositorio AWS ECR (especificar con --aws-ecr-repository).")

    try:
        # Publicar imagen puntual.
        cmd = utils.DockerPushEcrCmd()
        cmd.profile = aws_profile
        cmd.region = aws_region
        cmd.tag = image_name
        cmd.repository = aws_ecr_repository
        ret = cmd.run()
        logger.info(f"Docker push return code: {ret}")
    except Exception as ex:
        logger.error("Ocurrió un error ejecutando acción.")
        logger.exception(ex)
        exit(1)
