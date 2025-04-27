#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
#import time

from datetime import datetime

import yaml

YAML_ENTRIES_FILE = '../yaml/entries.yaml'
YAML_MASTERDATA_FILE = '../yaml/masterdata-svenskhandel-varningslistan.yaml'

CATEGORY_TAG = "varningslistan"

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

def getActiveSTA(source_dict):
  approved_org = []

  print(f"Processing {len(source_dict['organisations'])} organisations ..")
  if "organisations" in source_dict:
    for org in source_dict['organisations']:
      orgNumber = org['orgNumber']
      orgName = org['orgName']
      approved_org.append(orgNumber)
  return approved_org


def main():

  # Read raw list
  sta_raw_dict = readYAML(YAML_MASTERDATA_FILE)

  # Get a list of OrgNumbers
  sta_list = getActiveSTA(sta_raw_dict)

  # Get list of entries
  entries_dict = readYAML(YAML_ENTRIES_FILE)

  entries_changed = 0

  for entryVO in entries_dict['entries']:
    orgNumber = entryVO['orgNumber']
    categories_list = entryVO['categories']

    # Only process entries with categories
    if categories_list != None:

      # If desired category tag if found, remove it
      if CATEGORY_TAG in categories_list:
        categories_list.remove(CATEGORY_TAG)

      # if orgNumber match in list, add category tag, sort and save
      if orgNumber in sta_list:
        categories_list.append(CATEGORY_TAG)
        categories_list.sort()
        entryVO['categories'] = categories_list
        entries_changed += 1
        continue
        # We're done, skip out for next entry

  print(f"Entries changed: {entries_changed}")
  if entries_changed != 0:
    print("Writing entries ..")
    writeYAML(YAML_ENTRIES_FILE, entries_dict)
  else:
    print("No entries changed")


if __name__ == '__main__':
  main()
