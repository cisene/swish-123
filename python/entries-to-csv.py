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

CSV_DEST_FILE = '../text/swish-123-datasource.csv'

def writeCSV(filepath, contents):
  s = "\n".join(contents) + "\n"
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

def flattenList(data):
  return ",".join(data)

def validateEntry(data):
  return re.match(r"^123(\d{7})$", str(data), flags=re.IGNORECASE)

def main():
  print(f"Reading source YAML: {YAML_SOURCE_FILE} ..")
  source_dict = readYAML(YAML_SOURCE_FILE)

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

  # Set up destination dictionary
  now = datetime.now() # current date and time
  dest_date_date = now.strftime("%Y-%m-%d")
  dest_date_time = now.strftime("%H%M%S")

  dest_list = []
  dest_list.append("#")
  dest_list.append("# Title: Swish 123 Nummer")
  dest_list.append("# Author: Christopher Isene <christopher.isene@gmail.com>")
  dest_list.append(f"# Date: {dest_date_date}-rev-{dest_date_time}")
  dest_list.append("# Source: https://github.com/cisene/swish-123/text/swish-123-datasource.csv")
  dest_list.append("#")
  dest_list.append("# Legend: Swish-nummer, OrgNr, OrgNamn, Länk, Kategorier, Kommentar")
  dest_list.append("#")
  dest_list.append("\"entry\",\"orgNumber\",\"orgName\",\"web\",\"categories\",\"comment\"")

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
    if entryVO['comment'] == None:
      entryVO['comment'] = ""

    if entryVO['web'] == None:
      entryVO['web'] = ""

    line = f"\"{entryVO['entry']}\",\"{entryVO['orgNumber']}\",\"{entryVO['orgName']}\",\"{entryVO['web']}\",\"{flattenList(entryVO['categories'])}\",\"{entryVO['comment']}\""

    dest_list.append(line)
    line_count += 1

  source_dict_count = len(source_dict['entries'])

  print(f"\tRead {source_dict_count} raw entries")

  writeCSV(CSV_DEST_FILE, dest_list)
  print(f"\tWrote {line_count} CSV entries")

  print(f"Done writing {CSV_DEST_FILE}")

if __name__ == '__main__':
  main()
