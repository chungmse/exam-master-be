from fastapi import APIRouter, Depends
from db import db

router = APIRouter(prefix="/example", tags=["example"])


@router.get("/")
def read_example(db_conn: db.get_db = Depends()):
    cursor = db_conn.cursor()
    cursor.execute("SELECT 'Another example route!' as message")
    result = cursor.fetchone()
    return {"message": result["message"]}
