# Normal way
def advisorEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "gender":item["gender"],
        "current_age":item["current_age"],
        "average_return":item["average_return"],
        "funding_amount":item["funding_amount"],
        "payout_age":item["payout_age"],
        "withRounded":item["withRounded"],
        "withoutRounded":item["withoutRounded"],
        "multiplierRound":item["multiplierRound"]
    }

def advisorsEntity(entity) -> list:
    return [advisorEntity(item) for item in entity]

    
#Best way

def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]