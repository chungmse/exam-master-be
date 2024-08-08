from fastapi import APIRouter, Depends
from db import db

router = APIRouter(prefix="/exam", tags=["exam"])


# CRUD - Create, Read, Update, Delete
# REST API , RESTful API |  post, get, put, delete
@router.post("/")
def read_example(db_conn: db.get_db = Depends()):
    cursor = db_conn.cursor()
    cursor.execute("SELECT 'Another example route!' as message")
    result = cursor.fetchone()
    return {"message": result["message"]}


@router.post("/get-exams")
def get_exams(db_conn: db.get_db = Depends()):
    sql = "select * from exams"
    cursor = db_conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return {"message": result}


@router.post("/create-exam")
def create_exam(exam, db_conn: db.get_db = Depends()):
    sql = ("insert into exams"
           f"values ({exam.id}, {exam.subject_id}, {exam.exam_code}, {exam.duration}, {exam.number_of_question})")
    try:
        cursor = db_conn.cursor()
        cursor.execute(sql)
        db_conn.commit()
        return {f"message: create exam success"}
    except Exception as e:
        return {f"message: {e}"}


@router.post("/update-exam")
def update_exam(exam, db_conn: db.get_db = Depends()):
    sql = ("update exams"
           f"set ({exam.subject_id}, {exam.exam_code}, {exam.duration}, {exam.number_of_question})"
           f"where id = {exam.id}")
    try:
        cursor = db_conn.cursor()
        cursor.execute(sql)
        db_conn.commit()
        return {f"message: update exam success"}
    except Exception as e:
        return {f"message: {e}"}


@router.post("/delete-exam")
def delete_exam(exam_id, db_conn: db.get_db = Depends()):
    sql = ("delete from exams"
           f"where id = {exam_id}")
    try:
        cursor = db_conn.cursor()
        cursor.execute(sql)
        db_conn.commit()
        return {f"message: delete exam success"}
    except Exception as e:
        return {f"message: {e}"}
