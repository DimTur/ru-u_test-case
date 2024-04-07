FROM python:3.11-slim

WORKDIR /ru-u_test-case

RUN pip install poetry && poetry config virtualenvs.create false

COPY ./pyproject.toml .
RUN poetry install --no-dev

COPY . .

RUN chmod a+x docker/*.sh