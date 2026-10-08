from flask import Flask, render_template, request, jsonify

from tracekit.domain import resolve
from tracekit.web import inspect
from tracekit.youtube import inspect as youtube_inspect, download as youtube_download
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


@app.route("/api/youtube/download", methods=["GET"])
def api_youtube_download():
    target = request.args.get("target", "").strip()
    mode = request.args.get("mode", "").strip().lower()

    if not target:
        return jsonify({"error": "Missing target"}), 400

    if mode not in ("mp3", "mp4"):
        return jsonify({"error": "Mode must be mp3 or mp4"}), 400

    try:
        code = youtube_download(target, mode)
        if code != 0:
            return jsonify({
                "success": False,
                "error": f"yt-dlp exited with code {code}"
            }), 500

        return jsonify({
            "success": True,
            "mode": mode,
            "message": f"{mode.upper()} download completed",
        })
    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


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
