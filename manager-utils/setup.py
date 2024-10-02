
from setuptools import setup

setup(
    name='manager-utils',
    version='0.0.1',
    description='Herramienta que permite simplificar operaciones relacionadas al despliegue de aplicaciones en entornos cloud.',
    url='https://github.com/fabio-gonzalez-itti/manager-utils',
    author='Fabio Antonio González Sosa',
    author_email='fabio.gonzalez@itti.digital',
    license='MIT',
    packages=['manager-utils'],
    install_requires=[
        'boto3==1.34.120'
    ]
)
