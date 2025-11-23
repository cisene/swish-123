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

  # Only test if prefixed correctly
  if result == True:
    # Test if
    # 123[000 .. 699] and 123[900 .. 999]
    if re.search(r"^123([0-69]{1})([0-9]{6})$", str(data), flags=re.IGNORECASE):
      # Only 123[900 .. 909] are valid
      if re.search(r"^1239", str(data), flags=re.IGNORECASE):
        if re.search(r"^12390", str(data), flags=re.IGNORECASE):
          result = True
        else:
          result = False
          #print(f"'{data}' was malformed")
    else:
      result = False
      #print(f"'{data}' was malformed")

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
    'malformed-entry': [],
    
    'malformed-orgName-empty': [],
    'malformed-orgName-uppercase': [],
    'malformed-orgName-lowercase': [],
    'malformed-orgName-toolong': [],
    
    'malformed-orgNumber-empty': [],
    'malformed-orgNumber-type': [],
    'malformed-orgNumber-missing': [],
    'malformed-orgNumber-unmasked': [],

    'malformed-categories-empty': [],
    'malformed-categories-tolong': [],

    'malformed-web-empty': [],
    'malformed-web-http': [],
    'malformed-web-missing': [],
  }

  if entries != None:
    if "entries" in entries:
      for entryVO in entries['entries']:

        malformed_vo = False
        malformed_vo_filtered = False
        malformed_entry = False
        malformed_orgName = False
        malformed_orgName_empty = False
        malformed_orgName_toolong = False
        malformed_orgName_lowercase = False
        malformed_orgName_uppercase = False
        malformed_orgNumber = False
        malformed_orgNumber_empty = False
        malformed_orgNumber_toolong = False
        malformed_orgNumber_type = False
        malformed_orgNumber_unmasked = False
        malformed_categories = False
        malformed_categories_empty = False
        malformed_categories_toolong = False
        malformed_web = False

        # Detect malformed ValueObjects, missing properties
        for VOproperty in ['entry', 'orgName', 'orgNumber', 'comment', 'categories', 'web']:
          if not VOproperty in entryVO:
            malformed_vo = True

        # skip out early - invalid entry
        if testIsValidEntry(entryVO['entry']) == False:
          malformed_entry = True

        # Skip out early - invalid entry
        if testIsEntryNumber(entryVO['entry']) == False:
          malformed_vo = True

        if (
          malformed_vo == False
          and
          malformed_entry == False
        ):

          # Detect malformed or missing orgNames
          if entryVO['orgName'] != None:

            # orgName minimal length
            if len(entryVO['orgName']) < 1:
              malformed_orgName_empty = True
            
            # orgName maximal length
            if len(entryVO['orgName']) > 100:
              malformed_orgName_toolong = True

            # orgName - All uppercase test
            if entryVO['orgName'] == entryVO['orgName'].upper():
              malformed_orgName_uppercase = True

            # orgName - All lowercase test
            if entryVO['orgName'] == entryVO['orgName'].lower():
              malformed_orgName_lowercase = True

          else:
            malformed_orgName_empty = True

          # Detect malformed or missing orgNumbers
          if entryVO['orgNumber'] != None:
            if len(entryVO['orgNumber']) < 1:
              malformed_orgNumber_empty = True

            if len(entryVO['orgNumber']) > 11:
              malformed_orgNumber_toolong = True

            if (
              malformed_orgNumber_empty == False
              and
              malformed_orgNumber_toolong == False
            ):
              tested = testIsValidOrgNumber(entryVO['orgNumber'])
              if tested['type'] == None:
                malformed_orgNumber_type = True

              if (
                tested['type'] == 'person'
                and
                not re.search(r"^\d{6}\x2dXXXX$", str(entryVO['orgNumber']), flags=re.IGNORECASE)
              ):
                malformed_orgNumber_unmasked = True

          else:
            malformed_orgNumber_empty == True

          # Detect malformed or missing categories
          if entryVO['categories'] != None:
            if len(entryVO['categories']) < 1:
              malformed_categories_empty = True

            if len(entryVO['categories']) > 25:
              malformed_categories_toolong = True

          else:
            malformed_categories_empty = True


          # Detect categorization the disqualifies
          if malformed_categories == False:
            if "categories" in entryVO:
              if entryVO['categories'] != None:
                for category in entryVO['categories']:
                  if category in ['overifierad', 'retired', 'suspended', 'terminated', 'unverified']:
                    malformed_vo_filtered = True
                    break
              else:
                malformed_categories_empty = True

          # Detect malformed or missing web
          if entryVO['web'] != None:
            if len(entryVO['web']) < 1:
              malformed_web = True
              malformed_web_missing = True

            if not re.search(r"^http(s)?\x3a\x2f\x2f", str(entryVO['web']), flags=re.IGNORECASE):
              malformed_web = True

            else:
              if re.search(r"^http\x3a\x2f\x2f", str(entryVO['web']), flags=re.IGNORECASE):
                malformed_web_http = True

          else:
            malformed_web = True



          #if len(entryVO['orgName']) >











          # Detect malformed or missing URLs
          malformed_web_http = False
          malformed_web_missing = False
          if (
            entryVO['orgName'] != None
          and
            entryVO['orgNumber'] != None
          and
            entryVO['web'] == None
          ):
            malformed_web_missing = True


          # Detect malformed or http URLs
          malformed_web_http = False
          if entryVO['web'] != None:
            if re.search(r"^http\x3a\x2f", entryVO['web'], flags=re.IGNORECASE):
              malformed_web_http = True






        if malformed_vo_filtered == True:
          continue

        if malformed_vo == True:
          result['malformed-vo'].append(entryVO)

        if malformed_entry == True:
          result['malformed-entry'].append(entryVO)

        if malformed_orgName == True:
          result['malformed-orgName-empty'].append(entryVO)

        if malformed_orgName_lowercase == True:
          result['malformed-orgName-lowercase'].append(entryVO)

        if malformed_orgName_uppercase == True:
          result['malformed-orgName-uppercase'].append(entryVO)

        if malformed_orgName_toolong == True:
          result['malformed-orgName-toolong'].append(entryVO)


        if malformed_orgNumber_empty == True:
          result['malformed-orgNumber-empty'].append(entryVO)

        if malformed_orgNumber_toolong == True:
          result['malformed-orgNumber-toolong'].append(entryVO)

        if malformed_orgNumber_type == True:
          result['malformed-orgNumber-type'].append(entryVO)

        if malformed_orgNumber_unmasked == True:
          result['malformed-orgNumber-unmasked'].append(entryVO)


        if malformed_categories_empty == True:
          result['malformed-categories-empty'].append(entryVO)

        if malformed_web_missing == True:
          result['malformed-web-missing'].append(entryVO)

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

  if result != None:
    renderYAMLfromResult(result)

  #print(result)


if __name__ == '__main__':
  main()
