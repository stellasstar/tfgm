from setuptools import setup, find_packages
import os

version = '0.0.1dev0'

setup(name='findme',
      version=version,
      author="Stella Silverstein",
      author_email="stella.silverstein@isotoma.com",
      license="Apache Software License",
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'Django',
        'Markdown',
        'Paste',
        'PasteDeploy',
        'PasteScript',
        'Pillow',
        'PyJWT',
        'argparse',
        'django-awesome-avatar',
        'django-filter',
        'djangorestframework',
        'flake8',
        'mccabe',
        'oauthlib',
        'pep8',
        'psycopg2',
        'pyflakes',
        'python-openid',
        'python-social-auth',
        'requests',
        'requests-oauthlib',
        'six',
        'wsgiref'
      ],
      entry_points = """
      [paste.paster_create_template]
      """
      )
