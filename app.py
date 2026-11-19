
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        name = request.form.get("name")
        message = f"Hello, {name}! Welcome to Python."

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>My First Python App</title>
        <style>
            body {{
                font-family: Arial;
                text-align: center;
                margin-top: 100px;
                background: #f2f2f2;
            }}
            .container {{
                background: white;
                padding: 30px;
                width: 350px;
                margin: auto;
                border-radius: 10px;
            }}
            input, button {{
                padding: 12px;
                margin: 10px;
            }}
            button {{
                background: blue;
                color: white;
                border: none;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>My Python App</h1>
            <form method="POST">
                <input type="text" name="name"
                       placeholder="Enter your name" required>
                <br>
                <button type="submit">Submit</button>
            </form>
            <h3>{message}</h3>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run()
