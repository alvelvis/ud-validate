from flask import Flask, redirect, render_template, request
import os, sys, subprocess
import json
from deta import Deta

app = Flask(__name__)
app_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(app_path, "config.json")
validate_path = os.path.join(app_path, "tools", "validate.py")
on_deta = "deta-key.txt" in os.listdir(app_path)
sentence_path = os.path.join(app_path, "sentence.conllu") if not on_deta else "/tmp/sentence.conllu"

if on_deta:
    with open("deta-key.txt") as f:
        deta_key = f.read()
    deta = Deta(deta_key)

def save_config():
    if on_deta:
        db.put(config, "access_number")
    else:
        with open(config_path, "w") as f:
            json.dump(config, f)

def increase_access_number(n=1):
    config['access_number'] += n
    save_config()

# load config
default_config = {'access_number': 1}
if on_deta:
    db = deta.Base("config")
    config = db.get("access_number")
    if not config:
        config = default_config
else:
    if not os.path.isfile(config_path):
        config = default_config
        save_config()
    else:
        with open(config_path) as f:
            config = json.load(f)

@app.route('/', methods="POST GET".split())
def home(conllu="", validation="", update="", lang=""):
    on_heroku = "heroku" in request.url
    if request.method == "POST":
        # convert new-line to linux style and add empty line in the end (validation requirements)
        conllu = request.values.get("inputText").strip().replace("\r\n", "\n") + "\n\n"
        lang = request.values.get("lang").strip().lower()
        with open(sentence_path, "w") as f:
            f.write(conllu)
        command = "{} {} --max-err=0 --lang={} {}".format(# 2>&1
                os.path.abspath(sys.executable),
                validate_path,
                lang,
                sentence_path
            )
        try:
            validation = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ)
            validation.wait()
            validation = validation.stderr.read().decode()
        except Exception as e:
            validation = command + "\n" + str(e)
        os.remove(sentence_path)
        increase_access_number(conllu.count("\n\n"))    
    elif request.method == "GET":
        os.popen("git pull")
        update = os.popen("git pull --recurse-submodules 2>&1", "r").read()
    access_number = 0
    if on_heroku:
        access_number = config['access_number']
    elif on_deta:
        access_number = config.get("access_number")

    return render_template(
        'index.html', 
        title="",
        conllu=conllu.strip(),
        validation=validation,
        update=update,
        lang=lang,
        access_number=access_number
        )

@app.route("/validate", methods="POST GET".split())
def validate():
    return redirect("/")
