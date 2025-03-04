from pydantic import BaseModel, field_validator
from typing import List
from datetime import datetime


class AnalogValues(BaseModel):
    values: List[float]

    @field_validator("values")
    def round_values(cls, v: List[float]) -> List[float]:
        return [round(float(value), 1) for value in v]


class AnalogDates(BaseModel):
    dates: List[datetime]


class AnalogCriteria(BaseModel):
    criteria: List[float]
