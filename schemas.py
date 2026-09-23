from datetime import datetime
from pydantic import BaseModel, ConfigDict

class DatasetSummary(BaseModel):
    id: int
    filename: str
    rows: int
    columns: int
    missing_values: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
