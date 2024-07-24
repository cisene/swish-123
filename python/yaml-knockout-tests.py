#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import random

import yaml
import collections

#import xml.etree.ElementTree as ET

#from xml.etree.ElementTree import Element, SubElement, Comment, tostring
#from xml.dom import minidom

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


def readYAML(filepath):
  result = None
  contents = None
  if os.path.isfile(filepath):
    fp = None
    try:
      fp = open(filepath)
      contents = fp.read()
      fp.close()

    finally:
      pass
  else:
    print(f"{filepath} was not found.")

  if contents != None:
    result = yaml.safe_load(contents)

  return result



def testIsValidOrgName(data):
  result = False

  return result

def testPersonUnmasked(data):
  result = False
  if not re.search(r"^(\d{6})\x2dXXXX", str(data), flags=re.IGNORECASE):
    result = True

  return result

def testFragDay(data):
  result = None
  value = int(data)

  if value >= 1 and value <= 31:
    result = 'person'

  if value >= 61 and value <= 91:
    result = 'temporary'

  return result

def testFragMonth(data):
  result = None
  value = int(data)
  #print(value)
  if value >= 1 and value <= 12:
    result = 'person'

  if value >= 20 and value <= 99:
    result = 'organisation'

  return result

def getFractionsOrgNumber(data):
  result = None

  data = re.sub(r"^(\d{2})(\d{2})(\d{2})\x2d(.*)$", "\\1|\\2|\\3", str(data), flags=re.IGNORECASE)
  result = re.split(r"\x7c", data)

  if len(result) == 3:
    return result
  else:
    return None

def testIsValidOrgNumber(data):
  result = {
    'type': None,
    'subtype': None,
  }

  test_org_type = None

  if re.search(r"^(\d{6})\x2d(\d{4})$", str(data), flags=re.IGNORECASE):
    frags = getFractionsOrgNumber(data)
    if frags != None:
      test_org_type = testFragMonth(frags[1])
      if test_org_type != None:

        if test_org_type == 'organisation':
          result['type'] = 'organisation'
          result['subtype'] = 'organisation'

        if test_org_type == 'person':
          test_person_type = testFragDay(frags[2])
          if test_person_type == 'person':
            result['type'] = 'person'
            result['subtype'] = 'person'
          else:
            result['type'] = 'person'
            result['subtype'] = 'temporary'



  elif re.search(r"^(\d{6})\x2d(X{4})$", str(data), flags=re.IGNORECASE):
    frags = getFractionsOrgNumber(data)
    if frags != None:
      test_org_type = testFragMonth(frags[1])
      if test_org_type != None:
        if test_org_type == 'person':
          test_org_subtype = testFragDay(frags[2])
          result['type'] = 'person'
          result['subtype'] = test_org_subtype

  else:
    pass

  return result

def testIsEntryControlled(data):
  result = False
  if re.search(r"^1239(\d{6})$", str(data), flags=re.IGNORECASE):
    result = True
  return result

def testIsValidEntry(data):
  result = False
  if re.search(r"^123(\d{7})$", str(data), flags=re.IGNORECASE):
    result = True
  return result

def testIsEntryNumber(data):
  return re.match(r"^123(\d{7})$", str(data), flags=re.IGNORECASE)

def renderYAMLfromResult(result):
  for chunk  in result:
    if len(result[chunk]) > 0:
      filepath = f"../yaml/knockout-{chunk}.yaml"
      #print(result[chunk])
      print(f"Writing knockout to {filepath} .. {len(result[chunk])} entries")
      contents = { 'entries': [] }
      contents['entries'] = result[chunk]
      writeYAML(filepath, contents)

def validateEntry(data):
  return re.match(r"^123(\d{7})$", str(data), flags=re.IGNORECASE)


def testEntries(entries):

  result = {
    'malformed-vo': [],
    'malformed-orgName': [],
    'malformed-orgName-uppercase': [],
    'malformed-orgName-lowercase': [],
    'malformed-orgNumber': [],
    'malformed-orgNumberUnmasked': [],

    'malformed-categories-empty': [],

    'malformed-web-http': [],
    'malformed-web-missing': [],
  }

  if entries != None:
    if "entries" in entries:
      for entryVO in entries['entries']:

        # Skip out early - invalid entry
        if testIsEntryNumber(entryVO['entry']) == False:
          result['malformed-vo'].append(entryVO)
          continue

        # Detect categorization the disqualifies 
        skip_tests = False
        if "categories" in entryVO:
          if entryVO['categories'] != None:
            for category in entryVO['categories']:
              if category in ['overifierad', 'retired', 'suspended', 'terminated', 'unverified']:
                skip_tests = True
                # continue
                break
          else:
            result['malformed-categories-empty'].append(entryVO)

        if skip_tests == True:
          continue


        # Detect malformed ValueObjects, missing properties
        malformed_vo = False
        for VOproperty in ['entry', 'orgName', 'orgNumber', 'comment', 'categories', 'web']:
          if not VOproperty in entryVO:
            malformed_vo = True

        # Save them to a list
        if malformed_vo == True:
          result['malformed-vo'].append(entryVO)



        # Detect malformed or missing orgNames
        malformed_orgName = False
        if entryVO['orgName'] == None:
          malformed_orgName = True

        if malformed_orgName == True:
          result['malformed-orgName'].append(entryVO)

        # orgName - All uppercase test
        if entryVO['orgName'] != None:
          if entryVO['orgName'] == entryVO['orgName'].upper():
            result['malformed-orgName-uppercase'].append(entryVO)

        # orgName - All lowercase test
        if entryVO['orgName'] != None:
          if entryVO['orgName'] == entryVO['orgName'].lower():
            result['malformed-orgName-lowercase'].append(entryVO)


        # Detect malformed or missing orgNumbers
        malformed_orgNumber = False

        if entryVO['orgNumber'] != None:
          tested = testIsValidOrgNumber(entryVO['orgNumber'])
          if tested['type'] == None:
            malformed_orgNumber = True

          if tested['type'] not in ['organisation', 'person']:
            malformed_orgNumber = True


        if malformed_orgNumber == True:
          result['malformed-orgNumber'].append(entryVO)

        # Detect malformed or unmasked orgNumbers



        # Detect malformed or missing URLs
        malformed_web_missing = False
        if entryVO['web'] == None:
          malformed_web_missing = True

        if malformed_web_missing == True:
          result['malformed-web-missing'].append(entryVO)

        # Detect malformed or http URLs
        malformed_web_http = False
        if entryVO['web'] != None:
          if re.search(r"^http\x3a\x2f", entryVO['web'], flags=re.IGNORECASE):
            malformed_web_http = True

        if malformed_web_http == True:
          result['malformed-web-http'].append(entryVO)


  return result



def main():

  SOURCE_DIR = '../yaml/'
  for f in os.listdir(SOURCE_DIR):
    if re.search(r"knockout\x2d", f):
      os.remove(os.path.join(SOURCE_DIR, f))
      print(f"\tremoved {f} ..")

  SOURCE_DATAFILE = '../yaml/entries.yaml'

  entries = readYAML(SOURCE_DATAFILE)
  if entries != None:
    if "entries" in entries:
      print(f"{len(entries['entries'])} were successfully read from file {SOURCE_DATAFILE} ..")

    else:
      print(f"Something wrong, expexted more than None")
      exit(1)

  result = testEntries(entries)

  renderYAMLfromResult(result)

  #print(result)


if __name__ == '__main__':
  main()
