# app.py

from flask import Flask, render_template, session
from flask_cors import CORS
from config import Config

# Import Blueprints
from routes.auth import auth_bp
from routes.quiz import quiz_bp
from routes.admin import admin_bp

# =====================================================
# Initialize Flask App
# =====================================================
app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)

# Load configuration from Config class
app.config.from_object(Config)

# Secret key for sessions
app.secret_key = Config.SECRET_KEY

# Enable CORS with session/cookie support
CORS(app, supports_credentials=True)

# Session settings (important)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set True ONLY in HTTPS

# =====================================================
# Register API Blueprints
# =====================================================

# Auth Routes → /api/auth/*
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Quiz Routes → /api/*
app.register_blueprint(quiz_bp, url_prefix='/api')

# Admin Routes → /api/admin/*
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# =====================================================
# Frontend Routes
# =====================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    if 'user_id' in session:
        return render_template('dashboard.html')
    return render_template('login.html')

@app.route('/register')
def register_page():
    if 'user_id' in session:
        return render_template('dashboard.html')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return render_template('login.html')
    return render_template('dashboard.html')

@app.route('/quiz/<int:quiz_id>')
def quiz_page(quiz_id):
    if 'user_id' not in session:
        return render_template('login.html')
    return render_template('quiz.html')

@app.route('/results')
def results_page():
    if 'user_id' not in session:
        return render_template('login.html')
    return render_template('results.html')

@app.route('/leaderboard')
def leaderboard_page():
    return render_template('leaderboard.html')

# =====================================================
# Admin Frontend Routes
# =====================================================

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        return render_template('login.html')
    return render_template('admin/dashboard.html')

@app.route('/admin/quizzes')
def admin_quizzes():
    if 'user_id' not in session or session.get('role') != 'admin':
        return render_template('login.html')
    return render_template('admin/manage_quizzes.html')

@app.route('/admin/questions/<int:quiz_id>')
def admin_questions(quiz_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return render_template('login.html')
    return render_template('admin/manage_questions.html')

# =====================================================
# Error Handlers
# =====================================================

@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('index.html'), 500

# =====================================================
# Main Entry Point
# =====================================================

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
