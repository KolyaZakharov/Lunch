# Lunch

## Api service for lunch management written on DRF
## Features:

### JWT authenticated
### Admin panel /admin/
### Documentation is located via /api/doc/swagger/
### Managing restaurants and employees

### Creating restaurants, menus, employees


## Installing using GitHub:
### Install Postgres and create DB
### Copy this repository, by using your terminal:
   git clone https://github.com/KolyaZakharov/Lunch.git
### Change directory to main project folder. Use this command:
    cd Cinama-project
### Install venv, and activate it by using following commands:
    python3 -m venv venv
### to activate on Windows:

    venv\Scripts\activate
### to activate on Linux:
    source venv/bin/activate
### Install dependencies (requirements):
    pip install -r requirements.txt
### Run migrations to initialize database. Use this command:
    python manage.py migrate
### Open file .env-sample and change environment variables to yours. Also rename file extension to .env
### Run server and use!
    python manage.py runserver
## Run with Docker:
### Docker should be installed
    - docker-compose build
    - docker-compose up