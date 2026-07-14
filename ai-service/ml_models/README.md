# Fertilizer Recommendation Model Documentation

## 1. Overview

This model predicts the **recommended fertilizer type** for a plant based on plant characteristics, environmental conditions, and soil nutrient levels.

The model is implemented using a **machine learning pipeline** built with scikit-learn and a Random Forest Classifier.

The pipeline automatically handles **data preprocessing and prediction** in one step.

---

## 2. Model Pipeline

The prediction system is built using a **pipeline** that contains two stages:

1. **Preprocessing**

   * Handles categorical and numerical features.
   * Converts categorical values into numerical form.
   * Prepares data so the model can process it correctly.

2. **Model**

   * Algorithm: Random Forest Classifier
   * Parameters:

     * `n_estimators = 1000`
     * `max_depth = 10`
     * `random_state = 42`

Pipeline structure:

```python
rf_pipeline = Pipeline(
    steps=[
        ("preprocessing", preprocessor),
        ("model", RandomForestClassifier(
            n_estimators=1000,
            max_depth=10,
            random_state=42
        ))
    ]
)
```

---

# 3. Model Inputs

The model expects **one row of plant and soil information** with the following fields.

| Feature       | Type        | Description                                         |
| ------------- | ----------- | --------------------------------------------------- |
| plant_type    | categorical | Type of plant (e.g., Flower Plant, Vegetable Plant) |
| location      | categorical | Plant growing location (e.g., Rooftop, Garden)      |
| sunlight      | categorical | Sunlight exposure level (Low, Medium, High)         |
| soil_type     | categorical | Soil category (Loamy, Sandy, Clay)                  |
| soil_moisture | categorical | Current soil moisture level                         |
| nitrogen      | numeric     | Nitrogen level in soil                              |
| phosphorus    | numeric     | Phosphorus level in soil                            |
| potassium     | numeric     | Potassium level in soil                             |
| soil_ph       | numeric     | Soil pH level                                       |

---

# 4. Example Input

Example data passed to the model:

```python
sample = pd.DataFrame([{
    "plant_type": "Flower Plant",
    "location": "Rooftop",
    "sunlight": "High",
    "soil_type": "Loamy",
    "soil_moisture": "Medium",
    "nitrogen": 30,
    "phosphorus": 25,
    "potassium": 40,
    "soil_ph": 6.5
}])
```

---

# 5. Making a Prediction

Load the saved model and run prediction:

```python
result = rf_pipeline.predict(sample)

print("Recommended Fertilizer:", result[0])
```

---

# 6. Model Output

The model outputs:

**Recommended fertilizer type**

Example output:

```
Recommended Fertilizer: NPK 20-20-20
```

The prediction represents the **fertilizer best suited for the given plant and soil conditions**.

---

# 7. Expected Workflow

1. Load the trained pipeline (`.pkl` file).
2. Prepare input data in a **Pandas DataFrame** with the required features.
3. Call `.predict()` on the pipeline.
4. The model returns the **recommended fertilizer label**.

---

✅ This pipeline ensures:

* preprocessing and prediction happen **in one step**
* the same transformations used during training are applied during inference

---