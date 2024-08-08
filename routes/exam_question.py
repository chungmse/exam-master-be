from fastapi import APIRouter, Depends
from db import db
import random

router = APIRouter(prefix="/exam-question", tags=["exam-question"])


@router.get("/")
def read_example(db_conn: db.get_db = Depends()):
    cursor = db_conn.cursor()
    cursor.execute("SELECT 'Another example route!' as message")
    result = cursor.fetchone()
    return {"message": result["message"]}


@router.post('/create-exam-question')
def create_exam_questions(exam, db_conn: db.get_db = Depends()):
    cursor = db_conn.cursor()
    cursor.execute(f"select * from questions"
                   f"where subject_id = {exam.subject_id}"
                   f"order by random()"
                   f"limit {exam.number_of_questions}")
    questions = cursor.fetchall()

    sql = f""
    for question in questions:
        if question.mix:
            sql += (f"insert into exam_questions"
                    f"values ({exam.id}, {question.id}, {random.shuffle(list(range(1, 5)))})")
        else:
            sql += (f"insert into exam_questions"
                    f"values ({exam.id}, {question.id}, {list(range(1, 5))})")

    try:
        cursor.execute(sql)
        db_conn.commit()
        return {f"message: create exam questions success"}
    except Exception as e:
        return {f"message: {e}"}


@router.post('/delete-exam-question')
def delete_exam_questions(exam_id, db_conn: db.get_db = Depends()):
    sql = (f"delete from exam_questions"
           f"where exam_id = {exam_id}")
    try:
        cursor = db_conn.cursor()
        cursor.execute(sql)
        db_conn.commit()
        return {f"message: delete exam questions success"}
    except Exception as e:
        return {f"message: {e}"}
