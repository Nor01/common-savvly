import json
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
#Get Female liveNumber at payout age
#============================= 
def female_livenumber_at_payout_age(payoutAge):
    with open('livenumbers.json') as livenumbersAtPayout:
        data  = json.load(livenumbersAtPayout)
        for idx in data:
            if idx['age'] == str(payoutAge):
                livenumberFemalePayoutAge = idx['liveFemale']
        return livenumberFemalePayoutAge