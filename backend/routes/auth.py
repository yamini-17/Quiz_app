from flask import Blueprint, request, jsonify, session
from models import User
from datetime import datetime, timedelta
import jwt
from config import Config

auth_bp = Blueprint('auth', __name__)

# ---------------------- REGISTER ---------------------- #
# FIXED → removed /api
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'message': 'No data provided'}), 400

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')

        if not username or not email or not password:
            return jsonify({'message': 'Username, email, and password required'}), 400

        if '@' not in email or '.' not in email:
            return jsonify({'message': 'Invalid email format'}), 400

        if len(password) < 6:
            return jsonify({'message': 'Password must be at least 6 characters'}), 400

        existing = User.get_by_email(email)
        if existing:
            return jsonify({'message': 'Email already registered'}), 400

        user_id = User.create(username, email, password, role)

        return jsonify({'message': 'Registration successful', 'user_id': user_id}), 201

    except Exception as e:
        print("❌ Registration Error:", str(e))
        return jsonify({'message': 'Registration failed'}), 500


# ---------------------- LOGIN ---------------------- #
# FIXED → removed /api
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'Email and password required'}), 400

        user = User.get_by_email(email)
        if not user or not User.verify_password(user['password'], password):
            return jsonify({'message': 'Invalid email or password'}), 401

        # Create JWT
        token = jwt.encode({
            'user_id': user['id'],
            'role': user['role'],
            'exp': datetime.utcnow() + timedelta(hours=2)
        }, Config.JWT_SECRET_KEY, algorithm='HS256')

        # Save session
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']

        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            }
        }), 200

    except Exception as e:
        print("❌ Login Error:", str(e))
        return jsonify({'message': 'Login failed'}), 500


# ---------------------- LOGOUT ---------------------- #
# FIXED → removed /api
@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        print("❌ Logout Error:", str(e))
        return jsonify({'message': 'Logout failed'}), 500


# ---------------------- CURRENT USER ---------------------- #
# FIXED → removed /api
@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'Not authenticated'}), 401

        user = User.get_by_id(session['user_id'])

        if not user:
            session.clear()
            return jsonify({'message': 'User not found'}), 404

        return jsonify({
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            }
        }), 200

    except Exception as e:
        print("❌ /me Error:", str(e))
        return jsonify({'message': 'Failed to fetch user'}), 500
