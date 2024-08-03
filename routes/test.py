from fastapi import APIRouter, Depends
from db import db

router = APIRouter(prefix="/test", tags=["test"])


@router.post("/")
def test(db_conn: db.get_db = Depends()):
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return {"users": users}
