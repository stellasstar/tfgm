#!/bin/bash

echo "Resetting database"
python manage.py zap_and_create_postgis_db
python manage.py makemigrations --empty gatekeeper
python manage.py makemigrations --empty findme
python manage.py makemigrations --empty waypoints
python manage.py migrate 
