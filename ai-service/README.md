# Recommended `ai-service` Directory Structure

```text
ai-service/
    │
    ├── app/
    │   ├── main.py
    │   │
    │   ├── api/
    │   │   ├── routes_chat.py
    │   │   ├── routes_recommendation.py
    │   │   └── routes_disease.py
    │   │
    │   ├── services/
    │   │   ├── chat_service.py
    │   │   ├── fertilizer_service.py
    │   │   └── disease_detection_service.py
    │   │
    │   ├── models/
    │   │   ├── request_models.py
    │   │   └── response_models.py
    │   │
    │   ├── utils/
    │   │   ├── image_processing.py
    │   │   └── health_score.py
    │   │
    │   └── config/
    │       └── settings.py
    │
    ├── ml_models/
    │   ├── disease_model/
    │   └── recommendation_model/
    │
    ├── data/
    │   ├── plant_dataset.csv
    │   └── fertilizer_data.csv
    │
    ├── notebooks/
    │   └── model_training.ipynb
    │
    ├── tests/
    │   └── test_ai_routes.py

    ├── logs/
    │   └── ai_service.log
    │
    ├── requirements.txt
    ├── Dockerfile
    └── README.md
```

---

# What Each Directory Does

## `app/`

Main application code.

### `main.py`

Entry point of the FastAPI service.

Example:

```python
from fastapi import FastAPI
from app.api import routes_chat, routes_recommendation

app = FastAPI()

app.include_router(routes_chat.router)
app.include_router(routes_recommendation.router)
```

---

# `api/`

Contains **API endpoints**.

Example files:

```
routes_chat.py
routes_recommendation.py
routes_disease.py
```

Example endpoint:

```python
@router.post("/ai/chat")
def chat_with_ai(request: ChatRequest):
    return chat_service.generate_response(request.message)
```

---

# `services/`

Core **AI logic lives here**.

Examples:

```
chat_service.py
fertilizer_service.py
disease_detection_service.py
```

Example:

```python
def recommend_fertilizer(plant, soil_data):
    # AI or rule-based logic
    return "Use nitrogen-rich fertilizer"
```

---

# `models/`

Defines **data structures for requests and responses**.

Example:

```
request_models.py
response_models.py
```

Example:

```python
class FertilizerRequest(BaseModel):
    plant_name: str
    soil_moisture: float
    temperature: float
```

---

# `utils/`

Helper utilities.

Examples:

```
image_processing.py
health_score.py
```

Example:

```python
def calculate_health_score(moisture, temperature):
    score = (moisture * 0.5) + (temperature * 0.5)
    return score
```

---

# `config/`

Configuration files.

Example:

```
settings.py
```

Used for:

```
API keys
model paths
environment configs
```

---

# `ml_models/`

Stores trained ML models.

Example:

```
disease_model/
plant_disease_model.pkl
```

or

```
plant_disease_model.h5
```

---

# `data/`

Datasets used for training.

Example:

```
plant_dataset.csv
fertilizer_data.csv
```

---

# `notebooks/`

Jupyter notebooks used for:

* training models
* testing AI ideas
* data exploration

Example:

```
model_training.ipynb
```

---

# `tests/`

Unit tests for the AI service.

Example:

```
test_ai_routes.py
```

---

# Root Files

### `requirements.txt`

Example:

```text
fastapi
uvicorn
numpy
pandas
scikit-learn
opencv-python
tensorflow
```

---

### `Dockerfile`

Used if you containerize the AI service.

---

# Final Position in Your Repo

Your overall repo will look like:

```
plantive-ecosystem
│
├── mobile/
│
├── backend/
│
├── ai/
│   └── ai-service/
│
├── web/
│
├── database/
│
└── docs/
```

---

# Recommended AI API Endpoints

Your AI service might expose endpoints like:

```
POST /ai/chat
POST /ai/fertilizer-recommend
POST /ai/disease-detect
POST /ai/health-score
```

The **Node.js backend will call these APIs** when needed.

---