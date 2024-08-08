from fastapi import APIRouter, Depends
from db import db

router = APIRouter(prefix="/subject", tags=["subject"])


@router.get("")
def get_subject(db_conn: db.get_db = Depends()):
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()
    return subjects
