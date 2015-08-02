"""
  @file   bible/seed.py
  @author Brian Kim
  @brief  initialize the database with the good stuff
"""

from model import *
import requests

def mk_en_lang():
  return Language(u'en',u'English')

def mk_niv():
  en = mk_en_lang()
  return Version(en,u'NIV',u'New International Version')

def mk_rsv():
  en = mk_en_lang()
  return Version(en,u'RSV',u'Revised Standard Version')

def mk_nt():
  en = mk_en_lang()
  matt = Book(en,u'Matt',u'Matthew',28)
  mark = Book(en,u'Mark',u'Mark',16)
  luke = Book(en,u'Luke',u'Luke',24)
  john = Book(en,u'John',u'John',21)
  acts = Book(en,u'Acts',u'Acts',28)
  rom  = Book(en,u'Rom',u'Romans',16)
  cor1  = Book(en,u'1 Cor',u'1 Corinthians',16)
  cor2  = Book(en,u'2 Cor',u'2 Corinthians',13)
  gal   = Book(en,u'Gal',u'Galatians',6)
  eph   = Book(en,u'Eph',u'Ephesians',6)
  phil  = Book(en,u'Phil',u'Philippians',4)
  col   = Book(en,u'Col',u'Colossians',4)
  thes1 = Book(en,u'1 Thes',u'1 Thessalonians',5)
  thes2 = Book(en,u'2 Thes',u'2 Thessalonians',3)
  tim1  = Book(en,u'1 Tim',u'1 Timothy',6)
  tim2  = Book(en,u'2 Tim',u'2 Timothy',4)
  ti    = Book(en,u'Ti',u'Titus',3)
  phlm  = Book(en,u'Phlm',u'Philemon',1)
  heb   = Book(en,u'Heb',u'Hebrews',13)
  jm    = Book(en,u'Jm',u'James',5)
  pet1  = Book(en,u'1 Pet',u'1 Peter',5)
  pet2  = Book(en,u'2 Pet',u'2 Peter',3)
  jn1   = Book(en,u'1 Jn',u'1 John',5)
  jn2   = Book(en,u'2 Jn',u'2 John',1)
  jn3   = Book(en,u'3 Jn',u'3 John',1)
  jude  = Book(en,u'Jude',u'Jude',1)
  rev   = Book(en,u'Rev',u'Revelation',22)
  return [matt, mark, luke, john, acts, rom, 
        cor1, cor2, gal, eph, phil, col, thes2, thes2, 
        tim1, tim2, ti, phlm, heb, jm, pet1, pet2,
        jn1, jn2, jn3, jude, rev]

def seed():
  print 'adding language'
  requests.post('http://localhost/api/v1/lang',dict(mk_en_lang()))
  print 'adding versions (niv,rsv)'
  requests.post('http://localhost/api/v1/version',dict(mk_niv()))
  requests.post('http://localhost/api/v1/version',dict(mk_rsv()))
  print 'adding books'
  for book in mk_nt():
    print '\t%s' % book
    requests.post('http://localhost/api/v1/book',dict(book))
