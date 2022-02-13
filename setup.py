from setuptools import setup, find_packages
import sys, os
from pathlib import Path

version = '1.3'

this_directory = Path(__file__).parent
long_description = (this_directory / "README.txt").read_text()

setup(name='matchco',
      version=version,
      description="Match company names against a database of names and variations",
      long_description=long_description,
      long_description_content_type='text/plain',
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
      install_requires=["distance>=0.1.3", "jellyfish>=0.9.0"],
      tests_require=["pytest"],
)
