from flask import Flask, jsonify, render_template, request, url_for
import pandas as pd
import frameup

app = Flask(__name__)

df = pd.read_csv('/Users/scott/Downloads/ks-projects-201801.csv')

@app.route('/mydataframe')
def main():
    data = df.frameup.data(path=url_for('main'), **request.args)
    return render_template('example.j2.html', **data)
