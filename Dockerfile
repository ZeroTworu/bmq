FROM python:3.10

RUN useradd -u 1337 bot --create-home
USER bot

WORKDIR /home/bot

ADD poetry.lock /home/bot
ADD pyproject.toml /home/bot

ENV PATH="$PATH:/home/bot/.local/bin"

RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry install --only main

ADD app /home/bot/app

CMD ["poetry", "run", "python", "-m", "app"]