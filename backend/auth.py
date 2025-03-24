from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User  # Import db and User model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///careerpath.db'

with app.app_context():
    db.init_app(app)
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return jsonify({"message": "Login successful", "user_id": user.id})
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
