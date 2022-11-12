import uvicorn
from fastapi import FastAPI, Path, Query, HTTPException, status
import json
from typing import Optional
from pydantic import BaseModel

# generate random integer values
# from random import seed
# from random import randint
# seed random number generator
# seed(1)


app = FastAPI()

class Prospects(BaseModel):
    name:str
    current_age:int
    retirement_age:int
    payout_age:int
    current_gender:str
    funding_amount:float
    average_return:float
    monthly_installment:float
    with_savvly:float
    without_savvly:float
    multiplier:float

class RegisterPropects(BaseModel):
    average_return:float
    email:str
    fund:str
    fundingMethod:str
    name:str
    message:str
    initialFunding:float
    payoutAge:int
    gender:str
    emailSentAt:str
    status:bool

class UpdateProspects(BaseModel):
    name:Optional[str] = None
    current_age:Optional[int] = None
    retirement_age:Optional[int] = None
    payout_age:Optional[int] = None
    current_gender:Optional[str] = None
    funding_amount:Optional[float] = None
    average_return:Optional[float] = None
    monthly_installment:Optional[float] = None

#Empty dictionary to save Prospects
prospects = {}


#=============================
# functions to get livenumbers (livenumbers.json)
#=============================

#=============================
#Get Male liveNumber at current age
#============================= 
def male_livenumber_at_current_age(currentAge):
    with open('livenumbers.json') as livenumbersAtAge:
        data = json.load(livenumbersAtAge)
        for idx in data:
            if idx['age'] == str(currentAge):
                livenumberMaleCurrentAge = idx['liveMale']
        return livenumberMaleCurrentAge

#=============================
#Get Female liveNumber at current age
#============================= 
def female_livenumber_at_current_age(currentAge):
    with open('livenumbers.json') as livenumbersAtAge:
        data = json.load(livenumbersAtAge)
        for idx in data:
            if idx['age'] == str(currentAge):
                livenumberFemaleCurrentAge = idx['liveFemale']
        return livenumberFemaleCurrentAge

#=============================
#Get Male liveNumber at payout age
#============================= 
def male_livenumber_at_payout_age(payoutAge):
    with open('livenumbers.json') as livenumbersAtPayout:
        data  = json.load(livenumbersAtPayout)
        for idx in data:
            if idx['age'] == str(payoutAge):
                livenumberMalePayoutAge = idx['liveMale']
        return livenumberMalePayoutAge

#=============================
#Get Female liveNumber at payout age
#============================= 
def female_livenumber_at_payout_age(payoutAge):
    with open('livenumbers.json') as livenumbersAtPayout:
        data  = json.load(livenumbersAtPayout)
        for idx in data:
            if idx['age'] == str(payoutAge):
                livenumberFemalePayoutAge = idx['liveFemale']
        return livenumberFemalePayoutAge

#=============================
#Get Male COEFF liveNumber at current age and plus one
#============================= 
def male_life_coeff_livenumber_current_age(currentAge):
    with open('livenumbers.json') as coeff_livenumberAtAge:
        data = json.load(coeff_livenumberAtAge)
        for idx in data:
            if idx['age'] == str(int(currentAge)):
                valueLiveNumberAtCurrentAgeN = int(idx['liveMale'])
            
            if idx['age'] == str(int(currentAge + 1)):
                valueLiveNumberAtCurrentAgeN1 = int(idx['liveMale'])

        life_coeff_male = ((valueLiveNumberAtCurrentAgeN - valueLiveNumberAtCurrentAgeN1) / valueLiveNumberAtCurrentAgeN1)
  
        return life_coeff_male

#=============================
#Get Female COEFF liveNumber at current age and plus one
#============================= 
def female_life_coeff_livenumber_current_age(currentAge):
    with open('livenumbers.json') as coeff_livenumberAtAge:
        data = json.load(coeff_livenumberAtAge)
        for idx in data:
            if idx['age'] == str(int(currentAge)):
                valueLiveNumberAtCurrentAgeN = int(idx['liveFemale'])
            
            if idx['age'] == str(int(currentAge + 1)):
                valueLiveNumberAtCurrentAgeN1 = int(idx['liveFemale'])

        life_coeff_female = ((valueLiveNumberAtCurrentAgeN - valueLiveNumberAtCurrentAgeN1) / valueLiveNumberAtCurrentAgeN1)
  
        return life_coeff_female

#=============================
#Calculate Male COEFF liveNumber to get the installment_with at current age and minus one
#============================= 
def male_life_coeff_installment_minus_one(current_age,retirement_age,installment_with,calculated_average_return,monthly_installment):
    start = current_age + 2
    end = retirement_age
    while start <= end:
        with open('livenumbers.json') as json_data:
            data = json.load(json_data)
            for idx in data:
                if idx['age'] == str(int(start-1)):
                    valueTmpliveNumberAtCurrentN1 = int(idx['liveMale'])

                if idx['age'] == str(start):
                        valueTmpliveNumberAtCurrentN2 = int(idx['liveMale'])

            life_coeff_male = (valueTmpliveNumberAtCurrentN1 - valueTmpliveNumberAtCurrentN2) / valueTmpliveNumberAtCurrentN2
            installment_with = installment_with * (1 + calculated_average_return) * (1 + life_coeff_male) + (monthly_installment * 12) * (1 + (calculated_average_return / 2)) * (1 + (life_coeff_male / 2))

        start+=1
    return installment_with

#=============================
#Calculate Female COEFF liveNumber to get the installment_with at current age and minus one
#============================= 
def female_life_coeff_installment_minus_one(current_age,retirement_age,installment_with,calculated_average_return,monthly_installment):
    start = current_age + 2
    end = retirement_age
    while start <= end:
        with open('livenumbers.json') as json_data:
            data = json.load(json_data)
            for idx in data:
                if idx['age'] == str(int(start-1)):
                    valueTmpliveNumberAtCurrentN1 = int(idx['liveFemale'])

                if idx['age'] == str(start):
                        valueTmpliveNumberAtCurrentN2 = int(idx['liveFemale'])

            life_coeff_female = (valueTmpliveNumberAtCurrentN1 - valueTmpliveNumberAtCurrentN2) / valueTmpliveNumberAtCurrentN2
            installment_with = installment_with * (1 + calculated_average_return) * (1 + life_coeff_female) + (monthly_installment * 12) * (1 + (calculated_average_return / 2)) * (1 + (life_coeff_female / 2))

        start+=1
    return installment_with

#=============================
#Calculate Male MULTIPLIER_COEFF at retirement age and payout age
#============================= 
def male_life_multiplier_coeff_installment(payoutAge,retirementAge):
    with open('livenumbers.json') as multiplier_coeff_livenumber:
        data = json.load(multiplier_coeff_livenumber)
        for idx in data:
            if idx['age'] == str(retirementAge):
                valueLiveNumberAtRetirementAge = int(idx['liveMale'])

            if idx['age'] == str(payoutAge):
                    valueLiveNumberAtPayoutAgex = int(idx['liveMale'])

        multiplier_coeff = (valueLiveNumberAtRetirementAge - valueLiveNumberAtPayoutAgex) / valueLiveNumberAtPayoutAgex + 1

    return multiplier_coeff

#=============================
#Calculate Female MULTIPLIER_COEFF at retirement age and payout age
#============================= 
def female_life_multiplier_coeff_installment(payoutAge,retirementAge):
    with open('livenumbers.json') as multiplier_coeff_livenumber:
        data = json.load(multiplier_coeff_livenumber)
        for idx in data:
            if idx['age'] == str(retirementAge):
                valueLiveNumberAtRetirementAge = int(idx['liveFemale'])

            if idx['age'] == str(payoutAge):
                    valueLiveNumberAtPayoutAgex = int(idx['liveFemale'])

        multiplier_coeff = (valueLiveNumberAtRetirementAge - valueLiveNumberAtPayoutAgex) / valueLiveNumberAtPayoutAgex + 1

    return multiplier_coeff

#=============================
#Calculate Male_COEFF liveNumber to get the installment_with at current age and minus one with funding amount
#============================= 
def male_life_coeff_installment_minus_one_with_funding(current_age,retirement_age,installment_with,calculated_average_return,monthly_installment):
    start = current_age + 2
    end = retirement_age
    while start <= end:
        with open('livenumbers.json') as json_data:
            data = json.load(json_data)
            for idx in data:
                if idx['age'] == str(int(start-1)):
                    valueTmpliveNumberAtCurrentN1 = int(idx['liveMale'])

                if idx['age'] == str(int(start-2)):
                        valueTmpliveNumberAtCurrentN2 = int(idx['liveMale'])

            life_coeff_male = (valueTmpliveNumberAtCurrentN1 - valueTmpliveNumberAtCurrentN2) / valueTmpliveNumberAtCurrentN2
            installment_with = installment_with * (1 + calculated_average_return) * (1 + life_coeff_male) + (monthly_installment * 12) * (1 + (calculated_average_return / 2)) * (1 + (life_coeff_male / 2))

        start+=1
    return installment_with

#=============================
#API METHODS
#=============================

#=============================
#Calculator main function - Development usage
#=============================
@app.get("/calculator")
def calculator_function(*,name:Optional[str]=None,current_age:int,retirement_age:int,payout_age:int,gender:str,funding_amount:float,average_return:float,monthly_installment:float):
    #For development usage
    user_name = name
    user_age = current_age
    user_retirement_age = retirement_age
    user_payout_age = payout_age
    user_gender = gender
    user_funding_amount = funding_amount
    user_average_return = average_return
    user_monthly_installment = monthly_installment

    if monthly_installment == 0:
        if funding_amount == 0:

            withRounded = 0.0
            withoutRounded = 0.0
            multiplierRound = 0

            return {
                "name":user_name, 
                "current_age":user_age,
                "retirement_age":user_retirement_age,
                "payout_age":user_payout_age,
                "current_gender":user_gender,
                "funding_amount":user_funding_amount,
                "average_return":user_average_return,
                "monthly_installment":user_monthly_installment,
                "with_savvly":withRounded,
                "without_savvly":withoutRounded,
                "multiplier":multiplierRound
                }

            # print("Data-info":"funding_amount == 0")
        else:

            multiplier = 0
            withMultiplier = 0
            withoutMultiplier = 0
            calculated_average_return = float(average_return)/100

            withoutMultiplier = funding_amount * ((1 + calculated_average_return)**(payout_age - current_age))

            if gender == 'Male':
                multiplier = (int(male_livenumber_at_current_age(current_age)) - int(male_livenumber_at_payout_age(payout_age))) / int(male_livenumber_at_payout_age(payout_age)) + 1
                withMultiplier = withoutMultiplier * multiplier
            else:
                multiplier = (int(female_livenumber_at_current_age(current_age)) - int(female_livenumber_at_payout_age(payout_age))) / int(female_livenumber_at_payout_age(payout_age)) + 1
                withMultiplier = withoutMultiplier * multiplier

            withMultiplier = withoutMultiplier * multiplier

            withRounded = round(withMultiplier,0)            
            withoutRounded = round(withoutMultiplier,0)
            multiplierRound = format(multiplier, ".2f")
            
            return {
                "name":user_name, 
                "current_age":user_age,
                "retirement_age":user_retirement_age,
                "payout_age":user_payout_age,
                "current_gender":user_gender,
                "funding_amount":user_funding_amount,
                "average_return":user_average_return,
                "monthly_installment":user_monthly_installment,
                "with_savvly":withRounded,
                "without_savvly":withoutRounded,
                "multiplier":multiplierRound
                }
            # print("Data-info":"funding_amount != 0")

        # print("Data":"monthly_installment == 0")
    else:
        multiplier = 0
        withMultiplier = 0
        withoutMultiplier = 0
        installment_without = 0
        calculated_average_return = float(average_return)/100

        withoutMultiplier = funding_amount * ((1 + calculated_average_return)**(payout_age - current_age))
        installment_without = (monthly_installment * 12) * (1 + (calculated_average_return / 2))
        
        if funding_amount == 0:
            starts = current_age + 2
            ends = retirement_age
            while starts <= ends:
                installment_without = (installment_without * (1 + calculated_average_return)) + (monthly_installment * 12) * (1 + (calculated_average_return / 2))
                starts+=1
            
            installment_without = installment_without * ((1 + calculated_average_return)**(payout_age - retirement_age))
            
            if gender == 'Male':
                male_multiplier = format(((int(male_livenumber_at_current_age(current_age)) - int(male_livenumber_at_payout_age(payout_age))) / int(male_livenumber_at_payout_age(payout_age)) + 1), ".2f")
                withMultiplier = float(male_multiplier) * withoutMultiplier

                life_coeff_male = 0
                life_coeff_male = float(male_life_coeff_livenumber_current_age(current_age))
                installment_with = (monthly_installment * 12) * (1 + calculated_average_return / 2) * (1 + life_coeff_male / 2)

                installment_with = float(male_life_coeff_installment_minus_one(current_age,retirement_age,installment_with,calculated_average_return,monthly_installment))

                multiplier_coeff = 0
                multiplier_coeff = float(male_life_multiplier_coeff_installment(payout_age,retirement_age))

                installment_with = multiplier_coeff * installment_with *((1 + calculated_average_return)**(payout_age - 65))
                # print("Data":"gender == Male")
            else:
                female_multiplier = format(((int(female_livenumber_at_current_age(current_age)) - int(female_livenumber_at_payout_age(payout_age))) / int(female_livenumber_at_payout_age(payout_age)) + 1), ".2f")
                withMultiplier = float(female_multiplier) * withoutMultiplier

                life_coeff_female = 0
                life_coeff_female = float(female_life_coeff_livenumber_current_age(current_age))
                installment_with = (monthly_installment * 12) * (1 + calculated_average_return / 2) * (1 + life_coeff_female / 2)

                installment_with = float(female_life_coeff_installment_minus_one(current_age,retirement_age,installment_with,calculated_average_return,monthly_installment))

                multiplier_coeff = 0
                multiplier_coeff = float(female_life_multiplier_coeff_installment(payout_age,retirement_age))

                installment_with = multiplier_coeff * installment_with *((1 + calculated_average_return)**(payout_age - 65))
                # print("Data":"gender == Female")
            
            multiplier = installment_with / installment_without;

            withRounded = round(installment_with,0)            
            withoutRounded = round(installment_without,0)
            multiplierRound = format(multiplier, ".2f")

            return {
                "name":user_name, 
                "current_age":user_age,
                "retirement_age":user_retirement_age,
                "payout_age":user_payout_age,
                "current_gender":user_gender,
                "funding_amount":user_funding_amount,
                "average_return":user_average_return,
                "monthly_installment":user_monthly_installment,
                "with_savvly":withRounded,
                "without_savvly":withoutRounded,
                "multiplier":multiplierRound
                }
            # print("Data":"funding_amount == 0")
        else:

            starts = current_age + 2
            ends = retirement_age
            while starts <= ends:
                installment_without = (installment_without * (1 + calculated_average_return)) + (monthly_installment * 12) * (1 + (calculated_average_return / 2))
                starts+=1            

            installment_without = installment_without * ((1 + calculated_average_return)**(payout_age - retirement_age))
            final_without_multiplier = withoutMultiplier + installment_without

            if gender == 'Male':

                male_multiplier = (int(male_livenumber_at_current_age(current_age)) - int(male_livenumber_at_payout_age(payout_age))) / int(male_livenumber_at_payout_age(payout_age)) + 1
                withMultiplier = male_multiplier * withoutMultiplier

                life_coeff_male = 0
                life_coeff_male = float(male_life_coeff_livenumber_current_age(current_age))
                installment_with = (monthly_installment * 12) * (1 + calculated_average_return / 2) * (1 + life_coeff_male / 2)
                
                installment_with = float(male_life_coeff_installment_minus_one(current_age,retirement_age,installment_with,calculated_average_return,monthly_installment))

                multiplier_coeff = 0
                multiplier_coeff = float(male_life_multiplier_coeff_installment(payout_age,retirement_age))
                installment_with = multiplier_coeff * installment_with * ((1 + calculated_average_return)**(payout_age - 65))
                final_withMultiplier = withMultiplier + installment_with
                multiplier = final_withMultiplier / final_without_multiplier

                withRounded = round(final_withMultiplier,0)            
                withoutRounded = round(final_without_multiplier,0)
                multiplierRound = format(multiplier, ".2f")

                return {
                    "name":user_name, 
                    "current_age":user_age,
                    "retirement_age":user_retirement_age,
                    "payout_age":user_payout_age,
                    "current_gender":user_gender,
                    "funding_amount":user_funding_amount,
                    "average_return":user_average_return,
                    "monthly_installment":user_monthly_installment,
                    "with_savvly":withRounded,
                    "without_savvly":withoutRounded,
                    "multiplier":multiplierRound
                    }
            else:

                female_multiplier = (int(female_livenumber_at_current_age(current_age)) - int(female_livenumber_at_payout_age(payout_age))) / int(female_livenumber_at_payout_age(payout_age)) + 1
                withMultiplier = female_multiplier * withoutMultiplier

                life_coeff_female = 0
                life_coeff_female = float(female_life_coeff_livenumber_current_age(current_age))
                installment_with = (monthly_installment * 12) * (1 + calculated_average_return / 2) * (1 + life_coeff_female / 2)
                
                installment_with = float(female_life_coeff_installment_minus_one(current_age,retirement_age,installment_with,calculated_average_return,monthly_installment))

                multiplier_coeff = 0
                multiplier_coeff = float(female_life_multiplier_coeff_installment(payout_age,retirement_age))
                installment_with = multiplier_coeff * installment_with * ((1 + calculated_average_return)**(payout_age - 65))
                final_withMultiplier = withMultiplier + installment_with
                multiplier = final_withMultiplier / final_without_multiplier

                withRounded = round(final_withMultiplier,0)            
                withoutRounded = round(final_without_multiplier,0)
                multiplierRound = format(multiplier, ".2f")

                return {
                    "name":user_name, 
                    "current_age":user_age,
                    "retirement_age":user_retirement_age,
                    "payout_age":user_payout_age,
                    "current_gender":user_gender,
                    "funding_amount":user_funding_amount,
                    "average_return":user_average_return,
                    "monthly_installment":user_monthly_installment,
                    "with_savvly":withRounded,
                    "without_savvly":withoutRounded,
                    "multiplier":multiplierRound
                    }     

#=============================
#Prospect Planner Calculator
#=============================
@app.get("/prospect-planner")
def prospect_planner_calculator(*,gender:str,current_age:int,average_return:float,funding_amount:float,payout_age:int):

    # generate some integers as users ID
    # for _ in range(9000):
    #     guid = randint(0, 9001)
    prospect_planner = {}
    if funding_amount == 0:

        withRounded = 0.0
        withoutRounded = 0.0
        multiplierRound = 0

        payout_ages = [payout_age,80,85,90]

        for i in payout_ages:

            prospect_planner[i] =  {
                "gender":gender,
                "current_age":current_age, 
                "payout_age":i,
                "funding_amount":funding_amount,
                "average_return":average_return,
                "with_savvly":withRounded,
                "without_savvly":withoutRounded,
                "multiplier":multiplierRound
            }

        return prospect_planner

        # print("Data-info":"funding_amount == 0")
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
                "payout_age":i,
                "funding_amount":funding_amount,
                "average_return":average_return,
                "with_savvly":withRounded,
                "without_savvly":withoutRounded,
                "multiplier":multiplierRound
            }

        return prospect_planner   

      #=============================
#Prospect Planner for new Estimator
#=============================
@app.get("/simulate-prospect-planner")
def simulation_advisor1_preview(*,gender:str,current_age:int,average_return:float,funding_amount:float,payout_age:int):
    if funding_amount == 0:

        withRounded = 0.0
        withoutRounded = 0.0
        multiplierRound = 0

        prospect_planner = []
        temp_payout_ages = ()

        payout_ages = (payout_age,80,85,90)

        for i in payout_ages:
            temp_payout_ages += (i,)

        for x in temp_payout_ages:
            prospect_planner.append(
                (x, {"gender": gender,"current_age":current_age,"average_return":average_return,"funding_amount":funding_amount,"payout_age":x,"withRounded":withRounded,"withoutRounded":withoutRounded,"multiplierRound":multiplierRound})
            )
               
        return prospect_planner

    else:
        prospect_planner = []
        temp_payout_ages = ()

        payout_ages = (payout_age,80,85,90)

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

            temp_payout_ages += (i,)

            prospect_planner.append(
                (i, {"gender": gender,"current_age":current_age,"average_return":average_return,"funding_amount":funding_amount,"payout_age":i,"withRounded":withRounded,"withoutRounded":withoutRounded,"multiplierRound":multiplierRound})
            )

        return prospect_planner  

#Get Prospects
#=============================
@app.get("/prospects")
def get_all_prospects():
    for prospect in prospects:
        return prospect
    
    raise HTTPException(status_code=404,detail="No Propects data found.")

#Get Prospects by {uid}
#=============================
@app.get("/prospects/{guid}")
def get_prospect_information_by_id(*,guid:int = Path(None,description="Prospect ID to get information")):
    if guid not in prospects:
        raise HTTPException(status_code=404,detail="Prospect ID not found.")

    return prospects[guid]

#Get Prospects by {name}
#=============================
@app.get("/prospect-by-name")
def get_prospect_information_by_name(name: Optional[str] = None):
    for guid in prospects:
        if prospects[guid].name == name:
            return prospects[guid]

        raise HTTPException(status_code=404,detail="Prospect Name not found.")

#Create Prospects
#=============================
@app.post("/create-prospect/{guid}")
def create_prospect(guid:int,prospect:Prospects):
    if guid in prospects:
        raise HTTPException(status_code=400,detail="Prospect ID already exists.")
        
    prospects[guid] = prospect

    return prospects[guid]

#Update a Prospect information
#=============================
@app.put("/prospect-edit/{guid}")
def update_prospect_information(guid:int, prospect:UpdateProspects):
    if guid not in prospects:
        raise HTTPException(status_code=404,detail="Prospect Id doesn't exists.")
    
    if prospect.name != None:
       prospects[guid].name = prospect.name
    if prospect.current_age != None:
       prospects[guid].current_age = prospect.current_age
    if prospect.retirement_age != None:
       prospects[guid].retirement_age = prospect.retirement_age
    if prospect.payout_age != None:
       prospects[guid].payout_age = prospect.payout_age
    if prospect.current_gender != None:
       prospects[guid].current_gender = prospect.current_gender
    if prospect.funding_amount != None:
       prospects[guid].funding_amount = prospect.funding_amount
    if prospect.average_return != None:
       prospects[guid].average_return = prospect.average_return
    if prospect.monthly_installment != None:
       prospects[guid].monthly_installment = prospect.monthly_installment

    #With_savvly, without_savvly & multiplier pending
    
    return prospects[guid]

#Delete a Prospect information
#=============================
@app.delete("/prospect-delete")
def delete_prospect_id(guid:int = Query(...,description="Prospect ID to be deleted")):
    if guid not in prospects:
        raise HTTPException(status_code=404,detail="Prospect Id doesn't exists.")
    del prospects[guid]

    return {"Success":"Prospect deleted!"}

# A minimal app to demonstrate the get request 
@app.get("/", tags=['root'])
async def root() -> dict:
    return {"Ping": "Pong"}

@app.on_event("startup")
def save_openapi_json():
    openapi_data = app.openapi()
    # Change "openapi.json" to desired filename
    with open("simulator_functions.json", "w") as file:
        json.dump(openapi_data, file)

if __name__ == "__main__":
    uvicorn.run("api:app")
