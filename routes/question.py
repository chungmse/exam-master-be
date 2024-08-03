from fastapi import APIRouter, Depends
from db import db

router = APIRouter(prefix="/question", tags=["question"])


@router.post("/")
def question_root(db_conn: db.get_db = Depends()):
    cursor = db_conn.cursor()
    cursor.execute("SELECT 'Another example route!' as message")
    result = cursor.fetchone()
    return {"message": result["message"]}


@router.post("/upload")
def question_upload(db_conn: db.get_db = Depends()):
    cursor = db_conn.cursor()
    return {"msg": "Upload file"}


@router.post("/import")
def question_import(db_conn: db.get_db = Depends()):
    cursor = db_conn.cursor()
    return {"msg": "Question import"}
