from fastapi import FastAPI
from routes import root, test, example, question, exam, exam_question, subject

app = FastAPI()

app.include_router(root.router)
app.include_router(test.router)
app.include_router(example.router)
app.include_router(question.router)
app.include_router(exam.router)
app.include_router(exam_question.router)
app.include_router(subject.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
