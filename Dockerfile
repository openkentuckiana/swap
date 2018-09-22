FROM python:3.7

RUN apt-get update && \
	apt-get install binutils libproj-dev gdal-bin libgeoip1 python-gdal -y && \
	apt-get install python3-pip git -y && \
	pip3 install pipenv && \
	apt-get clean

RUN mkdir /app
WORKDIR /app

ADD Pipfile .
ADD Pipfile.lock .

# arg to pass to pipenv. useful for passing in `dev` when dev dependencies are needed.
ARG pipenv_arg=
RUN pipenv install --system --skip-lock $pipenv_arg

ADD ./swap/ /app

ENV DJANGO_SETTINGS_MODULE=swap.settings.production

CMD /app/docker-entrypoint.sh