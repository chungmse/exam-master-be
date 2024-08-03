from fastapi import APIRouter, Depends
from db import db

router = APIRouter(prefix="", tags=["root"])


@router.get("/")
def read_example(db_conn: db.get_db = Depends()):
    return {"msg": "OK"}
