#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re

import argparse

import yaml
import mysql.connector


YAML_SOURCE_FILE = '../yaml/swish-123-datasource.yaml'

APP_NAME = 'Yaml2MySQL'
APP_VERSION = '0.0.2#20250813'

global conn
global cur_channel_write

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

def updateTablesFromTemp():
  global cur_channel_write

  query = "TRUNCATE TABLE b19_se.categories;"
  cur_channel_write.execute(query)

  query = """INSERT INTO b19_se.categories (entry, category)
  SELECT entry, category FROM b19_se.tempcategories ORDER BY entry ASC, category ASC;"""

  cur_channel_write.execute(query)

  query = "TRUNCATE TABLE b19_se.swish;"
  cur_channel_write.execute(query)

  query = """INSERT INTO b19_se.swish (entry, orgName, orgNumber, comment, web)
  SELECT entry, orgName, orgNumber, comment, web FROM b19_se.tempswish ORDER BY entry ASC;"""
  cur_channel_write.execute(query)


def updateDatabase(entries):
  #result = { 'all': len(entries['entries']), 'blocked': 0, 'updated': 0 }
  result = { 'all': len(entries['entries']), 'updated': 0 }
  buffer = []

  line_count = 1

  if len(entries['entries']) > 0:
    #query = "TRUNCATE TABLE categories;"
    query = "TRUNCATE TABLE tempcategories;"
    cur_channel_write.execute(query)
    print(f"Truncating temporary table 'tempcategories' ..")

    #query = "TRUNCATE TABLE swish;"
    query = "TRUNCATE TABLE tempswish;"
    cur_channel_write.execute(query)
    print(f"Truncating temporary table 'tempswish' ..")

    conn.commit()

  for VO in entries['entries']:

    if "categories" in VO:
      categories = VO['categories']

    entry = ""
    if "entry" in VO:
      entry = VO['entry']

    # Print progress
    if (line_count % 500) == 0:
      line_p = round(((line_count / result['all']) * 100), 2)
      print(f"{line_p}% @ {entry}")

    orgName = ""
    if "orgName" in VO:
      if VO['orgName'] != None:
        orgName = safeSQL(VO['orgName'])

    orgNumber = ""
    if "orgNumber" in VO:
      if VO['orgNumber'] != None:
        orgNumber = safeSQL(VO['orgNumber'])

    web = ""
    if "web" in VO:
      if VO['web'] != None:
        web = safeSQL(VO['web'])

    comment = ""
    if "comment" in VO:
      if VO['comment'] != None:
        comment = safeSQL(VO['comment'])

    #query = f"INSERT INTO swish (entry, orgName, orgNumber, comment, web) VALUES({entry},'{orgName}','{orgNumber}','{comment}','{web}') ON DUPLICATE KEY UPDATE orgName = '{orgName}', orgNumber = '{orgNumber}', comment = '{comment}', web = '{web}';"
    query = f"INSERT INTO tempswish (entry, orgName, orgNumber, comment, web) VALUES({entry},'{orgName}','{orgNumber}','{comment}','{web}') ON DUPLICATE KEY UPDATE orgName = '{orgName}', orgNumber = '{orgNumber}', comment = '{comment}', web = '{web}';"
    #print(query)
    cur_channel_write.execute(query)

    for category in categories:
      safe_category = safeSQL(category)
      #query = f"INSERT INTO categories (entry, category) VALUES({entry}, '{safe_category}') ON DUPLICATE KEY UPDATE category = '{safe_category}';"
      query = f"INSERT INTO tempcategories (entry, category) VALUES({entry}, '{safe_category}') ON DUPLICATE KEY UPDATE category = '{safe_category}';"
      #print(query)
      cur_channel_write.execute(query)

    conn.commit()
    result['updated'] += 1
    line_count += 1

  line_p = round(((line_count / result['all']) * 100), 2)
  print(f"{line_p}% @ {entry}")

  return result

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

  #print(f"{db_host}:{db_port} - {db_username}:{db_password} - {db_database}")

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

  entries = loadEntries(YAML_SOURCE_FILE)
  print(f"Loaded {len(entries['entries'])} entries from {YAML_SOURCE_FILE}")

  stats = updateDatabase(entries)
  print(stats)

  updateTablesFromTemp()


if __name__ == '__main__':
  main()
