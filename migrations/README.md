# Database Migrations

## Introduction
This folder contains database migration scripts, currently managed by Alembic.


### Generating Migrations
To create a new migration, run:
```bash
alembic revision --autogenerate -m "description of the change"
```
This will generate a new migration script in the **versions** directory.
Review and edit this script as needed.


### Applying Migrations
To apply migrations, run:
```bash
alembic upgrade head
```


### Downgrading Migrations
To revert the last migration, run:
```bash
alembic downgrade -1
```
