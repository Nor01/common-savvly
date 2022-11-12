import json

from pydantic import ValidationError

from common.models.advisor_info_schema import AdvisorInfoScheme

external_data = {
    'firstname': 'John',
    'lastname': 'Doe',
    'middlename': 'The 3rd',
    'address': 'NYC',
    'email': 'mail@gmail.com',
    'phone': '+1 347-567-7890',
    'zip_code': "aaa",
    '_creation': 3
}

try:
    user = AdvisorInfoScheme(**external_data)
    print(json.dumps(json.loads(user.json()), indent=4))
except ValidationError as e:
    print(json.dumps(json.loads(e.json()), indent=4))
