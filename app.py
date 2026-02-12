from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "NEURO_SECRET_KEY"
# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
db = SQLAlchemy(app)

# --- Jinja2 Custom Filter ---
# Converts 0, 1, 2, 3 to 'a', 'b', 'c', 'd' for your templates
@app.template_filter('string_to_char')
def string_to_char(index):
    return chr(97 + int(index))

# --- Database Models ---
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))
    role = db.Column(db.String(20))

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    admin_id = db.Column(db.Integer)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    question_text = db.Column(db.Text)
    question_type = db.Column(db.String(20))
    correct_answer = db.Column(db.Text)
    marks = db.Column(db.Integer, default=1)

class Option(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    option_text = db.Column(db.Text)
    index_label = db.Column(db.String(1))

class Response(db.Model):
    __tablename__ = 'responses'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    score = db.Column(db.Integer)
    total_marks = db.Column(db.Integer)

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

# --- Admin Portal ---

@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        if request.form.get('access_key') != "NEURO2026":
            flash("Invalid Admin Access Key!")
            return redirect(url_for('admin_signup'))
        hashed_pw = generate_password_hash(request.form.get('password'))
        new_admin = User(username=request.form.get('username'), email=request.form.get('email'), 
                         password=hashed_pw, role='admin')
        db.session.add(new_admin)
        db.session.commit()
        return redirect(url_for('admin_login'))
    return render_template('admin_signup.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username'), role='admin').first()
        if user and check_password_hash(user.password, request.form.get('password')):
            session['user_id'] = user.id
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        flash("Invalid Credentials")
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    quizzes = Quiz.query.all()
    return render_template('admin_dashboard.html', quizzes=quizzes)

@app.route('/admin/create_quiz')
def create_quiz():
    if session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    return render_template('create_quiz.html')

@app.route('/admin/publish_quiz', methods=['POST'])
def publish_quiz():
    if session.get('role') != 'admin': return redirect(url_for('admin_login'))
    
    # Create Quiz entry
    title = request.form.get('quiz_title')
    new_quiz = Quiz(title=title, admin_id=session.get('user_id'))
    db.session.add(new_quiz)
    db.session.commit()

    # Get dynamic form lists
    q_texts = request.form.getlist('q_text[]')
    q_types = request.form.getlist('q_type[]')
    q_marks = request.form.getlist('q_marks[]')
    q_ans = request.form.getlist('q_ans[]')

    for i in range(len(q_texts)):
        question = Question(quiz_id=new_quiz.id, question_text=q_texts[i], 
                            question_type=q_types[i], correct_answer=q_ans[i], marks=q_marks[i])
        db.session.add(question)
        db.session.commit()

        if q_types[i] == 'MCQ':
            options = request.form.getlist(f'q_options_{i+1}[]')
            labels = ['a', 'b', 'c', 'd']
            for idx, opt_text in enumerate(options):
                opt = Option(question_id=question.id, option_text=opt_text, index_label=labels[idx])
                db.session.add(opt)
    db.session.commit()
    flash("Quiz Published Successfully!")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/responses/<int:quiz_id>')
def view_responses(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    responses = Response.query.filter_by(quiz_id=quiz_id).all()
    return render_template('view_responses.html', responses=responses, quiz_title=quiz.title)

# --- Student Portal ---

@app.route('/user/signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form.get('password'))
        new_user = User(username=request.form.get('username'), email=request.form.get('email'), 
                        password=hashed_pw, role='student')
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful!")
        return redirect(url_for('user_login'))
    return render_template('user_signup.html')

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username'), role='student').first()
        if user and check_password_hash(user.password, request.form.get('password')):
            session['user_id'] = user.id
            session['role'] = 'student'
            return redirect(url_for('student_dashboard'))
        flash("Invalid Credentials")
    return render_template('user_login.html')

@app.route('/student/dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('user_login'))
    quizzes = Quiz.query.all()
    return render_template('student_dashboard.html', quizzes=quizzes)

@app.route('/quiz/<int:quiz_id>')
def attempt_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    quiz_data = []
    for q in questions:
        opts = Option.query.filter_by(question_id=q.id).all()
        quiz_data.append({'question': q, 'options': opts})
    return render_template('attempt_quiz.html', quiz=quiz, quiz_data=quiz_data)

@app.route('/quiz/submit/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    score = 0
    total_marks = 0
    for q in questions:
        total_marks += q.marks
        user_ans = request.form.get(f'ans_{q.id}')
        if user_ans and user_ans.strip().lower() == q.correct_answer.strip().lower():
            score += q.marks
    
    res = Response(quiz_id=quiz_id, user_id=session.get('user_id'), score=score, total_marks=total_marks)
    db.session.add(res)
    db.session.commit()
    flash(f"Test Submitted! Score: {score}/{total_marks}")
    return redirect(url_for('student_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin/verify_answers/<int:res_id>')
def verify_answers(res_id):
    if session.get('role') != 'admin':
        return redirect(url_for('admin_login'))

    # 1. Get the Response record to find the User and Quiz
    res = Response.query.get_or_404(res_id)
    student = User.query.get(res.user_id)
    quiz = Quiz.query.get(res.quiz_id)

    # 2. Get all questions for this quiz
    questions = Question.query.filter_by(quiz_id=res.quiz_id).all()
    
    # 3. Build a list of questions and the student's actual answers
    # This matches the 'full_paper' loop in your verify_answers.html
    full_paper = []
    for q in questions:
        # In a production app, you'd query the 'student_answers' table here.
        # For now, we simulate the display logic used in your template.
        full_paper.append({
            'question_text': q.question_text,
            'answer': q.correct_answer # Replace with student_answer logic if saving to DB
        })

    return render_template('verify_answers.html', 
                           student_name=student.username,
                           quiz_title=quiz.title,
                           submission_time="Recent Submission",
                           full_paper=full_paper)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Ensure SQLite tables are ready
    app.run(debug=True)