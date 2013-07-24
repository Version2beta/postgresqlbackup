#!/usr/bin/python
import os
import sys
import simplejson as json
from datetime import datetime
from sh import sudo, psql, pg_dump, pg_dump, bzip2, mkdir, chmod
from hashlib import md5
import boto
from boto.s3.key import Key

CONFIG = '/etc/postgresql/backups.conf'

def get_configuration():
  try:
    return json.load(open(CONFIG, 'r'))
  except:
    print "Configuration file /etc/postgresql/backups.conf is missing!"
    raise

def get_file_name(prefix, weekday = True, hour = True):
  "Create a filename from prefix plus weekday plus hour."
  d = datetime.now()
  w = "-" + ['mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun'][d.weekday()] if weekday else ""
  h = "-" + str(d.hour) if hour else ""
  return "%s%s%s.sql.bz2" % (prefix, w, h)

def ensure_backup_directory(d):
  "If directory doesn't exist, create it."
  if not os.path.isdir(d):
    mkdir(d, '-p')

def get_list_of_databases():
  dbs = sudo.su(
      'postgres',
      '-c',
      'psql -Atc "select datname from pg_database where datistemplate = false order by datname;"')
  return [db.rstrip() for db in dbs]

def create_database_dump(d, f):
  "Dump database d using pg_dump to file 'f'."
  o = f.replace('.bz2', '')
  sudo.su('postgres', '-c', 'pg_dump %s' % d, _out=o)
  bzip2('-f', o)

def hash_of_file(f):
  "Calculate the md5sum of file 'f'."
  md5_hash = md5()
  with open(f, 'rb') as f:
    while True:
      d = f.read(8192)
      md5_hash.update(d)
      if len(d) < 8192:
        break
  return md5_hash.hexdigest()

def stored_hash_of_file(f):
  "Retrieve the stored md5sum has of file 'f'."
  try:
    with open(f, 'r') as fh:
      return fh.read()
  except:
    return

def store_hash_of_file(f, h):
  "Save the md5sum of a file in another file."
  with open(f, 'w') as fh:
    fh.write(h)

def store_file_in_bucket(s3, f, c):
  "Put file 'f' in S3 bucket 'b'."
  b = c['s3_bucket']
  d = c['local_directory']
  bucket = s3.lookup(b) or s3.create_bucket(b)
  key = Key(bucket)
  key.key = f[0]
  with open(d + '/' + f[0], 'r') as fd:
    key.set_contents_from_file(fd)
  key.copy(b, f[1])
  key.copy(b, f[2])

def copy_to_s3(s3, c, f):
  "Copy a file to S3 but only if the stored hash is different."
  h = hash_of_file(c['local_directory'] + '/' + f[0])
  hash_file = c['local_directory'] + '/.' + f[0] + '.hash'
  if h == stored_hash_of_file(hash_file):
    print "Files match for %s; doing nothing." % f[0]
    return
  else:
    print "Copying %s to S3." % f[0]
    store_file_in_bucket(s3, f, c)
    store_hash_of_file(hash_file, h)

def main():
  # get configuration
  _c = get_configuration()

  # Create an s3 connection for other functions to use
  s3 = boto.connect_s3(_c['s3_access_key'], _c['s3_secret_key'])

  # make sure the backup directory is present
  ensure_backup_directory(_c['local_directory'])

  # list all the databases postgresql knows
  dbs = get_list_of_databases()

  # Cycle through each database
  for db in dbs:
    # Generate file names for this backup
    backup_file = [
        get_file_name(db, weekday = False, hour = False), # base
        get_file_name(db, weekday = False), # hourly backup
        get_file_name(db, hour = False) # daily backup
    ]

    # create a local current backup
    create_database_dump(db, _c['local_directory'] + '/' + backup_file[0])

    # copy to S3
    copy_to_s3(s3, _c, backup_file)

if __name__ == "__main__":
  main()
