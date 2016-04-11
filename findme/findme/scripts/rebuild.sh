#!/bin/bash

### There's a bug in Django with custom user profiles where some of the tables 
### don't get created.  Doing just a zap and create, and then migrate will 
### cause database insertion errors, and the user profiles aren't created.
### adding in the makemigrations for each app in the project will explicitely
### tell it to create all the necessary tables in the db

echo "Resetting database"
python manage.py zap_and_create_postgis_db
python manage.py migrate 
