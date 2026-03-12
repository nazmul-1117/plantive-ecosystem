# app/api/routes_recommendation.py
from fastapi import APIRouter, HTTPException
from app.models.request_models import FertilizerRequest
from app.models.response_models import FertilizerResponse, FertilizerDetail
from app.services.fertilizer_service import recommend_fertilizers
from app.utils.logger import logger  # Ensure this utility exists

router = APIRouter(prefix="/ai/fertilizer", tags=["Fertilizer"])

@router.post(
    "/",
    # response_model ensures the output matches your Pydantic schema
    # summary and description are for the FastAPI /docs (Swagger)
    response_model=FertilizerResponse,
    summary="Get top fertilizer recommendations",
    description="""
Provides the **top fertilizer recommendations** for a plant based on its type, soil, nutrients, sunlight, and location.

Returns a list of recommended fertilizers with:
- `name`: Fertilizer name
- `probability`: Confidence (0-1)
- `description`: Optional details
"""
)
def get_fertilizer_recommendations(request: FertilizerRequest):
    # 1. Log the incoming request
    logger.info(f"Fertilizer recommendation request received: {request.dict()}")

    # 2. Convert Pydantic request model to dictionary
    input_data = request.dict()

    try:
        # 3. Get top 5 recommendations from service
        recs = recommend_fertilizers(input_data, top_n=5)

        if not recs:
            # Log warning before raising exception
            logger.warning(f"No recommendations found for criteria: {input_data}")
            raise HTTPException(
                status_code=404,
                detail="No fertilizer recommendations found for this input"
            )

        # 4. Convert dicts to Pydantic response objects
        recommendations = [
            FertilizerDetail(
                name=r["name"],
                probability=r["probability"],
                description=r.get("description", "")
            )
            for r in recs
        ]

        # 5. Log success and return
        response = FertilizerResponse(recommendations=recommendations)
        logger.info(f"Successfully generated {len(recommendations)} recommendations.")
        return response

    except Exception as e:
        # Log unexpected errors
        logger.error(f"Error in recommendation route: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")