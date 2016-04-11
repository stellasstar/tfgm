#!/bin/bash

NAME=geodatabase
USER=geouser 
PASSWORD=geopassword

sudo -u postgres psql -c "DROP DATABASE $NAME" 
sudo -u postgres psql -c "DROP USER $USER" 
sudo -u postgres psql -c "CREATE ROLE $USER PASSWORD '$PASSWORD' NOSUPERUSER CREATEDB NOCREATEROLE INHERIT LOGIN" 
sudo -u postgres psql -c "CREATE DATABASE $NAME WITH OWNER = $USER ENCODING = 'UTF8'" 
sudo -u postgres psql --dbname=$NAME -c "CREATE EXTENSION postgis"
sudo -u postgres psql --dbname=$NAME -c "CREATE EXTENSION postgis_topology;"

python manage.py makemigrations findme
python manage.py makemigrations gatekeeper
python manage.py makemigrations transport
