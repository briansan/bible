"""
  @file   bible/util.py
  @author Brian Kim
  @brief  definition convenience methods for this app
"""

import json
from flask import Response, abort

def clean_lang_abbr(lang):
  return lang.lower()

def clean_version_abbr(abbr):
  return abbr.upper()

def clean_version_name(name):
  return str.join(' ',[x.capitalize() for x in name.split(' ')])

def clean_book_abbr(abbr):
  if abbr[0].isdigit():
    abbr = abbr[0] + abbr[1:].strip(' ').capitalize()
  else:
    abbr = abbr.capitalize() 
  return abbr

def parse_verse_path(v,b,ch_a,verse_a,ch_b=None,verse_b=None):
  v = v.upper()
  b = clean_book_abbr(b)
  y = {'v':v,'b':b,'ch_a':ch_a,'verse_a':verse_a}
  if ch_b: 
    y['ch_b'] = ch_b
    y['verse_b'] = verse_b
  return y

def jsonify(data):
  if data:
    return Response(json.dumps(data),mimetype='application/json') 
  else:
    raise NotFoundException()
 

"""
  @file   exceptions.py
  @author Brian Kim
  @brief  a script defining exceptions that correspond to http response codes
"""

class AlreadyExistsException(Exception):
  def __init__(self):
    self.code = 409

class NotFoundException(Exception):
  def __init__(self):
    self.code = 404

class BadDataException(Exception):
  def __init__(self):
    self.code = 406
