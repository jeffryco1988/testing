
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    message = "Enter your name"

    if request.method == "POST":
        name = request.form.get("name", "").strip()

        if name:
            message = "Hello, " + name + "! Welcome to Python."

    return """
    <html>
    <body style="font-family: Arial; text-align:center; margin-top:100px;">

        <h1>My Python Application</h1>

        <form method="POST">
            <input type="text" name="name" placeholder="Your name" required>
            <button type="submit">Submit</button>
        </form>

        <h2>""" + message + """</h2>

    </body>
    </html>
    """

