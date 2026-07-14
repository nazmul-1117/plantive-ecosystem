from pydantic import BaseModel, Field
from typing import Literal

class FertilizerRequest(BaseModel):
    plant_type: Literal["Flower Plant", "Vegetable Plant", "Fruit Plant", "Herb"] = Field(
        ..., example="Vegetable Plant", description="Type of plant"
    )
    location: Literal["Rooftop", "Garden", "Indoor", "Greenhouse"] = Field(
        ..., example="Garden", description="Where the plant is growing"
    )
    sunlight: Literal["Low", "Medium", "High"] = Field(
        ..., example="High", description="Amount of sunlight exposure"
    )
    soil_type: Literal["Loamy", "Sandy", "Clay", "Peaty", "Silty"] = Field(
        ..., example="Loamy", description="Type of soil"
    )
    soil_moisture: Literal["Low", "Medium", "High"] = Field(
        ..., example="Medium", description="Current soil moisture"
    )
    nitrogen: float = Field(..., example=20.5, description="Nitrogen content in soil")
    phosphorus: float = Field(..., example=15.0, description="Phosphorus content in soil")
    potassium: float = Field(..., example=10.0, description="Potassium content in soil")
    soil_ph: float = Field(..., example=6.5, description="Soil pH value")