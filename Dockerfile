FROM python:3.10

RUN mkdir /hex
WORKDIR /hex

ADD alembic.ini /hex/
ADD migrations /hex/migrations/

ADD poetry.lock /hex/
ADD pyproject.toml /hex/

RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry install --no-dev


ADD app /hex/app/

CMD ["poetry", "run", "python", "-m", "app", "web"]
EXPOSE 5000