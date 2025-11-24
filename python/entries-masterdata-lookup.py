#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import random

import yaml
import json

import collections
from collections import defaultdict

from datetime import datetime

YAML_SOURCE_FILE = '../yaml/entries.yaml'

YAML_MASTERDATA_ORGS = '../yaml/masterdata-organisations.yaml'


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

  print(f"Reading Masterdata Organisations: {YAML_MASTERDATA_ORGS} ..")
  dest_dict = readYAML(YAML_MASTERDATA_ORGS)

  if source_dict == None:
    print(f"Could not read {YAML_SOURCE_FILE}")
    exit(1)

  #if "organisations" in dest_dict:
  #  dest_dict['organisations'] = {}


  line_count = 0
  for entryVO in source_dict['entries']:
    orgNumber = None
    orgName = None
    lo_orgName = None
    if "orgNumber" in entryVO:
      if entryVO['orgNumber'] != None:
        orgNumber = entryVO['orgNumber']
        orgName = None

      if re.search(r"\x2dXXXX$", str(orgNumber), flags=re.IGNORECASE):
        continue

    if "orgName" in entryVO:
      if entryVO['orgName'] != None:
        orgName = entryVO['orgName']

    if orgNumber != None:
      if orgNumber not in dest_dict['organisations']:
        print(f"'{orgNumber}' was not found in masterdata")
        dest_dict['organisations'][orgNumber] = orgName
        line_count += 1

    if orgNumber in dest_dict['organisations']:
      lo_orgName = dest_dict['organisations'][orgNumber]

      if str(lo_orgName) != str(entryVO['orgName']):
        print(f"{orgNumber}: '{lo_orgName}' isn't equal to '{entryVO['orgName']}'")


  #sorted(dest_dict)
  #dest_dict_sorted = collections.OrderedDict(sorted(dest_dict['organisations'].items()))
  dest_dict_sorted = {}
  dest_dict_sorted['organisations'] = dict(sorted(dest_dict['organisations'].items()))


  writeYAML(YAML_MASTERDATA_ORGS, dest_dict_sorted)
  print(f"\tWrote {line_count} YAML entries")

  print(f"Done writing {YAML_MASTERDATA_ORGS}")

if __name__ == '__main__':
  main()
