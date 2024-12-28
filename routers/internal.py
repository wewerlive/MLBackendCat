from serverUtils.db import getDatabase
from fastapi import APIRouter, Request
from serverUtils.requestModels import BusinessRequest
from serverUtils.dbModels import Business, TryRequestLog, Product
from typing import List
import datetime
import uuid
router = APIRouter()
import json 

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

@router.post("/addProducts")
async def addProducts(request: Request):
    db = getDatabase(request.app).get_collection("product")
    businessDb = getDatabase(request.app).get_collection("business")
    business = await businessDb.find_one({"businessName": "TwinverseBrand1"})
    print(business)
    f = open('products3.json', 'r')
    data = json.load(f)
    print(data)
    f.close()
    for product in data["products"]:
        productObj = Product(
            businessId=str(business["_id"]),
            product_id=str(product["product_id"]),
            product_name=product["product_name"],
            product_image=product["product_link"],
            product_page="",
            product_type=product["product_type"],
            product_category=product["product_category"],
            gender=product["gender"],
            created_at=str(datetime.datetime.now())
        )
        print(productObj.model_dump())
        await db.insert_one(productObj.model_dump())
    return {"status":"success"}