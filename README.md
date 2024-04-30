# API de Gestión de Paneles Solares

Esta API proporciona funcionalidades para gestionar la disposición óptima de paneles solares en un techo.

## Ejecución de la API

Sigue estos pasos para ejecutar la API en tu entorno local:

### Requisitos previos

- Python 3.x instalado en tu sistema.
- [pip](https://pip.pypa.io/en/stable/) para instalar dependencias.

### Pasos de instalación

1. Clona este repositorio en tu máquina local:

    ```bash
    git clone https://github.com/JoseAvanzada2019/solar-panels-api.git
    ```

2. Navega hasta el directorio del repositorio:

    ```bash
    cd solar-panels-api
    ```

3. Instala las dependencias utilizando pip:

    ```bash
    pip install -r requirements.txt
    ```

### Ejecución

Una vez que hayas instalado las dependencias, puedes ejecutar la API utilizando el siguiente comando:

```bash
uvicorn main:app --reload