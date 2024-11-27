from pydantic import BaseModel
from typing import Annotated, Optional, List

class TryRequest(BaseModel):
    personImage: str
    clothImage: str
    clothType: str
    userId: Optional[str] = None
    productId: Optional[str] = None
    num_inference_steps: int = 20
    seed: int = -1
    guidance_scale: float = 2.5

class BusinessRequest(BaseModel):
    businessName: str
    businessEmail: str
    businessPassword: str