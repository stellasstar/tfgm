#!/bin/bash

echo "Resetting database"
python manage.py zap_and_create_postgis_db
python manage.py makemigrations gatekeeper
python manage.py makemigrations findme
python manage.py makemigrations waypoints
python manage.py migrate 
