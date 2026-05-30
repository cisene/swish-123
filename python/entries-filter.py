#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import random

import yaml
import json

from collections import defaultdict

from datetime import datetime

YAML_SOURCE_FILE = '../yaml/entries.yaml'

YAML_DEST_DATASOURCE = '../yaml/swish-123-datasource.yaml'



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

def luhn10CalculateCheckDigit(data):
  result = None

  numbers = str(data)
  numbers_list = list(numbers)
  numbers_list.reverse()

  weights = [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]

  checkSum = 0
  for pos in range(0,len(numbers)):
    sums = 0

    sums = (int(weights[pos]) * int(numbers_list[pos]))
    if sums >= 10:
      digits = list(str(sums))
      dSum = int(digits[0]) + int(digits[1])
      checkSum += int(dSum)
    else:
      checkSum += int(sums)

  # c = (10 − (s mod 10 ) ) mod 10 .
  result = (10 - (checkSum % 10)) % 10
  return result


def flattenList(data):
  return ",".join(data)

def validateEntry(data):
  return re.match(r"^123(\d{7})$", str(data), flags=re.IGNORECASE)

def validateEntryStrict(data):
  result = False

  if re.match(r"^123(\d{7})$", str(data), flags=re.IGNORECASE):
    if(
      re.match(r"^123[0-6]{1}(\d{2})(\d{4})$", str(data), flags=re.IGNORECASE)
      or
      re.match(r"^^12390[0-9]{1}(\d{4})$", str(data), flags=re.IGNORECASE)
    ):
      result = True

  return result

def validateEntryNumerical(data):
  result = False
  data = int(data)
  if (
    ((data >= 1230000000) and (data <= 1236999999))
    or
    ((data >= 1239000000) and (data <= 1239099999))
  ):
    result = True

  return result

def getNumericalRange(data):
  result = None
  data = int(data)
  if (
    ((data >= 1230000000) and (data <= 1236999999))
  ):
    result = 'default'

  if (
    ((data >= 1239000000) and (data <= 1239099999))
  ):
    result = 'strict'

  return result

def validateEntryLunh10(data):
  result = False
  luhnableNumber = re.sub(r"^123(\d{6})(\d{1})$", "\\1", str(data), flags=re.IGNORECASE)
  luhnableNumberCheck = re.sub(r"^(\d{9})(\d{1})$", "\\2", str(data), flags=re.IGNORECASE)
  #print(f"\t{data} -> {luhnableNumber} as {luhnableNumberCheck}")

  val = luhn10CalculateCheckDigit(luhnableNumber)
  if int(val) == int(luhnableNumberCheck):
    result = True

  return result


def main():
  print(f"Reading source YAML: {YAML_SOURCE_FILE} ..")
  source_dict = readYAML(YAML_SOURCE_FILE)

  source_dict_count = len(source_dict['entries'])
  print(f"\tRead {source_dict_count} raw entries")

  # Set up destination dictionary
  dest_dict = {}
  dest_dict['entries'] = []

  category_block = [
    'overifierad',
    'suspended',
    'terminated',
    'verified',
    'verifierad',
    'retired',
  ]
  
  if source_dict == None:
    print(f"Could not read {YAML_SOURCE_FILE}")
    exit(1)

  print(f"\tIterating {len(source_dict['entries'])} items ..")

  line_count = 0
  for entryVO in source_dict['entries']:

    # Entry number
    entryNumber = entryVO['entry']

    # Collect categories
    cats = entryVO['categories']

    # Check format - simple
    if validateEntry(entryVO['entry']) == False:
      print(f"\t{entryVO['entry']} failed simple format check -- skipped")
      continue

    # Validate ranges - complex
    if validateEntryStrict(entryVO['entry']) == False:
      print(f"\t{entryVO['entry']} failed complex format check -- skipped")
      continue

    if validateEntryNumerical(entryVO['entry']) == False:
      print(f"\t{entryVO['entry']} failed numrical format check -- skipped")
      continue

    # Validate Luhn-10
    if validateEntryLunh10(entryNumber) == False:
      print(f"\t{entryNumber} failed Luhn-10 format check -- skipped")
      continue

    # Filter categories
    skip_cats = False
    if cats != None:
      for cat_block in category_block:
        if cat_block in cats:
          skip_cats = True
          break
    else:
      skip_cats = True
      continue

    if(
      entryVO['orgNumber'] != None
    and
      entryVO['orgName'] != None
    and
      entryVO['categories'] != None
    and
      skip_cats == False
    ):
      dest_dict['entries'].append(entryVO)
      line_count += 1


  writeYAML(YAML_DEST_DATASOURCE, dest_dict)
  print(f"\tWrote {line_count} YAML entries")

  print(f"Done writing {YAML_DEST_DATASOURCE}")

if __name__ == '__main__':
  main()
