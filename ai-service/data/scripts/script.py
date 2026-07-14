import random
import pandas as pd

random.seed(42)

# -----------------------------
# Plant categories
# -----------------------------

plant_types = [
    "Indoor Plant",
    "Flower Plant",
    "Vegetable Plant",
    "Herb",
    "Succulent",
    "Leafy Ornamental"
]

locations = [
    "Indoor",
    "Rooftop",
    "Balcony",
    "Outdoor Garden"
]

sunlight_levels = ["Low", "Medium", "High"]

soil_types = ["Sandy", "Loamy", "Clay", "Potting Mix"]

moisture_levels = ["Low", "Medium", "High"]

fertilizers = [
    "Compost",
    "Vermicompost",
    "Balanced NPK",
    "Nitrogen Rich",
    "Phosphorus Rich",
    "Liquid Fertilizer",
    "Bone Meal",
    "Seaweed Fertilizer"
]

# -----------------------------
# Fertilizer recommendation logic
# -----------------------------

def recommend_fertilizer(plant, n, p, k, ph):

    if n < 35 and p >= 35:
        return "Nitrogen Rich"

    if p < 35 and n >= 35:
        return "Phosphorus Rich"

    if k < 35:
        return "Balanced NPK"

    if plant == "Flower Plant":
        return "Bone Meal"

    if plant == "Indoor Plant":
        return "Liquid Fertilizer"

    if plant == "Succulent":
        return "Compost"

    return "Vermicompost"

# -----------------------------
# Dataset generation
# -----------------------------

rows = []
DATASET_SIZE = 10000

for i in range(DATASET_SIZE):

    plant = random.choice(plant_types)
    location = random.choice(locations)
    sunlight = random.choice(sunlight_levels)
    soil = random.choice(soil_types)
    moisture = random.choice(moisture_levels)

    nitrogen = random.randint(20, 80)
    phosphorus = random.randint(20, 80)
    potassium = random.randint(20, 80)

    soil_ph = round(random.uniform(5.0, 7.5), 1)

    fertilizer = recommend_fertilizer(
        plant,
        nitrogen,
        phosphorus,
        potassium,
        soil_ph
    )

    rows.append([
        plant,
        location,
        sunlight,
        soil,
        moisture,
        nitrogen,
        phosphorus,
        potassium,
        soil_ph,
        fertilizer
    ])

columns = [
    "plant_type",
    "location",
    "sunlight",
    "soil_type",
    "soil_moisture",
    "nitrogen",
    "phosphorus",
    "potassium",
    "soil_ph",
    "recommended_fertilizer"
]

df = pd.DataFrame(rows, columns=columns)

df.to_csv("rooftop_garden_fertilizer_dataset.csv", index=False)

print("Dataset generated successfully!")
print(df.head())
print("Dataset shape:", df.shape)