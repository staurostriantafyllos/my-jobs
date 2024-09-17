# FastAPI & PostgreSQL Backend Template

This repository provides a robust template for building backend applications using
FastAPI and PostgreSQL. It serves as a starting point for creating scalable
and efficient web services with Python.

<details open>
    <summary><h2>Features</h2></summary>

- **FastAPI**: High-performance, asynchronous web framework for building APIs.
- **SQLModel**: Combining SQLAlchemy and Pydantic, SQLModel provides fast and flexible
database interaction with type-safe models.
- **PostgreSQL**: Robust relational database used for persistent data storage.
- **Database Session Management**: Sessions are managed using FastAPI's dependency
injection system, ensuring proper lifecycle management that commits on success and
rolls back in case of errors.
- **CLI Tools**: Command-line interface (CLI) built with Click to easily manage
and automate tasks like running migrations, starting services, etc.
- **Secrets Management**: AWS Secrets Manager is used for securely handling sensitive
information (e.g., database credentials).
- **Authentication & Security**: Token-based authentication using JWT, ensuring secure
and stateless communication between clients and the backend, as well as custom token
authentication for administrative API calls and service to service communication.
- **Caching**: Configurable caching, supporting both in-memory and Redis-based backends
for better performance and scalability.
- **Separation of Concerns**: Enforce a clean architecture that separates business
logic, data models, and API routes, facilitating easy maintenance and extensibility.
- **Code Formatting with Black**: Ensures consistent code style across the project by
automatically formatting Python code to follow the PEP 8 standard. Black helps keep the
code clean and readable with minimal configuration, promoting a uniform development environment.
- **Database Migrations**: Seamless database schema management and migrations using Alembic.
- **Dockerized**: Fully containerized with Docker for simplified deployment and
development workflows.

</details>

<details open>
    <summary><h2>Code Structure</h2></summary>

```
.
├── Dockerfile
├── README.md
├── alembic.ini
├── migrations
│   ├── README.md
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── ...
├── requirements.txt
├── setup.py
└── template_project
    ├── __init__.py
    ├── api
    │   ├── __init__.py
    │   ├── __main__.py
    │   ├── auth.py
    │   ├── cache.py
    │   ├── cli.py
    │   ├── dependencies.py
    │   ├── exceptions.py
    │   ├── factories.py
    │   └── routers
    │       ├── __init__.py
    │       ├── accounts.py
    │       └── system.py
    ├── cli.py
    ├── config.py
    ├── db
    │   ├── __init__.py
    │   ├── controllers
    │   │   ├── __init__.py
    │   │   └── accounts.py
    │   └── factories.py
    ├── models
    │   ├── __init__.py
    │   ├── database.py
    │   └── validation.py
    ├── secrets.py
    └── security.py
```
</details>

<details open>
    <summary><h2>Development</h4></summary>


### Prerequisites

#### Python Installation

Ensure Python 3.11 is installed on your machine. Check your Python version by running:

```bash
python --version
```

#### Virtual Environment

Set up and activate a virtual environment with one of the following ways:

##### Using venv

```bash
python -m venv venv
source ./venv/bin/activate
```

##### Using pyenv

```bash
pyenv virtualenv 3.11 template-project
pyenv shell template-project
```

#### Installing Dependencies

To install required packages for the project, execute:

```bash
pip install -r requirements.txt && pip install -e .
```

#### Environment

First, copy `.env.sample` file to `.env` and replace the environment variables
accordingly.

```bash
cp .env.sample .env
```

#### Database

To setup the database for the project:

* 1. Create a database using a database administration tool (e.g. DBeaver)

* 2. Set the environment variables for the database

* 3. Use alembic to setup the schema:

    ```bash
    alembic upgrade head
    ```

#### Running the Application

You can see the available commands and their options by running:

```bash
template-cli --help
```

#### Building the docker image

To build the docker image, run the following command:

```bash
docker build -t project-template:latest .
```

#### Running the Application in Docker

To run the application in a docker container, execute:

```bash
docker run -it --rm project-template:latest template-cli --help
```

To run the api server using docker, execute:

```bash
docker run -it --rm --env-file=.env -p 8000:8000 project-template:latest template-cli api start
```

Yoy can now access the api interactive documentation at `http://localhost:8000/docs`.

</details>
