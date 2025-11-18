# models.py
import os
import mysql.connector
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()

def get_db_connection():
    """Return a new database connection using environment vars with sensible defaults."""
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'quiz_user'),
        password=os.getenv('MYSQL_PASSWORD', 'quiz_pass'),
        database=os.getenv('MYSQL_DB', 'quiz_app'),
        autocommit=False
    )

# ----------------- USER ----------------- #
class User:
    @staticmethod
    def create(username, email, password, role='user'):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cur.execute(
                "INSERT INTO users (username, email, password, role, created_at) "
                "VALUES (%s, %s, %s, %s, %s)",
                (username, email, hashed_password, role, datetime.utcnow())
            )
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            conn.rollback()
            print(f"[models.User.create] Error creating user: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cur.fetchone()
        except Exception as e:
            print(f"[models.User.get_by_email] Error: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cur.fetchone()
        except Exception as e:
            print(f"[models.User.get_by_id] Error: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def verify_password(hashed_password, password):
        try:
            return bcrypt.check_password_hash(hashed_password, password)
        except Exception as e:
            print(f"[models.User.verify_password] Error: {e}")
            return False

# ----------------- QUIZ ----------------- #
class Quiz:
    @staticmethod
    def create(title, description, category_id, time_limit, created_by):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                "INSERT INTO quizzes (title, description, category_id, time_limit, created_by, created_at) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (title, description, category_id, time_limit, created_by, datetime.utcnow())
            )
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            conn.rollback()
            print(f"[models.Quiz.create] Error creating quiz: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all_quizzes():
        """Return list of quizzes with category_name and created_by_name (matching routes)."""
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT q.id, q.title, q.description, q.time_limit,
                       q.category_id, c.name AS category_name,
                       q.created_by, u.username AS created_by_name,
                       q.is_active, q.created_at
                FROM quizzes q
                LEFT JOIN categories c ON q.category_id = c.id
                LEFT JOIN users u ON q.created_by = u.id
                WHERE q.is_active = 1
                ORDER BY q.created_at DESC
            """)
            rows = cur.fetchall()
            return rows or []
        except Exception as e:
            print(f"[models.Quiz.get_all_quizzes] Error: {e}")
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_quiz_by_id(quiz_id):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT q.id, q.title, q.description, q.time_limit,
                       q.category_id, c.name AS category_name,
                       q.created_by, u.username AS created_by_name,
                       q.is_active, q.created_at
                FROM quizzes q
                LEFT JOIN categories c ON q.category_id = c.id
                LEFT JOIN users u ON q.created_by = u.id
                WHERE q.id = %s
            """, (quiz_id,))
            return cur.fetchone()
        except Exception as e:
            print(f"[models.Quiz.get_quiz_by_id] Error: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def delete(quiz_id):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE quizzes SET is_active = 0 WHERE id = %s", (quiz_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"[models.Quiz.delete] Error: {e}")
            return False
        finally:
            cur.close()
            conn.close()

# ----------------- QUESTION ----------------- #
class Question:
    @staticmethod
    def create(quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option, points=10):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO questions (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option, points, created_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option, points, datetime.utcnow())
            )
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            conn.rollback()
            print(f"[models.Question.create] Error: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_questions_by_quiz(quiz_id):
        """
        Return questions but expose the correct answer as 'correct_answer' (so routes that expect that will work).
        """
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT id, quiz_id, question_text, option_a, option_b, option_c, option_d,
                       correct_option AS correct_answer, points, created_at
                FROM questions
                WHERE quiz_id = %s
                ORDER BY id
            """, (quiz_id,))
            rows = cur.fetchall()
            return rows or []
        except Exception as e:
            print(f"[models.Question.get_questions_by_quiz] Error: {e}")
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def delete(question_id):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM questions WHERE id = %s", (question_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"[models.Question.delete] Error: {e}")
            return False
        finally:
            cur.close()
            conn.close()

# ----------------- ATTEMPT ----------------- #
class Attempt:
    @staticmethod
    def create_attempt(user_id, quiz_id):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(
                "INSERT INTO attempts (user_id, quiz_id, started_at) VALUES (%s, %s, %s)",
                (user_id, quiz_id, datetime.utcnow())
            )
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            conn.rollback()
            print(f"[models.Attempt.create_attempt] Error: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def complete_attempt(attempt_id, score, total_questions):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE attempts SET score=%s, total_questions=%s, completed_at=%s WHERE id=%s",
                (score, total_questions, datetime.utcnow(), attempt_id)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"[models.Attempt.complete_attempt] Error: {e}")
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_user_attempts(user_id):
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT a.*, q.title AS quiz_title
                FROM attempts a
                LEFT JOIN quizzes q ON a.quiz_id = q.id
                WHERE a.user_id = %s AND a.completed_at IS NOT NULL
                ORDER BY a.completed_at DESC
            """, (user_id,))
            rows = cur.fetchall()
            return rows or []
        except Exception as e:
            print(f"[models.Attempt.get_user_attempts] Error: {e}")
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_leaderboard():
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT u.username,
                       COUNT(a.id) AS total_attempts,
                       AVG(a.score) AS avg_score,
                       SUM(a.score) AS total_score
                FROM users u
                INNER JOIN attempts a ON u.id = a.user_id
                WHERE a.completed_at IS NOT NULL
                GROUP BY u.id, u.username
                ORDER BY avg_score DESC, total_score DESC
                LIMIT 10
            """)
            rows = cur.fetchall()
            return rows or []
        except Exception as e:
            print(f"[models.Attempt.get_leaderboard] Error: {e}")
            return []
        finally:
            cur.close()
            conn.close()

# ----------------- CATEGORY ----------------- #
class Category:
    @staticmethod
    def create(name, description):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO categories (name, description, created_at) VALUES (%s, %s, %s)",
                        (name, description, datetime.utcnow()))
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            conn.rollback()
            print(f"[models.Category.create] Error: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT * FROM categories ORDER BY name")
            rows = cur.fetchall()
            return rows or []
        except Exception as e:
            print(f"[models.Category.get_all] Error: {e}")
            return []
        finally:
            cur.close()
            conn.close()
