# Event boards written in Django!

[![Build docker](https://github.com/ThePotatoCamera/event-board/actions/workflows/docker-image.yml/badge.svg)](https://github.com/ThePotatoCamera/event-board/actions/workflows/docker-image.yml)

## Requirements

Python 3.8 is required at least.

## Installation

You just have to copy the `docker-compose.yml` file in your machine, change the environment variables to your needs, generate a `DJANGO_SECRET` and `docker-compose up` the whole thing.

Remember that it **requires** [the latest version of docker-compose](https://docs.docker.com/compose/install/#install-compose).

## Setting up the environment

We use `pipenv`. To install it, run the following command:

`sudo pip install pipenv`

Once you have `pipenv` and Python 3.8, just run:

`pipenv install`

To access the newly created environment and load [the environment vars](#environment-variables) automagically:

`pipenv shell`

Now you just have to prepare the tables in the database (inside the environment):

`./manage.py migrate`

## Environment variables
- Django environment
  - DJANGO_SETTINGS_MODULE (_event-board.config._**local | production**)
- Database
  - DATABASE_DB
  - DATABASE_USER
  - DATABASE_PASS
  - DATABASE_HOST
  - DATABASE_PORT
- Redis
  - REDIS_HOST

**You can also load a `.env`, pipenv will recognise and use it**

## License
See `LICENSE`
