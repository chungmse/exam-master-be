from fastapi import APIRouter, Depends, Body, Header
from db import db
from pydantic import BaseModel
import bcrypt
import datetime
import jwt


router = APIRouter(prefix="/auth", tags=["auth"])


class DataSignIn(BaseModel):
    username: str
    password: str


@router.post("/sign-in")
def signin(db_conn: db.get_db = Depends(), data: DataSignIn = Body()):
    username = data.username
    password = data.password
    cursor = db_conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user is None or not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return {"err": True, "msg": "Tài khoản hoặc mật khẩu không đúng"}

    if user["role"] == "candidate":
        time_now = int(datetime.datetime.now().timestamp())
        cursor.execute(
            "SELECT * FROM exam_sessions WHERE start_time < ? AND end_time > ?",
            (time_now, time_now),
        )
        exam_session = cursor.fetchone()
        if exam_session is None:
            return {"err": True, "msg": "Không có bài thi nào đang diễn ra"}

    # Generate JWT token
    accessToken = jwt.encode(
        {
            "id": user["id"],
            "username": username,
            "role": user["role"],
            "exp": datetime.datetime.now() + datetime.timedelta(days=3),
        },
        "DQ;/_mU9<}La6%wJhF48:(Tg~#bK,BSy",
        algorithm="HS256",
    )

    # ...

    return {"accessToken": accessToken}


@router.get("/me")
def me(db_conn: db.get_db = Depends(), authorization: str = Header(...)):
    try:
        decoded_token = jwt.decode(
            authorization.replace("Bearer ", ""),
            "DQ;/_mU9<}La6%wJhF48:(Tg~#bK,BSy",
            algorithms=["HS256"],
        )
        user_id = decoded_token["id"]
        username = decoded_token["username"]
        role = decoded_token["role"]
        # Fetch user data from database using user_id
        cursor = db_conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        # Return user data
        return {"user": {"id": user_id, "username": username, "role": role}}
    except jwt.exceptions.DecodeError:
        return {"err": True, "msg": "Invalid token"}
    except jwt.exceptions.ExpiredSignatureError:
        return {"err": True, "msg": "Token has expired"}
