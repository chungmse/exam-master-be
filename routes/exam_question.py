from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel

from db import db
import random

router = APIRouter(prefix="/exam-question", tags=["exam-question"])


class DataExam(BaseModel):
    id: int
    subject_id: int
    exam_code: str
    duration: int
    number_of_questions: int


@router.get("/")
def read_example(db_conn: db.get_db = Depends()):
    cursor = db_conn.cursor()
    cursor.execute("SELECT 'Another example route!' as message")
    result = cursor.fetchone()
    return {"message": result["message"]}


@router.post('/create-exam-question')
def create_exam_questions(data: DataExam = Body(), db_conn: db.get_db = Depends()):
    cursor = db_conn.cursor()
    cursor.execute(f"select * from questions"
                   f"where subject_id = {data.subject_id}"
                   f"order by random()"
                   f"limit {data.number_of_questions}")
    questions = cursor.fetchall()

    sql = f""
    for question in questions:
        if question.mix:
            sql += (f"insert into exam_questions"
                    f"values ({data.id}, {question.id}, {random.shuffle(list(range(1, 5)))})")
        else:
            sql += (f"insert into exam_questions"
                    f"values ({data.id}, {question.id}, {list(range(1, 5))})")

    try:
        cursor.execute(sql)
        db_conn.commit()
        return {f"message: create exam questions success"}
    except Exception as e:
        return {f"message: {e}"}


@router.post('/delete-exam-question')
def delete_exam_questions(exam_id: int, db_conn: db.get_db = Depends()):
    sql = (f"delete from exam_questions"
           f"where exam_id = {exam_id}")
    try:
        cursor = db_conn.cursor()
        cursor.execute(sql)
        db_conn.commit()
        return {f"message: delete exam questions success"}
    except Exception as e:
        return {f"message: {e}"}
