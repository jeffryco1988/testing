
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Hello, World!</h1>
    <h2>My First Python Web Application</h2>
    <p>Successfully deployed using Render!</p>
    """

if __name__ == "__main__":
    app.run()
