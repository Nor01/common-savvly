from commontest import *
from common.controllers.contract import DocuSignContractHelper
import json

c = DocuSignContractHelper("d2ad719b-65cf-4514-a9f2-db7fd8d9596c")


res = c.contract_info()

if not res:
    print("error")
else:
    print(json.dumps(res, indent=4))
pass


res = c.retrieve_contract()

if not res:
    print("error")
else:
    print(f"returned binary size {len(res)}")
pass
