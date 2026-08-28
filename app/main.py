from fastapi import FastAPI, status
from app.schemas import RunCreate

app = FastAPI()

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/runs", status_code=status.HTTP_201_CREATED)
def create_run(run: RunCreate) -> RunCreate:
    return run