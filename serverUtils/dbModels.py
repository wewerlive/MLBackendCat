from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated, Optional, List
from bson import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]

class TryRequestLog(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    personImage: str
    clothImage: str
    clothType: str
    num_inference_steps: int
    seed: int = -1
    guidance_scale: float = 2.5
    resultImage: str
    productId: Optional[str]
    userId: Optional[str]
    businessId: str
    created_at: str

class Business(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    # businessId: str
    businessName: str
    businessEmail: str
    businessCreated_at: str
    businessAPIKey: str
    businessPassword: str
    # businessRequests: List[] = []

class Product(BaseModel):
    # id: Optional[PyObjectId] = Field(alias="_id", default=None)
    businessId: str
    product_id: str
    product_name: str
    product_image: str
    product_page: str
    product_type: str
    product_category: str
    gender: str
    created_at: str


# class APIKey(BaseModel):
#     apiKey: str
#     businessId: str
#     created_at: str
