.PHONY: lint test infra install-deps

lint:
	poetry run flake8 app/

test:
	poetry run pytest app/

infra:
	docker-compose -f docker/docker-compose.infra.yaml up --remove-orphans

app:
	docker build . -t mq_bot:latest
	docker-compose -f docker/docker-compose.app.yaml up --remove-orphans

install-deps:
	pip3 install --upgrade pip
	pip3 install poetry
	poetry install