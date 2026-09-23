from pydantic import BaseModel, ConfigDict
from datetime import datetime


class DatasetResponse(BaseModel):
    id:int
    filename:str
    file_path:str
    rows: int
    columns:int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
