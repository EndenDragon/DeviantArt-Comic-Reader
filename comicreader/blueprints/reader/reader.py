from flask import Blueprint, render_template

reader = Blueprint("reader", __name__, template_folder="../../templates")

@reader.route("/create")
def create():
    return render_template("create.html.jinja2")
