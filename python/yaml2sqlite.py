#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re

import yaml

import sqlite3
from sqlite3 import Error

YAML_SOURCE_FILE = '../yaml/entries.yaml'

SQLITE_FILE = '../swish-123-data.sqlite'

global conn

def safeSQL(data):
  data = re.sub(r"\x27", "''", str(data), flags=re.IGNORECASE)
  return data


def loadYamlIntoDb(filepath):
  global conn

  category_block = [
    'overifierad',
    'suspended',
    'terminated',
    'verified',
    'verifierad',
  ]

  cursor = conn.cursor()

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
    data = yaml.safe_load(contents)


    buffer = []
    values_list = []

    categories_list = []

    for VO in data['entries']:

      if len(buffer) == 0:
        buffer.append("INSERT INTO swish (entry, orgName, orgNumber, web, comment) VALUES ")

      entry = None
      orgName = None
      orgNumber = None
      web = None
      categories = None
      comment = None

      if "entry" in VO:
        entry = VO['entry']

      if "orgName" in VO:
        if VO['orgName'] != None:
          orgName = safeSQL(VO['orgName'])

      if "orgNumber" in VO:
        if VO['orgNumber'] != None:
          orgNumber = safeSQL(VO['orgNumber'])

      if "web" in VO:
        if VO['web'] != None:
          web = safeSQL(VO['web'])

      if "comment" in VO:
        if VO['comment'] != None:
          comment = safeSQL(VO['comment'])

      if "categories" in VO:
        categories = VO['categories']

        if categories != None:
          for cat in categories:
            if cat == "overifierad":
              continue

      if(
        web != None and
        orgNumber != None and
        orgName != None and
        entry != None
      ):

        values = f"({entry}, '{orgName}', '{orgNumber}', '{web}', '{comment}')"
        values_list.append(values)

        if categories != None:
          for category in categories:

            if category == 'overifierad':
              continue

            if category in category_block:
              continue

            values = f"({entry}, '{category}')"
            if values not in categories_list:
              categories_list.append(values)

            if len(categories_list) == 500:
              cl = ",".join(categories_list)
              categories_list = []
              query = "INSERT INTO categories (entry, category) VALUES " + cl + ";"
              cursor.execute(query)
              conn.commit()


      if len(values_list) == 500:
        vl = ",".join(values_list)
        buffer.append(vl)
        buffer.append(";")
        query = "".join(buffer)
        buffer = []
        values_list = []
        cursor.execute(query)
        conn.commit()




    if len(values_list) > 0:
      vl = ",".join(values_list)
      buffer.append(vl)
      buffer.append(";")
      query = "".join(buffer)
      buffer = []
      values_list = []
      cursor.execute(query)
      conn.commit()

    if len(categories_list) > 0:
      cl = ",".join(categories_list)
      categories_list = []
      query = "INSERT INTO categories (entry, category) VALUES " + cl + ";"
      cursor.execute(query)
      conn.commit()


  return


def initiate_database():
  global conn

  # Declare fields and data types
  swish_object = {
    "entry": "INTEGER NOT NULL",
    "orgName": "TEXT NOT NULL",
    "orgNumber": "TEXT NOT NULL",
    "web": "TEXT NOT NULL",
    "comment": "TEXT NOT NULL",

  }

  categories_object = {
    "entry": "INTEGER NOT NULL",
    "category": "TEXT NOT NULL"
  }

  # Create Swish objects
  elements = []
  elements.append("CREATE TABLE IF NOT EXISTS swish (")

  for field in swish_object.keys():
    field = f"{field} {str(swish_object[field])}, "
    elements.append(field)

  elements.append("PRIMARY KEY (entry)")
  elements.append(") WITHOUT ROWID;")

  query = "".join(elements)
  query = re.sub(r"\x2c\x20\x29", ")", str(query), flags=re.IGNORECASE)

  try:
    c = conn.cursor()
    c.execute(query)
  except Error as e:
    print(e)

  # Create Categories
  elements = []
  elements.append("CREATE TABLE IF NOT EXISTS categories (")

  for field in categories_object.keys():
    field = f"{field} {str(categories_object[field])}, "
    elements.append(field)

  elements.append("PRIMARY KEY (entry, category)")
  elements.append(") WITHOUT ROWID;")

  query = "".join(elements)
  query = re.sub(r"\x2c\x20\x29", ")", str(query), flags=re.IGNORECASE)
  #print(query)

  try:
    c = conn.cursor()
    c.execute(query)
  except Error as e:
    print(e)



  return

def destroy_connection():
  global conn
  if conn:
    conn.close()
    conn = None
  return

def create_connection(db_file):
  global conn
  conn = None
  try:
    conn = sqlite3.connect(db_file)
  except Error as e:
    print(e)
  finally:
    pass

  return

def removeDatabaseFile(filepath):
  if os.path.isfile(filepath):
    os.unlink(filepath)
    print(f"Deleted {filepath} as it existed")

def main():
  removeDatabaseFile(SQLITE_FILE)

  create_connection(SQLITE_FILE)

  initiate_database()
  loadYamlIntoDb(YAML_SOURCE_FILE)

  destroy_connection()


if __name__ == '__main__':
  main()
