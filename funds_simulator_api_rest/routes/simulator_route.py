from fastapi import APIRouter
from configuration.database_connection import client 
from models.simulator_model import Advisor,UpdateAdvisor 
from schemas.simulator_schema import serializeDict, serializeList
from functions.simulator_functions import male_livenumber_at_current_age, male_livenumber_at_payout_age, female_livenumber_at_current_age, female_livenumber_at_payout_age


from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from bson.json_util import dumps
from typing import Optional

import json


api_router = APIRouter()


#Prospect planner object to simulation
prospect_planner={}

@api_router.get("/", tags=['root'])
async def root() -> dict:
    return {"Ping": "Pong"}

#=============================
#Prospect Planner Calculator
#=============================

@api_router.get('/show-all-prospects', tags=['Prospect Planner'])
async def find_all_prospects():
    return serializeList(client.simulatordb.simulator_advisor1.find({}))

@api_router.get('/find-prospect-by-id/{id}', tags=['Prospect Planner'])
async def find_one_prospect(id):
    return serializeDict(client.simulatordb.simulator_advisor1.find_one({"_id":ObjectId(id)}))

@api_router.post('/create-prospect', tags=['Prospect Planner'])
async def create_prospect(advisor: Advisor):
    client.simulatordb.simulator_advisor1.insert_one(dict(advisor))
    return serializeList(client.simulatordb.simulator_advisor1.find())

@api_router.put('/update-prospect/{id}', tags=['Prospect Planner'])
async def update_prospect(id,uadvisor: UpdateAdvisor):
    client.simulatordb.simulator_advisor1.find_one_and_update({"_id":ObjectId(id)},{
        "$set":uadvisor.dict(exclude_unset=True)
    })
    return serializeDict(client.simulatordb.simulator_advisor1.find_one({"_id":ObjectId(id)}))

@api_router.delete('/delete-prospect/{id}', tags=['Prospect Planner'])
async def delete_prospect(id,advisor: Advisor):
    return serializeDict(client.simulatordb.simulator_advisor1.find_one_and_delete({"_id":ObjectId(id)}))

@api_router.get("/simulate-prospect-planner", tags=['Simulations'])
def simulation_advisor1_preview(*,gender:str,current_age:int,average_return:float,funding_amount:float,payout_age:int):

    if funding_amount == 0:

        withRounded = 0.0
        withoutRounded = 0.0
        multiplierRound = 0

        payout_ages = [payout_age,80,85,90]

        for i in payout_ages:

            prospect_planner[i] =  {
                "gender":gender,
                "current_age":current_age,
                "average_return":average_return,
                "funding_amount":funding_amount,
                "payout_age":i,
                "withRounded":withRounded,
                "withoutRounded":withoutRounded,
                "multiplierRound":multiplierRound
            }

        return prospect_planner

    else:

        payout_ages = [payout_age,80,85,90]

        for i in payout_ages:

            multiplier = 0
            withMultiplier = 0
            withoutMultiplier = 0
            calculated_average_return = float(average_return)/100

            withoutMultiplier = funding_amount * ((1 + calculated_average_return)**(i - current_age))

            if gender == 'Male':
                multiplier = (int(male_livenumber_at_current_age(current_age)) - int(male_livenumber_at_payout_age(i))) / int(male_livenumber_at_payout_age(i)) + 1
                withMultiplier = withoutMultiplier * multiplier
            else:
                multiplier = (int(female_livenumber_at_current_age(current_age)) - int(female_livenumber_at_payout_age(i))) / int(female_livenumber_at_payout_age(i)) + 1
                withMultiplier = withoutMultiplier * multiplier

            withMultiplier = withoutMultiplier * multiplier

            withRounded = round(withMultiplier,0)            
            withoutRounded = round(withoutMultiplier,0)
            multiplierRound = format(multiplier, ".2f")

            prospect_planner[i] =  {
                "gender":gender,
                "current_age":current_age,
                "average_return":average_return,
                "funding_amount":funding_amount,
                "payout_age":i,
                "withRounded":withRounded,
                "withoutRounded":withoutRounded,
                "multiplierRound":multiplierRound
            }

        return prospect_planner  

@api_router.get("/new-simulate-prospect-planner", tags=['Simulations'])
def simulation2_advisor1_preview(*,gender:str,current_age:int,average_return:float,funding_amount:float,payout_age:int):
    return {}

# @api_router.get("/all-prospect-planner")
# def find_all_advisors():
#     simulatordb = client.simulatordb #database instance
#     collection = simulatordb.simulator_advisor1 #database.collection_name
#     all_advisors = collection.find({})

#     # for advisor in all_advisors:
#     list_advisors = list(all_advisors)
#     json_data = dumps(list_advisors, indent = 2)

#     with open('all-prospect-planner.json', 'w') as file:
#         file.write(json_data)
    
#     with open('all-prospect-planner.json') as prospescts:
#         data = json.load(prospescts)

#         return data

    # return json_data

# @api_router.get("/prospect-planner/{oid}")
# def find_advisor_by_id(*,oid:str):

#     id = oid
#     simulatordb = client.simulatordb #database instance
#     collection = simulatordb.simulator_advisor1 #database.collection_name
#     all_advisors = collection.find_one({'_id':ObjectId(id)})

#     json_data = dumps(all_advisors, indent = 2)
    
#     with open('prospect-planner-id.json', 'w') as file:
#         file.write(json_data)
    
#     with open('prospect-planner-id.json') as prospescts:
#         data = json.load(prospescts)

#         return data

    # return json_data

# @api_router.post("/prospect-planner")
# def insert_advisor1_preview(*,gender:str,current_age:int,average_return:float,funding_amount:float,payout_age:int,withRounded:Optional[float]=None,withoutRounded:Optional[float]=None,multiplierRound:Optional[float]=None):
    
#     simulatordb = client.simulatordb #database instance
#     collection = simulatordb.simulator_advisor1 #database.collection_name

#     info_advisor1 = {
#         "gender":gender,
#         "current_age":current_age,
#         "average_return":average_return,
#         "funding_amount":funding_amount,
#         "payout_age":payout_age,
#         "with_savvly":withRounded,
#         "without_savvly":withoutRounded,
#         "multiplier":multiplierRound
#     }

#     collection.insert_one(info_advisor1)

#     return {"Message":"Successful registration"}





