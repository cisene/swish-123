#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import random

import yaml
from lxml import etree

from datetime import datetime

YAML_SOURCE_FILE = '../yaml/swish-123-datasource.yaml'

XML_DEST_FILE = '../xml/sitemap.xml'

def writeXML(filepath, contents):
  with open(filepath, "w") as f:
    f.write(contents)

def urlencode(data):
  data = re.sub(r"\x20", "+", str(data), flags=re.IGNORECASE)

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

def main():
  print(f"Reading source YAML: {YAML_SOURCE_FILE} ..")
  source_dict = readYAML(YAML_SOURCE_FILE)

  if source_dict == None:
    print(f"Could not read {YAML_SOURCE_FILE}")
    exit(1)

  # Set up destination dictionary
  now = datetime.now() # current date and time
  dest_date_date = now.strftime("%Y-%m-%d")
  dest_date_time = now.strftime("%H:%M:%S")

  entries_list = []
  categories_list = []
  org_list = []

  ns = {
    None: 'http://www.sitemaps.org/schemas/sitemap/0.9',
  }

  # <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  urlset = etree.Element("urlset", nsmap = ns)

  for entryVO in source_dict['entries']:
    entry = entryVO['entry']

    if entry not in entries_list:
      entries_list.append(str(entry))

    if "orgNumber" in entryVO:
      if entryVO['orgNumber'] != None:
        orgNumber = entryVO['orgNumber']
        if re.search(r"^\d{6}\x2d\d{4}$", str(orgNumber), flags=re.IGNORECASE):
          if orgNumber not in org_list:
            org_list.append(orgNumber)

    if "categories" in entryVO:
      if entryVO['categories'] != None:
        for cat in entryVO['categories']:
          if cat not in categories_list:
            categories_list.append(str(cat))

  elem_url = etree.Element("url")
  elem_loc = etree.Element("loc")
  elem_loc.text = f"https://b19.se/swish-katalogen/swish-123.pdf"

  elem_lastmod = etree.Element("lastmod")
  elem_lastmod.text = f"{dest_date_date}T{dest_date_time}+01:00"

  elem_url.append(elem_loc)
  elem_url.append(elem_lastmod)
  urlset.append(elem_url)

  random.shuffle(org_list)
  for org in org_list:
    elem_url = etree.Element("url")
    
    elem_loc = etree.Element("loc")
    elem_loc.text = f"https://b19.se/swish-katalogen/o/{org}"

    elem_lastmod = etree.Element("lastmod")
    elem_lastmod.text = f"{dest_date_date}T{dest_date_time}+01:00"

    elem_url.append(elem_loc)
    elem_url.append(elem_lastmod)
    urlset.append(elem_url)

  random.shuffle(categories_list)
  for cat in categories_list:
    cat_urlencoded = urlencode(cat)

    elem_url = etree.Element("url")
    
    elem_loc = etree.Element("loc")
    elem_loc.text = f"https://b19.se/swish-katalogen/k/{cat_urlencoded}"

    elem_lastmod = etree.Element("lastmod")
    elem_lastmod.text = f"{dest_date_date}T{dest_date_time}+01:00"

    elem_url.append(elem_loc)
    elem_url.append(elem_lastmod)
    urlset.append(elem_url)

  random.shuffle(entries_list)
  for ent in entries_list:
    elem_url = etree.Element("url")
    elem_loc = etree.Element("loc")
    elem_loc.text = f"https://b19.se/swish-katalogen/{ent}"

    elem_lastmod = etree.Element("lastmod")
    elem_lastmod.text = f"{dest_date_date}T{dest_date_time}+01:00"

    elem_url.append(elem_loc)
    elem_url.append(elem_lastmod)
    urlset.append(elem_url)


  xml_contents = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()


  writeXML(XML_DEST_FILE, xml_contents)
  print(f"Done writing {XML_DEST_FILE}")

if __name__ == '__main__':
  main()
