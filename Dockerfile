FROM python:3.7

RUN apt-get update && \
	apt-get install python3-pip git -y && \
	pip3 install pipenv && \
	apt-get clean

RUN mkdir /app
WORKDIR /app

ADD Pipfile /app
ADD Pipfile.lock /app

ARG pipenv_arg=
RUN pipenv install --system $pipenv_arg

ADD ./swap/ /app

ENV DJANGO_SETTINGS_MODULE=swap.settings.production

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]