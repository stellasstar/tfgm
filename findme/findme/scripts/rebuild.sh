#!/bin/bash

echo "Resetting database"
python manage.py zap_and_create_postgis_db
python manage.py migrate 
