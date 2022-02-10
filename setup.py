from setuptools import setup, find_packages
import sys, os

version = '1.2.3'

setup(name='matchco',
      version=version,
      description="Match company names against a database of names and variations",
      long_description="""""",
      classifiers=[
         "Topic :: Office/Business",
         "Development Status :: 4 - Beta",
         "Intended Audience :: Developers",
         "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
         "Programming Language :: Python :: 3"
      ],
      keywords='',
      author='Petri Savolainen',
      author_email='petri@koodaamo.fi',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=["cleanco>=2.2", "distance", "jellyfish"],
      tests_require=["pytest"],
)
