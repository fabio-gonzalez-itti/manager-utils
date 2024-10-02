import argparse
import logging
import subprocess
import os
import io
import uuid


def exit_log_message(logger: logging.Logger, msg: str) -> None:
    """
    Emite un mensaje de texto en el logger de programa y termina el proceso actual.
    """
    logger.error(msg)
    exit(1)


def exit_return_code_unexpected(ret: int, expected: int = 0) -> None:
    """
    Evalúa el código de retorno para un comando ejecutado y termina el proceso actual
    en caso de no coincidir con el valor esperado.
    """
    if ret != expected:
        exit(1)


def coalesce_str(*arg) -> str | None:
    """
    Retorna el primer valor de texto no nulo ni vacío. Caso contrario se retorna None.
    """
    for el in arg:
        if el != None and el != "":
            return el
    return None


def configure_logger(logger_name: str, logger_file: str) -> logging.Logger:
    """
    Configura un nuevo logger.
    """
    logger = logging.getLogger(logger_name)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(logger_file, mode="w")]
    )
    return logger


def read_required_cmd_arg(logger: logging.Logger, args: argparse.Namespace, argname: str, msg: str) -> str:
    """
    Obtiene el valor de un argumento mandatorio de línea de comandos. Caso
    contrario termina el proceso actual.
    """
    if argname not in args:
        exit_log_message(logger, msg)

    value = args.__dict__[argname]
    if value is None or value == "":
        exit_log_message(logger, msg)

    return value.strip()


def read_optional_cmd_arg(args: argparse.Namespace, argname: str, default: str = "") -> str:
    """
    Obtiene el valor de un argumento opcional de línea de comandos. Se puede indicar un valor por
    defecto si aplica.
    """
    if argname not in args:
        return default

    value = args.__dict__[argname]
    if value is None or value == "":
        return default

    return value.strip()


def delete_file(fd: io.FileIO | str) -> bool:
    """
    Intenta eliminar un archivo.
    """
    try:
        if isinstance(fd, str):
            os.unlink(fd)
        elif isinstance(fd, io.FileIO):
            os.unlink(fd.name)
        return True
    except Exception:
        return False


class DockerTagCmd:
    """
    Abstrae el comando de tagging de imagenes Docker.

    Attributes:
        tag_from    Tag de imagen origen.
        tag_to      Tag para imagen destino.
    """
    tag_from: str
    tag_to: str

    def __init__(self):
        self.tag_from = ""
        self.tag_to = ""

    def _to_cmd(self) -> list[str]:
        args = list()
        args.append("docker")
        args.append("tag")
        args.append(self.tag_from.strip())
        args.append(self.tag_to.strip())
        return args

    def run(self) -> int:
        tempfile = None
        try:
            with open("/tmp/output", "w") as tempfile:
                proc = subprocess.run(
                    self._to_cmd(),
                    stderr=tempfile,
                    stdout=tempfile
                )
                return proc.returncode
        finally:
            delete_file(tempfile)


class DockerPushEcrCmd:
    """
    Abstrae la operación de publicación de imagenes Docker a un repositorio 
    Elastic Container Registry de Amazon.

    Attributes:
        profile     Perfil AWS para uso con aws cli.
        region      Región a considerar para uso con aws cli.
        repository  Nombre de host/dominio para repositorio ECR.
        tag         Tag de imagen a publicar.
    """
    profile: str
    region: str
    repository: str
    tag: str

    def __init__(self):
        self.profile = ""
        self.region = ""
        self.repository = ""
        self.tag = ""

    def run(self) -> int:
        # Construir comando principal agregando multiples comandos en uno solo.
        cmds = [
            ["aws", "ecr", "get-login-password", "--profile", self.profile, "--region", self.region, "|", "docker", "login", "--username", "AWS", "--password-stdin", self.repository],
            ["docker", "tag", self.tag, f"{self.repository}/{self.tag}"],
            ["docker", "push", f"{self.repository}/{self.tag}"],
            ["docker", "logout"]
        ]
        cmd = " && ".join([" ".join(x) for x in cmds])

        # Ejecutar comando principal.
        tempfile = None
        try:
            with open(f"/tmp/{str(uuid.uuid4())}", "w") as tempfile:
                proc = subprocess.run(
                    [cmd],
                    shell=True,
                    stderr=tempfile,
                    stdout=tempfile
                )
                return proc.returncode
        finally:
            delete_file(tempfile)
