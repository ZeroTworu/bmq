FROM python:3.10

RUN mkdir /bot
WORKDIR /bot

ADD poetry.lock /bot
ADD pyproject.toml /bot

RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry install --no-dev


ADD app /bot/app

CMD ["poetry", "run", "python", "-m", "app"]