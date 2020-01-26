from flask import Flask
from flask import jsonify
from repositories import get_repo_list

app = Flask(__name__)

@app.route("/<user>")
def get_repo_name(user):
    return jsonify(get_repo_list(user))

@app.route("/")
def index():
    return {
        "usage": "http://your-app-url/{repo-user}"
    }
