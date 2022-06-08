from flask import Flask, render_template, request
import os
import sys
import shutil
import re

app = Flask(__name__)

@app.route('/validate', methods="POST".split())
def validate():
    conllu = request.values.get("inputText")
    with open("sentence.conllu", "w") as f:
        f.write(conllu)
    try:
        validation = os.popen("python3 '{}/tools/validate.py' --max-err=0 --lang=pt sentence.conllu 2>&1".format(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
        ), "r").read()
    except Exception as e:
        validation = str(e)
    os.remove("sentence.conllu")
    return render_template(
        'index.html',
        title="",
        conllu=conllu,
        validation=validation
        )

@app.route('/')
def home():
    update = os.popen("git pull --recurse-submodules 2>&1", "r").read()
    return render_template(
        'index.html', 
        title="",
        update=update,
        )
