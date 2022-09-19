from flask import Flask, jsonify, request
from utils import json_by_title, json_by_realise, json_by_rating, json_by_genre

app = Flask(__name__)


@app.route("/movie/<title>")
def by_title(title):
    return jsonify(json_by_title(title))


@app.route("/movie/year/to/year")
def by_realise():
    from_year = request.args.get("from_year")
    to_year = request.args.get("to_year")
    return jsonify(json_by_realise(from_year, to_year))


@app.route("/rating/<age>")
def by_rating(age):
    match age:
        case "children":
            return jsonify(json_by_rating("children"))
        case "family":
            return jsonify(json_by_rating("family"))
        case "adult":
            return jsonify(json_by_rating("adult"))


@app.route("/genre/<genre>")
def by_genre(genre):
    return jsonify(json_by_genre(genre))


if __name__ == "__main__":
    app.run()