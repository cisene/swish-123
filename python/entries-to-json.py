#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import random

import yaml
import json

from collections import defaultdict

from datetime import datetime

#YAML_SOURCE_FILE = '../yaml/entries.yaml'
YAML_SOURCE_FILE = '../yaml/swish-123-datasource.yaml'

JSON_DEST_FILE = '../json/swish-123-datasource.json'

def writeJSON(filepath, contents):
  s = json.dumps(
    contents,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    cls=None,
    indent=2,
    separators=None,
    default=None,
    sort_keys=False
  )
  with open(filepath, "w") as f:
    f.write(s)

def readYAML(filepath):
  contents = None
  data = None
  if os.path.isfile(filepath):
    fp = None

    try:
      fp = open(filepath)
      contents = fp.read()
      fp.close()

    finally:
      pass

  if contents != None:
    data = yaml.safe_load(contents)

  return data

def validateEntry(data):
  return re.match(r"^123(\d{7})$", str(data), flags=re.IGNORECASE)

def main():
  print(f"Reading source YAML: {YAML_SOURCE_FILE} ..")
  source_dict = readYAML(YAML_SOURCE_FILE)

  #category_block = [
  #  'overifierad',
  #  'suspended',
  #  'terminated',
  #  'verified',
  #  'verifierad',
  #  'retired',
  #]
  
  if source_dict == None:
    print(f"Could not read {YAML_SOURCE_FILE}")
    exit(1)

  # Set up destination dictionary
  now = datetime.now() # current date and time
  dest_date_date = now.strftime("%Y-%m-%d")
  dest_date_time = now.strftime("%H%M%S")

  dest_dict = {
    '#meta': {
      'title': 'Swish 123 Nummer',
      'author': 'Christopher Isene <christopher.isene@gmail.com>',
      'date': f"{dest_date_date}-rev-{dest_date_time}",
      'source': 'https://github.com/cisene/swish-123/json/swish-123-datasource.json'
    },
    'data': []
  }

  line_count = 0
  for entryVO in source_dict['entries']:
    #if validateEntry(entryVO['entry']) == False:
    #  continue

    #cats = entryVO['categories']

    # Filter categories
    #skip_cats = False
    #if cats != None:
    #  for cat_block in category_block:
    #    if cat_block in cats:
    #      skip_cats = True
    #      break
    #else:
    #  skip_cats = True
    #  continue

    #if(
    #  entryVO['orgNumber'] != None
    #  and
    #  entryVO['orgName'] != None
    #  and
    #  entryVO['categories'] != None
    #  and
    #  skip_cats == False
    #):
    dest_dict['data'].append(entryVO)
    line_count += 1

  source_dict_count = len(source_dict['entries'])
  dest_dict_count = len(dest_dict['data'])

  print(f"\tRead {source_dict_count} raw entries")

  writeJSON(JSON_DEST_FILE, dest_dict)
  print(f"\tWrote {dest_dict_count} JSON entries")

  print(f"Done writing {JSON_DEST_FILE}")

if __name__ == '__main__':
  main()
