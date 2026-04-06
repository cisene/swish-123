#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
#import time

from datetime import datetime

import yaml

YAML_ENTRIES_FILE = '../yaml/entries.yaml'
#YAML_MASTERDATA_STA_FILE = '../yaml/masterdata-skatteverket-godkända-gåvomottagare.yaml'

CATEGORY_TAG = "insamlingskontroll"

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
    #f.write(s)
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

def main():

  # Get list of entries
  entries_dict = readYAML(YAML_ENTRIES_FILE)

  for entryVO in entries_dict['entries']:
    orgNumber = entryVO['orgNumber']
    categories_list = entryVO['categories']

    #if orgNumber == None:
    #  continue

    # Only process entries with categories
    if categories_list != None:

      # If desired category tag if found, remove it
      if CATEGORY_TAG in categories_list:
        categories_list.remove(CATEGORY_TAG)

        if len(categories_list) == 0:
          categories_list = None

    if re.search(r"^12390(\d{5})$", str(entryVO['entry']), flags=re.IGNORECASE):
      if categories_list == None:
        categories_list = []

      categories_list.append(CATEGORY_TAG)
      categories_list.sort()
      entryVO['categories'] = categories_list
      continue

  writeYAML(YAML_ENTRIES_FILE, entries_dict)



if __name__ == '__main__':
  main()
