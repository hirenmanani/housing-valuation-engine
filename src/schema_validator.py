from pydantic import BaseModel, Field, validator
from typing import List


class PropertySchema(BaseModel):
    """The 'Data Contract' for a single Mumbai Property"""
    locality: str
    bhk: int = Field(gt=0, lt=11)  # Must be between 1 and 10
    sqft: int = Field(gt=100)      # Must be at least 100 sqft
    price_cr: float = Field(gt=0)  # Price must be positive

    @validator('locality')
    def locality_must_be_known(cls, v):
        allowed = ['Worli', 'Andheri West', 'Bandra East', 'Chembur', 'Powai']
        if v not in allowed:
            raise ValueError(f'{v} is not a valid Mumbai locality')
        return v
