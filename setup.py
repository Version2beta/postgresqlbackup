from distutils.core import setup

setup(
  name = 'postgresql_backup',
  url = 'https://github.com/Version2beta/postgresql_backup',
  version = '1.0.0',
  author = 'Rob Martin',
  author_email = 'rob@version2beta.com',
  packages = ['postgresql_backup'],
  install_requires = [],
  data_files = [('/etc/postgresql', ['backups.conf'])],
  entry_points = {
    'console_scripts': [
      'postgresql_backup = postgresql_backup:main'
    ]
  }
)
