#!/bin/bash

NAME=geodatabase
USER=geouser 
PASSWORD=geopassword
sudo -u postgres psql -c "CREATE ROLE $USER PASSWORD '$PASSWORD' NOSUPERUSER CREATEDB NOCREATEROLE INHERIT LOGIN" 
sudo -u postgres psql -c "CREATE DATABASE $NAME WITH OWNER = $USER ENCODING = 'UTF8'" 
sudo -u postgres psql --dbname=$NAME -c "CREATE EXTENSION postgis"
sudo -u postgres psql --dbname=$NAME -c "CREATE EXTENSION postgis_topology;"
