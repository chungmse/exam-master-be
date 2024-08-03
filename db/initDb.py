import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("db/exammaster.db")
cursor = conn.cursor()

# Create users table
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username VARCHAR(45) NOT NULL UNIQUE, 
    password VARCHAR(255) NOT NULL, 
    role TEXT CHECK(role IN ('importer', 'editor', 'generator', 'scheduler', 'candidate')) NOT NULL
)
"""
)

# Create subjects table
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    subject_name VARCHAR(45) NOT NULL UNIQUE
)
"""
)

# Create questions table
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    subject_id INTEGER NOT NULL, 
    question_text TEXT NOT NULL, 
    answer TINYINT NOT NULL, 
    option1 TEXT NOT NULL, 
    option2 TEXT NOT NULL, 
    option3 TEXT NOT NULL, 
    option4 TEXT NOT NULL, 
    mark FLOAT NOT NULL, 
    unit TEXT NOT NULL, 
    mix BOOLEAN NOT NULL DEFAULT 1, 
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
)
"""
)

# Create exams table
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    subject_id INTEGER NOT NULL, 
    exam_code VARCHAR(45) NOT NULL UNIQUE, 
    duration INTEGER NOT NULL, 
    number_of_questions INTEGER NOT NULL, 
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
)
"""
)

# Create exam_questions table
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS exam_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    exam_id INTEGER NOT NULL, 
    question_id INTEGER NOT NULL, 
    answer_order TEXT NOT NULL, 
    FOREIGN KEY (exam_id) REFERENCES exams(id), 
    FOREIGN KEY (question_id) REFERENCES questions(id)
)
"""
)

# Create exam_sessions table
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS exam_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    exam_id INTEGER NOT NULL, 
    start_time DATETIME NOT NULL, 
    end_time DATETIME NOT NULL, 
    FOREIGN KEY (exam_id) REFERENCES exams(id)
)
"""
)

# Create exam_users table
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS exam_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    user_id INTEGER NOT NULL, 
    session_id INTEGER NOT NULL, 
    score FLOAT NOT NULL, 
    FOREIGN KEY (user_id) REFERENCES users(id), 
    FOREIGN KEY (session_id) REFERENCES exam_sessions(id)
)
"""
)

# Commit changes and close connection
conn.commit()
conn.close()
