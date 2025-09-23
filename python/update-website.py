#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re

import argparse

import yaml
import json
import mysql.connector

YAML_SOURCE_FILE = '../yaml/swish-123-datasource.yaml'
JSON_SOURCE_FILE = '../json/swish-123-datasource.json'

APP_NAME = 'Update-Website'
APP_VERSION = '0.0.2#20250923'

global conn
global cur_channel_write

def readJSON(filepath):
  contents = None
  if os.path.isfile(filepath):
    with open(filepath) as json_data:
      contents = json.load(json_data)
      json_data.close()

  return contents

def safeSQL(data):
  data = re.sub(r"\x27", "''", str(data), flags=re.IGNORECASE)
  return data

def loadEntries(filepath):
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

def updateEntries(entries):
  entries_list = []
  entries_count = 0

  if "entries" in entries:
    for entryVO in entries['entries']:
      item = f"({safeSQL(entryVO['entry'])},'{safeSQL(entryVO['orgName'])}','{safeSQL(entryVO['orgNumber'])}','{safeSQL(entryVO['comment'])}','{safeSQL(entryVO['web'])}')"
      entries_list.append(item)


    query = "TRUNCATE TABLE b19_se.tempswish;"
    cur_channel_write.execute(query)
    print(f"Truncating table 'swish' ..")
    conn.commit()

    entries_count = len(entries_list)
    while (len(entries_list) > 0):
      line_count = 0
      line_buffer = []

      while ((len(line_buffer) < 500) and (len(entries_list) >= 1)):
        line_buffer.append(entries_list.pop())
        line_count += 1

      line_values = ", ".join(line_buffer)
      query = f"INSERT INTO b19_se.swish (entry, orgName, orgNumber, comment, web) VALUES {line_values} ON DUPLICATE KEY UPDATE entry = entry;"
      cur_channel_write.execute(query)

    conn.commit()


def updateCategories(entries):
  categories_list = []
  categories_count = 0

  if "entries" in entries:
    for entryVO in entries['entries']:
      entry_id = entryVO['entry']
      entry_cats = None
      
      if entryVO['categories'] == None:
        continue
      else:
        entry_cats = entryVO['categories']

      for cat in entry_cats:
        item_cat = f"({entry_id},'{safeSQL(cat)}')"
        if item_cat not in categories_list:
          categories_list.append(item_cat)

    query = "TRUNCATE TABLE b19_se.categories;"
    cur_channel_write.execute(query)
    conn.commit()
    print(f"Truncating table 'categories' ..")

    categories_count = len(categories_list)
    while (len(categories_list) > 0):
      line_count = 0
      line_buffer = []
      while ((len(line_buffer) < 500) and (len(categories_list) >= 1)):
        line_buffer.append(categories_list.pop())
        line_count += 1

      line_values = ", ".join(line_buffer)
      query = f"INSERT INTO b19_se.categories (entry, category) VALUES {line_values} ON DUPLICATE KEY UPDATE entry = entry;"
      #print(query)
      cur_channel_write.execute(query)

      #print(len(categories_list))

    conn.commit()

def connectMySQL(db_host, db_port, db_database, db_username, db_password):
  global conn

  global cur_channel_read
  global cur_channel_write
 
  conn = mysql.connector.connect(
    user=db_username,
    password=db_password,
    host=db_host,
    database=db_database,
    charset='utf8',
    use_unicode=True,
    auth_plugin='mysql_native_password'
  )

  cur_channel_read = conn.cursor(buffered=True)
  cur_channel_write = conn.cursor(buffered=True)

  cur_channel_read.execute('SET NAMES utf8mb4')
  cur_channel_read.execute("SET CHARACTER SET utf8mb4")
  cur_channel_read.execute("SET character_set_connection=utf8mb4")
  cur_channel_read.execute("SET autocommit=0;")

  cur_channel_write.execute('SET NAMES utf8mb4')
  cur_channel_write.execute("SET CHARACTER SET utf8mb4")
  cur_channel_write.execute("SET character_set_connection=utf8mb4")
  cur_channel_write.execute("SET autocommit=0;")

  return

def main():
  global conn
  global cur_channel_write

  print(f"{APP_NAME} Version {APP_VERSION}")

  db_host = None
  if "DB_HOST" in os.environ:
    db_host = os.environ['DB_HOST']

  db_port = None
  if "DB_PORT" in os.environ:
    db_port = os.environ['DB_PORT']

  db_database = None
  if "DB_DATABASE" in os.environ:
    db_database = os.environ['DB_DATABASE']
  
  db_username = None
  if "DB_USERNAME" in os.environ:
    db_username = os.environ['DB_USERNAME']
  
  db_password = None
  if "DB_PASSWORD" in os.environ:
    db_password = os.environ['DB_PASSWORD']

  if(
    db_host is not None and
    db_port is not None and
    db_database is not None and
    db_username is not None and
    db_password is not None
  ):

    connectMySQL(db_host, db_port, db_database, db_username, db_password)
    if conn is not None:
      print(f"\t* MySQL client happily connected")
  else:
    print("** No MySQL credentials found")
    exit(1)

  #entries = loadEntries(YAML_SOURCE_FILE)
  contents = readJSON(JSON_SOURCE_FILE)
  entries = {}
  entries['entries'] = []
  entries['entries'] = contents['data']
  print(f"Loaded {len(entries['entries'])} entries from {YAML_SOURCE_FILE}")

  updateCategories(entries)
  updateEntries(entries)

  print("Done\n")

if __name__ == '__main__':
  main()
