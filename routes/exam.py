import random
from fastapi import APIRouter, Depends, Body
from db import db
from pydantic import BaseModel

router = APIRouter(prefix="/exam", tags=["exam"])


class DataExam(BaseModel):
    subject_id: int
    exam_code: str
    duration: int
    number_of_questions: int


@router.post("")
def create_exam(db_conn: db.get_db = Depends(), data: DataExam = Body()):
    cursor = db_conn.cursor()
    try:
        # Check if the exam_code is already existed
        cursor.execute(
            """ SELECT * FROM exams WHERE exam_code = ? """,
            (data.exam_code,),
        )
        exam = cursor.fetchone()
        if exam:
            return {"err": True, "msg": "Mã đề thi đã tồn tại"}
        # Save the data exam into the database
        cursor.execute(
            """ INSERT INTO exams (subject_id, exam_code, duration, number_of_questions) VALUES (?, ?, ?, ?) """,
            (data.subject_id, data.exam_code, data.duration, data.number_of_questions),
        )
        db_conn.commit()
        exam_id = cursor.lastrowid
        # Generate the exam_questions
        cursor.execute(
            """
            SELECT * FROM questions WHERE subject_id = ?
            """,
            (data.subject_id,),
        )
        exam_questions = cursor.fetchall()
        random_questions = random.sample(exam_questions, data.number_of_questions)
        #  Shuffle the answer order
        for question in random_questions:
            answer_order = list(range(1, 5))
            random.shuffle(answer_order)
            answer_order_str = ",".join(map(str, answer_order))
            cursor.execute(
                """
                INSERT INTO exam_questions (exam_id, question_id, answer_order) VALUES
                (?, ?, ?)
            """,
                (exam_id, question["id"], answer_order_str),
            )
        db_conn.commit()
        return {"msg": "Tạo đề thi thành công. ID: {}".format(exam_id)}
    except Exception as e:
        print(e)
        return {"err": True, "msg": "Lỗi dữ liệu"}
