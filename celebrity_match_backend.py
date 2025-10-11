# Flask backend for celebrity matchmaking
from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# List of celebrities (can be expanded)
celebrities = [
    {"name": "Taylor Swift", "profession": "Singer", "interest": "music"},
    {"name": "Cristiano Ronaldo", "profession": "Footballer", "interest": "sports"},
    {"name": "Emma Watson", "profession": "Actor", "interest": "reading"},
    {"name": "Zendaya", "profession": "Actor", "interest": "travel"},
    {"name": "Elon Musk", "profession": "Entrepreneur", "interest": "gaming"}
]

@app.route('/api/match-celebrity', methods=['POST'])
def match_celebrity():
    data = request.get_json()
    interest = data.get('interest')
    # Match by interest, else random
    match = next((c for c in celebrities if c['interest'] == interest), None)
    if not match:
        match = random.choice(celebrities)
    return jsonify({"success": True, "celebrity": match})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
