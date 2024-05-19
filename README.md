# Bug Tracker

[![CI/CD Pipeline](https://github.com/Jharopa/bug-tracker-fyp/actions/workflows/cicd.yml/badge.svg)](https://github.com/Jharopa/bug-tracker-fyp/actions/workflows/cicd.yml)

This repository contains the source code for a Django based bug tracking web application created as part of the major project module for the course BSc. Contemparary Software Development at ATU Donegal Letterkenny.

## Running Application

### Docker (Recommended)
The perfered method to run the application is to use Docker which requires Both Git and Docker to be installed on the machine being used.
### Setps
* Run `git clone https://github.com/Jharopa/bug-tracker.git` to clone the respoitory to local machine.
* Navigate into the newly cloned respostiory's directory and create a copy of the `.env.sample` calling it `.env`
* Update the contents of the copied `.env` file setting `DJANGO_DEBUG=` to true and `DJANGO_SECRET_KEY=` to a secret key of your choice.
* From the same directory run the following docker compose command `docker compose up -d --build` (Please ensure that no application docker or otherwise is bound to localhost port 80 before running this).
* To create a superuser for the application which will allow you to login to both the application and the Django admin area to create further users run the commnand `docker exec -it bug-tracker-web-1 python manage.py createsuperuser` and follow the prompts on screen.
* Navigate to [this URL](http://localhost) within a browser and use the credentails created previously to login. You can also access the Django admin from [this URL](http://localhost/admin) and login there for access to the Django admin area.

### Dockerless
The application can also be ran on a machine without the use of Docker, however this does require the machine to have python 3.11 or later installed.
### Steps
* Run `git clone https://github.com/Jharopa/bug-tracker.git` to clone the respoitory to local machine.
* Create two environment variables within your machines OS `DJANGO_DEBUG` with the value of true and `DJANGO_SECRET_KEY` with the value of a secret key of your choice.
* Navigate to the clone repository's directory and run the command `python -m venv venv` to create a python virtual environment.
* To activate the virtual environment run the command `source venv/bin/activate` on a linux machine or `venv/bin/activate.bat` on a windows machine.
* Install the projects requirements by then running `pip install -r bug_tracker\requirements.txt`
* To create a superuser for the application which will allow you to login to both the application and the Django admin area to create further users run the commnand `python bug_tracker\manage.py createsuperuser` and follow the prompts on screen.
* To then start up the application run the command `python bug_tracker\manage.py runserver`.
* Navigate to [this URL](http://localhost) within a browser and use the credentails created previously to login. You can also access the Django admin from [this URL](http://localhost/admin) and login there for access to the Django admin area.
