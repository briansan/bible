"""
  @file   bible/tests.py
  @author Brian Kim
  @brief  unit tests on the bible api
"""

from flask import Flask 
from bible import create_app
from bible.seed import *
import json, os, tempfile, unittest

class BibleTestCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app('conf/testing.cfg').test_client()

  def tearDown(self):
    os.unlink('/var/bible/test.db')
  
  def test_api_lang(self):
    # post
    en = mk_en_lang()
    rv = self.app.post('/api/v1/lang', data=dict(en))
    want = dict(en)
    got = json.loads(rv.data)
    assert want==got
    # get all
    rv = self.app.get('/api/v1/lang')
    want = [want]
    got = json.loads(rv.data)
    assert want==got
    # get 
    rv = self.app.get('/api/v1/lang/en')
    want = dict(en)
    got = json.loads(rv.data)
    assert want==got
    # put
    en.name = u'Ingles'
    rv = self.app.put('/api/v1/lang/en',data=dict(en))
    want = dict(en)
    got = json.loads(rv.data)
    assert want==got
    # delete
    rv = self.app.delete('/api/v1/lang/en')
    got = json.loads(rv.data)
    assert want==got

  def test_api_version(self):
    # post
    en = mk_en_lang()
    self.app.post('/api/v1/lang', data=dict(en))
    niv = mk_niv()
    rv = self.app.post('/api/v1/version',data=dict(niv))
    want = dict(niv)
    got = json.loads(rv.data)
    assert want==got
    # get all
    rv = self.app.get('/api/v1/version')
    want = [want]
    got = json.loads(rv.data)
    assert want==got
    # get
    rv = self.app.get('/api/v1/version/niv')
    want = want[0]
    got = json.loads(rv.data)
    assert want==got
    # put
    niv.abbr = 'NIVS'
    rv = self.app.put('/api/v1/version/niv',data=dict(niv))
    want = dict(niv)
    got = json.loads(rv.data)
    assert want==got
    # delete
    rv = self.app.delete('/api/v1/version/nivs')
    want = dict(niv)
    got = json.loads(rv.data)
    assert want==got
    
  def test_api_book(self):
    # initialization
    en = mk_en_lang()
    self.app.post('/api/v1/lang', data=dict(en))
    # post
    matt = mk_nt()[0]
    rv = self.app.post('/api/v1/book',data=dict(matt))
    want = dict(matt)
    got = json.loads(rv.data)
    assert want==got
    # get
    en = mk_en_lang()
    rv = self.app.get('/api/v1/book')
    want = [want]
    got = json.loads(rv.data)
    assert want==got
    # put
    matt.name = 'Mattias'
    rv = self.app.put('/api/v1/book/matt',data=dict(matt))
    want = dict(matt)
    got = json.loads(rv.data)
    assert want==got
    # delete
    rv = self.app.delete('/api/v1/book/matt')
    got = json.loads(rv.data)
    assert want==got
    
  def test_api_chapter(self):
    # initialization
    niv = mk_niv()
    matt = mk_nt()[0]
    self.app.post('/api/v1/lang',data=dict(matt.lang))
    self.app.post('/api/v1/version',data=dict(niv))
    self.app.post('/api/v1/book',data=dict(matt))
    chap = Chapter(niv,matt,1)
    # get
    rv = self.app.get('/api/v1/niv/matt/1')
    want = dict(chap)
    got = json.loads(rv.data)
    assert want==got

  def test_api_verse(self):
    # initialization
    niv = mk_niv()
    matt = mk_nt()[0]
    self.app.post('/api/v1/lang',data=dict(matt.lang))
    self.app.post('/api/v1/version',data=dict(niv))
    self.app.post('/api/v1/book',data=dict(matt))
    chap = Chapter(niv,matt,1)
    # post
    v1 = Verse(chap,1,'In the beginning was the Word and the Word was with God, and the Word was God.')
    v2 = Verse(chap,2,'He was with God in the beginning.')
    rv = self.app.post('/api/v1/niv/matt/1/1',data=dict(v1))
    want = dict(v1)
    got = json.loads(rv.data)
    rv = self.app.post('/api/v1/niv/matt/1',data=dict(v2))
    want = dict(v2)
    got = json.loads(rv.data)
    assert want==got
    # get
    rv = self.app.get('/api/v1/niv/matt/1/1')
    want = dict(v1)
    got = json.loads(rv.data)
    assert want==got
    # get range
    rv = self.app.get('/api/v1/niv/matt/1/1/2')
    want = [dict(v1),dict(v2)]
    got = json.loads(rv.data)
    assert want==got
    # set
    v2.text = 'He was with God in the beginning and the end.'
    rv = self.app.put('/api/v1/niv/matt/1/2',data=dict(v2))
    want = dict(v2)
    got = json.loads(rv.data)
    assert want==got
    # rm
    rv = self.app.delete('/api/v1/niv/matt/1/1')
    want = dict(v1)
    got = json.loads(rv.data)
    assert want==got
    
if __name__=="__main__":
  unittest.main()
