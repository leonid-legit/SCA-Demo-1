from flask import Flask, request, render_template_string
import requests
import yaml
from PIL import Image
from lxml import etree
import simplejson as json

app = Flask(__name__)

# 🔐 Simulated secrets for testing secret scanning tools
aws_access_key_id = "AKIAIOSFODNN7EXAMPLE"
aws_secret_access_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

github_token = "ghp_1234567890abcdefghijklmnopqrstuvwx"
slack_webhook_url = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
private_api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

# Stripe test key
stripe_test_key = "sk_test_51H8G9BLoEjP8Qv6P9FAKEKEY1234567890"

# Firebase test config
firebase_config = {
    "apiKey": "AIzaSyA-FakeKey-1234567890abcdefghijklmnop",
    "authDomain": "fake-project.firebaseapp.com",
    "projectId": "fake-project",
    "storageBucket": "fake-project.appspot.com"
}

# SendGrid test API key
sendgrid_api_key = "SG.fake_key-1234567890abcdefghijklmnop"

# Mapbox token
mapbox_token = "pk.eyJ1IjoiZmFrZXVzZXIiLCJhIjoiY2t3fWxlbW9jMjF5YzJ0bTA4cGs1bDkzZiJ9.FAKEKEY123"

# Generic API token (used in many scanners)
api_token = "api_key=12345-abcdef-67890-ghijkl"

administrator_login_password = "AdminPassword123!"

jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.fake.payload.signature"

slack_webhook = "https://hooks.slack.com/services/T00000000/B00000000/FAKEWEBHOOK123456"


facebook_key = "eb3692aa10723d1d3fca8a55eb78cbc9"
fb_key = "eb3692aa10723d1d3fca8a55eb78cbc9"



@app.route("/")
def index():
    return render_template_string("Welcome to a vulnerable app!")

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
