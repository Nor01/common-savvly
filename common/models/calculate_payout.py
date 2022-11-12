from common.models.simulation_mat import *


# ---------------------------------------------------------------------------------------------
# Calculate Payout for a specified age, gender and amount
# Returns: Three float numbers
# with_savvly   - The payout with Savvly
# without_savvly - The payout without Savvly
# multiplier - The multiplier
# returns 0,0,0 if the ages are out of the matrix ranges
# ---------------------------------------------------------------------------------------------

# 1. Amount without Savvly = Investment amount * ( 1 + Annual return ) ^ (Payout age – current age)
# [this is basically the old formula for the Without Savvly]
# 2. Amount with Savvly = Amount without Savvly * MULTIPLE
#
# MULTIPLE :
# In the Excel file the multiple is identified by the intersection between the current age row and the
# payout age column. For instance, if a 50-year-old person select a payout age of 85 the MULTIPLE is the
# intersection of the row of 50 years with the column of 85 years. Obviously there is a matrix for men and
# a matrix for women
# This is a much easier formula and (more precise… we got the multiple from matlab simulations)

def calculate_payout(gender: str, current_age: int, average_return: float, funding_amount: float, payout_age: int) -> (
        float, float, float):
    with_savvly = without_savvly = multiplier = 0

    if gender.startswith("M"):
        mat = Mat_M
    elif gender.startswith("F"):
        mat = Mat_F
    else:
        return 0, 0, 0
    rows = len(mat)
    cols = len(mat[0])
    row = col = -1

    # find multiplier
    # find row for age
    for i in range(rows):
        if mat[i][0] == current_age:
            row = i
            break

    if row == -1:
        print(f"did not found current age {current_age} in Matrix")
        return 0, 0, 0

    # find col for payout age
    for j in range(cols):
        if mat[0][j] == payout_age:
            col = j
            break
    if col == -1:
        print(f"did not found payout {payout_age} in Matrix")
        return 0, 0, 0
    multiplier = mat[row][col]

    # 1. Amount without Savvly = Investment amount * ( 1.0 + Annual return ) ^ (Payout age – current age)
    # [this is basically the old formula for the Without Savvly]
    # 2. Amount with Savvly = Amount without Savvly * MULTIPLE

    without_savvly = funding_amount * (1 + average_return/100.0) ** (payout_age - current_age)
    with_savvly = without_savvly * multiplier

    return with_savvly, without_savvly, multiplier
