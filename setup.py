from setuptools import setup, find_packages
import sys, os

version = '0.3'

setup(name='cotendo',
      version=version,
      description="Cotendo API",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='Cotendo Python API',
      author='Josh Toft',
      author_email='joshtoft@gmail.com',
      url='https://github.com/seryl/Python-Cotendo',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "lxml>=2.3beta1",
          "BeautifulSoup>=3.2.0",
          "suds>=0.4"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
