import uvicorn, jwt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import question, auth, exam, subject, candidate
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

app = FastAPI()

# ====== PERMISSION ======
# guest, importer, editor, generator, scheduler, candidate
list_permission = {
    "POST|/auth/sign-in": ["guest"],
    "GET|/auth/me": ["importer", "editor", "generator", "scheduler", "candidate"],
    "POST|/candidate": ["candidate"],
    "GET|/candidate": ["candidate"],
    "POST|/exam": ["generator"],
    "POST|/question/upload": ["importer"],
    "POST|/question/import": ["importer"],
    "GET|/subject": ["generator"],
}


@app.middleware("http")
async def auth_middleware(request, call_next):
    if request.url.path.startswith("/static"):
        return await call_next(request)
    role = "guest"
    authorization = request.headers.get("Authorization")
    if authorization:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(
            token, "DQ;/_mU9<}La6%wJhF48:(Tg~#bK,BSy", algorithms=["HS256"]
        )
        request.state.user = payload
        role = payload["role"]
    has_permission = list_permission.get(f"{request.method}|{request.url.path}")
    if isinstance(has_permission, list) and role in has_permission:
        return await call_next(request)
    return JSONResponse(status_code=403, content="Unauthorized")


# ====== ROUTES ======
app.include_router(question.router)
app.include_router(auth.router)
app.include_router(exam.router)
app.include_router(subject.router)
app.include_router(candidate.router)

# ====== CORS ======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== STATIC FILES ======
app.mount("/static", StaticFiles(directory="public"), name="static")

# ====== RUN ======
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
