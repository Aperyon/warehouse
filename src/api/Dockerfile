FROM python:3.8-alpine

WORKDIR /code
RUN apk add --no-cache gcc libffi-dev musl-dev postgresql-dev
RUN pip install poetry

COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false
RUN poetry install
