#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import random

import yaml
import json

from lxml import etree

from datetime import datetime

#YAML_SOURCE_FILE = '../yaml/swish-123-datasource.yaml'
JSON_SOURCE_FILE = '../json/swish-123-datasource.json'

XML_DEST_FILE = '../xml/sitemap.xml'

def writeXML(filepath, contents):
  with open(filepath, "w") as f:
    f.write(contents)

def siteMapUrlencode(data):
  #data = str(data.encode('utf-8'))
  data = re.sub(r"\x20", "+", str(data), flags=re.IGNORECASE)

  # å
  data = re.sub(r"å", r"%C3%A5", str(data), flags=re.IGNORECASE)

  # ä
  data = re.sub(r"ä", r"%C3%A4", str(data), flags=re.IGNORECASE)

  # ö
  data = re.sub(r"ö", r"%C3%B6", str(data), flags=re.IGNORECASE)

  # é
  data = re.sub(r"é", r"%C3%A9", str(data), flags=re.IGNORECASE)

  return data

def readJSON(filepath):
  contents = None
  if os.path.isfile(filepath):
    #print(f"file exists '{filepath}")
    with open(filepath) as json_data:
      contents = json.load(json_data)
      json_data.close()

  return contents

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

def sitemapMisc(filelist):
  url_base = "https://b19.se/swish-katalogen/"

  global dest_date_date
  global dest_date_time
  global ns

  files_created = []

  file_split_counter = 0
  line_count = 0

  while (True):

    if line_count == 0:
      # <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      urlset = etree.Element("urlset", nsmap = ns)

    for ent in sorted(filelist):
      elem_url = etree.Element("url")
      elem_loc = etree.Element("loc")
      elem_loc.text = f"{url_base}{siteMapUrlencode(ent)}"

      elem_lastmod = etree.Element("lastmod")
      elem_lastmod.text = f"{dest_date_date}T{dest_date_time}+01:00"

      #elem_changefreq = etree.Element("changefreq")
      #elem_changefreq.text = str("weekly")

      elem_url.append(elem_loc)
      elem_url.append(elem_lastmod)
      #elem_url.append(elem_changefreq)

      urlset.append(elem_url)
      line_count += 1

      if line_count >= 5000:
        xml_contents = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()
        filename = f"sitemap-misc-{file_split_counter}.xml"
        filepath = f"../{filename}"
        writeXML(filepath, xml_contents)

        print(f"Writing {line_count} entries to {filename} .. ")
        files_created.append(filename)

        line_count = 0
        file_split_counter += 1

    # We're out of the main loop, save stuff
    if line_count > 0:
      xml_contents = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()
      filename = f"sitemap-misc-{file_split_counter}.xml"
      filepath = f"../{filename}"
      writeXML(filepath, xml_contents)

      print(f"Writing {line_count} entries to {filename} .. ")
      files_created.append(filename)

    break

  return files_created

def sitemapOrganizations(organisationList):
  url_base = "https://b19.se/swish-katalogen/o/"

  global dest_date_date
  global dest_date_time
  global ns

  files_created = []

  file_split_counter = 0
  line_count = 0

  while (True):

    if line_count == 0:
      # <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      urlset = etree.Element("urlset", nsmap = ns)

    for ent in sorted(organisationList):
      elem_url = etree.Element("url")
      elem_loc = etree.Element("loc")
      elem_loc.text = f"{url_base}{ent}"

      elem_lastmod = etree.Element("lastmod")
      elem_lastmod.text = f"{dest_date_date}T{dest_date_time}+01:00"

      #elem_changefreq = etree.Element("changefreq")
      #elem_changefreq.text = str("weekly")

      elem_url.append(elem_loc)
      elem_url.append(elem_lastmod)
      #elem_url.append(elem_changefreq)

      urlset.append(elem_url)
      line_count += 1

      if line_count >= 5000:
        xml_contents = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()
        filename = f"sitemap-organisations-{file_split_counter}.xml"
        filepath = f"../{filename}"
        writeXML(filepath, xml_contents)

        print(f"Writing {line_count} entries to {filename} .. ")
        files_created.append(filename)

        line_count = 0
        file_split_counter += 1

    # We're out of the main loop, save stuff
    if line_count > 0:
      xml_contents = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()
      filename = f"sitemap-organisations-{file_split_counter}.xml"
      filepath = f"../{filename}"
      writeXML(filepath, xml_contents)

      print(f"Writing {line_count} entries to {filename} .. ")
      files_created.append(filename)

    break

  return files_created

def sitemapCategories(categoriesList):
  url_base = "https://b19.se/swish-katalogen/k/"

  global dest_date_date
  global dest_date_time
  global ns

  files_created = []

  file_split_counter = 0
  line_count = 0

  while (True):

    if line_count == 0:
      # <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      urlset = etree.Element("urlset", nsmap = ns)

    for ent in sorted(categoriesList):
      elem_url = etree.Element("url")
      elem_loc = etree.Element("loc")
      elem_loc.text = f"{url_base}{siteMapUrlencode(ent)}"

      elem_lastmod = etree.Element("lastmod")
      elem_lastmod.text = f"{dest_date_date}T{dest_date_time}+01:00"

      #elem_changefreq = etree.Element("changefreq")
      #elem_changefreq.text = str("weekly")

      elem_url.append(elem_loc)
      elem_url.append(elem_lastmod)
      #elem_url.append(elem_changefreq)

      urlset.append(elem_url)
      line_count += 1

      if line_count >= 5000:
        xml_contents = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()
        filename = f"sitemap-categories-{file_split_counter}.xml"
        filepath = f"../{filename}"
        writeXML(filepath, xml_contents)

        print(f"Writing {line_count} entries to {filename} .. ")
        files_created.append(filename)

        line_count = 0
        file_split_counter += 1

    # We're out of the main loop, save stuff
    if line_count > 0:
      xml_contents = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()
      filename = f"sitemap-categories-{file_split_counter}.xml"
      filepath = f"../{filename}"
      writeXML(filepath, xml_contents)

      print(f"Writing {line_count} entries to {filename} .. ")
      files_created.append(filename)

    break

  return files_created

def sitemapNumbers(numbersList):
  global dest_date_date
  global dest_date_time
  global ns

  files_created = []

  url_base = "https://b19.se/swish-katalogen/"
  file_split_counter = 0
  line_count = 0

  while (True):

    if line_count == 0:
      # <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      urlset = etree.Element("urlset", nsmap = ns)

    for ent in sorted(numbersList):
      elem_url = etree.Element("url")
      elem_loc = etree.Element("loc")
      elem_loc.text = f"{url_base}{ent}"

      elem_lastmod = etree.Element("lastmod")
      elem_lastmod.text = f"{dest_date_date}T{dest_date_time}+01:00"

      # <changefreq>weekly</changefreq>
      #elem_changefreq = etree.Element("changefreq")
      #elem_changefreq.text = str("weekly")

      elem_url.append(elem_loc)
      elem_url.append(elem_lastmod)
      #elem_url.append(elem_changefreq)

      urlset.append(elem_url)
      line_count += 1

      if line_count >= 5000:
        xml_contents = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()
        filename = f"sitemap-numbers-{file_split_counter}.xml"
        filepath = f"../{filename}"
        writeXML(filepath, xml_contents)

        print(f"Writing {line_count} entries to {filename} .. ")
        files_created.append(filename)

        line_count = 0
        file_split_counter += 1

    # We're out of the main loop, save stuff
    if line_count > 0:
      xml_contents = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()
      filename = f"sitemap-numbers-{file_split_counter}.xml"
      filepath = f"../{filename}"
      writeXML(filepath, xml_contents)

      print(f"Writing {line_count} entries to {filename} .. ")
      files_created.append(filename)

    break

  return files_created

def sitemapIndex(filelist):
  url_base = "https://b19.se/swish-katalogen/"

  line_count = 0

  urlset = etree.Element("sitemapindex", nsmap = ns)

  for ent in sorted(filelist):
    elem_sitemap = etree.Element("sitemap")
    elem_loc = etree.Element("loc")
    elem_loc.text = f"{url_base}{ent}"

    elem_lastmod = etree.Element("lastmod")
    elem_lastmod.text = f"{dest_date_date}T{dest_date_time}+01:00"

    # <changefreq>weekly</changefreq>
    #elem_changefreq = etree.Element("changefreq")
    #elem_changefreq.text = str("weekly")

    elem_sitemap.append(elem_loc)
    elem_sitemap.append(elem_lastmod)
    #elem_sitemap.append(elem_changefreq)

    urlset.append(elem_sitemap)
    line_count += 1

  filename = f"sitemap.xml"
  filepath = f"../{filename}"
  xml_contents = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode()
  writeXML(filepath, xml_contents)

  print(f"Writing {line_count} SiteMapIndex entries to {filename} .. ")

  return

def main():
  global source_dict

  global dest_date_time
  global dest_date_date

  global ns

  print(f"Reading source JSON: {JSON_SOURCE_FILE} ..")
  source_dict = readJSON(JSON_SOURCE_FILE)

  if source_dict == None:
    print(f"Could not read {JSON_SOURCE_FILE}")
    exit(1)

  sitemapIndex_files = []

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

  for entryVO in source_dict['data']:
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

  sitemap_files = sitemapNumbers(entries_list)
  for f in sitemap_files:
    if f not in sitemapIndex_files:
      sitemapIndex_files.append(f)

  sitemap_files = sitemapOrganizations(org_list)
  for f in sitemap_files:
    if f not in sitemapIndex_files:
      sitemapIndex_files.append(f)

  sitemap_files = sitemapCategories(categories_list)
  for f in sitemap_files:
    if f not in sitemapIndex_files:
      sitemapIndex_files.append(f)

  # Special cast - add everything else of importance
  files_list = [
    'swish-123.pdf',
    'swishkatalogen-godkanda-gavomottagare.pdf',
    'swishkatalogen-insamlingskontroll.pdf',
    'swishkatalogen-kvinnojourer.pdf'
  ]

  sitemap_files = sitemapMisc(files_list)
  for f in sitemap_files:
    if f not in sitemapIndex_files:
      sitemapIndex_files.append(f)


  sitemapIndex(sitemapIndex_files)


if __name__ == '__main__':
  main()
