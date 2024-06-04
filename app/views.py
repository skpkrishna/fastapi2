from app.controllers import ComputeController
from app.schemas import Compute, ComputeRequest, ComputeResponse
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, APIRouter
from typing import List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

controller = ComputeController()

@router.get('/compute/',response_model=List[Compute],status_code=200)
def get_all_results():
    try:
        results=controller.get_all_data()
    except Exception as e:
        logger.error(f"Unable to fetch the results: {str(e)}")
    return results

@router.get('/compute/{id}',response_model=Compute,status_code=status.HTTP_200_OK)
def get_result_by_id(id: str):
    result=controller.get_data(id)
    return result

@router.post('/compute/',response_model=ComputeResponse,
        status_code=status.HTTP_201_CREATED)
def create_an_item(request: ComputeRequest):
    logger.info(request)
    print(request)
    id = str(request.batch_id)
    # result=controller.get_data(id)

    # if result is not None:
    #     raise HTTPException(status_code=400,detail="Batch ID already exists")
    
    result = controller.create(request.batch_id, request.payload)
    return result