#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import random

import yaml
# import collections
from collections import defaultdict


YAML_SOURCE_FILE = '../yaml/entries.yaml'
YAML_DEST_FILE = '../yaml/entries-sorted.yaml'


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

def fulltrim(data):

  # Strip leading spaces
  data = re.sub(r"^\s{1,}", "", str(data))

  # Strip trailing spaces
  data = re.sub(r"\s{1,}$", "", str(data))

  # Strip double spaces within strings
  data = re.sub(r"\s{2,}", " ", str(data))

  return data

def ReplaceFilter(data):

  data = re.sub(r"\sförsamling$", " Församling", data, flags=re.IGNORECASE)
  data = re.sub(r"\spastorat$", " Pastorat", data, flags=re.IGNORECASE)

  data = re.sub(r"\sscoutkår$", " Scoutkår", data, flags=re.IGNORECASE)
  return data


def cloneVO(valueObject):
  
  # Template ValueObject
  vo = {
    'entry': None,
    'orgName': None,
    'orgNumber': None,
    'comment': None,
    'categories': None,
    'web': None
  }

  # Read and assign into new VO if present
  if valueObject['entry'] != None:
    vo['entry'] = valueObject['entry']

  if valueObject['orgName'] != None:
    vo['orgName'] = fulltrim(ReplaceFilter(valueObject['orgName']))

  if valueObject['orgNumber'] != None:
    vo['orgNumber'] = valueObject['orgNumber']

  if valueObject['comment'] != None:
    vo['comment'] = fulltrim(valueObject['comment'])

  if valueObject['web'] != None:
    vo['web'] = fulltrim(valueObject['web'])

  if valueObject['categories'] != None:
    if len(valueObject['categories']) > 0:
      categories_list = []
      for cat in valueObject['categories']:
        if fulltrim(cat) not in categories_list:
          categories_list.append(fulltrim(cat))
      categories_list.sort()
      vo['categories'] = categories_list

  return vo


def main():
  print(f"Reading source YAML: {YAML_SOURCE_FILE} ..")
  source_dict = readYAML(YAML_SOURCE_FILE)
  
  if source_dict == None:
    print(f"Could not read {YAML_SOURCE_FILE}")
    exit(1)

  # Set up destination dictionary
  dest_dict = {}
  dest_dict['entries'] = []

  source_dict_count = len(source_dict['entries'])
  print(f"\tRead {source_dict_count} raw entries")

  # Get list of unique entries->entry
  print("Sorting ...")
  entry_list = []
  for vo in source_dict['entries']:
    entry = vo['entry']
    if str(entry) not in entry_list:
      entry_list.append(str(entry))
    else:
      continue
  entry_list.sort()
  print("... sorted")

  for entry in entry_list:
    for vo in source_dict['entries']:
      if str(entry) == str(vo['entry']):
        dest_dict['entries'].append(cloneVO(vo))
        break

  # Count entries
  dest_dict_count = len(dest_dict['entries'])
  print(f"\tWriting {dest_dict_count} entries")
  print(f"Writing destination YAML: {YAML_SOURCE_FILE} ..")
  writeYAML(YAML_SOURCE_FILE, dest_dict)
  print("Done")

if __name__ == '__main__':
  main()
