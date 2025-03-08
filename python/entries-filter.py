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

YAML_SOURCE_FILE = '../yaml/entries.yaml'

YAML_DEST_DATASOURCE = '../yaml/swish-123-datasource.yaml'



def writeYAML(filepath, contents):
  s = yaml.safe_dump(
    contents,
    indent=2,
    width=1000,
    canonical=False,
    sort_keys=False,
    explicit_start=False,
    default_flow_style=False,
    default_style='',
    allow_unicode=True,
    line_break='\n'
  )
  with open(filepath, "w") as f:
    f.write(s.replace('\n- ', '\n\n- '))

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

def flattenList(data):
  return ",".join(data)

def validateEntry(data):
  return re.match(r"^123(\d{7})$", str(data), flags=re.IGNORECASE)

def validateEntryStrict(data):
  result = False

  if re.match(r"^123(\d{7})$", str(data), flags=re.IGNORECASE):
    if(
      re.match(r"^123[0-6]{1}(\d{2})(\d{4})$", str(data), flags=re.IGNORECASE)
      or
      re.match(r"^^12390[0-9]{1}(\d{4})$", str(data), flags=re.IGNORECASE)
    ):
      result = True

  return result

def main():
  print(f"Reading source YAML: {YAML_SOURCE_FILE} ..")
  source_dict = readYAML(YAML_SOURCE_FILE)

  # Set up destination dictionary
  dest_dict = {}
  dest_dict['entries'] = []

  category_block = [
    'overifierad',
    'suspended',
    'terminated',
    'verified',
    'verifierad',
    'retired',
  ]
  
  if source_dict == None:
    print(f"Could not read {YAML_SOURCE_FILE}")
    exit(1)

  line_count = 0
  for entryVO in source_dict['entries']:

    # Check format - simple
    if validateEntry(entryVO['entry']) == False:
      continue

    # Validate ranges - complex
    if validateEntryStrict(entryVO['entry']) == False:
      continue

    # Collect categories
    cats = entryVO['categories']

    # Filter categories
    skip_cats = False
    if cats != None:
      for cat_block in category_block:
        if cat_block in cats:
          skip_cats = True
          break
    else:
      skip_cats = True
      continue

    if(
      entryVO['orgNumber'] != None
    and
      entryVO['orgName'] != None
    and
      entryVO['categories'] != None
    and
      skip_cats == False
    ):
      dest_dict['entries'].append(entryVO)
      line_count += 1

  source_dict_count = len(source_dict['entries'])

  print(f"\tRead {source_dict_count} raw entries")

  writeYAML(YAML_DEST_DATASOURCE, dest_dict)
  print(f"\tWrote {line_count} YAML entries")

  print(f"Done writing {YAML_DEST_DATASOURCE}")

if __name__ == '__main__':
  main()
