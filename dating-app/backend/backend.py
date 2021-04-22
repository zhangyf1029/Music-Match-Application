from .app import app

# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

from .__init__ import app 

 # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable

app.config.from_envvar('BACKEND_SETTINGS', silent=True)