#!/usr/bin/env python3 

from flask import Flask, render_template
from flask_flatpages import FlatPages

DEBUG = False 
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
flatpages = FlatPages(app)

@app.route('/')
def index():
    pages = (p for p in flatpages if 'date' in p.meta)
    return render_template('index.html', pages=pages)

@app.route('/pages/<path:path>/')
def page(path):
    page = flatpages.get_or_404(path)
    return render_template('page.html', page=page)

if __name__ == '__main__':
    app.run(port=8000)
