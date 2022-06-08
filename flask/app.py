from flask import Flask, redirect, render_template, request
import os
import sys
import shutil
import re

app = Flask(__name__)

@app.route("/validate", methods="POST GET".split())
def validate():
    return redirect("/")

@app.route('/', methods="POST GET".split())
def home():
    conllu = ""
    validation = ""
    update = ""
    
    # POST
    if 'inputText' in request.values:
        conllu = request.values.get("inputText").strip().replace("\r\n", "\n") + "\n\n"
        with open("sentence.conllu", "w") as f:
            f.write(conllu)
        try:
            validation = os.popen("python3 '{}/tools/validate.py' --max-err=0 --lang=pt sentence.conllu 2>&1".format(
            os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
            ), "r").read()
        except Exception as e:
            validation = str(e)
        os.remove("sentence.conllu")
    
    # GET
    else:
        os.popen("git pull")
        update = os.popen("git pull --recurse-submodules 2>&1", "r").read()
    return render_template(
        'index.html', 
        title="",
        conllu=conllu.strip(),
        validation=validation,
        update=update,
        )
