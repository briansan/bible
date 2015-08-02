# -*- coding: utf-8 -*-
"""
  @file   bible/api.py
  @author Brian Kim
  @brief  the definition of routes for the api 
"""

from flask import Blueprint, request, abort
import controller, methods, model
from util import *
import traceback as tb

api = Blueprint('api',__name__)

parse_dispatch = {
  'lang' : controller.parse_lang,
  'version' : controller.parse_version,
  'book' : controller.parse_book,
  'verse' : controller.parse_verse
}

post_dispatch = {
  'lang' : controller.add_lang,
  'version' : controller.add_version,
  'book' : controller.add_book,
  'verse' : controller.add_verse
}

@api.route('/', methods=['GET','POST'])
def api_root():
  if request.method == 'GET':
    return jsonify({'title':'Bible API','author':'BreadTech'})
  elif request.method == 'POST':
    # add a verse to the api
    what = request.form.get('what')
    x = parse_dispatch[what]()
    y = post_dispatch[what](**x)
    return jsonify(y)

dispatch = {
  'lang': {'GET':controller.get_lang_all,'POST':controller.add_lang},
  'version': {'GET':controller.get_version_all,'POST':controller.add_version},
  'book': {'GET':controller.get_book_all,'POST':controller.add_book},
}

dispatch_id = {
  'lang': {'GET':controller.get_lang,'PUT':controller.set_lang,'DELETE':controller.rm_lang},
  'version': {'GET':controller.get_version,'PUT':controller.set_version,'DELETE':controller.rm_version},
  'book': {'GET':controller.get_book,'PUT':controller.set_book,'DELETE':controller.rm_book},
}

@api.route('/<category>', methods=['GET','POST'])
def api_category(category):
  method = dispatch.get(category)
  if not method: abort(405)
  try:
    return method.get(request.method)()
  except (AlreadyExistsException, BadDataException, NotFoundException) as e:
    abort(e.code)
  except Exception:
    print(tb.format_exc())
    abort(500)

clean_dispatch = {
  'lang' : clean_lang_abbr,
  'version' : clean_version_abbr,
  'book' : clean_book_abbr
}

@api.route('/<category>/<name>', methods=['GET','PUT','DELETE','POST'])
def api_category_name(category,name):
  # look up on the dispatch
  method = dispatch_id.get(category)
  clean_method = clean_dispatch.get(category)
  if not method: 
    abort (405)
  try:
    abbr = clean_method(name)
    return method.get(request.method)(abbr)
  except (BadDataException, NotFoundException) as e:
    abort(e.code)
  except Exception:
    print(tb.format_exc())
    abort(500)

@api.route('/<version>/<book>/<int:chnum>', methods=['GET','POST'])
def get_chapter(version,book,chnum):
  try:
    v = version.upper()
    b = clean_book_abbr(book)
    if request.method == 'GET':
      x = controller.get_chapter(v,b,chnum)
      return x
    elif request.method == 'POST':
      x = controller.add_verse(v,b,chnum)
      return x
  except (NotFoundException,BadDataException,AlreadyExistsException) as e:
    print(tb.format_exc())
    abort(e.code)
  except Exception:
    print(tb.format_exc())
    abort(500)

@api.route('/<version>/<book>/<int:chnum>/<int:verse>', methods=['GET','POST','PUT','DELETE'])
def handle_verse(version,book,chnum,verse):
  try:
    data = parse_verse_path(version,book,chnum,verse)
    if request.method == 'GET':
      return controller.get_verse(**data)
    elif request.method == 'POST':
      request.form = {'number':data['verse_a'],'text':request.form['text']}
      return controller.add_verse(**data)
    elif request.method == 'PUT':
      return controller.set_verse(**data)
    elif request.method == 'DELETE':
      return controller.rm_verse(**data)
  except (NotFoundException,BadDataException,AlreadyExistsException) as e:
    abort(e.code)
  except Exception:
    print(tb.format_exc())
    abort(500)

@api.route('/<version>/<book>/<ch_a>/<verse_a>/<verse_b>', methods=['GET'])
def handle_verse_range(version,book,ch_a,verse_a,verse_b):
  return handle_verse_range_ch(version,book,ch_a,verse_a,ch_a,verse_b)

@api.route('/<version>/<book>/<ch_a>/<verse_a>/<ch_b>/<verse_b>', methods=['GET'])
def handle_verse_range_ch(version,book,ch_a,verse_a,ch_b,verse_b):
  try: 
    data = parse_verse_path(version,book,ch_a,verse_a,ch_b,verse_b)
    return controller.get_verse_range(**data)
  except NotFoundException as e:
    abort(e.code)
  except Exception:
    abort(500)
