from flask import *
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
@app.route('/')

def index():
  