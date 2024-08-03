import sqlite3
import random

# Connect to SQLite database
conn = sqlite3.connect("db/exammaster.db")
cursor = conn.cursor()

# Insert sample data into users table
cursor.execute(
    """
INSERT INTO users (username, password, role) VALUES 
('user1', 'password1', 'importer'),
('user2', 'password2', 'editor'),
('user3', 'password3', 'generator'),
('user4', 'password4', 'scheduler'),
('user5', 'password5', 'candidate'),
('user6', 'password6', 'candidate'),
('user7', 'password7', 'candidate'),
('user8', 'password8', 'candidate'),
('user9', 'password9', 'candidate'),
('user10', 'password10', 'candidate');
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
(1, '2024-09-01 09:00:00', '2024-09-01 10:00:00'),
(2, '2024-09-01 11:00:00', '2024-09-01 12:00:00'),
(3, '2024-09-02 09:00:00', '2024-09-02 10:00:00'),
(4, '2024-09-02 11:00:00', '2024-09-02 12:00:00'),
(5, '2024-09-03 09:00:00', '2024-09-03 10:00:00');
"""
)

# Insert sample data into exam_users table
cursor.execute(
    """
INSERT INTO exam_users (user_id, session_id, score) VALUES 
(5, 1, 85.0),
(5, 2, 90.0),
(5, 3, 75.0),
(5, 4, 80.0),
(5, 5, 95.0);
"""
)

# Commit changes and close connection
conn.commit()
conn.close()
