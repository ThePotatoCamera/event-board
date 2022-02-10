# Información importante

[![Build docker](https://github.com/ThePotatoCamera/event-board/actions/workflows/docker-image.yml/badge.svg)](https://github.com/ThePotatoCamera/appcenas/actions/workflows/docker-image.yml)

## Requirements

Python 3.8 is required at least.

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
