# Flask backend for celebrity matchmaking
from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import hashlib
import json
import os

app = Flask(__name__)
CORS(app)

# File to store previous users
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

# Load previous users at startup
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        previous_users = json.load(f)
else:
    previous_users = []

# List of celebrities
celebrities = [
    {"name": "Taylor Swift", "profession": "Singer", "interest": "music"},
    {"name": "Cristiano Ronaldo", "profession": "Footballer", "interest": "sports"},
    {"name": "Emma Watson", "profession": "Actor", "interest": "reading"},
    {"name": "Zendaya", "profession": "Actor", "interest": "travel"},
    {"name": "Elon Musk", "profession": "Entrepreneur", "interest": "gaming"}
]

# --- Compatibility scoring function ---
def compute_score(name1, name2, interest1, interest2):
    h = hashlib.md5((name1.lower() + '|' + name2.lower()).encode('utf-8')).hexdigest()
    score = int(h[:8], 16) % 101
    if interest1 and interest2 and interest1 == interest2:
        score = min(100, score + 10)
    return score

# --- Home route ---
@app.route('/', methods=['GET'])
def home():
    return (
        "<h1>Celebrity Match API</h1>"
        "<p>Use <code>POST /api/match-user</code> with JSON {\"name\": \"Alice\", \"age\": 25, \"interest\": \"music\"} to get your best matches.</p>"
    )

# --- Match user with best previous user and celebrity ---
@app.route('/api/match-user', methods=['POST'])
def match_user():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    age = data.get('age')
    interest = (data.get('interest') or '').strip().lower()

    if not name or not interest:
        return jsonify({"success": False, "error": "Name and interest required."}), 400

    # Load users fresh
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    else:
        users = []

    # Save current user if not already present
    if not any(u['name'].lower() == name.lower() for u in users):
        user = {"name": name, "age": age, "interest": interest}
        users.append(user)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)

    # --- Find best previous user ---
    possible_users = [u for u in users if u['name'].lower() != name.lower()]
    best_user = None
    best_user_score = -1
    for u in possible_users:
        score = compute_score(name, u['name'], interest, u['interest'])
        if score > best_user_score:
            best_user_score = score
            best_user = u

    # --- Find best celebrity ---
    best_celebrity = None
    best_celebrity_score = -1
    for c in celebrities:
        score = compute_score(name, c['name'], interest, c['interest'])
        if score > best_celebrity_score:
            best_celebrity_score = score
            best_celebrity = c

    return jsonify({
        "success": True,
        "best_user_match": best_user,
        "user_score": best_user_score if best_user else None,
        "best_celebrity_match": best_celebrity,
        "celebrity_score": best_celebrity_score
    })

# --- Previous users endpoint ---
@app.route('/api/previous-users', methods=['GET'])
def list_previous_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    else:
        users = []
    return jsonify({"success": True, "users": users})

# --- Compatibility endpoint ---
@app.route('/api/compatibility', methods=['POST'])
def compatibility():
    data = request.get_json() or {}
    name1 = (data.get('name1') or data.get('user') or '').strip()
    name2 = (data.get('name2') or data.get('celebrity') or data.get('celebrity_name') or '').strip()
    interest1 = (data.get('interest1') or data.get('user_interest') or '').strip().lower()
    interest2 = (data.get('interest2') or data.get('celebrity_interest') or '').strip().lower()

    if not name1 or not name2:
        return jsonify({"success": False, "error": "Both name1 and name2 are required."}), 400

    score = compute_score(name1, name2, interest1, interest2)

    # Friendly explanation based on score
    if score >= 90:
        tone = "A near-perfect match — sparks are flying! ✨"
    elif score >= 75:
        tone = "Great compatibility — you two would get along really well. 😄"
    elif score >= 50:
        tone = "Decent match — with a little effort, this could work nicely. 🙂"
    elif score >= 30:
        tone = "Some differences — interesting pairing, could be a fun challenge. 🤔"
    else:
        tone = "Low compatibility — might be best as friends, but never say never. 💬"

    return jsonify({
        "success": True,
        "score": score,
        "explanation": tone
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
