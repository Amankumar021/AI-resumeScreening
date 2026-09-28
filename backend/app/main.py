from fastapi import FastAPI

app = FastAPI(
    title="AI Resume Screening System",
    description="AI-powered resume screening and candidate analysis API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AI Resume Screening API is running"
    }