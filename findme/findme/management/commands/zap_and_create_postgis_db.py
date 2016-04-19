"""Zaps and creates postgres database and installs posgis extensions
"""
import sys
import subprocess

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    args = ""
    help = "Zaps and creates postgres database and installs posgis extensions"
    option_list = BaseCommand.option_list + ()

    def handle(self, *args, **kwargs):
        self.log("Zapping and creating the postgis database...")

        database = 'default'

        self.engine = settings.DATABASES[database]['ENGINE']
        self.name = settings.DATABASES[database]['NAME']
        self.user = settings.DATABASES[database]['USER']
        self.password = settings.DATABASES[database]['PASSWORD']
        self.host = settings.DATABASES[database]['HOST']
        self.port = settings.DATABASES[database]['PORT']
        self.debug = settings.DEBUG
        self.database = database
        self.kwargs = kwargs

        self.zap_db()
        self.zap_user()
        self.create_user()
        self.create_db()
        self.create_postgis_ext()
        self.create_topology_ext()

    def log(self, message):
        print >>sys.stderr, message

    def _psql(self, command, db_name=''):
        ''' Run a command via psql as the postgres user '''
        self.log('psql -c "' + command + '"')

        if db_name:
            base_command = ['sudo', '-u', 'postgres',
                            'psql', '-d', db_name,  '-c']
        else:
            base_command = ['sudo', '-u', 'postgres', 'psql', '-c']

        base_command.append(command)

        p = subprocess.Popen(
            base_command,
            stdout=sys.stdout,
            stderr=sys.stderr,
            stdin=sys.stdin,
        )
        p.wait()
        return p.returncode == 0

    def zap_db(self):
        self.log("Removing db...")
        return self._psql('DROP DATABASE {0}'.format(self.name))

    def zap_user(self):
        self.log("Removing user...")
        return self._psql('DROP ROLE {0}'.format(self.user))

    def create_user(self):

        self.log("Creating user...")
        return self._psql(
            "CREATE ROLE {user} PASSWORD '{password}' "
            "SUPERUSER CREATEDB NOCREATEROLE INHERIT LOGIN".format(
                user=self.user,
                password=self.password))

    def create_db(self):
        self.log("Creating db...")
        return self._psql(
            "CREATE DATABASE {name} WITH OWNER = {owner} "
            "TEMPLATE = template0 ENCODING = 'UTF8'".format(
                name=self.name, owner=self.user,
            )
        )

    def create_postgis_ext(self):
        self.log("Adding postgis extension...")
        return self._psql("CREATE EXTENSION postgis;", self.name)

    def create_topology_ext(self):
        self.log("Adding postgis topology extension...")
        return self._psql("CREATE EXTENSION postgis_topology;", self.name)
