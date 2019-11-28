# SportsMatch API (backend)

## Installation guide

First clone this repository. Then install pipenv:
```
$ brew install pipenv
$ cd path/to/directory
$ pipenv --three
```

Then enter the virtual environment:
```
$ pipenv shell
$ pipenv install
```

Create a .env file in the home directory and add the following:
```
export FLASK_ENV=development
export FLASK_ENV_TEST=test
export DATABASE_URL="postgres://localhost/sportsmatch_api_db"
export JWT_SECRET_KEY=[ADD_SECRET_KEY_HERE]
export TEST_DATABASE_URL="postgres://localhost/sportsmatch_api_test_db"
```

Run database migrations:
```
$ python manage.py db upgrade
$ python manage_test.py db upgrade
```

Run the app:
```
$ python run.py
```

## User Stories

[Add here]

## Technologies used
- Python
- Pylint