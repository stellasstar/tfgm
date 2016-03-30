FindMe 1.0

Dependencies:

sudo sh -c 'sudo echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main 9.5" > /etc/apt/sources.list.d/postgresql.list'

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

sudo apt-get update

sudo apt-get install binutils libproj-dev postgresql-9.5 postgresql-9.5-postgis-2.2 postgresql-server-dev-9.5 python-psycopg2
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

1) Add virtual environment 

Virtualenv findme

2) Move into virtual environment and activate it

Cd findme

Activate

3)	Install Django 

Pip Install Django

4)  install other dependencies through pip
pip install -r requirements.txt --upgrade -e .

5)  Configuring PostgreSQL:

Ensure that there is a line in /etc/postgresql/9.3/main/pg_hba.conf that allows local connections using md5:

# "local" is for Unix domain socket connections only
local   all         all                               md5

6)  Unfortunately the django management command zap_and_create_postgis_db does not work until a PostgreSQL database with postgis already exists. The role and password can be taken from settings.py

./findme/scripts/builddb.sh

7) ./findme/scripts/rebuild.sh

