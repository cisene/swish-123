#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import random

import json
from collections import OrderedDict
from datetime import datetime

import operator
from operator import *

from operator import itemgetter

JSON_SOURCE_FILE = '../json/swish-123-datasource.json'

def writeMarkdown(filepath, contents):
  with open(filepath, "w") as f:
    f.write(contents)

def readJSON(filepath):
  data = None
  contents = None
  if os.path.isfile(filepath):
    fp = None
    try:
      fp = open(filepath)
      contents = fp.read()
      fp.close()
    finally:
      pass

  if contents != None:
    data = json.loads(contents)

  return data

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


def flattenName(name):
  if name != None:
    name = name.lower()
    name = re.sub(r"[^a-z0-9åäö]", "_", str(name), flags=re.IGNORECASE)
    name = re.sub(r"\x20", "_", str(name), flags=re.IGNORECASE)
    name = re.sub(r"\x5f{2,}", "_", str(name), flags=re.IGNORECASE)
  else:
    name = ""
  return name


def prettyprintSwish(data):
  if re.search(r"^\d{10}$", str(data), flags=re.IGNORECASE):
    data = re.sub(r"^(\d{3})(\d{3})(\d{2})(\d{2})$", "\\1 \\2 \\3 \\4", str(data), flags=re.IGNORECASE)
    data = re.sub(r"\x20", "\xa0", str(data), flags=re.IGNORECASE)

  return data


def main():

  themes = [
    {
      'title': 'Godkända Gåvomottagare',
      'slug': 'swishkatalogen-godkända-gåvomottagare',
      'categories': [
        'godkänd gåvomottagare',
      ]
    },
    {
      'title': 'kvinnojourer',
      'slug': 'swishkatalogen-kvinnojourer',
      'categories': [
        'kvinnojour',
        'tjejjour',
        'transjour',
      ]
    }
  ]

  print(f"Reading source JSON: {JSON_SOURCE_FILE} ..")
  source_dict = readJSON(JSON_SOURCE_FILE)
  
  if source_dict == None:
    print(f"Could not read {JSON_SOURCE_FILE}")
    exit(1)

  source_dict_count = len(source_dict['data'])
  print(f"\tRead {source_dict_count} raw entries")

  for theme in themes:

    # Set up destination dictionary
    dest_dict = {}
    dest_dict['vos'] = []
    dest_dict_count = 0

    seen = []

    for vo in source_dict['data']:
      if vo['orgName'] != None and vo['orgNumber'] != None:

        if "categories" in vo:
          for cat in theme['categories']:
            if cat in vo['categories'] and vo['entry'] not in seen:
              dest_dict['vos'].append(vo)
              seen.append(vo['entry'])

    dest_dict['vos'] = sorted(dest_dict['vos'], key=itemgetter('orgName'))
    dest_dict_count = len(dest_dict['vos'])

    # Set up destination dictionary
    now = datetime.now() # current date and time
    dest_date_date = now.strftime("%Y-%m-%d")
    dest_date_time = now.strftime("%H%M%S")

    buffer = []
    buffer.append(f"# Swishnummer - {theme['title']}")
    buffer.append("")
    buffer.append(f"Revision: {dest_date_date}-rev-{dest_date_time}")
    buffer.append("")
    buffer.append(f"Nummer: {dest_dict_count}")
    buffer.append("")
    buffer.append(f"PDF: [https://b19.se/swish-katalogen/{theme['slug']}.pdf](https://b19.se/swish-katalogen/{theme['slug']}.pdf)")
    buffer.append("")
    buffer.append("")
    buffer.append("")

    buffer.append("| Swishnummer     | Organisation                                                 | Kommentar |")
    buffer.append("| --------------- | ------------------------------------------------------------ | --------- |")

    for vo in dest_dict['vos']:
      if vo['comment'] == None:
        vo['comment'] = ""

      prettySwish = prettyprintSwish(vo['entry'])

      buffer.append(f"| `{prettySwish}` | {vo['orgName']:<60} | {vo['comment']:<20} |")

    buffer.append("")
    buffer.append("")
    buffer.append("")
    buffer.append("")

    rendered = "\n".join(buffer)

    filepath = f"../{theme['slug']}.md"
    writeMarkdown(filepath, rendered)
    print(f"\tWrote {filepath} with {dest_dict_count} entries")



if __name__ == '__main__':
  main()
