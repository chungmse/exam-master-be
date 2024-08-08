from fastapi import APIRouter, Depends
from db import db

router = APIRouter(prefix="/subject", tags=["subject"])


@router.get("/")
def get_subject(db_conn: db.get_db = Depends()):
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()
    return subjects


@router.post("/get-subjects")
async def get_subjects(db_conn: db.get_db = Depends()):
    cursor = db_conn.cursor()
    cursor.execute("select * from subjects")
    result = cursor.fetchall()
    return {"message": result}


@router.post("/create-subject")
def create_subject(subject, db_conn: db.get_db = Depends()):
    sql = ("insert into subjects"
           f"values ({subject.id}, {subject.subject_name})")
    try:
        cursor = db_conn.cursor()
        cursor.execute(sql)
        db_conn.commit()
        return {f"message: create subject success"}
    except Exception as e:
        return {f"message: {e}"}


@router.post("/update-subject")
def update_subject(subject, db_conn: db.get_db = Depends()):
    sql = ("update subjects"
           f"set ({subject.subject_name})"
           f"where id = {subject.id}")
    try:
        cursor = db_conn.cursor()
        cursor.execute(sql)
        db_conn.commit()
        return {f"message: update subject success"}
    except Exception as e:
        return {f"message: {e}"}


@router.post("/delete-subject")
def delete_subject(subject_id, db_conn: db.get_db = Depends()):
    sql = ("delete from subjects"
           f"where id = {subject_id}")
    try:
        cursor = db_conn.cursor()
        cursor.execute(sql)
        db_conn.commit()
        return {f"message: delete subject success"}
    except Exception as e:
        return {f"message: {e}"}
