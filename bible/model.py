"""
 @file   bible/model.py
 @author Brian Kim
 @brief  definition of bible objects
         Language, Version, Chapter, Verse
"""
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Language(db.Model):
  abbr = db.Column(db.String(5), primary_key=True)
  name = db.Column(db.String(32))
  def __init__(self,abbr,name):
    self.abbr = abbr
    self.name = name
  def __repr__(self):
    return '<Language %s>' % self
  def __str__(self):
    return '%s (%s)' % (self.name,self.abbr)
  def __iter__(self):
    yield (u'abbr', self.abbr)
    yield (u'name', self.name)

class Version(db.Model):
  lang_id = db.Column(db.Integer, db.ForeignKey('language.abbr'))
  lang = db.relationship('Language',backref=db.backref('versions',lazy='dynamic'))
  abbr = db.Column(db.String(5), primary_key=True)
  name = db.Column(db.String(32))
  def chapters(self):
    return self.lang.chapters()
  def __init__(self,lang,abbr,name):
    self.lang = lang
    self.abbr = abbr
    self.name = name
  def __repr__(self):
    return '<Translation %s>' % self
  def __str__(self):
    return '%s (%s)' % (self.name,self.abbr)
  def __iter__(self):
    yield (u'abbr', self.abbr)
    yield (u'name', self.name)
    yield (u'lang', self.lang.abbr)

class Book(db.Model):
  lang_id = db.Column(db.Integer, db.ForeignKey('language.abbr'))
  lang = db.relationship('Language',backref=db.backref('books',lazy='dynamic'))
  abbr = db.Column(db.String(5), primary_key=True)
  name = db.Column(db.String(32))
  numch = db.Column(db.Integer)

  def __init__(self,lang,abbr,name,numch):
    self.lang = lang
    self.abbr = abbr
    self.name = name
    self.numch = numch

  def __repr__(self):
    return '<Book %s>' % self
  def __str__(self):
    return '%s (%s)' % (self.name,self.abbr)
  def __iter__(self):
    yield (u'abbr', self.abbr)
    yield (u'name', self.name)
    yield (u'lang', self.lang.abbr)
    yield (u'numch', self.numch)

class Chapter(db.Model):
  id = db.Column(db.Integer,primary_key=True)
  version_id = db.Column(db.String(5), db.ForeignKey('version.abbr'))
  book_id    = db.Column(db.String(5), db.ForeignKey('book.abbr'))
  number     = db.Column(db.Integer)

  version = db.relationship('Version',backref=db.backref('chapters',lazy='dynamic'))
  book = db.relationship('Book',backref=db.backref('chapters',lazy='dynamic'))

  def __init__(self,v,b,num):
    self.version = v
    self.book = b
    self.number = num

  def __repr__(self):
    return '<Chapter %s>' % self
  def __str__(self):
    return '%s %s %i' % (self.version.abbr,self.book.abbr,self.number)
  def __iter__(self):
    yield (u'version',self.version.abbr)
    yield (u'book',self.book.abbr)
    yield (u'number',self.number)
    yield (u'verses',[ dict(x) for x in self.verses.all() ])

class Verse(db.Model):
  id = db.Column(db.Integer,primary_key=True)
  ch_id  = db.Column(db.Integer, db.ForeignKey('chapter.id'))
  number = db.Column(db.Integer)
  text   = db.Column(db.String(1024,convert_unicode=True))
  
  chapter = db.relationship('Chapter',backref=db.backref('verses',lazy='dynamic'))
  
  def __init__(self,ch,num,txt):
    self.chapter = ch
    self.number  = num
    self.text    = txt

  def __repr__(self):
    return '<Verse %s>' % self
  def __str__(self):
    return '%s:%i' % (self.chapter,self.number)
  def __iter__(self):
    yield (u'chapter',str(self.chapter))
    yield (u'number',self.number)
    yield (u'text',self.text)
    
