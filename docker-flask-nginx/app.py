from flask import Flask
import os

app = Flask(__name__)
APP_ENV = os.getenv("APP_ENV", "development")

@app.route("/")
def home():
    return f"Hello from my Docker container! Environment:{APP_ENV}"

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000"))
    )
