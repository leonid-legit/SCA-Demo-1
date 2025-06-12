from flask import Flask, request, render_template_string
import requests
import yaml
from PIL import Image
from lxml import etree
import simplejson as json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string("Welcome to a vulnerable app")

@app.route("/external")
def external():
    url = request.args.get("url", "http://example.com")
    r = requests.get(url)
    return r.text

@app.route("/yaml", methods=["POST"])
def yaml_loader():
    data = request.data.decode()
    loaded = yaml.load(data)  # 🚨 Unsafe PyYAML load
    return str(loaded)

@app.route("/template")
def template_injection():
    template = request.args.get("tpl", "{{config}}")
    return render_template_string(template, config="<script>alert('xss')</script>")

@app.route("/image")
def load_image():
    try:
        img = Image.open("untrusted_image.jpg")  # 🚨 Vulnerable Pillow usage
        return f"Image format: {img.format}"
    except Exception as e:
        return str(e)

@app.route("/xml", methods=["POST"])
def xml_parser():
    xml_data = request.data
    try:
        tree = etree.fromstring(xml_data)  # 🚨 Unsafe XXE parse
        return etree.tostring(tree, pretty_print=True).decode()
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
