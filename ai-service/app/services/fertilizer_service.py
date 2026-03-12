# app/services/fertilizer_service.py
import joblib
import pandas as pd
from app.config.settings import settings
from typing import List, Dict

# Load pre-trained model once when the service starts
pipeline = joblib.load(settings.fertilizer_model_path)

# Optional: map fertilizer names to details
fertilizer_info = {
    "Urea": "High nitrogen fertilizer",
    "DAP": "Phosphorus-rich fertilizer",
    "MOP": "Potassium-rich fertilizer",
    "Compost": "Organic matter for soil",
    "NPK": "Balanced fertilizer for all nutrients"
}

def recommend_fertilizers(input_data: dict, top_n: int = 5) -> List[Dict]:
    """
    input_data: dict with keys matching your training features
    top_n: number of top recommendations to return

    Returns a list of dicts:
    [
        {"name": "Urea", "probability": 45.23, "description": "..."},
        ...
    ]
    """

    # Convert input dict to DataFrame
    df = pd.DataFrame([input_data])

    # Predict probabilities
    probs = pipeline.predict_proba(df)
    classes = pipeline.classes_

    # Get top N indices
    top_indices = probs[0].argsort()[-top_n:][::-1]

    recommendations = []
    for i in top_indices:
        name = classes[i]
        prob = float(probs[0][i] * 100)
        desc = fertilizer_info.get(name, "No details available")
        recommendations.append({
            "name": name,
            "probability": prob,
            "description": desc
        })

    return recommendations