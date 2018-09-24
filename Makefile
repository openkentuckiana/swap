# Thanks to https://gist.github.com/miketheman/e17a9e5c6fedac4c34383931c01beb28

CURRENT_DIRECTORY := $(shell pwd)
GIT_SHA := $(shell git rev-parse HEAD)

help:
	@echo "Docker Compose Help"
	@echo "-----------------------"
	@echo ""
	@echo "Run tests to ensure current state is good:"
	@echo "    make test"
	@echo ""
	@echo "If tests pass, add fixture data and start up the app:"
	@echo "    make begin"
	@echo ""
	@echo "Really, really start over:"
	@echo "    make clean"
	@echo ""
	@echo "See contents of Makefile for more targets."

begin: migrate fixtures start

start:
	@docker-compose up -d
	@echo "Ready at http://localhost/"

stop:
	@docker-compose stop

status:
	@docker-compose ps

restart: stop start

clean: stop
	@docker-compose rm --force
	@docker-compose down --volumes
	@find . -name \*.pyc -delete

build:
	@docker-compose build app

test: 
	@docker-compose run -e DJANGO_SETTINGS_MODULE=swap.settings.test --rm app ./wait-for-it.sh db:5432 --timeout=60 -- python ./manage.py test --keepdb

testwithcoverage: build 
	@docker-compose run -e DJANGO_SETTINGS_MODULE=swap.settings.test -e GIT_SHA=$(GIT_SHA) -e CODECOV_TOKEN=$(CODECOV_TOKEN) --rm app bash -c "./wait-for-it.sh db:5432 --timeout=60 -- coverage run --source='.' ./manage.py test --keepdb && codecov --commit=$(GIT_SHA)"

makemigrations:
	@docker-compose run --rm app ./wait-for-it.sh db:5432 --timeout=60 -- python ./manage.py makemigrations

migrate:
	@docker-compose run --rm app ./wait-for-it.sh db:5432 --timeout=60 -- python ./manage.py migrate

fixtures:
	@docker-compose run --rm app ./wait-for-it.sh db:5432 --timeout=60 -- ./load-all-fixtures.sh

flushdb:
	@docker-compose run --rm app ./wait-for-it.sh db:5432 --timeout=60 -- python ./manage.py flushdb

cli:
	@docker-compose run --rm app bash

tail:
	@docker-compose logs -f

.PHONY: start stop status restart clean build test makemigrations migrate fixtures flushdb cli tail