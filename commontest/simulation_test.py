from common.models.calculate_payout import calculate_payout


def test_pay(gender, current_age, payout_age, average_return, funding_amount):
    with_savvly, without_savvly, mult = calculate_payout(gender=gender, current_age=current_age, payout_age=payout_age,
                                                         average_return=average_return, funding_amount=funding_amount)

    return f"gender={gender}, current_age={current_age}, return={average_return}%, payout_age={payout_age}, funding=${funding_amount}, without=${without_savvly:.0f}, with=${with_savvly:.0f}, mult={mult:.2f}"


# 1)
# Input:
# Male
# Initial age: 50 years
# Payout Age: 80 years
# Average market return: 6%
# Funding amount: $10,000
# Output:
# Without Savvly:  $10,000*1.06^(80-50) =  $57,435
# With Savvly:   $57,435 * 1.75163058486469 = $100,605
#
print(test_pay("M", current_age=50, payout_age=80, average_return=6, funding_amount=10000))

#
# 2)
# Input:
# Male
# Initial age: 55 years
# Payout Age: 87 years
# Average market return: 6%
# Funding amount: $25,000
# Output:
# Without Savvly:  $161,335
# With Savvly:   $469,956
#
print(test_pay("M", current_age=55, payout_age=87, average_return=6, funding_amount=25000))

# 3)
# Input:
# Female
# Initial age: 68 years
# Payout Age: 94 years
# Average market return: 6%
# Funding amount: $10,000
# Output:
# Without Savvly:  $45,494
# With Savvly:   $222,310
#
#
print(test_pay("F", current_age=68, payout_age=94, average_return=6, funding_amount=10000))
# 4)
# Input:
# Female
# Initial age: 52 years
# Payout Age: 84 years
# Average market return: 6%
# Funding amount: $25,000
# Output:
# Without Savvly:  $161,335
# With Savvly:   $280,286
#
#
print(test_pay("F", current_age=52, payout_age=84, average_return=6, funding_amount=25000))

### addditional tests
print(test_pay("M", current_age=50, payout_age=91, average_return=0.04, funding_amount=1000))

print(test_pay("Male", current_age=50, payout_age=75, average_return=0.04, funding_amount=1000))

print(test_pay("Female", current_age=50, payout_age=75, average_return=0.04, funding_amount=1000))
