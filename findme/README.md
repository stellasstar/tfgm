# FindMe 1.0

## Dependencies:

- sudo apt-get update

- sudo apt-get install binutils libproj-dev postgresql-9.3 postgresql-9.3-postgis-2.1 postgresql-server-dev-9.3 python-psycopg2 postgis

- sudo apt-get install libgdal-dev

- sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

- sudo apt-get install python-pip (if needed)

## CD into the project directory
- git clone git@github.com:isotoma/stella_tfgm

- cd stella_tfgm

## Set up the virtual environment
- virtualenv --setuptools venv 
- source venv/bin/activate Cd findme

## Install other dependencies through pip 
- pip install -r requirements.txt --upgrade -e .

## Configuring PostgreSQL:

Ensure that there is a line in /etc/postgresql/9.3/main/pg_hba.conf that allows local connections using md5:
- edit /etc/postgresql/9.3/main/pg_hba.conf to look like the line below

- "local" is for Unix domain socket connections only local all all md5

### Unfortunately the django management command zap_and_create_postgis_db does not work until a PostgreSQL database with postgis already exists. The role and password can be taken from settings.py, and the builddb.sh file can be edited with this information. builddb.sh will install the initial database, and rebuild.sh will build the necessary tables.

- ./findme/scripts/builddb.sh 
- ./findme/scripts/rebuild.sh

## load in initial data into the database, the script will run in the following order

- load bus stops

- load test Users

- load test Comments, ran 2x


    $ ./findme/scripts/importData.sh

now go and grab a cup of tea, the import script takes about 5 minutes to run
its quite a bit of data
