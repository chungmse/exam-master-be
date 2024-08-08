from fastapi import APIRouter, Depends, Body, Request
from db import db
from pydantic import BaseModel
import datetime

router = APIRouter(prefix="/candidate", tags=["candidate"])


@router.get("")
def get_exam(db_conn: db.get_db = Depends(), request: Request = None):
    cursor = db_conn.cursor()
    time_now = int(datetime.datetime.now().timestamp())
    cursor.execute(
        "SELECT * FROM exam_sessions WHERE start_time < ? AND end_time > ?",
        (time_now, time_now),
    )
    exam_session = cursor.fetchone()
    if exam_session is None:
        return {"err": True, "msg": "Không có bài thi nào đang diễn ra"}

    cursor.execute("SELECT * FROM exams WHERE id = ?", (exam_session["exam_id"],))
    exam = cursor.fetchone()

    cursor.execute("SELECT * FROM subjects WHERE id = ?", (exam["subject_id"],))
    subject = cursor.fetchone()

    # Check if user has already taken the exam
    cursor.execute(
        "SELECT * FROM exam_users WHERE user_id = ? AND session_id = ?",
        (request.state.user["id"], exam_session["id"]),
    )
    user_exam = cursor.fetchone()
    if user_exam is not None:
        return {
            "err": True,
            "code": 2,
            "msg": "Bạn đã thi bài này rồi",
            "score": user_exam["score"],
            "subject_name": subject["subject_name"],
            "exam_code": exam["exam_code"],
        }

    # List of questions
    cursor.execute("SELECT * FROM exam_questions WHERE exam_id = ?", (exam["id"],))
    questions = cursor.fetchall()

    list_questions = []

    for question in questions:
        this_question = {}
        this_question["id"] = question["question_id"]
        this_question["final_options"] = []
        answer_order = question["answer_order"].split(",")
        cursor.execute(
            "SELECT * FROM questions WHERE id = ?", (question["question_id"],)
        )
        question_data = cursor.fetchone()
        this_question["question"] = question_data["question_text"]
        for answer in answer_order:
            this_question["final_options"].append(
                {
                    "id": answer,
                    "content": question_data[f"option{answer}"],
                }
            )

        list_questions.append(this_question)

    return {
        "session_id": exam_session["id"],
        "exam_id": exam["id"],
        "subject_name": subject["subject_name"],
        "exam_code": exam["exam_code"],
        "duration": exam["duration"],
        "number_of_questions": exam["number_of_questions"],
        "list_questions": list_questions,
    }


class DataExam(BaseModel):
    exam_id: int
    session_id: int
    list_answers: dict


@router.post("")
def submit_exam(
    db_conn: db.get_db = Depends(), data: DataExam = Body(), request: Request = None
):
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM exam_questions WHERE exam_id = ?", (data.exam_id,))
    questions = cursor.fetchall()
    total_mark = 0
    for question in questions:
        cursor.execute(
            "SELECT * FROM questions WHERE id = ?", (question["question_id"],)
        )
        question_data = cursor.fetchone()
        user_answer = int(data.list_answers.get(str(question["question_id"]), 0))
        true_answer = question_data["answer"]
        if user_answer == true_answer:
            total_mark += float(question_data["mark"])

    cursor.execute(
        "INSERT INTO exam_users (user_id, session_id, score) VALUES (?, ?, ?)",
        (request.state.user["id"], data.session_id, total_mark),
    )

    db_conn.commit()

    return {"total_mark": total_mark}
