FindMe 1.0

Dependencies:

sudo apt-get install binutils libproj-dev postgresql-9.5 postgresql-9.5-postgis-2.2 postgresql-server-dev-9.5 python-psycopg2
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

1) Add virtual environment 

Virtualenv findme

2) Move into virtual environment and activate it

Cd findme

Activate

3)	Install Django 

Pip Install Django

4) 



6) Unfortunately the django management command zap_and_create_postgis_db does not work until a PostgreSQL database with postgis already exists. The role and password can be taken from settings.py

ROLE=geouser
PASSWORD=geodatabase
sudo -u postgres psql -c "CREATE ROLE $ROLE PASSWORD '$PASSWORD' NOSUPERUSER CREATEDB NOCREATEROLE INHERIT LOGIN"
sudo -u postgres psql -c "CREATE DATABASE $ROLE WITH OWNER = $ROLE TEMPLATE = template0 ENCODING = 'UTF8'"
sudo -u postgres psql $ROLE -c "CREATE EXTENSION postgis"


7) ./findme/scripts/rebuild.sh

