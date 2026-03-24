# API de Gestión de Posts y Tags (FastAPI + SQLModel)

Esta es una API RESTful construida con FastAPI y SQLModel. Diseñado para gestionar publicaciones (posts), etiquetas (tags) y usuarios, incluyendo un sistema automatizado de población de base de datos (Seeds) a través de una interfaz de línea de comandos (CLI).

## Tecnologías Principales

* **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/)
* **ORM y Base de Datos:** [SQLModel](https://sqlmodel.tiangolo.com/) (Pydantic y SQLAlchemy)
* **CLI (Semillas):** [Typer](https://typer.tiangolo.com/)
* **Seguridad:** `pwdlib` para el hashing seguro de contraseñas.

## Estructura del Proyecto

El proyecto sigue una arquitectura modular y orientada a dominios:

```text
posts-sqlmodel/
├── backend/
│   ├── app/
│   │   ├── api/v1/         # Routers y endpoints (auth, posts, tag)
│   │   ├── core/           # Configuración global (CORS, Base de datos, Configuración)
│   │   ├── models/         # Modelos de SQLModel y Pydantic
│   │   ├── seeds/          # Herramienta CLI para poblar la base de datos
│   │   └── main.py         # Punto de entrada de la aplicación FastAPI
│   └── tests/              # Entorno de pruebas automatizadas
└── README.md
```

## Instalacion y Configuración
1. Clonar el repositorio y entrar a la carpeta

    ```bash
    git clone <tu-repositorio>
    cd posts-sqlmodel
    ```

2. Crear y activar el entorno virtual

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Instalar las dependencias
    ```bash
    pip install -r requirements.txt
    ```

## Comandos Principales

1. Poblar la base de datos (Seeds)
    ```bash
    python3 -m backend.app.seeds all
    ```

2. Levantar el servidor, iniciar la API en modo desarrollo:

    ```bash
    fastapi dev backend/app/main.py
    ```