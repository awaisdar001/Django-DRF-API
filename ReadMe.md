Django RestFramework API
================================
This is Python REST API that calls an external API service to get information about books. Additionally, it implements a simple CRUD (Create, Read, Update, Delete) API with a local sql database.

Prerequisites
-------------
In order to setup this project, make sure you have python's `pip` peckage installed on your system.

FYI
---
You should run all ``make`` commands described below on your local machine, within virtualenvs.

Getting Started
---------------
1. Clone the Reop in your local machine.

       git clone https://github.com/awaisdar001/Django-DRF-API.git

2. Install the requirements inside of a `Python virtualenv`_.
   
       make requirements
3. Run migrations and setup the database locally. 
   
       make update_db
4. [Optional] Create a superuser to get admin access to add/update data manually
   
       make create_su

5. Run tests and verify everything has setup correctly.
   
       make test
6. Run the development server
   
       make dev.up
7. Generate books data in local database.

       make generate_books

| Service             | URL                                       |
| -------------       | -------------                             |
| External Books API  | http://localhost:8080/api/external-api/   |
| Books API           | http://localhost:8080/api/v1/books/       |
| API Admin           | http://localhost:8080/admin               |


