# backend/routes/quiz.py
from flask import Blueprint, request, jsonify, session
from models import Quiz, Question, Attempt
from utils.decorators import login_required

quiz_bp = Blueprint('quiz', __name__)

# -------------------------
# GET /api/quizzes
# -------------------------
@quiz_bp.route('/quizzes', methods=['GET'])
def get_quizzes():
    """Return list of quizzes (public)."""
    try:
        quizzes = Quiz.get_all_quizzes() or []
        # Return exactly: { "quizzes": [...] }
        return jsonify({'quizzes': quizzes}), 200
    except Exception as e:
        print(f"[quiz.get_quizzes] Error: {e}")
        return jsonify({'message': f'Error: {str(e)}'}), 500


# -------------------------
# GET /api/quizzes/<id>
# -------------------------
@quiz_bp.route('/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Return quiz details (public)."""
    try:
        quiz = Quiz.get_quiz_by_id(quiz_id)
        if not quiz:
            return jsonify({'message': 'Quiz not found'}), 404
        return jsonify({'quiz': quiz}), 200
    except Exception as e:
        print(f"[quiz.get_quiz] Error: {e}")
        return jsonify({'message': f'Error: {str(e)}'}), 500


# -------------------------
# GET /api/quizzes/<id>/questions
# -------------------------
@quiz_bp.route('/quizzes/<int:quiz_id>/questions', methods=['GET'])
@login_required
def get_quiz_questions(quiz_id):
    """Return questions for a quiz (protected). Correct answers are included in DB but will be returned as 'correct_answer'
       (your frontend must not show them)."""
    try:
        quiz = Quiz.get_quiz_by_id(quiz_id)
        if not quiz:
            return jsonify({'message': 'Quiz not found'}), 404

        questions = Question.get_questions_by_quiz(quiz_id) or []
        # Build safe response (frontend code expects these keys)
        safe_questions = []
        for q in questions:
            safe_questions.append({
                'id': q.get('id'),
                'question_text': q.get('question_text'),
                'option_a': q.get('option_a'),
                'option_b': q.get('option_b'),
                'option_c': q.get('option_c'),
                'option_d': q.get('option_d'),
                'points': q.get('points'),
                # NOTE: correct_answer exists in DB rows (correct_answer or correct_option),
                # but frontend should NOT display it. We still include it if you later need it for admin routes.
                'correct_answer': q.get('correct_answer')
            })

        return jsonify({'questions': safe_questions}), 200
    except Exception as e:
        print(f"[quiz.get_quiz_questions] Error: {e}")
        return jsonify({'message': f'Error: {str(e)}'}), 500


# -------------------------
# POST /api/quizzes/<id>/start
# -------------------------
@quiz_bp.route('/quizzes/<int:quiz_id>/start', methods=['POST'])
@login_required
def start_quiz(quiz_id):
    """Create an attempt record and return attempt_id (protected)."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'message': 'Please log in to take quiz'}), 401

        quiz = Quiz.get_quiz_by_id(quiz_id)
        if not quiz:
            return jsonify({'message': 'Quiz not found'}), 404

        attempt_id = Attempt.create_attempt(user_id, quiz_id)
        if attempt_id is None:
            return jsonify({'message': 'Failed to start attempt'}), 500

        return jsonify({'message': 'Quiz started', 'attempt_id': attempt_id}), 201
    except Exception as e:
        print(f"[quiz.start_quiz] Error: {e}")
        return jsonify({'message': f'Error: {str(e)}'}), 500


# -------------------------
# POST /api/quizzes/<id>/submit
# -------------------------
@quiz_bp.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    """Submit answers for an attempt. Expects JSON: { attempt_id: int, answers: { question_id: selected_option } }"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'message': 'Please log in'}), 401

        data = request.get_json() or {}
        attempt_id = data.get('attempt_id')
        answers = data.get('answers', {})

        if not attempt_id:
            return jsonify({'message': 'attempt_id is required'}), 400

        questions = Question.get_questions_by_quiz(quiz_id) or []
        score = 0
        total_questions = len(questions)
        results = []

        for question in questions:
            qid = question.get('id')
            qid_str = str(qid)
            selected_option = answers.get(qid_str) or answers.get(qid)  # accept either key type
            correct_option = question.get('correct_answer')  # models returns this column
            is_correct = (selected_option == correct_option)
            points_awarded = question.get('points') if is_correct else 0
            if is_correct:
                # Depending on your scoring logic you might sum points or count corrects; here we add points.
                score += points_awarded

            results.append({
                'question_id': qid,
                'selected_option': selected_option,
                'correct_option': correct_option,
                'is_correct': is_correct,
                'points_awarded': points_awarded
            })

        # Save completion info
        ok = Attempt.complete_attempt(attempt_id, score, total_questions)
        if not ok:
            return jsonify({'message': 'Failed to save attempt result'}), 500

        return jsonify({
            'message': 'Quiz submitted successfully',
            'score': score,
            'total_questions': total_questions,
            'results': results
        }), 200
    except Exception as e:
        print(f"[quiz.submit_quiz] Error: {e}")
        return jsonify({'message': f'Error: {str(e)}'}), 500


# -------------------------
# GET /api/my-attempts
# -------------------------
@quiz_bp.route('/my-attempts', methods=['GET'])
@login_required
def get_my_attempts():
    """Return completed attempts for the logged-in user."""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'message': 'Please log in'}), 401

        attempts = Attempt.get_user_attempts(user_id) or []
        return jsonify({'attempts': attempts}), 200
    except Exception as e:
        print(f"[quiz.get_my_attempts] Error: {e}")
        return jsonify({'message': f'Error: {str(e)}'}), 500


# -------------------------
# GET /api/leaderboard
# -------------------------
@quiz_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Return leaderboard (public)."""
    try:
        leaderboard = Attempt.get_leaderboard() or []
        return jsonify({'leaderboard': leaderboard}), 200
    except Exception as e:
        print(f"[quiz.get_leaderboard] Error: {e}")
        return jsonify({'message': f'Error: {str(e)}'}), 500
