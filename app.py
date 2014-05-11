import json
import flask
import requests
from collections import OrderedDict

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html")


# @app.route("/data")
# #@app.route("/data/<int:ndata>")
# def data():

#     data = {"1400130000":3,
#             "1400133600":2,
#             "1400137200":2,
#             "1400140800":1,
#             "1400144400":2,
#             "1400148000":1,
#             "1400151600":0,
#             "1400155200":1,
#             "1400158800":1}

#     data = getData()

#     return json.dumps(data)


@app.route("/data")
def getData():
    n_hours=3
    json_response=ts_along_path()
    list_ts=json_response["data"][0][0]
    ## convert to dictionary
    list_ts = map(lambda x : eval(str(x)), list_ts)
    ## remove None elements (from RC)
    list_ts = [x for x in list_ts if x is not None]

    # ---> dict in list_ts are sorted by keys

    ##keep MAX element for each til
    # in case time series don't have same keys : create list of all keys
    final_ts = {k:0 for d in list_ts for k in d.keys()}

    # # now get max for each key
    final_ts={k:max(final_ts[k],v) for d in list_ts for k, v in  d.items()}

    # # ---> final_ts is sorted by keys, but final_ts.keys() are not sorted
    final_ts=OrderedDict(sorted(final_ts.items()))

    l=final_ts.values()
            
    return json.dumps({k: sum(l[i:i+n_hours]) for i,k in enumerate(final_ts.keys()) if len(l[i:i+n_hours]) > 2})


def ts_along_path(start="4bb541f8-6665-11e3-afff-01f464e0362d", end="4bb5b51a-6665-11e3-afff-01f464e0362d"):
    # status_code = 200 OK
    # status_code = 400 Bad Request
    url_cypher = "http://localhost:7474/db/data/cypher"
    headers = {'content-type': 'application/json'}
    
    _query = "MATCH p=(end:TIL {til:{end}})-[:CONNECT_TIL*]- (start:TIL {til:{start}})"
    _query += "RETURN extract(n in nodes(p)| n.test)"
    r = requests.post(url_cypher, data=json.dumps({'query': _query, 'params':{"start":start, "end":end}}), headers=headers)
    print r.text
    return r.json()

if __name__ == "__main__":
    port = 8000
    app.debug = True
    app.run(port=port)
