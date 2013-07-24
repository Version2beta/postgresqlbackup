# postgresql_backup

This project provides a Python package for managing rotating Postgres backups by database to the local filesystem and to a specified AWS S3 bucket.

## Usage

Edit ```/etc/postgresql/backups.conf``` and symlink the executable to /etc/cron.hourly with ```ln -s /usr/local/bin/postgresql_backup /etc/cron.hourly/```.

