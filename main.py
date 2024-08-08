import uvicorn, jwt
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from routes import question, auth, exam, subject, candidate

security = HTTPBearer()


async def get_token_data(token: str):
    try:
        payload = jwt.decode(
            token, "DQ;/_mU9<}La6%wJhF48:(Tg~#bK,BSy", algorithms=["HS256"]
        )
        return payload
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def auth_middleware(request: Request, call_next):
    credentials: HTTPAuthorizationCredentials = await security(request)
    token = credentials.credentials

    print(token)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")

    payload = await get_token_data(token)
    request.state.user = payload

    response = await call_next(request)
    return response


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question.router)
app.include_router(auth.router)
app.include_router(exam.router)
app.include_router(subject.router)
app.include_router(candidate.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
