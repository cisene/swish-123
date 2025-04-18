#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import random

import yaml
from collections import OrderedDict
from datetime import datetime


#YAML_SOURCE_FILE = '../yaml/entries.yaml'
YAML_SOURCE_FILE = '../yaml/swish-123-datasource.yaml'

MD_DEST_FILE = '../swish-123.md'

def writeMarkdown(filepath, contents):
  with open(filepath, "w") as f:
    f.write(contents)


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
  return data


def main():
  print(f"Reading source YAML: {YAML_SOURCE_FILE} ..")
  source_dict = readYAML(YAML_SOURCE_FILE)
  
  if source_dict == None:
    print(f"Could not read {YAML_SOURCE_FILE}")
    exit(1)

  # Set up destination dictionary
  dest_dict = {}
  dest_dict['vos'] = []
  dest_dict_count = 0

  source_dict_count = len(source_dict['entries'])
  print(f"\tRead {source_dict_count} raw entries")


  for vo in source_dict['entries']:
    if vo['orgName'] != None and vo['orgNumber'] != None:
      vo_sort_key = f"{flattenName(vo['orgName'])}:{vo['orgNumber']}"

      if vo_sort_key not in dest_dict:
        # Add non-existent key
        obj = {
          'name': vo['orgName'],
          'entries': [{
            'entry': vo['entry'],
            'comment': vo['comment'],
          }],
        }
        dest_dict[vo_sort_key] = obj
        dest_dict_count += 1
      else:
        e = { 'entry': vo['entry'], 'comment': vo['comment'], }
        dest_dict[vo_sort_key]['entries'].append(e)
        dest_dict_count += 1

  dest_dict_keys = sorted(dest_dict.keys())

  # Set up destination dictionary
  now = datetime.now() # current date and time
  dest_date_date = now.strftime("%Y-%m-%d")
  dest_date_time = now.strftime("%H%M%S")

  buffer = []
  buffer.append(f"# Swishnummer - Bokstavsordning")
  buffer.append("")
  buffer.append("Source: [swish-123](https://github.com/cisene/swish-123/swish-123.md)")
  buffer.append("")
  buffer.append(f"Revision: {dest_date_date}-rev-{dest_date_time}")
  buffer.append("")
  buffer.append(f"Nummer: {dest_dict_count}")
  buffer.append("")
  buffer.append(f"PDF: [https://b19.se/swish-katalogen/swish-123.pdf](https://b19.se/swish-katalogen/swish-123.pdf)")
  buffer.append("")
  buffer.append("")
  buffer.append("")

  old_letter = None

  for di in dest_dict_keys:
    obj = dest_dict[di]
    if "name" in obj:
      if obj['name'] != None:
        if obj['name'][:1] != None:
          current_letter = str(obj['name'][:1]).upper()

          if current_letter != old_letter:
            buffer.append("")
            buffer.append("")
            buffer.append(f"## {current_letter}")
            buffer.append("")
            old_letter = current_letter

          buffer.append(f"**{obj['name']}**")
          buffer.append("")
          for e in obj['entries']:
            if e['comment'] == None:
              buffer.append(f"    {prettyprintSwish(e['entry'])}")
              buffer.append("")
            else:
              buffer.append(f"    {prettyprintSwish(e['entry'])} - {e['comment']}")
              buffer.append("")

          buffer.append("")
          buffer.append("")
          buffer.append("")

  rendered = "\n".join(buffer)

  #print(rendered)
  writeMarkdown(MD_DEST_FILE, rendered)
  print(f"\tWrote {dest_dict_count} Markdown entries")



if __name__ == '__main__':
  main()
