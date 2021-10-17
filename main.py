from flask import Flask, render_template, request, redirect, send_file
from scrapper_so import get_so_jobs
from scrapper_ro import get_ro_jobs
from scrapper_wwr import get_wwr_jobs
from expoter import save_to_file

# import os

app = Flask("Job scrapper")
app = Flask(__name__, template_folder="templates")


db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    word = request.args.get("word")
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = []
            wwr_jobs = get_wwr_jobs(word)
            ro_jobs = get_ro_jobs(word)
            so_jobs = get_so_jobs(word)
            if wwr_jobs:
                jobs += wwr_jobs
            if ro_jobs:
                jobs += ro_jobs
            if so_jobs:
                jobs += so_jobs
            db[word] = jobs
    else:
        return redirect("/")
    return render_template("report.html", word=word, resultsNumber=len(jobs), jobs=jobs)


@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs, word)
        return send_file(f"{word}_jobs.csv")
    except:
        return redirect("/")


app.run(host="0.0.0.0")
