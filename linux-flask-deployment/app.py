from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from my Linux server!"

@app.route("/health")
def health():
    return {"status": "healthy"}

app.run(host="127.0.0.1", port=5000)
