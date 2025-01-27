#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
#import random

import yaml
#import json

import urllib3
urllib3.disable_warnings()
from urllib3.exceptions import InsecureRequestWarning

import requests
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)
#from collections import defaultdict

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


#from datetime import datetime

YAML_SOURCE_FILE = '../yaml/knockout-malformed-web-http.yaml'
YAML_DEST_FILE = '../yaml/knockout-malformed-web-http-updated.yaml'

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

def replaceHTTPwithHTTPS(data):
  if re.search(r"^http\x3a\x2f\x2f", str(data), flags=re.IGNORECASE):
    data = re.sub(r"^http\x3a\x2f\x2f", "https://", str(data), flags=re.IGNORECASE)

  return data


def httpGET(url):
  pass


def httpHEAD(url):
  session = requests.Session()
  response = { 'status' : None, 'message': None, 'url' : url }

  try:
    r = session.head(
      url,
      verify=True,
      timeout=(5, 5),
      allow_redirects=True
    )

    response['status']  = r.status_code
    response['url']     = r.url

    if r.status_code == 200:
      response['message'] = 'OK'

    if r.status_code in [401, 402, 403, 404, 410]:
      response['message'] = 'OK'


  except requests.exceptions.ConnectTimeout:
    response['status'] = 0
    response['message'] = 'requests.exceptions.ConnectTimeout'
    pass

  except requests.exceptions.ConnectionError:
    response['status'] = 0
    response['message'] = 'requests.exceptions.ConnectionError'
    pass

  except requests.exceptions.ReadTimeout:
    response['status'] = 0
    response['message'] = 'requests.exceptions.ReadTimeout'
    pass

  except requests.exceptions.SSLError:
    response['status'] = 0
    response['message'] = 'requests.exceptions.SSLError'
    pass

  except urllib3.exceptions.SSLError:
    response['status'] = 0
    response['message'] = 'urllib3.exceptions.SSLError'
    pass

  except ssl.SSLCertVerificationError:
    response['status'] = 0
    response['message'] = 'ssl.SSLCertVerificationError'
    pass

  finally:
    #response['message'] = 'OK'
    #response['status'] = r.status_code
    pass


  return response

def main():
  print(f"Reading source YAML: {YAML_SOURCE_FILE} ..")
  source_dict = readYAML(YAML_SOURCE_FILE)
  dest_dict = {}
  dest_dict['entries'] = []

  source_dict_length = len(source_dict['entries'])
  print(f"{source_dict_length} entries read from file ..")

  line_count = 1

  for entryVO in source_dict['entries']:
    web_url = entryVO['web']
    web_url_upgraded = replaceHTTPwithHTTPS(web_url)

    print(f"{line_count:> 4} '{web_url_upgraded}'")

    response = httpHEAD(web_url_upgraded)

    #if response['status'] == 200:
    if response['status'] in [200, 401, 402, 403, 404, 410]:
      # Write back upgraded URL here - Done

      if web_url_upgraded != response['url']:
        
        if not re.search(r"\x2fstart\x2f\x3fID\x3d(\d{1,})$", str(response['url']), flags=re.IGNORECASE):
          entryVO['web'] = response['url']
        else:
          response['url'] = re.sub(r"\x2fstart\x2f\x3fID\x3d(\d{1,})$", "", str(response['url']), flags=re.IGNORECASE)

        entryVO['web'] = response['url']

      else:
        entryVO['web'] = web_url_upgraded

      dest_dict['entries'].append(entryVO)

    else:
      print(f"\t{response['status']} - {response['message']}")

    line_count += 1

  writeYAML(YAML_SOURCE_FILE, dest_dict)

if __name__ == '__main__':
  main()
