from setuptools import setup

setup(name='I2C-AO-Actor',
      version='0.0.6',
      description='CraftBeerPi Plugin',
      author='Marc Adler',
      author_email='aeda@gmx.de',
      url='https://github.com/adler72/I2C-AO-Actor',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'I2C-AO-Actor': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['I2C-AO-Actor'],
     )
