from flask import Flask, redirect, render_template, request
import os
import json

app = Flask(__name__)
app_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(app_path, "config.json")
validate_path = os.path.join(os.path.dirname(app_path), "tools", "validate.py")
sentence_path = os.path.join(app_path, "sentence.conllu")

def save_config():
    with open(config_path, "w") as f:
        json.dump(config, f)

def increase_access_number(n=1):
    config['access_number'] += n
    save_config()

# load config
if not os.path.isfile(config_path):
    config = {'access_number': 1}
    save_config()
else:
    with open(config_path) as f:
        config = json.load(f)

@app.route('/', methods="POST GET".split())
def home(conllu="", validation="", update=""):
    on_heroku = "heroku" in request.url
    if request.method == "POST":
        # convert new-line to linux style and add empty line in the end (validation requirements)
        conllu = request.values.get("inputText").strip().replace("\r\n", "\n") + "\n\n"
        with open(sentence_path, "w") as f:
            f.write(conllu)
        try:
            validation = os.popen("python3 '{}' --max-err=0 --lang=pt '{}' 2>&1".format(
                validate_path,
                sentence_path
            ), "r").read()
        except Exception as e:
            validation = str(e)
        os.remove(sentence_path)
        increase_access_number(conllu.count("\n\n"))    
    elif request.method == "GET":
        os.popen("git pull")
        update = os.popen("git pull --recurse-submodules 2>&1", "r").read()
    return render_template(
        'index.html', 
        title="",
        conllu=conllu.strip(),
        validation=validation,
        update=update,
        access_number=config['access_number'] if not on_heroku else 0
        )

@app.route("/validate", methods="POST GET".split())
def validate():
    return redirect("/")
