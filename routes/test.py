from fastapi import APIRouter, Depends, Body
from db import db

router = APIRouter(prefix="/test", tags=["test"])


@router.post("/")
async def test(db_conn: db.get_db = Depends(), data: dict = Body(default=None)):
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return {"users": users, "data": data}
