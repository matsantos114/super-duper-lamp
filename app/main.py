from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Run
from app.schemas import RunCreate, RunRead

app = FastAPI()

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.post(
    "/runs",
    response_model=RunRead,
    status_code=status.HTTP_201_CREATED,
)
def create_run(
    run: RunCreate,
    db: Session = Depends(get_db),
) -> Run:
    db_run = Run(**run.model_dump())

    db.add(db_run)
    db.commit()
    db.refresh(db_run)

    return db_run