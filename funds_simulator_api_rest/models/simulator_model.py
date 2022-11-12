from pydantic import BaseModel
from typing import Optional

class Advisor(BaseModel):
    gender:str
    current_age:int
    average_return:float
    funding_amount:float
    payout_age:int
    withRounded:float
    withoutRounded:float
    multiplierRound:float

class UpdateAdvisor(BaseModel):
    gender:Optional[str] = None
    current_age:Optional[int] = None
    average_return:Optional[float] = None
    funding_amount:Optional[float] = None
    payout_age:Optional[int] = None
    withRounded:Optional[float] = None
    withoutRounded:Optional[float] = None
    multiplierRound:Optional[float] = None

