#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import random

import yaml

import collections
from collections import defaultdict
from collections import OrderedDict

YAML_SOURCE_FILE = '../yaml/masterdata-skatteverket-godkända-gåvomottagare-2026-curren.yaml'
YAML_DEST_FILE = '../yaml/masterdata-skatteverket-godkända-gåvomottagare-2026-curren.yaml'


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
  print(f"Reading source YAML: {YAML_SOURCE_FILE} ..")
  source_dict = readYAML(YAML_SOURCE_FILE)
  
  if source_dict == None:
    print(f"Could not read {YAML_SOURCE_FILE}")
    exit(1)

  dest_dict_sorted = {}
  dest_dict_sorted['organisations'] = {}

  dest_dict_sorted['organisations'] = sorted(source_dict['organisations'], key = lambda d: d.get('orgNumber'), reverse=False)

  #print(dest_dict_sorted['organisations'])

  print(f"Writing destination YAML: {YAML_SOURCE_FILE} ..")
  writeYAML(YAML_DEST_FILE, dest_dict_sorted)

if __name__ == '__main__':
  main()
