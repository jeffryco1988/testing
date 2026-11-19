import os
from flask import Flask, request, session
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"

# Initialize OpenAI client (will automatically read OPENAI_API_KEY environment variable)
client = OpenAI(api_key=os.environ.get("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"))

# System prompt to define the assistant's persona
SYSTEM_PROMPT = "You are a simple, friendly virtual assistant. Keep responses concise and helpful."

def get_ai_response(user_message, chat_history):
    """Call OpenAI API to get a response and return the updated chat history."""
    # Build the message list for this request
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history
    messages.append({"role": "user", "content": user_message})

    try:
        # Call Chat Completions API (non-streaming for simplicity)
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Can be changed to gpt-4o, etc.
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        reply = response.choices[0].message.content
    except Exception as e:
        # Return a friendly error message when API call fails
        reply = f"Sorry, I encountered an error while processing your request: {str(e)}"

    # Update chat history: add user message and assistant reply
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": reply})
    
    return reply, chat_history


@app.route("/", methods=["GET", "POST"])
def home():
    # Initialize chat history (only store user/assistant messages, system prompt is added dynamically each time)
    if "chat" not in session:
        session["chat"] = []

    if request.method == "POST":
        user_message = request.form.get("message", "").strip()
        if user_message:
            # Get AI reply and updated history
            reply, updated_history = get_ai_response(user_message, session["chat"])
            session["chat"] = updated_history  # Save back to session

    # Build chat log HTML
    chat_html = ""
    for msg in session.get("chat", []):
        role = "You" if msg["role"] == "user" else "Assistant"
        css_class = "user" if msg["role"] == "user" else "bot"
        chat_html += f"""
            <div class="msg {css_class}"><b>{role}:</b> {msg['content']}</div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>My AI Assistant</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f2f2f2;
                margin: 0;
                padding: 40px 0;
            }}
            .container {{
                background: white;
                padding: 25px;
                width: 550px;
                margin: auto;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
            h1 {{ text-align: center; color: #2c3e50; }}
            .chat {{
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 15px;
                background: #fafafa;
            }}
            .msg {{ padding: 8px 10px; margin: 6px 0; border-radius: 8px; white-space: pre-wrap; }}
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
            <h1>🤖 My OpenAI Assistant</h1>
            <div class="chat">{chat_html or "<p style='color:#888;'>Send a message to start chatting...</p>"}</div>
            <form method="POST" autocomplete="off">
                <input type="text" name="message" placeholder="Type a message..." autofocus required>
                <button type="submit">Send</button>
            </form>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
