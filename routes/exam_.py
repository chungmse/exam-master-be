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
