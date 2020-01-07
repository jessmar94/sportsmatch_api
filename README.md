# SportsMatch Backend
## Introduction
SportsMatch encourages people to be more active by enabling them to find fellow racket sports fans to play a game with. This application serves as the backend for our final project at Makers Academy. You can find our frontend app [here](https://github.com/smasonmalik/sportsmatch_react).

The team consisted of:
- [Sid Mason-Malik](https://github.com/smasonmalik)
- [Duncan Skinner](https://github.com/Duncan9099)
- [Jess Marais](https://github.com/jessmar94)
- [Pam Mezue](https://github.com/Mezela)
- [Dom Tunstill](https://github.com/domtunstill)
- [Vijay Kurian](https://github.com/kurianvijay)

Technologies used
- Python
- Flask
- Pylint (to check code quality)
- Pytest (unit testing)
- BCrypt
- CircleCI
- SQLAlchemy
- PostgreSQL

We have 31 passing tests with an 89% test coverage. 

The project has been deployed to [Heroku](http://sportsmatch-app.herokuapp.com/).   

## Trello
https://trello.com/b/Twlp2CTz/sportsmatch

## Documented Learning
https://github.com/jessmar94/sportsmatch_api/wiki

## How to Install and Run
1. Clone this repository.
2. Install pipenv:
```
$ brew install pipenv
$ cd path/to/directory
$ pipenv --three
```
3. Enter the virtual environment:
```
$ pipenv shell
$ pipenv install
```
4. Create an .env file in the home directory and add the following:
```
export FLASK_ENV=development
export FLASK_ENV_TEST=test
export DATABASE_URL="postgres://localhost/sportsmatch_api_db"
export JWT_SECRET_KEY=[ADD_SECRET_KEY_HERE]
export TEST_DATABASE_URL="postgres://localhost/sportsmatch_api_test_db"
```
5. Run database migrations:
```
$ python manage.py db upgrade
$ python manage_test.py db upgrade
```
6. Run the app:
```
$ python run.py
```
## How to Run Tests
1. Run the following command in your terminal:
```
$ py.test --cov=src --cov-config .coveragerc --cov-report term-missing
```

### Check code quality

To check code quality for all python files in a directory and it's subdirectories
```
$  pylint **/*.py
```

## User Stories
```bash
As a keen tennis player,
So I check out SportsMatch,
I want to be able to signup.
```
```bash
As a keen tennis player,
So I can keep my account secure,
I want to be able to login and logout.
```
```bash
As a keen tennis player,
So I can always keep my information up-to-date,
I want to be able to update my information on my profile.
```  
```bash
As a keen tennis player,
So I can find a fellow racket-sport fan,
I want to be able to see other players on the platform.
```
```bash
As a keen tennis player,
So I can plan my week,
I want to be able to see all my games coming up.
```
```bash
As a keen tennis player,
So I can arrange a game of tennis with someone,
I want to be able to request a game with a player.
```
```bash
As a keen tennis player,
So I can accept a fellow tennis player game request,
I want to be able to respond to their game request.
```
```bash
As a keen tennis player,
So I can keep track of my wins,
I want to be able to record who won the game I organised.
```
```bash
As a keen tennis player,
So I can feel proud of all my wins,
I want to be able to see the results of my games.
```
```bash
As a keen tennis and squash player,
So that I can also find squash players,
I want to be able to choose my sport from a few options.
```

## Database Tables
1. Players Table
   ID | first_name | last_name | email | password | ability | gender | dob | postcode | rank_points | profile_image | bio | sport

2. Games Table
   ID | opponent_id | organiser_id | status | game_date | game_time

3. Results Table
   ID | game_id | winner_id | loser_id | result_confirmed

4. Messages Table
   ID | game_id | sender_id | organiser_id | opponent_id | content

## Domain Relationships
1. Players can have many games
1. Players can have many results
1. Players can have many messages

2. Games can have one result
2. Games can have many players

3. Results can have many players
3. Results can have one game

4. Messages can have many players
4. Messages can have one game

## Additional Features
If we had more time, we would have looked to implement the following features:
- Ability to submit the score of the game.
- Ability to register with multiple sports, rather than picking just one.
- Ability for player to input their availability for other players to see - this would require creating an Availability table.
- Ability to register the result of a game as a draw.
- Add in a weather API to help players pick the best day to play.
