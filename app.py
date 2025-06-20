from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv
import os

app = Flask(__name__)

CORS(app)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def init_db():
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS agents")
    c.execute('''CREATE TABLE IF NOT EXISTS agents
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, emotion TEXT, avatar TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, agent_id INTEGER, role TEXT, content TEXT,
                  FOREIGN KEY(agent_id) REFERENCES agents(id))''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("index1.html")

@app.route("/create_agent", methods=["POST"])
def create_agent():
    data = request.json
    name = data.get("name")
    emotion = data.get("emotion")
    avatar = data.get("avatar", "")

    if not name or not emotion:
        return jsonify(success=False, error="Name and emotion are required."), 400

    try:
        conn = sqlite3.connect("chatbot.db")
        c = conn.cursor()
        c.execute("INSERT INTO agents (name, emotion, avatar) VALUES (?, ?, ?)", (name, emotion, avatar))
        agent_id = c.lastrowid
        conn.commit()
        conn.close()
        return jsonify(success=True, agent_id=agent_id)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    message = data.get("message")
    conversation = data.get("conversation", [])
    agent_id = data.get("agent_id")

    if not agent_id:
        return jsonify({"reply": "Agent ID not provided."}), 400

    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    c.execute("SELECT id, name, emotion, avatar FROM agents WHERE id = ?", (agent_id,))
    agent_data = c.fetchone()
    if not agent_data:
        return jsonify({"reply": "Agent not found."}), 404

    agent_id, agent_name, mood, avatar = agent_data

    messages = [
        {
            "role": "system",
            "content": f"You are a {mood.lower()} AI assistant named {agent_name}. Always reply in a {mood.lower()} tone."
        }
    ]
    for msg in conversation:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"OpenAI Error: {str(e)}"

    c.execute("INSERT INTO messages (agent_id, role, content) VALUES (?, ?, ?)", (agent_id, "user", message))
    c.execute("INSERT INTO messages (agent_id, role, content) VALUES (?, ?, ?)", (agent_id, "assistant", reply))
    conn.commit()
    conn.close()

    return jsonify({"reply": reply})

@app.route("/get_history", methods=["GET"])
def get_history():
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    c.execute("""
        SELECT a.id, a.name, a.emotion, a.avatar, m.role, m.content
        FROM agents a
        LEFT JOIN messages m ON a.id = m.agent_id
        ORDER BY a.id, m.id
    """)
    rows = c.fetchall()
    conn.close()

    chat_by_agent = {}
    for agent_id, name, emotion, avatar, role, content in rows:
        if name not in chat_by_agent:
            chat_by_agent[name] = {
                "id": agent_id,
                "emotion": emotion,
                "avatar": avatar,
                "messages": []
            }
        if role and content:
            chat_by_agent[name]["messages"].append({
                "role": role,
                "content": content
            })

    return jsonify(chat_by_agent)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
