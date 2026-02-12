import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, email TEXT, password TEXT, role TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, admin_id INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, quiz_id INTEGER, 
        question_text TEXT, question_type TEXT, 
        correct_answer TEXT, marks INTEGER DEFAULT 1)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS options (
        id INTEGER PRIMARY KEY AUTOINCREMENT, question_id INTEGER, 
        option_text TEXT, index_label TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT, quiz_id INTEGER, 
        user_id INTEGER, score INTEGER, total_marks INTEGER, 
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # This fixes the error in Screenshot (154/155)
    cursor.execute('''CREATE TABLE IF NOT EXISTS student_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        response_id INTEGER,
        question_id INTEGER,
        submitted_text TEXT,
        FOREIGN KEY (response_id) REFERENCES responses (id),
        FOREIGN KEY (question_id) REFERENCES questions (id))''')
    
    

    conn.commit()
    conn.close()
    print("Database Reset: All tables created successfully.")

if __name__ == "__main__":
    init_db()