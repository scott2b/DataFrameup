import os
from flask import Flask, jsonify, render_template, request, url_for
import pandas as pd
import frameup

app = Flask(__name__)

df = pd.read_csv(os.environ['CSV_FILE'])

@app.route('/mydataframe')
def main():
    data = df.frameup.data(path=url_for('main'), **request.args)
    if 'text/html' in request.accept_mimetypes:
        return render_template('example.j2.html', **data)
    else:
        return jsonify(**data)
