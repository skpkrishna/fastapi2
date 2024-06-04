from pydantic import BaseModel
from datetime import datetime

class Compute(BaseModel):
    batch_id: str | None = None
    input: str
    output: str
    started_at: str | None = None

    # class Config:
    #     orm_mode = True
    #     allow_population_by_field_name = True
    #     arbitrary_types_allowed = True

class ComputeResponse(BaseModel):
    batch_id: str | None = None
    response: list
    status: str
    started_at: str
    completed_at: str

class ComputeRequest(BaseModel):
    batch_id: str | None = None
    payload: list
