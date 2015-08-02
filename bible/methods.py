"""
  @file   bible/methods.py
  @author Brian Kim
  @brief  definition of app methods to add get set and remove the bible objects 
"""

from model import *
from util import *
import traceback as tb

#
# utility
def save():
  db.session.commit()

def add(obj):
  try:
    db.session.add(obj)
    save()
  except:
    raise AlreadyExistsException()

def rm(obj):
  db.session.delete(obj)
  save()

def obj2dict(x):
  return [dict(y) for y in x]
  
#
# language
def add_lang(abbr,name):
  lang = Language(abbr,name)
  add(lang)
  return dict(lang)

def get_lang_multi(want_dict=True):
  x = Language.query.filter_by().all()
  return obj2dict(x) if want_dict else x

def get_lang_uni(abbr,want_dict=True):
  try:
    x = Language.query.filter_by(abbr=abbr).first()
    return dict(x) if x and want_dict else x
  except:
    raise NotFoundException()

def get_lang_versions(abbr):
  x = get_lang_uni(abbr,False)
  return obj2dict(x.versions.all()) if x else x

def set_lang(abbr,name=None,newabbr=None):
  lang = get_lang_uni(abbr,False)
  lang.abbr = newabbr if newabbr else abbr
  lang.name = name if name else lang.name
  save()
  return dict(lang)

def rm_lang(abbr):
  lang = get_lang_uni(abbr,False)
  rm(lang)
  return dict(lang) 

#
# version
def add_version(lang,abbr,name):
  # add the version
  lang = get_lang_uni(lang,False)
  version = Version(lang,abbr,name)
  add(version)

  # add all the chapters for each book in that version
  books = lang.books.all()
  for book in books:
    add_chapters(version,book)
  return dict(version)

def get_version_multi(want_dict=True):
  x = Version.query.filter_by().all()
  return obj2dict(x) if want_dict else x

def get_version_uni(abbr,want_dict=True):
  try:
    x = Version.query.filter_by(abbr=abbr).first()
    return dict(x) if x and want_dict else x
  except:
    raise NotFoundException()

def set_version(abbr,name=None,lang=None,newabbr=None):
  version = get_version_uni(abbr,False)
  version.abbr = newabbr if newabbr else abbr
  version.name = name if name else version.name
  version.lang = get_lang_uni(lang,False) if lang else version.lang
  save()
  return dict(version)

def rm_version(abbr):
  version = get_version_uni(abbr,False)
  rm(version)
  return dict(version)

#
# book
def add_book(lang,abbr,name,numch):
  # add the book
  lang = get_lang_uni(lang,False)
  book = Book(lang,abbr,name,numch)
  add(book)

  # add chapters to book of each version
  versions = lang.versions.all()
  for version in versions:
    add_chapters(version,book)
  return dict(book)

def get_book_multi(want_dict=True):
  x = Book.query.filter_by().all()
  return obj2dict(x) if want_dict else x

def get_book_uni(abbr,want_dict=True):
  try:
    x = Book.query.filter_by(abbr=abbr).first()
    return dict(x) if x and want_dict else x
  except:
    raise NotFoundException()

def set_book(abbr,name=None,lang=None,newabbr=None,numch=None):
  book = get_book_uni(abbr,False)
  book.abbr = newabbr if newabbr else abbr
  book.name = name if name else book.name
  book.lang = get_lang_uni(lang,False) if lang else book.lang
  book.numch = int(numch) if numch else book.numch
  save()
  return dict(book)

def rm_book(abbr):
  book = get_book_uni(abbr,False)
  rm(book)
  return dict(book)

#
# chapter
def add_chapters(version,book):
  # keep on adding chapters until the count hits 0
  for i in range(book.numch):
    ch = Chapter(version,book,i+1)
    add(ch)
  return dict(ch)

def get_chapter_count(v,b):
  v = Chapter.version.has(abbr=v)
  b = Chapter.book.has(abbr=b)
  return Chapter.query.filter(v,b).count()

def get_chapter(v,b,num,want_dict=True):
  try:
    v = Chapter.version.has(abbr=v)
    b = Chapter.book.has(abbr=b)
    n = Chapter.number.is_(num)
    x = Chapter.query.filter(v,b,n).first()
    return dict(x) if x and want_dict else x
  except:
    raise NotFoundException()

def rm_chapter(v,b,n):
  ch = get_chapter(v,b,n,False)
  rm(ch)
  return dict(ch)

#
# verse
def add_verse(chapter,number,text):
  v = Verse(chapter,number,text)
  add(v)
  return dict(v)

def get_verse(ch,n,want_dict=True):
  try:
    ch_q = Verse.chapter.has(id=ch.id)
    n_q = Verse.number.is_(n)
    x = Verse.query.filter(ch_q,n_q).first()
    return dict(x) if x and want_dict else x
  except:
    raise NotFoundException()

def get_verse_all(ch,want_dict=True):
  try:
    ch_q = Verse.chapter.has(id=ch.id)
    x = Verse.query.filter(ch_q).all()
    return obj2dict(x) if want_dict else x
  except:
    raise NotFoundException()

def get_verse_count(ch):
  return Verse.query.filter(Verse.chapter.has(id=ch.id)).count()

def get_verse_range(ch_a,v_a,v_b,want_dict=True):
  try:
    ch_q = Verse.chapter.has(id=ch_a.id)
    v1_q = Verse.number >= v_a
    v2_q = Verse.number <= v_b
    x = Verse.query.filter(ch_q,v1_q,v2_q).all()
    return obj2dict(x) if want_dict else x
  except:
    raise NotFoundException()
  
def get_verse_range_ch(ch_a,v_a,ch_b,v_b,want_dict=True):
  try:
    y = []
    # first, verse starting point; 
    # ch, chapter index
    # n, number of chapters 
    first = v_a
    ch = ch_a
    n = ch_b.number - ch_a.number
    for i in range(n):
      # set up the queries
      last = get_verse_count(ch)
      x = get_verse_range(ch,first,last,want_dict)
      # find the verse and add to return list
      y += x
      # move the ch pointer to the next one and first back to 1
      first = 1
      ch = get_verse_range(ch_a.version,ch_a.book,ch_a.id+i)
    # do one more time for last chapter
    x = get_verse_range(ch,first,v_b,want_dict)
    y += x
    return y
  except:
    raise NotFoundException()

def set_verse(v,txt):
  v.text = txt if txt else v.text
  save()
  return dict(v)

def rm_verse(v):
  old_ch = v.chapter
  rm(v)
  v.chapter = old_ch
  return dict(v)




