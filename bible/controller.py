"""
  @file   bible/controller.py
  @author Brian Kim
  @brief  a script that acts as a middleware between the http requests and the actual methods
"""

from flask import request
import methods
from util import *

#
# language
def parse_lang():
  abbr = request.form.get('abbr')
  abbr = abbr.lower() if abbr else None
  name = request.form.get('name')
  name = str.join(' ',[ x.capitalize() for x in name.split(' ') ]) if name else None
  return {'abbr':abbr,'name':name}

def get_lang(name):
  return jsonify( methods.get_lang_uni(name) )

def get_lang_all():
  return jsonify( methods.get_lang_multi() )

def add_lang():
  data = parse_lang()
  if None in data:
    raise BadDataException()
  return jsonify( methods.add_lang(**data) )

def set_lang(name):
  data = parse_lang()
  data['newabbr'] = data['abbr']
  data['abbr'] = name
  return jsonify( methods.set_lang( **data ))

def rm_lang(name):
  return jsonify( methods.rm_lang(name) )

#
# version
def parse_version():
  y = parse_lang()
  y['abbr'] = y['abbr'].upper() if y['abbr'] else None
  lang = request.form.get('lang')
  y['lang'] = lang.lower() if lang else 'en' 
  return y

def get_version(name):
  return jsonify( methods.get_version_uni(name) )

def get_version_all():
  return jsonify( methods.get_version_multi() )

def add_version():
  data = parse_version()
  return jsonify( methods.add_version(**data) )

def set_version(name):
  data = parse_version()
  data['newabbr'] = data['abbr']
  data['abbr'] = name
  return jsonify( methods.set_version( **data ))

def rm_version(name):
  return jsonify( methods.rm_version(name) )

#
# book
def parse_book():
  y = parse_version()
  y['abbr'] = clean_book_abbr(y['abbr'])
  y['numch'] = request.form['numch']
  return y

def get_book(name):
  return jsonify( methods.get_book_uni(name) )

def get_book_all():
  return jsonify( methods.get_book_multi() )

def add_book():
  data = parse_book()
  return jsonify( methods.add_book(**data) )

def set_book(name):
  data = parse_book()
  data['newabbr'] = data['abbr']
  data['abbr'] = name
  return jsonify( methods.set_book( **data ))

def rm_book(name):
  return jsonify( methods.rm_book(name) )

#
# chapter
def get_chapter(version,book,ch_num):
  x = methods.get_chapter(version,book,ch_num) 
  return jsonify( x )

#
# verse
def parse_verse():
  verse_num = request.form.get('number')
  text = request.form.get('text')
  return (verse_num,text)

def get_chapter_obj(v,b,c):
  return methods.get_chapter(v,b,c,False)

def get_verse_obj(v,b,c,n,want_dict=False):
  ch = get_chapter_obj(v,b,c)
  return methods.get_verse(ch,n,want_dict)

def get_verse(v,b,ch_a,verse_a):
  return jsonify( get_verse_obj(v,b,ch_a,verse_a,True) )

def get_verse_range(v,b,ch_a,verse_a,ch_b,verse_b):
  if ch_a < ch_b: raise BadDataException()
  ch_a = get_chapter_obj(v,b,ch_a)
  ch_b = get_chapter_obj(v,b,ch_b)
  return jsonify( methods.get_verse_range_ch(ch_a,verse_a,ch_b,verse_b)  )

def add_verse(v,b,ch_a,verse_a=None):
  # get form fields
  data = parse_verse()
  # make sure the verse number field has been filled
  if data[0] is None: 
    # fall back to the verse_a arg
    if verse_a:
      data = (verse_a,data[1])
    # if that's none, then 406
    else:
      raise BadDataException()
  # add the verse according
  ch = get_chapter_obj(v,b,ch_a)
  return jsonify( methods.add_verse(ch,*data) )

def set_verse(v,b,ch_a,verse_a):
  data = parse_verse()
  v = get_verse_obj(v,b,ch_a,verse_a)
  return jsonify( methods.set_verse(v,data[1]) )

def rm_verse(v,b,ch_a,verse_a):
  v = get_verse_obj(v,b,ch_a,verse_a)
  return jsonify( methods.rm_verse(v) )
  
