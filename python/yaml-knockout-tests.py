#!/usr/bin/python
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
  #print(value)
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


# def parseEntries():
#   global yamlsource
#   entries_dict = {}

#   for entryVO in yamlsource['entries']:
#     entry = entryVO['entry']

#     if entry not in entries_dict.keys():
#       entries_dict[entry] = entryVO


#   for entry in sorted(entries_dict.keys()):
#     entryVO = entries_dict[entry]
#     tests = {
#       'entry': {
#         'validation': False,
#         'controlled': False,
#       },
#       'orgNumber': {
#         'formatting': False,
#         'checkDigit': False,
#         'orgType': 'Unknown',
#       },
#       'orgName': None,
#       'categories': None,
#       'web': None
#     }

#     print(entry)

#     test_entry = testIsValidEntry(entry)

#     if test_entry != None:
#       tests['entry']['validation'] = test_entry

#       test_entry_controlled = testIsEntryControlled(entry)
#       if test_entry_controlled != None:
#         tests['entry']['controlled'] = test_entry_controlled


#     if entryVO['orgNumber'] != None:
#       test_orgNumber = testIsValidOrgNumber(entryVO['orgNumber'])
#       if test_orgNumber != None:
#         tests['orgNumber']['formatting'] = True

#     else:
#       test_orgNumber = False


#     if entryVO['orgName'] != None:
#       test_orgName = testIsValidOrgName(entryVO['orgName'])
#     else:
#       test_orgName = False


#     # Skip on empty entries
#     if entryVO['orgName'] == None and entryVO['orgNumber'] == None:
#       continue

#     # Unverified entries are skipped
#     if entryVO['categories'] != None:
#       if "overifierad" in entryVO['categories']:
#         continue

#       if "terminated" in entryVO['categories']:
#         continue

#     if "orgNumber" not in entryVO:
#       entryVO['orgNumber'] = None

#     if "comment" not in entryVO:
#       entryVO['comment'] = None


#     #print(f"tested '{entry}' validation: '{test_entry}' controlled: '{test_entry_controlled}'")

#     print(str(tests))

def renderYAMLfromResult(result):
  for chunk  in result:
    if len(result[chunk]) > 0:
      filepath = f"../yaml/knockout-{chunk}.yaml"
      #print(result[chunk])
      print(f"Writing knockout to {filepath} .. {len(result[chunk])} entries")
      contents = { 'entries': [] }
      contents['entries'] = result[chunk]
      writeYAML(filepath, contents)



def testEntries(entries):

  result = {
    'malformed-vo': [],
    'malformed-orgName': [],
    'malformed-orgNumber': [],
    'malformed-orgNumberUnmasked': [],

    'malformed-web-http': [],
    'malformed-web-missing': [],
  }

  if entries != None:
    if "entries" in entries:
      for entryVO in entries['entries']:

        # Detect categorization the disqualifies 
        skip_tests = False
        if "categories" in entryVO:
          if entryVO['categories'] != None:
            for category in entryVO['categories']:
              if category in ['overifierad', 'retired', 'suspended', 'terminated', 'unverified']:
                #print(f"{entryVO['entry']} had {category} .. skipped")
                skip_tests = True
                continue

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



        # Detect malformed or missing orgNumbers
        malformed_orgNumber = False
        if entryVO['orgNumber'] == None:
          malformed_orgNumber = True

        else:
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
