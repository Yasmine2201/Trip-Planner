# Trip-Planner
Here is a small overview of our brilliant Engineering Project

## Introduction
This project is a web application that helps users to plan their trips and connect with new people.

## Features

## Technologies
### - Backend: Django :

Please add a folder **.venv** at the root of this folder [back](.), then place yourself in the created folder and install the dependencies listed in the [`requirements.txt`](requirements.txt) file using the following command:
```bash
  pip install -r requirements.txt
```
> You can also configure your IDE to use the virtual environment and add a configuration to run the Django server. 

  - Remember to run the following command to start a new Django app:
    ```bash
    python manage.py startapp <app_name>
    ```
  - Here are the credentials to access the Django admin page:
    - Username: admin
    - Password: efrei
    - To run the server, please run the following command:
        ```bash
        python manage.py runserver
        ```
    
- Database: 
  - SQLite : for the development phase:
    - Please run the following command to create your local database:
      ```bash
      python manage.py migrate
      ``` 
    - Ensure that `db.sqlite3` file has been added to the project directory after running the previous command.
    - Each time you create a new model, please run the following command to create a new migration file and apply the changes to the database:
      ```bash
      python manage.py makemigrations
      python manage.py migrate
      ```
      
  - XXX : for the production phase
