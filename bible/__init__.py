# -*- coding: utf-8 -*-
"""
  Bible
  -----
  
  A minimalist app to store and recall bible verses

  :copyright: (c) 2015 by Brian Kim
  :license: BSD

"""

from flask import Flask 
from api import api
import model

def create_app(conf='conf/debug.cfg'):
  """
   use this method to create an instance of the app for serving 
  """
  # init app
  app = Flask(__name__)
  app.config.from_pyfile(conf)
  # connect the model the app
  model.db.init_app(app)
  with app.app_context():
    model.db.create_all()
  # register blueprint
  app.register_blueprint(api,url_prefix='/api/v1')
  return app

if __name__=="__main__":
  create_app().run(host='0.0.0.0')
