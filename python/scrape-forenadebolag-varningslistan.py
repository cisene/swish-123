#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import yaml
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse

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
  return data

def formatOrgNumber(data):
  data = re.sub(r"[^x\d\x2d]", "", data, flags=re.IGNORECASE)
  if not re.search(r"^(\d{6})\x2d(\d{4}|XXXX)$", data, flags=re.IGNORECASE):
    data = re.sub(r"^(\d{6})(\d{4}|XXXX)$", "\\1-\\2", data, flags=re.IGNORECASE)

  return data


def main():
  url = 'https://forenadebolag.se/varningslistan-filter/'

  vl = {}
  vl["organisations"] = []

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
            #print(link_href)

    #exit(0)
    results = soup.find_all("div", class_="result-sf-filter-box")

    for chunk in results:
      objs = {}

      item_date = None
      item_orgName = None
      item_orgNumber = None

      li_list = chunk.find_all("li")
      for li in li_list:

        #print(f"li: {li.text}")

        if re.match(r"senast\sändrad\x3a", li.text, flags=re.IGNORECASE):
          item_date = extractDate(li.text)

          if item_date == '' or item_date == None:
            item_date = '1970-01-01'

        if re.match(r"Företagsnamn\x3a", li.text, flags=re.IGNORECASE):
          item_orgName = extractOrgName(li.text)

        if re.match(r"Org\x2enr\x3a", li.text, flags=re.IGNORECASE):
          item_orgNumber = extractOrgNumber(li.text)
          #print(item_orgNumber)
          if item_orgNumber != None:
            item_orgNumber = formatOrgNumber(item_orgNumber)
            #print(item_orgNumber)

      obj = {
        'orgNumber': item_orgNumber,
        'orgName': item_orgName,
        'date': item_date
      }

      if obj["orgNumber"] != None:
        if re.match(r"^(\d{6})\x2d([0-9X]{4})$", obj["orgNumber"], flags=re.IGNORECASE):
          vl["organisations"].append(obj)
          print(f"\t{obj}")


  writeYAML('../yaml/masterdata-forenadebolag-varningslistan.yaml', vl)

if __name__ == '__main__':
  main()
