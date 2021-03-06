# DataFrameup

```
 $ pip install frameup
 $ frameup <path-to-csvfile>
```

Frameup is the easiest way to get your Pandas DataFrame up into a Python-based web application. Simply `import frameup` and your DataFrames will become URL query parameter, and pagination aware.

Supports:

 * Most of the [Pandas DataFrame to_html parameters](https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.DataFrame.to_html.html) as URL query parameters
 * Pagination query parameters: `page`, `limit`, `offset`
 * Filtering of the DataFrame using the parameter `query` and the [Pandas DataFrame query syntax](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html#pandas.DataFrame.query)

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

Given a template similar to example.j2.html

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

## On query parameter objects

Be sure the query parameter object you pass frameup does not return lists for values. `classes` is the only multi-valued parameter accepted, and should be passed as a comma-delimited string rather than multiple `classes` keys.

Python web frameworks all have their own way of dealing with the vagaries of GET parameter specification hell. Most implement some concept of a `MultiDict`, but the APIs for these vary from one framework to the next. Thus, the requirement of only single-valued GET params greatly simplifies things here.

## Other projects

Projects to review / learn from / use instead

 * [Datasette](https://github.com/simonw/datasette)
 * [Workbench](https://workbenchdata.com/)
 * [Table Stacker](https://latimes-table-stacker.readthedocs.io)
 * [R Reactable](https://glin.github.io/reactable/)
