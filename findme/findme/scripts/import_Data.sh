#!/bin/bash

TIMEFORMAT='It takes %R seconds to complete this task...'

time {
    python manage.py import_Transport
    python manage.py import_Test_Users
    python manage.py import_Tfgm_CSV
    python manage.py import_Comments
    python manage.py import_Comments
}
