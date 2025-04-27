#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import yaml
import requests
import csv
from dateutil.parser import parse

from datetime import datetime

import operator
from operator import *

from operator import itemgetter

CSV_SOURCE_FILE = './varningslistan.csv'

YAML_SOURCE_FILE = '../yaml/masterdata-svenskhandel-varningslistan.yaml'

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

def writeText(filepath, contents):
  with open(filepath, "w") as f:
    f.write(contents)

def fulltrim(data):
  data = re.sub(r"^\s{1,}", "", str(data), flags=re.IGNORECASE)
  data = re.sub(r"\s{1,}$", "", str(data), flags=re.IGNORECASE)
  data = re.sub(r"\s{2,}", " ", str(data), flags=re.IGNORECASE)
  return data

def formatOrgNumber(data):
  data = re.sub(r"[^x\d\x2d]", "", data, flags=re.IGNORECASE)
  if not re.search(r"^(\d{6})\x2d(\d{4}|XXXX)$", data, flags=re.IGNORECASE):
    data = re.sub(r"^(\d{6})(\d{4}|XXXX)$", "\\1-\\2", data, flags=re.IGNORECASE)

  return data

def cloneVO(thisVO):

  vo =  {
    'orgNumber': None,
    'orgName': None,
    'date': None,

    '_SeenFirst': None,
    '_SeenLast': None,
  }

  if thisVO != None:

    if "orgNumber" in thisVO:
      if thisVO['orgNumber'] != None:
        vo['orgNumber'] = thisVO['orgNumber']

    if "orgName" in thisVO:
      if thisVO['orgName'] != None:
        vo['orgName'] = thisVO['orgName']

    if "date" in thisVO:
      if thisVO['date'] != None:
        vo['date'] = thisVO['date']

    if "_SeenFirst" in thisVO:
      if thisVO['_SeenFirst'] != None:
        vo['_SeenFirst'] = thisVO['_SeenFirst']

    if "_SeenLast" in thisVO:
      if thisVO['_SeenLast'] != None:
        vo['_SeenLast'] = thisVO['_SeenLast']

  return vo

def findVO(orgNumber):
  global vl

  obj = None

  if orgNumber != None:

    for o in vl['organisations']:
      if o['orgNumber'] != None:

        if o['orgNumber'] == orgNumber:
          obj = o
          break

  return obj

#  0 - "Namn";
#  1 - "Bolagsnamn";
#  2 - "Org.Nr.";
#  3 - "Bankgiro";
#  4 - "Plusgiro";
#  5 - "Gatuadress";
#  6 - "Postadress";
#  7 - "Telefonnummer";
#  8 - "Faxnummer";
#  9 - "Status"

# https://analys.bisnis.se/external/warninglist

def main():
  global vl
  source_dict = readYAML(YAML_SOURCE_FILE)

  url = 'https://www.svenskhandel.se/api/varningslistan/csv'

  csvhead = [
    "Namn",
    "Bolagsnamn",
    "Org.Nr.",
    "Bankgiro",
    "Plusgiro",
    "Gatuadress",
    "Postadress",
    "Telefonnummer",
    "Faxnummer",
    "Status",
  ]

  seen_before = []

  if source_dict == None:
    vl = {}
  else:
    vl = source_dict

  if "organisations" not in vl:
    vl["organisations"] = []

  dest_list = []

  urls = []
  urls.append(url)

  now = datetime.now()
  for url in urls:
    print(f"Requested URL: {url}")
    headers = {
      'Accept-Content':   'text/csv',
      'Accept-Charset':   'iso-8859-2',
    }

    csv_data = requests.get(url, headers=headers)
    if csv_data.encoding != 'utf-8':
      csv_data.encoding = 'utf-8'

    writeText(CSV_SOURCE_FILE, csv_data.text)

    with open(CSV_SOURCE_FILE, newline='') as csvfile:
      dialect = csv.Sniffer().sniff(csvfile.read(1024))
      csvfile.seek(0)
      reader = csv.reader(csvfile, dialect)

      for row in reader:
        row_BolagsNamn  = fulltrim(row[1])
        row_orgNumber   = fulltrim(row[2])

        if re.match(r"^(\d{6})\x2d(\d{4})$", row_orgNumber):

          if row_orgNumber not in seen_before:
            thisVO = findVO(row_orgNumber)
            if thisVO == None:
              obj = {
                'orgNumber' : f"{row_orgNumber}",
                'orgName': f"{row_BolagsNamn}",
                'date': None,
                '_SeenFirst': None,
                '_SeenLast': None
              }
            else:
              obj = cloneVO(thisVO)

              obj['_SeenLast'] = now.strftime("%Y-%m-%dT%H:%M:%S%z")
          
              if obj['_SeenFirst'] == None:
                obj['_SeenFirst'] = now.strftime("%Y-%m-%dT%H:%M:%S%z")

              if obj['date'] == None:
                obj['date'] = '1970-01-01'

              if obj['orgName'] != row_BolagsNamn:
                obj['orgName'] = row_BolagsNamn

              #if obj['date'] != item_date:
              #  obj['date'] = item_date

          else:
            continue

          dest_list.append(obj)
          seen_before.append(row_orgNumber)

  sorted_vl = sorted(dest_list, key=itemgetter('orgNumber'))

  #print(sorted_vl)
  vl['organisations'] = sorted_vl


  writeYAML(YAML_SOURCE_FILE, vl)
  print(f"Wrote '{YAML_SOURCE_FILE} ..")

  # Cleanup - remove the saved CSV
  if os.path.exists(CSV_SOURCE_FILE):
    os.remove(CSV_SOURCE_FILE)


if __name__ == '__main__':
  main()
