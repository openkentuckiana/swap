APP_NAME := "swap"
IMAGE_NAME := "tbd/$(APP_NAME)"
GIT_HASH := $(shell git rev-parse --short HEAD)
GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
GIT_TAG := $(shell git describe --tags)

# Probably deprecating this in favor of docker-compose, for cross-platform reasons.
# Need to update Travis CI before this can go away.

init:
	WORKON_HOME=./.venv/ \
	pipenv install --dev

clean-local-dependencies:
	docker rm -f /postgres-$(GIT_HASH)

local-dependencies: clean-local-dependencies
	docker run -d \
		--name postgres-$(GIT_HASH) \
		-e POSTGRES_PASSWORD=pass postgres:9.6.5-alpine

migrate:
	pipenv run \
		swap/manage.py migrate

run: local-dependencies migrate
	pipenv run \
		swap/manage.py runserver \
			--settings=swap.settings.local
test:
	pipenv run swap/manage.py test