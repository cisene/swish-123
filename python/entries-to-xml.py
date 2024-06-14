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
XML_DEST_FILE = '../xml/swish-123-datasource.xml'

def writeXML(filepath, contents):
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

def escapeXML(data):
  data = re.sub(r"\x26", "&amp;", data, flags=re.IGNORECASE)
  return data

def validateEntry(data):
  result = False
  if re.search(r"^123(\d{7})$", str(data), flags=re.IGNORECASE):
    result = True

  return result

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

  dest_list.append("<?xml version=\"1.0\" ?>")
  dest_list.append("<!--")
  dest_list.append("Title: Swish 123 Nummer")
  dest_list.append("Author: Christopher Isene <christopher.isene@gmail.com>")
  dest_list.append(f"Date: {dest_date_date}-rev-{dest_date_time}")
  dest_list.append("Source: https://github.com/cisene/swish-123/xml/swish-123-datasource.xml")
  dest_list.append("-->")
  dest_list.append("<root>")
  dest_list.append("  <entries>")

  line_count = 0
  for entryVO in source_dict['entries']:
    if validateEntry(entryVO['entry']) == False:
      continue

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
      if entryVO['comment'] == None:
        entryVO['comment'] = ""

      if entryVO['web'] == None:
        entryVO['web'] = ""

      frag = []

      # Open entry
      frag.append(f"<entry number=\"{entryVO['entry']}\">")
      
      # Organisation
      frag.append("<organization>")
      frag.append(f"<number>{entryVO['orgNumber']}</number>")
      frag.append(f"<name>{escapeXML(entryVO['orgName'])}</name>")
      frag.append("</organization>")
      
      # Comment
      if entryVO['comment'] == "":
        frag.append("<comment/>")
      else:
        frag.append(f"<comment>{escapeXML(entryVO['comment'])}</comment>")
      
      # Categories
      frag.append("<categories>")
      for cat in entryVO['categories']:
        frag.append(f"<category type=\"{escapeXML(cat)}\"/>")

      frag.append("</categories>")
      
      # Web
      frag.append(f"<web>{escapeXML(entryVO['web'])}</web>")

      # Close entry
      frag.append("</entry>")

      line = "".join(frag)
      dest_list.append(f"    {line}")
      line_count += 1

  dest_list.append("  </entries>")
  dest_list.append("</root>")

  source_dict_count = len(source_dict['entries'])

  print(f"\tRead {source_dict_count} raw entries")

  writeXML(XML_DEST_FILE, dest_list)
  print(f"\tWrote {line_count} XML entries")

  print(f"Done writing {XML_DEST_FILE}")

if __name__ == '__main__':
  main()
