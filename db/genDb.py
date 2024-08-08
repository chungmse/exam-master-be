import sqlite3
import random
import datetime

nowRaw = datetime.datetime.now()
now = datetime.datetime.now().timestamp()
one_hour_ago = (nowRaw - datetime.timedelta(hours=1)).timestamp()
one_hour_later = (nowRaw + datetime.timedelta(hours=10)).timestamp()

# Connect to SQLite database
conn = sqlite3.connect("db/exammaster.db")
cursor = conn.cursor()

# Insert sample data into users table
cursor.execute(
    """
INSERT INTO users (username, password, role) VALUES 
('kienpt', '$2b$12$vxryEPr9xn4jxFAGH0q9zuW63s0gjlXyNWrwUlKzTBsB3iHBa6bu6', 'importer'),
('editor', '$2b$12$vxryEPr9xn4jxFAGH0q9zuW63s0gjlXyNWrwUlKzTBsB3iHBa6bu6', 'editor'),
('anhdt', '$2b$12$vxryEPr9xn4jxFAGH0q9zuW63s0gjlXyNWrwUlKzTBsB3iHBa6bu6', 'generator'),
('scheduler', '$2b$12$vxryEPr9xn4jxFAGH0q9zuW63s0gjlXyNWrwUlKzTBsB3iHBa6bu6', 'scheduler'),
('chungnv', '$2b$12$vxryEPr9xn4jxFAGH0q9zuW63s0gjlXyNWrwUlKzTBsB3iHBa6bu6', 'candidate'),
('candidate1', '$2b$12$vxryEPr9xn4jxFAGH0q9zuW63s0gjlXyNWrwUlKzTBsB3iHBa6bu6', 'candidate'),
('candidate2', '$2b$12$vxryEPr9xn4jxFAGH0q9zuW63s0gjlXyNWrwUlKzTBsB3iHBa6bu6', 'candidate'),
('candidate3', '$2b$12$vxryEPr9xn4jxFAGH0q9zuW63s0gjlXyNWrwUlKzTBsB3iHBa6bu6', 'candidate'),
('candidate4', '$2b$12$vxryEPr9xn4jxFAGH0q9zuW63s0gjlXyNWrwUlKzTBsB3iHBa6bu6', 'candidate'),
('candidate5', '$2b$12$vxryEPr9xn4jxFAGH0q9zuW63s0gjlXyNWrwUlKzTBsB3iHBa6bu6', 'candidate');
"""
)

# Insert sample data into subjects table
cursor.execute(
    """
INSERT INTO subjects (subject_name) VALUES 
('MAT'),
('PHY'),
('CHE'),
('BIO'),
('HIS');
"""
)


# Function to generate sample questions
def generate_questions(subject_id, subject_name, start_id, count):
    for i in range(start_id, start_id + count):
        question_text = f"Question {i} for subject {subject_name}"
        answer = (i % 4) + 1  # Cycle through 1, 2, 3, 4
        option1 = f"Option 1 for question {i}"
        option2 = f"Option 2 for question {i}"
        option3 = f"Option 3 for question {i}"
        option4 = f"Option 4 for question {i}"
        mark = 1.0
        unit = f"Chapter {((i - start_id) // 10) + 1}"  # Group every 10 questions into a chapter
        mix = True
        cursor.execute(
            """
            INSERT INTO questions (subject_id, question_text, answer, option1, option2, option3, option4, mark, unit, mix) VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                subject_id,
                question_text,
                answer,
                option1,
                option2,
                option3,
                option4,
                mark,
                unit,
                mix,
            ),
        )


# Generate 50 questions for each subject with specific ranges
subject_ids = [1, 2, 3, 4, 5]
subject_names = ["MAT", "PHY", "CHE", "BIO", "HIS"]
start_ids = [1, 51, 101, 151, 201]
for subject_id, subject_name, start_id in zip(subject_ids, subject_names, start_ids):
    generate_questions(subject_id, subject_name, start_id, 50)

# Insert sample data into exams table
cursor.execute(
    """
INSERT INTO exams (subject_id, exam_code, duration, number_of_questions) VALUES 
(1, 'MAT101', 60, 10),
(2, 'PHY101', 60, 10),
(3, 'CHE101', 60, 10),
(4, 'BIO101', 60, 10),
(5, 'HIS101', 60, 10);
"""
)

# Insert sample data into exam_questions table with shuffled answer order
for exam_id in range(1, 6):
    # Get subject_id for the current exam_id
    cursor.execute("SELECT subject_id FROM exams WHERE id = ?", (exam_id,))
    subject_id = cursor.fetchone()[0]

    # Get question ids for the current exam_id
    cursor.execute(
        "SELECT MIN(id), MAX(id) FROM questions WHERE subject_id = ?", (subject_id,)
    )
    min_question_id, max_question_id = cursor.fetchone()

    for question_id in range(min_question_id, min_question_id + 10):
        answer_order = list(range(1, 5))
        random.shuffle(answer_order)
        answer_order_str = ",".join(map(str, answer_order))
        cursor.execute(
            """
            INSERT INTO exam_questions (exam_id, question_id, answer_order) VALUES 
            (?, ?, ?)
        """,
            (exam_id, question_id, answer_order_str),
        )

# Insert sample data into exam_sessions table

cursor.execute(
    """
INSERT INTO exam_sessions (exam_id, start_time, end_time) VALUES 
(1, ?, ?),
(2, ?, ?),
(3, ?, ?),
(4, ?, ?),
(5, ?, ?);
""",
    (
        one_hour_ago,
        one_hour_later,
        datetime.datetime(2024, 9, 1, 11, 0, 0).timestamp(),
        datetime.datetime(2024, 9, 1, 12, 0, 0).timestamp(),
        datetime.datetime(2024, 9, 2, 9, 0, 0).timestamp(),
        datetime.datetime(2024, 9, 2, 10, 0, 0).timestamp(),
        datetime.datetime(2024, 9, 2, 11, 0, 0).timestamp(),
        datetime.datetime(2024, 9, 2, 12, 0, 0).timestamp(),
        datetime.datetime(2024, 9, 3, 9, 0, 0).timestamp(),
        datetime.datetime(2024, 9, 3, 10, 0, 0).timestamp(),
    ),
)

# Insert sample data into exam_users table
cursor.execute(
    """
INSERT INTO exam_users (user_id, session_id, score) VALUES 
(6, 1, 85.0),
(6, 2, 90.0),
(6, 3, 75.0),
(6, 4, 80.0),
(6, 5, 95.0);
"""
)

# Commit changes and close connection
conn.commit()
conn.close()
