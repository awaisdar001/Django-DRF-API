Django Rest Framework API
================================
This is Python REST API that calls an external API service to get information about books. Additionally, it implements a simple CRUD (Create, Read, Update, Delete) API with a local sql database.

Compatibility
-------------
This project is developed and tested with `python2.7`

Prerequisites
-------------
In order to setup this project, make sure you have python's `pip` package installed on your system.


FYI
---
You should run all ``make`` commands described below on your local machine, within virtualenvs.

Getting Started
---------------
1. Clone the Reop in your local machine.

       git clone https://github.com/awaisdar001/Django-DRF-API.git

2. Create a [virtualenv](https://virtualenv.pypa.io/en/latest/installation/) and activate it.

       virtualenv venv
       source venv/bin/activate

3. Install the requirements inside of a `Python virtualenv`.
   
       make requirements
4. Run migrations and setup the database locally.
   
       make update_db
5. [Optional] Create a superuser to get admin access to add/update data manually
   
       make create_su

6. Run tests and verify everything has setup correctly.
   
       make test

7. Generate books data in local database.

       make generate_books

8. Run the development server
   
       make dev.up

| Service             | URL                                       |
| -------------       | -------------                             |
| External Books API  | http://localhost:8080/api/external-books  |
| Books API           | http://localhost:8080/api/v1/books/       |
| API Admin           | http://localhost:8080/admin               |


