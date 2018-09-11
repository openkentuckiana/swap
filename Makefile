APP_NAME := "swap"
IMAGE_NAME := "tbd/$(APP_NAME)"
GIT_HASH := $(shell git rev-parse --short HEAD)
GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
#tag used to set release candidate to publish version to s3
GIT_TAG := $(shell git describe --tags)

init:
	WORKON_HOME=./.venv/ \
	pipenv install --dev

clean-local-dependencies:
	docker rm -f postgres-$(GIT_HASH)

local-dependencies: clean-local-dependencies
	docker run -d --name postgres-$(GIT_HASH) -e POSTGRES_PASSWORD=pass postgres:9.6.5-alpine

run: local-dependencies
	pipenv run \
		swap/manage.py runserver \
			--settings=swap.settings.local
test:
	pipenv run swap/manage.py test