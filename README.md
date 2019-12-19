# DataFrameup

```
 $ pip install frameup
 $ frameup <path-to-csvfile>
```

Frameup is the easiest way to get your Pandas DataFrame up into a Python-based web application. Simply `import frameup` and your DataFrames will become URL query parameter, and pagination aware.

Zero dependencies, except Pandas of course.

## Quick look

Serve a csv as a frameup dataframe on localhost

```
 $ python -m frameup.serve <path-to-csv-file>
```

Then navigate to http://localhost:8000/. Use the [Pandas DataFrame query syntax](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) in the query box.

... or, get a JSON payload:

```
 $ curl 'http://localhost:8000/?query=&limit=10&page=1' | python -m json.tool
```


## Use it in your web application

### Flask example

Given a template similar to example.js.html

```
from flask import Flask, jsonify, render_template, request, url_for
import pandas as pd
import frameup

app = Flask(__name__)

df = pd.read_csv(YOUR_CSV_FILE)

@app.route('/mydataframe')
def main():
    data = df.frameup.data(path=url_for('main'), **request.args)
    return render_template('example.j2.html', **data)
```

For something ajaxy, just replace the return with:

```
return jsonify(**data)
```

## Other projects

Projects to review / learn from / use instead

 * [Datasette](https://github.com/simonw/datasette)
 * [Workbench](https://workbenchdata.com/)
