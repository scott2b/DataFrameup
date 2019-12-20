import copy
from collections import namedtuple
from itertools import chain
from urllib.parse import parse_qsl, urlencode
import json
import math
import pandas as pd

DEFAULT_PAGE = 1
DEFAULT_LIMIT = 50

"""
See pandas docs for to_html params
https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.DataFrame.to_html.html

See also Extending pandas:
https://pandas.pydata.org/pandas-docs/stable/development/extending.html
"""

Navigation = namedtuple('Navigation',
    ['query', 'limit', 'offset', 'page'])

@pd.api.extensions.register_dataframe_accessor('frameup')
class Frameup:

    def __init__(self, pandas_obj):
        self.default_page = DEFAULT_PAGE
        self.default_limit = DEFAULT_LIMIT
        self._obj = pandas_obj

    passthrough_params = {
        'bold_rows': {
            'type': bool
        },
        'classes': {
            'type': None # special case, comma-separated string
        },
        'escape': {
            'type': bool
        },
        'max_rows': {
            'type': int
        },
        'max_cols': {
            'type': int
        },
        'decimal': {
            'type': str
        },
        'border': {
            'type': int
        },
        'table_id': {
            'type': str
        },
        # buf: not supported
        'columns': {
            'type': list
        },
        'col_space': {
            'type': int
        },
        'header': {
            'type': bool
        },
        'index': {
            'type': bool
        },
        'na_rep': {
            'type': str
        },
        # formatters: not supported
        # 'float_format': not supported
        'sparsify': {
            'type': bool
        },
        'index_names': {
            'type': bool
        },
        'line_width': {
            'type': int
        },
        'justify': {
            'type': str
        }
    }
    int_params = [ k for k,v in passthrough_params.items() if v['type'] == int ]
    bool_params = [ k for k,v in passthrough_params.items() if v['type'] == bool ]

    def prep_params(self, **params):
        """Return subset of query parameters as proper types for passing to
        the to_html of the DataFrame.
        """
        r = {}
        for k,v in params.items():
            if k == 'classes':
                r['classes'] = v.split(',')
                continue
            if k in self.int_params:
                r[k] = int(v)
            elif k in self.bool_params:
                if isinstance(v, str):
                    r[k] = v.lower() in ['1', 't', 'true']
            elif k in self.passthrough_params:
                # only string param types should be remaining
                assert self.passthrough_params[k]['type'] == str, \
                    f'{k} is not a string parameter'
                r[k] = v
        return r

    def extract_navigation(self, **params):
        return Navigation(
            query=params.get('query', ''),
            limit=int(params.get('limit', self.default_limit)),
            offset=int(params.get('offset', 0)),
            page=int(params.get('page', self.default_page))
        )

    def page_qs(self, path, nav, page):
        nav = nav._replace(page=page)
        return '%s?%s' % (path, urlencode(nav._asdict()))

    def data(self, qs='', path='/', render_html=True, include_data=True, **params):
        if qs:
            params.update({ k:v for k,v in parse_qsl(qs)})
        results = self._obj
        nav = self.extract_navigation(**params)
        if nav.query:
            results = results.query(nav.query)
        rows = results.shape[0]
        start = (nav.page - 1) * nav.limit + nav.offset
        end = start + nav.limit
        results = results.iloc[ start:end, : ]
        pages = math.ceil(rows / nav.limit)
        prev_page = nav.page - 1 if nav.page > 1 else 1
        next_page = nav.page + 1 if nav.page < pages else pages
        return {
            'rows': rows,
            'page': nav.page,
            'prev_page': prev_page,
            'next_page': next_page,
            'prev': self.page_qs(path, nav, prev_page),
            'next': self.page_qs(path, nav, next_page),
            'first': self.page_qs(path, nav, 1),
            'last': self.page_qs(path, nav, pages),
            'pages': pages,
            'offset': nav.offset,
            'limit': nav.limit,
            'html': results.to_html(**self.prep_params(**params)) if render_html else None,
            'data': results.to_dict() if include_data else None,
            'params': params,
            'query': nav.query
        }

    def json(self, **params):
        return json.dumps(self.data, **params)
