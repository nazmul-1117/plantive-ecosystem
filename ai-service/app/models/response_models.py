from pydantic import BaseModel, Field
from typing import List

class FertilizerDetail(BaseModel):
    name: str = Field(..., example="NPK 15-15-15", description="Fertilizer name")
    probability: float = Field(..., example=0.87, description="Recommendation confidence (0-1)")
    description: str = Field("", example="Balanced fertilizer for vegetative growth", description="Optional details about the fertilizer")

class FertilizerResponse(BaseModel):
    recommendations: List[FertilizerDetail]