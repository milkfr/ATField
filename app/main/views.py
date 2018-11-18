from flask import render_template, current_app, send_from_directory

from . import main

# from app.async.scan import do_scan_task
from workers.domain_resolution import worker


@main.route('/', methods=["GET"])
def index():
    return render_template("index.html")


@main.route("/test/", methods=["GET", "POST"])
def test():
    # do_scan_task.delay("service probe by masscan",
    #               "every day", "-p1-5000 --rate 1000", "127.0.0.1", "test")
    result = worker.delay(targets=2)
    print(result)
    return render_template("index.html")


@main.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(current_app.config['BASEDIR'], filename, as_attachment=True)
