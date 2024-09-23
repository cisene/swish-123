#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import yaml
import requests
import csv

from dateutil.parser import parse

from collections import OrderedDict

CSV_SOURCE_FILE = './varningslistan.csv'

YAML_DEST_FILE = '../yaml/masterdata-svenskhandel-varningslistan.yaml'

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

def writeText(filepath, contents):
  with open(filepath, "w") as f:
    f.write(contents)

def fulltrim(data):
  data = re.sub(r"^\s{1,}", "", str(data), flags=re.IGNORECASE)
  data = re.sub(r"\s{1,}$", "", str(data), flags=re.IGNORECASE)
  data = re.sub(r"\s{2,}", " ", str(data), flags=re.IGNORECASE)
  return data

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

  vl = {}
  vl["organisations"] = []

  urls = []
  urls.append(url)

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

        if(
          re.match(r"^(\d{6})\x2d(\d{4})$", row_orgNumber)
        ):
          org = {
            'orgNumber' : f"{row_orgNumber}",
            'orgName': f"{row_BolagsNamn}",
          }
          vl['organisations'].append(org)

  writeYAML(YAML_DEST_FILE, vl)

if __name__ == '__main__':
  main()
