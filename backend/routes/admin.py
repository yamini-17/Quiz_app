from flask import Blueprint, request, jsonify, session
from models import Quiz, Question, Category
from utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

def check_admin():
    """Helper function to check if user is admin"""
    if 'user_id' not in session or session.get('role') != 'admin':
        return False
    return True

@admin_bp.route('/quizzes', methods=['POST'])
def create_quiz():
    """Create a new quiz"""
    try:
        if not check_admin():
            return jsonify({'message': 'Admin access required'}), 403
        
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        category_id = data.get('category_id')
        time_limit = data.get('time_limit', 30)
        
        if not title or not description:
            return jsonify({'message': 'Title and description are required'}), 400
        
        quiz_id = Quiz.create(title, description, category_id, time_limit, session['user_id'])
        
        return jsonify({
            'message': 'Quiz created successfully',
            'quiz_id': quiz_id
        }), 201
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@admin_bp.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    """Delete a quiz"""
    try:
        if not check_admin():
            return jsonify({'message': 'Admin access required'}), 403
        
        Quiz.delete(quiz_id)
        return jsonify({'message': 'Quiz deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@admin_bp.route('/questions', methods=['POST'])
def create_question():
    """Create a new question"""
    try:
        if not check_admin():
            return jsonify({'message': 'Admin access required'}), 403
        
        data = request.get_json()
        quiz_id = data.get('quiz_id')
        question_text = data.get('question_text')
        option_a = data.get('option_a')
        option_b = data.get('option_b')
        option_c = data.get('option_c')
        option_d = data.get('option_d')
        correct_option = data.get('correct_option')
        points = data.get('points', 10)
        
        if not all([quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option]):
            return jsonify({'message': 'All fields are required'}), 400
        
        if correct_option not in ['A', 'B', 'C', 'D']:
            return jsonify({'message': 'Correct option must be A, B, C, or D'}), 400
        
        question_id = Question.create(
            quiz_id, question_text, option_a, option_b, 
            option_c, option_d, correct_option, points
        )
        
        return jsonify({
            'message': 'Question created successfully',
            'question_id': question_id
        }), 201
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@admin_bp.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """Delete a question"""
    try:
        if not check_admin():
            return jsonify({'message': 'Admin access required'}), 403
        
        Question.delete(question_id)
        return jsonify({'message': 'Question deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@admin_bp.route('/categories', methods=['POST'])
def create_category():
    """Create a new category"""
    try:
        if not check_admin():
            return jsonify({'message': 'Admin access required'}), 403
        
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({'message': 'Category name is required'}), 400
        
        category_id = Category.create(name, description)
        
        return jsonify({
            'message': 'Category created successfully',
            'category_id': category_id
        }), 201
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@admin_bp.route('/quizzes/<int:quiz_id>/questions', methods=['GET'])
def get_quiz_questions_admin(quiz_id):
    """Get all questions for a quiz (including correct answers)"""
    try:
        if not check_admin():
            return jsonify({'message': 'Admin access required'}), 403
        
        questions = Question.get_by_quiz(quiz_id)
        return jsonify({'questions': questions}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500