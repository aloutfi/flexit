![platform-version](https://img.shields.io/badge/python-3.10.2-1666a9)
![formatter](https://img.shields.io/badge/formatter-Black-000000)
![flexit-ci](https://github.com/aloutfi/flexit/actions/workflows/flexit-ci.yml/badge.svg)

# flexit

This package represents the persistence and business logic layers for flexit. 
It utilizes SQLAlchemy for database transactions and Pydantic for data transfer objects.

The project uses poetry for packaging functionality and pytest for its tests.

# Installation

## As a dependency
You can install flexit as you would any other python package.
```bash
pip install https://github.com/aloutfi/flexit/raw/main/dist/flexit-1.0.0-py3-none-any.whl
```
Then, add the `DATABASE_URL` as an environment variable.

## Development

- Install python dependencies: `poetry install`
- copy environment variables so you can safely add secrets if necessary: `cp settings.ini.in settings.ini`
- build the database: `make build`
  - You can rebuild the database with `make rebuild`

#### If you do not wish to use the Makefile...

If you do not wish to use the Makefile, you can configure local setup via docker-compose

```bash
docker-compose up
```
Set the `DATABASE_URL` in the `settings.ini` file if you are not using the docker-compose setup.

Finally, load the initial data into the database:
```bash
python -c 'from flexit.config import init_db; init_db(True)'
```