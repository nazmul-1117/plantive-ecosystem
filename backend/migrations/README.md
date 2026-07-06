## Install Alembic
```shell
uv add alembic
```

## Alembic Migration
```shell
alembic init -t async migrations
```

## Alembic Revision
```shell
alembic revision --autogenerate -m "init migration"
```

## Alembic Upgrade
```shell
alembic upgrade head
```