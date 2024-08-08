from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel

from db import db

router = APIRouter(prefix="/subject", tags=["subject"])


class DataSubject(BaseModel):
    id: int
    subject_name: str


@router.get("/")
def get_subject(db_conn: db.get_db = Depends()):
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()
    return subjects


@router.post("/create-subject")
def create_subject(data: DataSubject = Body(), db_conn: db.get_db = Depends()):
    sql = ("insert into subjects"
           f"values ({data.id}, {data.subject_name})")
    try:
        cursor = db_conn.cursor()
        cursor.execute(sql)
        db_conn.commit()
        return {f"message: create subject success"}
    except Exception as e:
        return {f"message: {e}"}


@router.post("/update-subject")
def update_subject(data: DataSubject = Body(), db_conn: db.get_db = Depends()):
    sql = ("update subjects"
           f"set ({data.subject_name})"
           f"where id = {data.id}")
    try:
        cursor = db_conn.cursor()
        cursor.execute(sql)
        db_conn.commit()
        return {f"message: update subject success"}
    except Exception as e:
        return {f"message: {e}"}


@router.post("/delete-subject")
def delete_subject(subject_id: int, db_conn: db.get_db = Depends()):
    sql = ("delete from subjects"
           f"where id = {subject_id}")
    try:
        cursor = db_conn.cursor()
        cursor.execute(sql)
        db_conn.commit()
        return {f"message: delete subject success"}
    except Exception as e:
        return {f"message: {e}"}
