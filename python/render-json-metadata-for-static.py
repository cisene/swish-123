#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re

import json
import datetime

import sqlite3
from sqlite3 import Error

SQLITE_FILE = '../swish-123-data.sqlite'

JSON_CATEGORIES_WEIGHTED_FILE = '../json/categories-weighted.json'
JSON_CATEGORIES_UNIQUE_FILE = '../json/categories-unique.json'
JSON_SEARCHDICTIONARY_FILE = '../json/search-dictionary.json'
JSON_STATISTICS_FILE = '../json/statistics.json'

global conn
global cursor

def fulltrim(data):
  data = re.sub(r"^\s{1,}", "", str(data), flags=re.IGNORECASE)
  data = re.sub(r"\s{1,}$", "", str(data), flags=re.IGNORECASE)
  data = re.sub(r"\s{2,}", " ", str(data), flags=re.IGNORECASE)
  return data


def writeFile(contents, filepath):
  with open(filepath, "w") as f:
    f.write(contents)

def destroy_connection():
  global conn
  global cursor

  if cursor:
    cursor.close()
    cursor = None

  if conn:
    conn.close()
    conn = None

  return

def create_connection(db_file):
  global conn
  global cursor
  conn = None
  cursor = None

  try:
    conn = sqlite3.connect(db_file)
  except Error as e:
    print(e)
  finally:
    pass

  try:
    cursor = conn.cursor()
  except Error as e:
    print(e)
  finally:
    pass

  return


def filterOrgName(data):
  result = []

  not_words = [
    'a',
    'ab',
    'and',
    'as',
    'at',
    'att',
    'den',
    'en',
    'for',
    'för',
    'i',
    'med',
    'mot',
    'och',
    'of'
    'oss',
    'the',
    'to',
    'utan',
    'we',
  ]

  data = data.lower()
  data = re.sub(r"[^a-z0-9åäöẽêĩí\s]", "", str(data), flags=re.IGNORECASE)
  data = fulltrim(data)

  words = re.split(r"\s", data)
  for wrd in words:
    if str(wrd) in not_words:
      continue

    if str(wrd) not in result:
      result.append(str(wrd))

  return result

def filterOrgNumber(data):
  result = []
  data = re.sub(r"[^\d]", "", str(data), flags=re.IGNORECASE)
  if re.search(r"^(\d{10})$", str(data), flags=re.IGNORECASE):
    # Slide with two digits
    for i in range(0,6):
      pat = data[i:(i+2):1]
      if str(pat) not in result:
        result.append(pat)

    # Slide with three digits
    for i in range(0,5):
      pat = data[i:(i+3):1]
      if str(pat) not in result:
        result.append(pat)

  result.sort()
  return result

def filterEntries(data):
  result = []
  if re.search(r"^123(\d{7})$", str(data), flags=re.IGNORECASE):
    data = re.sub(r"^123(\d{7})$", "\\1", str(data), flags=re.IGNORECASE)

    #result.append(data)

    # string[start:end:step]

    # Split and slide with two digits
    for i in range(0,6):
      pat = data[i:(i+2):1]
      if str(pat) not in result:
        result.append(pat)

    # Slide with three digits
    for i in range(0,5):
      pat = data[i:(i+3):1]
      if str(pat) not in result:
        result.append(pat)

  result.sort()
  return result


def filterURL(data):
  data = data.lower()
  data = re.sub(r"^http(s)?\x3a\x2f\x2f", "", str(data), flags=re.IGNORECASE)
  data = re.sub(r"^www\x2e", "", str(data), flags=re.IGNORECASE)

  parts = []
  frags = re.split(r"\x2f", str(data))
  for f in frags:
    print(f)


def getEntriesForMatrix():
  global conn
  global cursor

  filterdict = {}

  query = "SELECT * FROM swish ORDER BY entry ASC;"

  cursor.execute(query)
  records = cursor.fetchall()
  for row in records:
    this_obj = {
      'entry': int(row[0]),
      'orgName': str(row[1]),
      'link': '/swish-katalogen/' + str(row[0])
    }
    coll = []

    if(row[0] != 'None'):
      result = filterEntries(row[0])

      for item in result:
        if str(item) not in filterdict.keys():
          filterdict[str(item)] = []

        if str(item) not in filterdict[str(item)]:
          filterdict[str(item)].append(this_obj)

    if(row[1] != 'None'):
      result = filterOrgName(row[1])

      for item in result:
        if str(item) not in filterdict.keys():
          filterdict[str(item)] = []

        if str(item) not in filterdict[str(item)]:
          filterdict[str(item)].append(this_obj)

    if(row[2] != 'None'):
      result = filterOrgNumber(row[2])

      for item in result:
        if str(item) not in filterdict.keys():
          filterdict[str(item)] = []

        if str(item) not in filterdict[str(item)]:
          filterdict[str(item)].append(this_obj)


  #print(filterdict)
  return filterdict


def getCategoriesUnique():
  global conn
  global cursor

  categories = {}

  categories['data'] = []
  query = "SELECT DISTINCT category FROM categories ORDER BY category ASC;"

  cursor.execute(query)
  records = cursor.fetchall()
  for row in records:
    obj = {
      'caption': str(row[0]),
      'link': "/swish-katalogen/k/" + str(row[0]),
    }

    categories['data'].append(obj)
  return categories

def getEntriesCount():
  global conn
  global cursor

  result = 0

  query = "SELECT COUNT(*) AS cnt FROM swish;"

  cursor.execute(query)
  records = cursor.fetchall()
  for row in records:
    result = int(row[0])

  return result

def getCategoriesCount():
  global conn
  global cursor

  result = 0

  query = "SELECT DISTINCT category AS cnt FROM categories;"

  cursor.execute(query)
  records = cursor.fetchall()
  #for row in records:
  #  result = int(row[0])
  result = len(records)

  return result



def getCategoriesByCount():
  global conn
  global cursor

  categories = {}

  categories['data'] = []
  # let min = 12, max = 24
  # for each tag
  #   font = (items / items in biggest tag) * (max - min) + min



  query = "SELECT category, COUNT(*) AS cnt FROM categories GROUP BY category HAVING cnt >= 3 ORDER BY cnt DESC, category ASC;"

  cursor.execute(query)
  records = cursor.fetchall()
  #print("Total rows are:  ", len(records))

  weights_max = 0
  weights_min = 9999

  tag_min = 0.8
  tag_max = 2.4

  for row in records:
    if int(row[1]) >= weights_max:
      weights_max = int(row[1])

    if int(row[1]) <= weights_min:
      weights_min = int(row[1])

  for row in records:

    cloud_weight = round( (row[1] / weights_max) * (tag_max - tag_min) + tag_min, 2 )

    obj = {
      'caption': str(row[0]),
      'cloud-weight': cloud_weight,
      'link': "/swish-katalogen/k/" + str(row[0]),
      'weight': int(row[1]),
    }

    categories['data'].append(obj)
  return categories


def renderFilterDictionary():
  fullpath = JSON_SEARCHDICTIONARY_FILE
  jsonObj = getEntriesForMatrix()
  file_contents = json.dumps(jsonObj, indent=2, sort_keys=True)

  writeFile(file_contents, fullpath)
  print("Wrote {0} ..".format(str(fullpath)))


def renderCategoriesWeighted():
  fullpath = JSON_CATEGORIES_WEIGHTED_FILE

  jsonObj = getCategoriesByCount()
  
  file_contents = json.dumps(jsonObj, indent=2)

  writeFile(file_contents, fullpath)
  print("Wrote {0} ..".format(str(fullpath)))


def renderCategoriesUnique():
  fullpath = JSON_CATEGORIES_UNIQUE_FILE

  jsonObj = getCategoriesUnique()
  file_contents = json.dumps(jsonObj, indent=2)
  writeFile(file_contents, fullpath)
  print("Wrote {0} ..".format(str(fullpath)))

def renderStatistics():
  fullpath = JSON_STATISTICS_FILE

  entries_count = getEntriesCount()
  categories_count = getCategoriesCount()

  updated = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()

  obj = {
    'entries': entries_count,
    'categories': categories_count,
    'updated': updated,
  }

  file_contents = json.dumps(obj, indent=2)
  writeFile(file_contents, fullpath)
  print("Wrote {0} ..".format(str(fullpath)))




def main():
  create_connection(SQLITE_FILE)

  #renderCategoriesWeighted()
  #renderCategoriesUnique()
  #renderFilterDictionary()

  renderStatistics()

  destroy_connection()


if __name__ == '__main__':
  main()
