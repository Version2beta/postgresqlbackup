from distutils.core import setup

setup(
  name = 'postgresqlbackup',
  url = 'https://github.com/Version2beta/postgresqlbackup',
  version = '1.0.0',
  author = 'Rob Martin',
  author_email = 'rob@version2beta.com',
  packages = ['postgresqlbackup'],
  install_requires = [],
  data_files = [('/etc/postgresql', ['backups.conf'])],
  entry_points = {
    'console_scripts': [
      'postgresql_backup = postgresqlbackup:main'
    ]
  }
)
