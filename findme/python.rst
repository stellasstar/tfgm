===============
Python & Django
===============

Environment
===========

All environments for your project must use the same Python version as each
other, and be installed using virtualenv with setuptools and pip.

Python versions
---------------

You should target Python 2.7 or Python 3 for all new development.  Python 3
still misses some library support, so check your dependencies carefully before
choosing it.

.. index::
   single: pip

Install Pip
----------

You need to install pip after python.  You should use pip to perform all package installation and removal.::

    $ sudo apt-get install python-pip


Pip provides a built-in download cache_ as of version 6.0. You can turn this off and force use of PyPI using the :code:`--no-cache-dir` command-line option.

.. _cache: https://pip.pypa.io/en/stable/reference/pip_install.html#caching

.. index::
   single: virtualenv

Virtualenv
----------

You should install the appropriate Ubuntu package to get hold of virtualenv::

    $ sudo apt-get install python-virtualenv

Create a dir to store your virtualenvs::

    $ mkdir ~/virtualenvs

.. index::
   single: virtualenvwrapper
   single: workon

Virtualenvwrapper
~~~~~~~~~~~~~~~~~

At this point you are all set to use virtualenv with the standard commands.  But
it is preferrable to also use virtualenvwrapper_ and its extra commands in development.

This makes life maintaining virtual environments much easier.

Install virtualenvwrapper::
    
    $ sudo pip install virtualenvwrapper

Set WORKON_HOME to your virtualenv dir at this moment::
    
    $ export WORKON_HOME=~/virtualenvs

Set VIRTUALENVWRAPPER_HOOK_DIR to the virtualenv dir at this moment::

    $ export VIRTUALENVWRAPPER_HOOK_DIR=~/virtualenvs

Add virtualenvwrapper.sh to .bashrc

Add these lines to the end of ~/.bashrc so that the virtualenvwrapper commands are loaded in the correct directory and every log in.
::

    export VIRTUALENVWRAPPER_HOOK_DIR=~/virtualenvs
    export WORKON_HOME=~/virtualenvs
    . /usr/local/bin/virtualenvwrapper.sh

Start the virtualenvwrapper script::

    $ source ~/.bashrc

    $ source /usr/local/bin/virtualenvwrapper.sh

For a 1-step process, to cd to your project directory and then to activate 
the environment. Add a post-activate trigger script, so
when you type the above command, it also changes to your project directory
automatically. Your project dir and virtual env will have the same name.  
To achieve this, go to your envs directory and edit the postactivate 
and postmkvirtualenv scripts::

    $ cd ~/virutalenvs
    $ chmod +x postactivate
    $ chmod +x postmkvirtualenv

edit both postactivate and postmkvirtualenv to look like this::

    #!/bin/bash
    # This hook is sourced after every virtualenv is activated.

    PROJ_NAME=$(basename $VIRTUAL_ENV)
    PROJECT_DIR=$HOME/projects/$PROJ_NAME

    if [ -d $PROJECT_DIR ]; then
        # If we aren't already within the project dir, cd into it
        if [[ ! `pwd` == "$PROJECT_DIR*" ]]; then
            export PRE_VENV_ACTIVATE_DIR=`pwd`
            cd "$PROJECT_DIR"
        fi
    else
        mkdir -p $PROJECT_DIR
        cd $PROJECT_DIR
    fi
    unset PROJECT_DIR

With virtualenvwrapper, when you need to create a new virtual environment,
rather than running the old virtualenv command, you do::

    mkvirtualenv project_name

This creates your new environment, but not in the current directory.
Virtualenvwrapper keeps all your environments in one place, and 
then you activate the correct one by typing::

    workon project_name

Your virtual env will be created in ~/virtualenvs/<project_name>
Your project will be created in ~/projects/<project_name>

If you want, edit the postdeactivate script (optional)::

    #!/bin/bash

    if [ $PRE_VENV_ACTIVATE_DIR ]; then
        cd $PRE_VENV_ACTIVATE_DIR
        unset PRE_VENV_ACTIVATE_DIR
    fi

Now when you type workon project_name, you will be taken straight to the
project directory with the environment activated. Hooray!

Scripts based on this_ post, with modifications (see bottom of post)


.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
.. _this: http://hmarr.com/2010/jan/19/making-virtualenv-play-nice-with-git/

.. index::
   single: django

Install Django
--------------

Now we install django::

    $ pip install django

This ends the basic installation.  To continue with the basic steps as a 
tutorial, follow the instructions at  
https://docs.djangoproject.com/en/1.9/intro/tutorial01/

Running your software
---------------------

In development you can run your software with runserver as usual::

    django runserver

The django script is part of our standard setup - see :ref:`django-command`.

Be aware that in production your application will run within gunicorn::

    gunicorn -b localhost:nnnnn <package>.wsgi

.. todo:: waitress?
.. todo:: heroku workers?

Background workers
~~~~~~~~~~~~~~~~~~

In production celery background workers will run as the same user as the web
worker, but will be started and stopped independently in production using the
OS init system.

In development run these in a separate terminal.

Standard python components
==========================

In addition to all of the above, you should be familiar with all of these
packages and know when and how to use them.

.. index::
   single: celery

celery
------

Provides communication with asynchronous workers using a variety of backends.
We use only the Redis backend.

You no longer need to use dj-celery with Django for Celery version 3. The
`Celery Django documentation`_ provides a lot of detail about how to make this
work.


haystack
--------

for search. start with whoosh.  see solr.

dj-database-url
---------------

Define your database settings using a `twelve-factor`_ inspired :code:`DATABASE_URL` environment variable.
Your database settings are therfore not defined in files that are checked into a code repository.
This is directly compatible with the postgres URLs used on cloud services like `Heroku`_.

A standard Postgres database URL looks like::

    postgres://USER:PASSWORD@HOST:PORT/NAME

Our default way of specifying the database in settings.py is::

    import dj_database_url
    PROJECT_NAME = 'example'
    DATABASES = {'default': dj_database_url.config(
        default='postgres://{0}:{0}@localhost/{0}'.format(PROJECT_NAME))}



.. _`twelve-factor`: http://12factor.net/
.. _`Heroku`: http://www.heroku.com/

django-constance
----------------

For support for configurable constants.

Uses pickles! bleugh! how about django-livesettings?


Managing dependencies
---------------------

All direct dependencies of your package should be listed in setup.py.

All dependencies (not just direct ones, but your dependencies dependencies too)
should be listed and pinned in requirements.txt. 

This is quite a complex subject and there's a good explanation here of why::

    https://caremad.io/blog/setup-vs-requirement/

You can find out what your current dependencies are using::

    pip freeze -l

You should pin all dependencies at some point during development and before the
project enters QA. This is to ensure the software version tested is the version
actually deployed.

To pin your dependencies, list your dependencies thusly::

    lxml==2.3.4

It is good practice to actively select package versions based on actually
understanding them and pin them at the beginning of development.

Where checkouts from git are required pin the sha in requirements.txt like this::

    git+https://github.com/spectras/django-hvad@0972cf8900b66df542d289dcf46ad2192c5ee639#egg=django-hvad

Modifications should be pushed up-stream if possible and these links reviewed while a project is still in development.

README.rst
----------

This is the file we'll refer to when deploying your application. It should
provide enough clues for us to deploy the software without having to hunt you
down and murder you to find out the many Secret Things about your software.

 * What configuration is required for a production or staging environment
 * files that are written that are not media or static
 * if celery is used or not
 * how to decide how many celery workers to use for an environment
 * what happens if the queues go away
 * what logfiles are produced by your application

.. todo:: link to a great example (authordirect)

CHANGES.rst
-----------

You should update this file when you first cut a release and you must keep it
up to date after that. zest.releaser does this for you.

You should list every substantive change made to the software, at a high level,
with ticket references as appropriate.

.. todo:: link to a good example


.. _`python docs`: http://docs.python.org/2/distutils/sourcedist.html#the-manifest-in-template

.. index::
   single: releasing

Releasing your software
=======================

To cut a release of your software you MUST use the `zest.releaser` command
`fullrelease`. This performs all of the activities around releasing, including
updating version numbers and tagging.

Install the blessed version of `zest.releaser` with::

    sudo pip install zest.releaser==3.49

To install this on your machine.

This is an arbitrary version of it, but it means we're using the same version
everywhere.

.. index::
   single: configuration


Stack configuration
===================

You may use django-stackhelper to generate configuration files for the rest of
your stack, if you are running in an environment where this makes sense. If you
are using Yaybu or similar to handle deployments, you may wish to use that
instead.

Examples are provided in the production section of this document for common
components.

Deployment checklist
====================

You must run through this checklist before completing your production configuration:

https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


View based models
=================


Using db views means we can still use the ORM (and the raw SQL
disappears into the database) - that's the beauty. Django can't tell the
difference between a db view and a table. The big difference though is
that if the db view is anything other than a simple table you can't
save/update through it - the database will reject it. You still need the
table-based models for that.

I think the view-based models will be most useful for handling listings
of objects spread across multiple tables; and for stabilising APIs
(read-wise at least).

There's definitely an analysis step needed to identify which view-based
models to build. And I think adding them early on and growing them is
probably better than trying to retro fit them to an already exploded
project, although both could be valid depending on the expected system
size/development time.

I think the developers need to be aware that they're using a view-based
model (although they don't all necessarily need to know the underlying
query) and so a naming scheme would be good, e.g. prefixing the
view-based models with 'v'.

