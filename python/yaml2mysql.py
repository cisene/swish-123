#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re

import argparse


import yaml
import mysql.connector


# YAML_SOURCE_FILE = '../yaml/entries.yaml'
YAML_SOURCE_FILE = '../yaml/swish-123-datasource.yaml'

APP_NAME = 'Yaml2MySQL'
APP_VERSION = '0.0.1#20240106'

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

def updateDatabase(entries):
  result = { 'all': len(entries['entries']), 'blocked': 0, 'updated': 0 }
  buffer = []

  line_count = 1

  #category_block = [
  #  'overifierad',
  #  'suspended',
  #  'terminated',
  #  'verified',
  #  'verifierad',
  #  'retired',
  #]

  if len(entries['entries']) > 0:
    query = "TRUNCATE TABLE categories;"
    cur_channel_write.execute(query)
    print(f"Truncating table 'categories' ..")

    query = "TRUNCATE TABLE swish;"
    cur_channel_write.execute(query)
    print(f"Truncating table 'swish' ..")

    conn.commit()


  for VO in entries['entries']:

    if "categories" in VO:
      categories = VO['categories']

    entry = ""
    if "entry" in VO:
      entry = VO['entry']

    #if categories == None:
    #  #print(f"{entry} had no categories .. skipping")
    #  result['blocked'] += 1
    #  continue

    #category_skip = False
    #for category in categories:
    #  if category in category_block:
    #    #print(f"{entry} had '{category}' .. skipping")
    #    category_skip = True

    #if category_skip == True:
    #  result['blocked'] += 1
    #  continue

    # Print progress
    if (line_count % 500) == 0:
      line_p = round(((line_count / result['all']) * 100), 2)
      print(f"{line_p}% @ {entry}")

    orgName = ""
    if "orgName" in VO:
      if VO['orgName'] != None:
        orgName = safeSQL(VO['orgName'])

    # If orgName is missing, skip it
    #if orgName == "":
    #  result['blocked'] += 1
    #  continue

    orgNumber = ""
    if "orgNumber" in VO:
      if VO['orgNumber'] != None:
        orgNumber = safeSQL(VO['orgNumber'])

    # If orgNumber is missing, skip it
    #if orgNumber == "":
    #  result['blocked'] += 1
    #  continue

    web = ""
    if "web" in VO:
      if VO['web'] != None:
        web = safeSQL(VO['web'])

    comment = ""
    if "comment" in VO:
      if VO['comment'] != None:
        comment = safeSQL(VO['comment'])

    query = f"INSERT INTO swish (entry, orgName, orgNumber, comment, web) VALUES({entry},'{orgName}','{orgNumber}','{comment}','{web}') ON DUPLICATE KEY UPDATE orgName = '{orgName}', orgNumber = '{orgNumber}', comment = '{comment}', web = '{web}';"
    #print(query)
    cur_channel_write.execute(query)

    for category in categories:
      safe_category = safeSQL(category)
      query = f"INSERT INTO categories (entry, category) VALUES({entry}, '{safe_category}') ON DUPLICATE KEY UPDATE category = '{safe_category}';"
      #print(query)
      cur_channel_write.execute(query)

    conn.commit()
    result['updated'] += 1
    line_count += 1

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

  print(f"{db_host}:{db_port} - {db_username}:{db_password} - {db_database}")

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

if __name__ == '__main__':
  main()
