from typing import Optional
from datetime import date
from pydantic import BaseModel, ValidationError, conlist, constr, confloat, EmailStr, PrivateAttr
from pydantic import validator
from typing import Literal


# def calculate_age(born):
#     today = date.today()
#     return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

# phone number regex ^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$

class AdvisorInfoScheme(BaseModel):
    # mandtory
    firstname: Optional[str]
    lastname: Optional[str]
    address: Optional[str]
    email: EmailStr
    phone: Optional[str]  # Optional[constr(regex=r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')]

    # timestamp for dict record
    creation: Optional[int] = 0
    lastupdate: Optional[int] = 0

