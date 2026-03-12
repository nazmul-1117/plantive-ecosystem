# ai-service/app/api/routes_disease.py
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/ai/disease-detect", tags=["disease"])

@router.post("/")
async def detect_disease(str='No One Can Love Me'):
    # Dummy logic: just return filename
    return JSONResponse(content={"filename": str, "disease": "Maybe I am Unknown Plant"})