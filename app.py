import json
import flask

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/data")
#@app.route("/data/<int:ndata>")
def data():

    data = {"1400130000":3,
            "1400133600":2,
            "1400137200":2,
            "1400140800":1,
            "1400144400":2,
            "1400148000":1,
            "1400151600":0,
            "1400155200":1,
            "1400158800":1}

    return json.dumps(data)


if __name__ == "__main__":
    port = 8000
    app.debug = True
    app.run(port=port)
