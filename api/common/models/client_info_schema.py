from datetime import date
from typing import Literal
from typing import Optional
import datetime

from pydantic import BaseModel, conlist, constr, confloat, EmailStr
from pydantic import validator


# todo: add validation for spouse _is_us_citizen
# zip code ^\d{5}(?:[-\s]\d{4})?$
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


# pii_list = ['firstname', 'lastname',
#             'address', 'birthdate', 'ssn', 'phone', 'zip_code', 'city',
#             'spouse_firstname', 'spouse_lastname', 'spouse_email', 'spouse_address', 'spouse_zip_code',
#             'spouse_passport_data', 'spouse_alien_id_or_visa',
#             'spouse_birthdate', 'spouse_ssn', 'passport_data', 'alien_id_or_visa']

pii_list = ['firstname', 'lastname', 'middlename',
            'address', 'birthdate', 'ssn']


def split_pii_info(info: dict, pii_lst: list) -> (dict, dict):
    pii = dict()
    non_pii = dict()
    for key in info.keys():
        if key in pii_lst:
            pii[key] = info[key]
        else:
            non_pii[key] = info[key]
    return pii, non_pii


def first_day_of_next_month(dt):
    '''Get the first day of the next month. Preserves the timezone.

    Args:
        dt (datetime.datetime): The current datetime

    Returns:
        datetime.datetime: The first day of the next month at 00:00:00.
    '''
    if dt.month == 12:
        return datetime.date(year=dt.year + 1,
                             month=1,
                             day=1)
        # tzinfo=dt.tzinfo)
    else:
        return datetime.date(year=dt.year,
                             month=dt.month + 1,
                             day=1)
        # tzinfo=dt.tzinfo)


# ssn reg r'^(?!000|.+0{4})(?:\d{9}|\d{3}-\d{2}-\d{4})$'
class ClientInfoScheme(BaseModel):
    # mandtory
    firstname: str
    lastname: str
    middlename: Optional[str]
    address: str
    sex: Literal['M', 'F']
    birthdate: date
    ssn: constr(regex=r'^(?!000|.+0{4})(?:\d{9}|\d{3}-\d{2}-\d{4})$')
    is_married: Literal['Y', 'N']
    is_US_citizen: Literal['Y', 'N']
    funding: confloat(gt=0)
    payout_ages: conlist(int, min_items=1)
    ETF: str = 'VOO Vanguard'
    purchaser_type: Literal['Accredited Investor', 'Qualified Purchaser']
    # optional fields
    phone: Optional[str]  # = '+1 (000) 000-0000'
    zip_code: Optional[constr(regex=r'^\d{5}(?:[-\s]\d{4})?$')] = '00000'
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    investment_start_date: Optional[date]
    # email: Optional[str]  # the email field is stored outside the dictionary,

    # optional spouse
    spouse_firstname: Optional[str]
    spouse_lastname: Optional[str]
    spouse_middlename: Optional[str]
    spouse_address: Optional[str]
    spouse_sex: Optional[Literal['F', 'M']]
    spouse_birthdate: Optional[date]
    spouse_ssn: Optional[constr(regex=r'^(?!000|.+0{4})(?:\d{9}|\d{3}-\d{2}-\d{4})$')]
    spouse_email: Optional[EmailStr]
    spouse_zip_code: Optional[constr(regex=r'^\d{5}(?:[-\s]\d{4})?$')] = '00000'
    spouse_city: Optional[str]
    spouse_state: Optional[str]
    spouse_country: Optional[str]

    # must in case of non US citizen
    is_green_card: Optional[Literal['Y', 'N']]
    passport_data: Optional[str]
    passport_expiration: Optional[date]
    passport_country: Optional[str]
    alien_id_or_visa: Optional[str]
    alien_id_or_visa_expiration: Optional[date]

    # must in case of non US citizen
    spouse_is_green_card: Optional[Literal['Y', 'N']]
    spouse_passport_data: Optional[str]
    spouse_passport_expiration: Optional[date]
    spouse_passport_country: Optional[str]
    spouse_alien_id_or_visa: Optional[str]
    spouse_alien_id_or_visa_expiration: Optional[date]
    spouse_is_US_citizen: Optional[Literal['Y', 'N']]

    # internal data store to be passed later on to the user tables
    contract_id: Optional[str] = 'empty'
    email: Optional[EmailStr]
    signed_date: Optional[date]
    advisor_id: Optional[str]  # the advisor id at the time of contract creation
    advisor_fee: Optional[int] = 0
    age: Optional[int] = 0  # calculated age at time of creation

    # timestamp for dict record
    creation: Optional[int] = 0
    lastupdate: Optional[int] = 0

    @validator('payout_ages', each_item=True)
    def check_ages(cls, v, values, **kwargs):
        if 'birthdate' in values:
            assert v > calculate_age(values['birthdate']), 'payout age must be in the future'
            assert v < 120, 'payout age must be less than 120'
        return v

    @validator('birthdate')
    def check_birthdate(cls, v):
        assert calculate_age(v) > 0, 'Age must be positive'
        return v

    ### spouse data
    @validator('spouse_firstname', always=True)
    def check_spouse_firstname(cls, v, values, **kwargs):
        # print(f"validating spouse first name, values['is_married']={values['is_married']} , v={v}")
        if values['is_married'] == 'Y':
            assert v is not None, "Spouse firstname needed when is married"
        return v

    @validator('spouse_sex', always=True)
    def check_spouse_spouse_sex(cls, v, values, **kwargs):
        if values['is_married'] == 'Y':
            assert v is not None, "Spouse sex needed when is married"
        return v

    # @validator('spouse_address', always=True)
    # def check_spouse_spouse_address(cls, v, values, **kwargs):
    #     assert values['is_married'] == 'Y' and v not None, "Spouse address needed when is married"
    #     return v

    @validator('spouse_lastname', always=True)
    def check_spouse_lastname(cls, v, values, **kwargs):
        if values['is_married'] == 'Y':
            assert v is not None, "Spouse last name needed when is married"
        return v

    @validator('spouse_birthdate', always=True)
    def check_spouse_birthdate(cls, v, values, **kwargs):
        if values['is_married'] == 'Y':
            assert v is not None, "Spouse birthdate needed when is married"
            assert calculate_age(v) >= 18, 'Spouse age must be greater than 18'
        return v

    ## passport data for non US citizen
    @validator('passport_data', always=True)
    def check_passport_data(cls, v, values, **kwargs):
        if values['is_US_citizen'] == 'N':
            assert v is not None, "passport_data needed for non US citizen"
        return v

    @validator('passport_expiration', always=True)
    def check_passport_expiration(cls, v, values, **kwargs):
        if values['is_US_citizen'] == 'N':
            assert v is not None, "passport_expiration needed for non US citizen"
        return v

    @validator('passport_country', always=True)
    def check_passport_country(cls, v, values, **kwargs):
        if values['is_US_citizen'] == 'N':
            assert v is not None, "passport_country needed for non US citizen"
        return v

    @validator('alien_id_or_visa', always=True)
    def check_alien_id_or_visa(cls, v, values, **kwargs):
        if values['is_US_citizen'] == 'N':
            assert v is not None, "alien_id_or_visa needed for non US citizen"
        return v

    @validator('alien_id_or_visa_expiration', always=True)
    def check_alien_id_or_visa_expiration(cls, v, values, **kwargs):
        if values['is_US_citizen'] == 'N':
            assert v is not None, "alien_id_or_visa_expiration needed for non US citizen"
        return v

    @validator('advisor_fee')
    def check_advisor_fee(cls, v):
        assert 0 <= v <= 100, 'Advisor fee should be between 0 and 100'
        return v

    # if investment_start_date is not filled, set it to begining of next month
    @validator('investment_start_date', always=True)
    def set_investment_start_date(cls, v, values, **kwargs):
        return v or first_day_of_next_month(datetime.datetime.now())

    # age calculated at time of creation
    @validator('age', always=True)
    def set_age(cls, v, values, **kwargs):
        return v or calculate_age(values['birthdate'])
