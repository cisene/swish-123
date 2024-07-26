#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import random

import yaml
from collections import defaultdict

# Source data found at https://www.skatteverket.se/privat/skatter/arbeteochinkomst/skattereduktioner/skattereduktionforgavor.4.5fc8c94513259a4ba1d800064144.html


YAML_SOURCE_FILE = '../yaml/masterdata-skatteverket-godkända-gåvomottagare.yaml'


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
    'orgNumber': None,
    'orgName': None,
    'issued': None,
    'expires': None,
    'location': None,
  }

  # Read and assign into new VO if present
  if "orgNumber" in valueObject:
    if valueObject['orgNumber'] != None:
      vo['orgNumber'] = valueObject['orgNumber']

  if "orgName" in valueObject:
    if valueObject['orgName'] != None:
      vo['orgName'] = fulltrim(ReplaceFilter(valueObject['orgName']))

  if "issued" in valueObject:
    if valueObject['issued'] != None:
      vo['issued'] = fulltrim(valueObject['issued'])

  if "expires" in valueObject:
    if valueObject['expires'] != None:
      vo['expires'] = fulltrim(valueObject['expires'])

  if "location" in valueObject:
    if valueObject['location'] != None:
      vo['location'] = fulltrim(valueObject['location'])

  return vo


def main():
  print(f"Reading source YAML: {YAML_SOURCE_FILE} ..")
  source_dict = readYAML(YAML_SOURCE_FILE)
  
  if source_dict == None:
    print(f"Could not read {YAML_SOURCE_FILE}")
    exit(1)

  # Set up destination dictionary
  dest_dict = {}
  dest_dict['organisations'] = []

  source_dict_count = len(source_dict['organisations'])
  print(f"\tRead {source_dict_count} raw entries")

  # Get list of unique entries->entry
  print("Sorting ...")
  entry_list = []
  for vo in source_dict['organisations']:
    orgNumber = vo['orgNumber']
    if str(orgNumber) not in entry_list:
      entry_list.append(str(orgNumber))
    else:
      print(f"\tEntry '{str(orgNumber)}' skipped as duplicate ..")
      continue

  entry_list.sort()
  print("... sorted")

  for orgNumber in entry_list:
    for vo in source_dict['organisations']:
      if str(orgNumber) == str(vo['orgNumber']):
        dest_dict['organisations'].append(cloneVO(vo))
        break

  # Count entries
  dest_dict_count = len(dest_dict['organisations'])
  print(f"\tWriting {dest_dict_count} organisations")
  print(f"Writing destination YAML: {YAML_SOURCE_FILE} ..")
  writeYAML(YAML_SOURCE_FILE, dest_dict)

if __name__ == '__main__':
  main()
