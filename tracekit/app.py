from flask import Flask, render_template, request, jsonify

from tracekit.domain import resolve
from tracekit.web import inspect
from tracekit.youtube import inspect as youtube_inspect
from tracekit.username import check_username

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/domain")
def api_domain():
    target = request.args.get("target", "").strip()

    if not target:
        return jsonify({"error": "Missing target"}), 400

    return jsonify(resolve(target))


@app.route("/api/web")
def api_web():
    target = request.args.get("target", "").strip()

    if not target:
        return jsonify({"error": "Missing target"}), 400

    return jsonify(inspect(target))


@app.route("/api/youtube")
def api_youtube():
    target = request.args.get("target", "").strip()

    if not target:
        return jsonify({"error": "Missing target"}), 400

    return jsonify(youtube_inspect(target))


@app.route("/api/username")
def api_username():
    target = request.args.get("target", "").strip()

    if not target:
        return jsonify({"error": "Missing username"}), 400

    return jsonify(check_username(target))


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False,
    )
