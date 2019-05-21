# Gameweb [![Build Status](https://travis-ci.org/dawidbudzynski/gameweb_python_django.svg?branch=master)](https://travis-ci.org/dawidbudzynski/gameweb_python_django)



## General info
A web application made using Python 3, Django 2, Bootstrap and REST API.
It's website about technology where user can find interesting news (displayed used API), 
add new games to database and find new titles (using recommendation feature).

## Main functions
* displaying gaming and tech news - updated every few hours using API
* adding new users and games to database
* recommending new games based on user's preferences

## Technologies
* Python 3
* Django 2.0
* Bootstrap
* REST API

## Setup
To run this project:
1. Create PostgreSQL database
2. Rename settings.ini.example to settings.ini and fill required fields. 
3. Install required libraries using pip:
    ```
    $ pip install -r requirements.txt
    ```
4. To run your local server use command: 
    ```
    $ python manage.py runserver
    ```
    
To run asynchronous tasks:
1. Install Redis
2. Start Redis server:
    ```
    $ redis-server
    ```
3. Open new terminal tab
4. Go to project root
5. Start Celery worker:
    ```
    $ celery -A final_project_coderslab worker -l info
    ```

To run periodic tasks:
1. Open new terminal tab
2. Go to project root
3. Start Celery beat:
    ```
    $ celery -A final_project_coderslab beat -l info
    ```

## Demo
## http://dawidb.pythonanywhere.com

**Gaming and tech news updated every few hours using API from sites like: Polygon, IGN, The Verge and TechRadar**

![alt text](https://raw.githubusercontent.com/dawidbudzynski/game_picker_python_django/master/examples/example1.png)


**Games recommendation based on user's preferences**

![alt text](https://raw.githubusercontent.com/dawidbudzynski/game_picker_python_django/master/examples/example2.png)

