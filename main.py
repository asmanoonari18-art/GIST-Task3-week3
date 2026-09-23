import json
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Dataset
from .schemas import DatasetSummary
from .services import analyze_csv, clean_csv, validate_csv

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DataFlow API",
    description="Professional CSV data profiling, cleaning, and analytics service.",
    version="1.0.0",
)

@app.get("/health", tags=["System"])
def health():
    return {"status": "healthy", "service": "DataFlow API"}

@app.post("/datasets/profile", tags=["Datasets"])
async def profile_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        validate_csv(file.filename)
        content = await file.read()
        profile = analyze_csv(content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    dataset = Dataset(
        filename=file.filename,
        rows=profile["shape"]["rows"],
        columns=profile["shape"]["columns"],
        missing_values=sum(profile["missing_by_column"].values()),
        profile_json=json.dumps(profile),
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return {"dataset_id": dataset.id, "filename": dataset.filename, "profile": profile}

@app.get("/datasets", response_model=list[DatasetSummary], tags=["Datasets"])
def list_datasets(db: Session = Depends(get_db)):
    return db.query(Dataset).order_by(Dataset.id.desc()).all()

@app.get("/datasets/{dataset_id}", tags=["Datasets"])
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    return {
        "id": dataset.id,
        "filename": dataset.filename,
        "rows": dataset.rows,
        "columns": dataset.columns,
        "missing_values": dataset.missing_values,
        "created_at": dataset.created_at,
        "profile": json.loads(dataset.profile_json),
    }

@app.post("/datasets/clean", tags=["Data Processing"])
async def clean_dataset(file: UploadFile = File(...)):
    try:
        validate_csv(file.filename)
        content = await file.read()
        cleaned, report = clean_csv(content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return Response(
        content=cleaned,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="cleaned_{file.filename}"',
            "X-Cleaning-Report": json.dumps(report),
        },
    )
