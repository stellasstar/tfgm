#!/bin/bash

ROLE=geouser 
PASSWORD=geodatabase 
sudo -u postgres psql -c "CREATE ROLE $ROLE PASSWORD '$PASSWORD' NOSUPERUSER CREATEDB NOCREATEROLE INHERIT LOGIN" 
sudo -u postgres psql -c "CREATE DATABASE $ROLE WITH OWNER = $ROLE ENCODING = 'UTF8'" 
sudo -u postgres psql --dbname=$ROLE -c "CREATE EXTENSION postgis"
sudo -u postgres psql --dbname=$ROLE -c "CREATE EXTENSION postgis_topology;"
