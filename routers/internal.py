from serverUtils.db import getDatabase
from fastapi import APIRouter, Request
from serverUtils.requestModels import BusinessRequest
from serverUtils.dbModels import Business, TryRequestLog
from typing import List
import datetime
import uuid
router = APIRouter()

@router.post("/createBusiness",response_model=Business)
async def createBusiness(request: Request, businessReq: BusinessRequest):
    db = getDatabase(request.app).get_collection("business")
    uniqueApiKey = str(uuid.uuid4())
    business = Business(
        businessName=businessReq.businessName,
        businessEmail=businessReq.businessEmail,
        businessPassword=businessReq.businessPassword,
        businessCreated_at= str(datetime.datetime.now()),
        businessAPIKey=uniqueApiKey
    )
    await db.insert_one(business.model_dump())
    return business

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/getAllBusinesses", response_model=List[Business])
async def getAllBusinesses(request: Request):
    db = getDatabase(request.app).get_collection("business")
    businessEntries = await db.find().to_list(None)
    print(businessEntries)
    return businessEntries

@router.get("/getAllLogs", response_model=List[TryRequestLog])
async def getAllLogs(request: Request):
    db = getDatabase(request.app).get_collection("tryRequestLog")
    logs = await db.find().to_list(None)
    print(logs)
    return logs