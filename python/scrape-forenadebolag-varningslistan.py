#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import yaml
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse

from datetime import datetime

import operator
from operator import *

from operator import itemgetter

YAML_SOURCE_FILE = '../yaml/masterdata-varningslistan.yaml'

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


def fulltrim(data):
  data = re.sub(r"^\s{1,}", "", str(data), flags=re.IGNORECASE)
  data = re.sub(r"\s{1,}$", "", str(data), flags=re.IGNORECASE)
  data = re.sub(r"\s{2,}", " ", str(data), flags=re.IGNORECASE)
  return data

def extractDate(data):
  data = re.sub(r"senast\sändrad\x3a\s", "", data, flags=re.IGNORECASE)

  if data == "":
    return ""

  data = re.sub(r"januari", "January", data, flags=re.IGNORECASE)
  data = re.sub(r"februari", "February", data, flags=re.IGNORECASE)
  data = re.sub(r"mars", "March", data, flags=re.IGNORECASE)
  data = re.sub(r"april", "April", data, flags=re.IGNORECASE)
  data = re.sub(r"maj", "May", data, flags=re.IGNORECASE)
  data = re.sub(r"juni", "June", data, flags=re.IGNORECASE)

  data = re.sub(r"juli", "July", data, flags=re.IGNORECASE)
  data = re.sub(r"augusti", "August", data, flags=re.IGNORECASE)
  data = re.sub(r"september", "September", data, flags=re.IGNORECASE)
  data = re.sub(r"oktober", "October", data, flags=re.IGNORECASE)
  data = re.sub(r"november", "November", data, flags=re.IGNORECASE)
  data = re.sub(r"december", "December", data, flags=re.IGNORECASE)

  #print(data)
  dt = parse(data)
  #print(dt.strftime('%Y-%m-%d'))

  return dt.strftime('%Y-%m-%d')

def extractOrgName(data):
  data = re.sub(r"Företagsnamn\x3a\s", "", data, flags=re.IGNORECASE)
  return data

def extractOrgNumber(data):
  data = re.sub(r"Org\x2enr\x3a\s", "", data, flags=re.IGNORECASE)
    
  if not re.search(r"^(\d{6})\x2d(\d{4})$", str(data), flags=re.IGNORECASE):
    data = None

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


#  dest_date_date = now.strftime("%Y-%m-%d")


def main():
  global vl
  source_dict = readYAML(YAML_SOURCE_FILE)

  url = 'https://forenadebolag.se/varningslistan-filter/'

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

  for url in urls:
    print(f"Requested URL: {url}")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    links = soup.find_all('a')
    for link in links:
      link_href = link["href"]
      if link_href != None:
        if re.match(r"^https\x3a\x2f\x2fforenadebolag\x2ese\x2fvarningslistan\x2dfilter\x2f\x3fsf\x5fpaged\x3d(\d{1,})$", link_href, flags=re.IGNORECASE):
          if link_href not in urls:
            urls.append(link_href)

    results = soup.find_all("div", class_="result-sf-filter-box")

    print(f"\tFound {len(results)} entries ...")
    for chunk in results:
      objs = {}

      item_date = None
      item_orgName = None
      item_orgNumber = None

      li_list = chunk.find_all("li")
      now = datetime.now()

      for li in li_list:

        if re.match(r"senast\sändrad\x3a", li.text, flags=re.IGNORECASE):
          item_date = extractDate(li.text)

          if item_date == '' or item_date == None:
            item_date = '1970-01-01'

        if re.match(r"Företagsnamn\x3a", li.text, flags=re.IGNORECASE):
          item_orgName = extractOrgName(li.text)

        if re.match(r"Org\x2enr\x3a", li.text, flags=re.IGNORECASE):
          item_orgNumber = extractOrgNumber(li.text)
          if item_orgNumber != None:
            item_orgNumber = formatOrgNumber(item_orgNumber)

            if item_orgNumber not in seen_before:

              thisVO = findVO(item_orgNumber)
              if thisVO == None: 
                print(f"Object lookup missed")
                obj = {
                  'orgNumber': item_orgNumber,
                  'orgName': [item_orgName],
                  'date': item_date,
                  '_SeenFirst': None,
                  '_SeenLast': None
                }

              else:
                obj = cloneVO(thisVO)

              obj['_SeenLast'] = now.strftime("%Y-%m-%dT%H:%M:%S%z")
              
              if obj['_SeenFirst'] == None:
                obj['_SeenFirst'] = now.strftime("%Y-%m-%dT%H:%M:%S%z")

              if obj['orgName'] != item_orgName:
                if item_orgName not in obj['orgName']:
                  obj['orgName'].append(item_orgName)

              if obj['date'] != item_date:
                obj['date'] = item_date

            else:
              continue

            dest_list.append(obj)
            seen_before.append(item_orgNumber)

  for vo in source_dict['organisations']:
    if vo['orgNumber'] not in seen_before:
      dest_list.append(vo)
      print(f"\t{vo['orgNumber']} wasn't seen, copying from source")

  sorted_vl = sorted(dest_list, key=itemgetter('orgNumber'))

  #print(sorted_vl)
  vl['organisations'] = sorted_vl


  writeYAML(YAML_SOURCE_FILE, vl)
  print(f"Wrote '{YAML_SOURCE_FILE} ..")


if __name__ == '__main__':
  main()
