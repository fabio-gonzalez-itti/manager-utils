# Manager Utils
Herramienta que permite simplificar operaciones relacionadas al despliegue de aplicaciones en entornos cloud.

## Requerimientos
- Python 3.10 o superior.
- AWS CLI, versión `2.x.x` o superior.

## Instalación
Ver la sección de [releases](https://github.com/fabio-gonzalez-itti/manager-utils/releases) para conocer la última versión disponible. Se disponibiliza el módulo tanto como *source distribution* como *build distribution*.

Ejemplo de instalación con `pip`:

```
pip install https://github.com/fabio-gonzalez-itti/manager-utils/releases/download/v0.0.3/manager_utils-0.0.3-py3-none-any.whl
```

## Modo de Uso
La herramienta permite ejecutar acciones pre-definidas que encapsulan operaciones generales que se llevan a cabo durante el despliegue de aplicaciones en entornos *cloud*.

## Mejoras a Futuro
- Dar soporte a otros tipos de identidad AWS. De momento solo se utilizan perfiles de usuarios IAM.