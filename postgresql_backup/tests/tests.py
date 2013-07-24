#!/usr/bin/env python
from datetime import datetime
import os.path
import sys
import unittest
from postgresql_backup import *
from expecter import expect

sys.path.append(os.path.dirname(__file__))

class TestFileName(unittest.TestCase):
  def test_default_case(self):
    d = datetime.now()
    w = ['mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun'][d.weekday()]
    h = d.hour
    expect(get_file_name('a')) == "a-%s-%s.sql.bz2" % (w, h)
  def test_without_weekday(self):
    d = datetime.now()
    h = d.hour
    expect(get_file_name('a', weekday = False)) == "a-%s.sql.bz2" % h
  def test_without_hour(self):
    d = datetime.now()
    w = ['mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun'][d.weekday()]
    expect(get_file_name('a', hour = False)) == "a-%s.sql.bz2" % w

