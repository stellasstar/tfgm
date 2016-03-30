from setuptools import setup, find_packages
import os

version = '0.0.1dev0'

setup(name='findme',
      version=version,
      author="Isotoma Limited",
      author_email="support@isotoma.com",
      license="Apache Software License",
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'pastescript'
      ],
      entry_points = """
      [paste.paster_create_template]
      isotoma_django=isotoma_django.template:DjangoProjectTemplate
      """
      )
