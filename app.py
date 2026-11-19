from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"  # needed for session

def get_response(user_input):
    """Simple rule-based virtual assistant logic."""
    text = user_input.lower().strip()

    # Greetings
    if any(word in text for word in ["hello", "hi", "hey", "hola"]):
        return "Hi there! 👋 I'm your virtual assistant. How can I help you today?"

    # Name introduction
    if "my name is" in text:
        name = user_input.split("my name is", 1)[1].strip().title()
        session["user_name"] = name
        return f"Nice to meet you, {name}! 😊"

    # Asking for the name back
    if "what is my name" in text or "who am i" in text:
        name = session.get("user_name")
        return f"You told me your name is {name}." if name else "I don't know your name yet. Tell me: 'My name is ...'"

    # Time
    if "time" in text:
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%H:%M')}."

    # Date
    if "date" in text or "today" in text:
        from datetime import datetime
        return f"Today is {datetime.now().strftime('%A, %d %B %Y')}."

    # Weather (no real API — just a canned reply)
    if "weather" in text:
        return "Sorry, I can't check live weather yet, but it's always a good day to code! ☀️"

    # Jokes
    if "joke" in text:
        return "Why do programmers prefer dark mode? Because light attracts bugs! 🐛"

    # Help
    if "help" in text:
        return ("You can try: 'hello', 'my name is ...', 'what is my name?', "
                "'time', 'date', 'joke', 'help', or 'bye'.")

    # Goodbye
    if any(word in text for word in ["bye", "goodbye", "see you"]):
        return "Goodbye! 👋 Have a great day!"

    # Fallback
    return "I'm not sure how to answer that. Type 'help' to see what I can do."

@app.route("/", methods=["GET", "POST"])
def home():
    if "chat" not in session:
        session["chat"] = []

    if request.method == "POST":
        user_message = request.form.get("message", "")
        if user_message.strip():
            reply = get_response(user_message)
            chat = session["chat"]
            chat.append({"user": user_message, "bot": reply})
            session["chat"] = chat  # save back to session

    # Build the chat log HTML
    chat_html = ""
    for msg in session.get("chat", []):
        chat_html += f"""
            <div class="msg user"><b>You:</b> {msg['user']}</div>
            <div class="msg bot"><b>Assistant:</b> {msg['bot']}</div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Virtual Assistant</title>
        <style>
            body {{
                font-family: Arial;
                background: #f2f2f2;
                margin: 0;
                padding: 40px 0;
            }}
            .container {{
                background: white;
                padding: 25px;
                width: 500px;
                margin: auto;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
            h1 {{ text-align: center; color: #2c3e50; }}
            .chat {{
                max-height: 350px;
                overflow-y: auto;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 15px;
                background: #fafafa;
            }}
            .msg {{ padding: 8px 10px; margin: 6px 0; border-radius: 8px; }}
            .user {{ background: #d6eaff; text-align: right; }}
            .bot  {{ background: #e9f7e9; text-align: left; }}
            form {{ display: flex; gap: 8px; }}
            input[type=text] {{
                flex: 1; padding: 12px; border: 1px solid #ccc;
                border-radius: 6px; font-size: 14px;
            }}
            button {{
                padding: 12px 18px; background: #2c7be5; color: white;
                border: none; border-radius: 6px; cursor: pointer;
                font-size: 14px;
            }}
            button:hover {{ background: #1a5fc0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 My Virtual Assistant</h1>
            <div class="chat">{chat_html or "<p style='color:#888;'>Say hello to start chatting...</p>"}</div>
            <form method="POST" autocomplete="off">
                <input type="text" name="message" placeholder="Type a message..." autofocus required>
                <button type="submit">Send</button>
            </form>
        </div>
    </body>
    </html>
    """
