import datetime
from fastapi import APIRouter, Depends, HTTPException, Security, Request
from serverUtils.auth import getBusinessUser
from serverUtils.dbModels import Business, TryRequestLog
from serverUtils.db import getDatabase
from serverUtils.modelUtils import predictTryOn
from serverUtils.requestModels import TryRequest
from concurrent.futures import ThreadPoolExecutor
import asyncio
from typing import List
from serverUtils.awsUtils import s3, uploadImage
from serverUtils.imageUtils import imageFromBase64, base64FromBytes,imageToBase64, imageFromBytes, imageToBytes, base64ToBytes
from serverUtils.dbModels import Product
import uuid 

router = APIRouter()

modelExecutor = ThreadPoolExecutor(max_workers=1)
uploadExecutor = ThreadPoolExecutor(max_workers=6)
dbExecutor = ThreadPoolExecutor(max_workers=2)

@router.get("/",response_model=Business)
async def business(business: Business = Depends(getBusinessUser)):
    return business

@router.post("/tryon")
async def tryon(request: Request, tryRequest: TryRequest, business: Business = Depends(getBusinessUser)):
    # try:

        personBytes = base64ToBytes(tryRequest.personImage)
        clothBytes = base64ToBytes(tryRequest.clothImage)

        personImage = imageFromBytes(personBytes)
        clothImage = imageFromBytes(clothBytes)

        result = await asyncio.get_event_loop().run_in_executor(
            modelExecutor,
            predictTryOn,
            personImage,
            clothImage,
            tryRequest.clothType,
            tryRequest.num_inference_steps,
            tryRequest.seed,
            tryRequest.guidance_scale
        )
        
        # result = predictTryOn(
        #     tryRequest.personImage,
        #     tryRequest.clothImage,
        #     tryRequest.clothType,
        #     tryRequest.num_inference_steps,
        #     tryRequest.seed,
        #     tryRequest.guidance_scale
        # )

        resultBytes = imageToBytes(result)

        unique_id = uuid.uuid4()
        print(unique_id)
        personFilename = str(unique_id) + "-person.jpg"
        clothFilename = str(unique_id) + "-cloth-" + tryRequest.clothType + ".jpg"
        resultFilename = str(unique_id) +"-"+ tryRequest.clothType + "-result.jpg"

        personBytes.seek(0)
        clothBytes.seek(0)
        resultBytes.seek(0)

        asyncio.get_event_loop().run_in_executor(
            uploadExecutor,
            uploadImage,
            personBytes,
            "devbackendpersonimage",
            personFilename
        )
        asyncio.get_event_loop().run_in_executor(
            uploadExecutor,
            uploadImage,
            clothBytes,
            "devbackendclothimage",
            clothFilename
        )
        asyncio.get_event_loop().run_in_executor(
            uploadExecutor,
            uploadImage,
            resultBytes,
            "devbackendresultimage",
            resultFilename
        )

        # uploadImage(personBytes, "devbackendpersonimage", personFilename)
        # uploadImage(clothBytes, "devbackendclothimage", clothFilename)
        # uploadImage(resultBytes, "devbackendresultimage", resultFilename)

        resultString = imageToBase64(result)

        logCollection = getDatabase(request.app).get_collection("tryRequestLog")

        print(business["_id"])

        tryRequestLog = TryRequestLog(
            personImage=personFilename,
            clothImage=clothFilename,
            clothType=tryRequest.clothType,
            num_inference_steps=tryRequest.num_inference_steps,
            seed=tryRequest.seed,
            guidance_scale=tryRequest.guidance_scale,
            resultImage=resultFilename,
            productId=tryRequest.productId,
            userId=tryRequest.userId,
            businessId=str(business["_id"]),
            created_at= str(datetime.datetime.now())
        )
        print(tryRequestLog.model_dump())
        logCollection.insert_one(tryRequestLog.model_dump())
        return {"result": resultString}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

@router.get("/products")
async def products(request:Request,business: Business = Depends(getBusinessUser), response_model=List[Product]):
    product_collection = getDatabase(request.app).get_collection("product")
    products = await product_collection.find({"businessId": str(business["_id"])}).to_list(None)
    print(products)
    for product in products:
        product["_id"] = str(product["_id"])
    return products