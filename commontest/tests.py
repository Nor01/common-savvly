from common.controllers.deaduser import *
from common.controllers.dividend import *
from common.controllers.fee import *
from common.controllers.firmvaluemarket import *
from common.controllers.moneytransfer import *
from commontest import *  # Common to all tests in nthis repository


# -------------------------------------------------------------------------
# Let the user to select a user
# -------------------------------------------------------------------------
def test_select_user():
    global gselected_user
    num_users = len(guser_list)
    gselected_user = test_get_integer_input(f"Select a user between 0 to %d: " % (num_users - 1), num_users - 1)


# -------------------------------------------------------------------------
# Delete the tables
# -------------------------------------------------------------------------
def test_delete_tables():
    dbh = Dbhandles.get_instance()
    dbh.delete_all_tables()


# -------------------------------------------------------------------------
# Create a list of users
# -------------------------------------------------------------------------
def test_create_users():
    dbh = Dbhandles.get_instance()
    usertable = dbh.get_usertables()

    for userinfo in guser_list:
        idx = userinfo[0]
        user_info = userinfo[1]
        parent = userinfo[2]
        if not usertable.add_new_user(idx, user_info):
            break
        usertable.set_statusflag_active(idx)
        if parent is not None:
            usertable.set_parentid(idx, parent)


# -------------------------------------------------------------------------
# Deposit money to the user's account
# -------------------------------------------------------------------------
def test_deposit_money():
    moneytr = MoneyTransfer()
    for userinfo in guser_list:
        idx = userinfo[0]
        amount = userinfo[3]  # Deposit
        if amount == 0:
            continue
        print("Deposing %d to account of %s @share-price: %d" % (amount, idx, gshare_price))
        moneytr = MoneyTransfer()
        moneytr.deposit_money(idx, amount, "book_11h5znvq9ptmmn")  # This is done by the user
        moneytr.set_transfer_complete(idx)  # This is done by bank-adaptor
        moneytr.set_purchase_pending(idx)  # This is done by trader
        moneytr.set_purchase_complete(idx, gshare_price)  # This is done by trader


# -------------------------------------------------------------------------
# Simulate: Deposit money  - User's side
# -------------------------------------------------------------------------
def test_simulate_deposit_by_user():
    moneytr = MoneyTransfer()
    userinfo = guser_list[gselected_user]
    idx = userinfo[0]
    amount = userinfo[3]  # Deposit
    print("Deposing %d to account of %s @share-price: %d" % (amount, idx, gshare_price))
    moneytr.deposit_money(idx, amount, "book_11h5znvq9ptmmn")  # This is done by the user


# -------------------------------------------------------------------------
# Simulate: Deposit money - bankAdaptor's side
# -------------------------------------------------------------------------
def test_simulate_deposit_by_bankadaptor():
    moneytr = MoneyTransfer()
    userinfo = guser_list[gselected_user]
    idx = userinfo[0]
    moneytr.set_transfer_complete(idx)  # This is done by bank-adaptor


# -------------------------------------------------------------------------
# Simulate: Deposit money - Trader's side
# -------------------------------------------------------------------------
def test_simulate_deposit_by_trader():
    moneytr = MoneyTransfer()
    userinfo = guser_list[gselected_user]
    idx = userinfo[0]
    moneytr.set_purchase_pending(idx)  # This is done by trader
    moneytr.set_purchase_complete(idx, gshare_price)  # This is done by trader


# -------------------------------------------------------------------------
# withdraw money to the user's account
# -------------------------------------------------------------------------
def test_withdraw_money():
    moneytr = MoneyTransfer()
    for userinfo in guser_list:
        idx = userinfo[0]
        amount = userinfo[4]  # Withdraw
        if amount == 0:
            continue
        print("Withdrawing %d from account of %s @share-price: %d" % (amount, idx, gshare_price))
        moneytr.withdrawal_money(idx, amount)  # This is done by the user
        moneytr.set_withdrawal_pending(idx)  # This is done by bank-adaptor
        moneytr.set_withdrawal_complete(idx, gshare_price)  # This is done by trader


# -------------------------------------------------------------------------
# Deduct a fee
# -------------------------------------------------------------------------
def test_deduct_fee():
    fee = Fee()
    for userinfo in guser_list:
        idx = userinfo[0]
        amount = userinfo[4]  # Withdraw
        if amount == 0:
            continue
        fee.deduct_management_fee(idx, (-1.0) * gshare_price, gshare_price)


# -------------------------------------------------------------------------
# Grant dividend
# -------------------------------------------------------------------------
def test_add_dividend():
    dividend = Dividend()
    for userinfo in guser_list:
        idx = userinfo[0]
        amount = userinfo[4]  # Withdraw
        if amount == 0:
            continue
        dividend.add_dividend(idx, 3.0 * gshare_price, gshare_price)


# -------------------------------------------------------------------------
# Withdrawal: Withdrawal money  - User's side
# -------------------------------------------------------------------------
def test_simulate_withdrawal_by_user():
    moneytr = MoneyTransfer()
    userinfo = guser_list[gselected_user]
    idx = userinfo[0]
    amount = userinfo[4]  # Withdraw
    print("Withdrawing %d from account of %s @share-price: %d" % (amount, idx, gshare_price))
    moneytr.withdrawal_money(idx, amount)  # This is done by the user


# -------------------------------------------------------------------------
# Withdrawal: Withdrawal money - bankAdaptor's side
# -------------------------------------------------------------------------
def test_simulate_withdrawal_by_bankadaptor():
    moneytr = MoneyTransfer()
    userinfo = guser_list[gselected_user]
    idx = userinfo[0]
    moneytr.set_withdrawal_pending(idx)  # This is done by bank-adaptor


# -------------------------------------------------------------------------
# Withdrawal: Withdrawal money - Trader's side
# -------------------------------------------------------------------------
def test_simulate_withdrawal_by_trader():
    moneytr = MoneyTransfer()
    userinfo = guser_list[gselected_user]
    idx = userinfo[0]
    moneytr.set_withdrawal_complete(idx, gshare_price)  # This is done by trader


# ----------------------------------------
# Update Daily Table
# ----------------------------------------
def test_update_daily_table():
    import random
    fmv = FirmMarketValue()
    share_cost = random.uniform(gshare_price - 2.0, gshare_price + 2.0)
    total_portfolio = random.uniform(1000000.1, 1001000.1)
    fmv.update_today_values(share_cost, total_portfolio)


# -------------------------------------------------------------------------
# Prints users Totals
# -------------------------------------------------------------------------
def test_print_users_totals():
    dbh = Dbhandles.get_instance()
    usertable = dbh.get_usertables()
    totals = usertable.get_all_totals()
    print(totals)


# -------------------------------------------------------------------------
# Prints users data
# -------------------------------------------------------------------------
def test_print_users():
    dbh = Dbhandles.get_instance()
    usertable = dbh.get_usertables()
    for userinfo in guser_list:
        idx = userinfo[0]
        user_values = usertable.get_all_values(idx)
        print(user_values)


# -------------------------------------------------------------------------
# Prints the selected user
# -------------------------------------------------------------------------
def test_print_selected_user():
    dbh = Dbhandles.get_instance()
    usertable = dbh.get_usertables()
    userinfo = guser_list[gselected_user]
    idx = userinfo[0]
    user_values = usertable.get_all_values(idx)
    print(user_values)


# -------------------------------------------------------------------------
# Prints all status flags
# -------------------------------------------------------------------------
def test_print_status_flags():
    moneytr = MoneyTransfer()

    print("Transfer:")
    status_list = moneytr.get_all_statusflag_transfer()
    if status_list: print(status_list)

    print("Transfer Complete:")
    status_list = moneytr.get_all_statusflag_transfer_complete()
    if status_list: print(status_list)

    print("Purchase Pending:")
    status_list = moneytr.get_all_statusflag_purchase_pending()
    if status_list: print(status_list)

    print("Withdrawal:")
    status_list = moneytr.get_all_statusflag_withdrawal()
    if status_list: print(status_list)

    print("Withdrawal Pending:")
    status_list = moneytr.get_all_statusflag_withdrawal_pending()
    if status_list: print(status_list)

    dbh = Dbhandles.get_instance()
    usertable = dbh.get_usertables()
    print("Active:")
    status_list = usertable.get_all_statusflag_active()
    if status_list: print(status_list)
    print("Pending:")
    status_list = usertable.get_all_statusflag_pending()
    if status_list: print(status_list)
    print("Deceased:")
    status_list = usertable.get_all_statusflag_deceased()
    if status_list: print(status_list)
    print("Closed:")
    status_list = usertable.get_all_statusflag_closed()
    if status_list: print(status_list)
    print("Cancel:")
    status_list = usertable.get_all_statusflag_transfer_cancel()
    if status_list: print(status_list)


# -------------------------------------------------------------------------
# Show parents info
# -------------------------------------------------------------------------
def test_print_parents_info():
    dbh = Dbhandles.get_instance()
    usertable = dbh.get_usertables()
    parent_list = usertable.get_all_parentids()
    orphan_list = usertable.get_all_orphan_users()
    children1 = usertable.get_my_children("advisor1")
    children2 = usertable.get_my_children("advisor2")
    print("All users and parents:" + str(parent_list))
    print("Users with no parent" + str(orphan_list))
    print("Children of advisor1:" + str(children1))
    print("Children of advisor2:" + str(children2))


# -------------------------------------------------------------------------
# Print Death Probabilty
# -------------------------------------------------------------------------
def test_print_death_probability():
    dbh = Dbhandles.get_instance()
    usertable = dbh.get_usertables()

    for userinfo in guser_list:
        idx = userinfo[0]
        sex = userinfo[1]['sex']
        age = usertable.get_age(idx)
        dp = dp_get_probability(age, sex)
        print("User:%s  Sex:%s  Age=%d DP=%f" % (idx, sex, age, dp))


# -------------------------------------------------------------------------
# Print users transactions
# -------------------------------------------------------------------------
def test_print_user_transactions():
    dbh = Dbhandles.get_instance()
    trtable = dbh.get_transactiontable()

    for userinfo in guser_list:
        idx = userinfo[0]
        user_amounts = trtable.get_user_values(idx)
        user_total = trtable.get_total_user_amounts(idx)
        user_shares = trtable.get_total_user_shares(idx)
        print(idx)
        print("---------------")
        print("   Amounts: " + str(user_amounts))
        print("   Total: " + str(user_total))
        print("   Shares: " + str(user_shares))


# -------------------------------------------------------------------------
# Print transactions table
# -------------------------------------------------------------------------
def test_print_transactions_table():
    dbh = Dbhandles.get_instance()
    trtable = dbh.get_transactiontable()
    for userinfo in guser_list:
        idx = userinfo[0]
        transactions = trtable.get_all_values(idx)
        print(transactions)

    # dbh = Dbhandles.get_instance()
    # trtable = dbh.get_transactiontable()
    # tr_diag = trtable.get_diag()
    # tr_tables = trtable.get_all_tables()
    # tr_keylist = trtable.get_idx_list()
    # tr_amounts = trtable.get_all_amounts()
    #
    # print("Transactions Diag")
    # print("---------------------------")
    # print(tr_diag)
    #
    # print("Transactions Tables")
    # print("---------------------------")
    # print(tr_tables)
    #
    # print("Transactions Key List")
    # print("---------------------------")
    # print(tr_keylist)
    #
    # print("Transactions Amounts")
    # print("---------------------------")
    # print(tr_amounts)


# -------------------------------------------------------------------------
# Print Daily Table
# -------------------------------------------------------------------------
def test_print_daily_table():
    dbh = Dbhandles.get_instance()
    dailytable = dbh.get_dailydatatable()
    today_values = dailytable.get_today_values()
    all_values = dailytable.get_all_portfolio_values()

    print("All Values")
    print("---------------------------")
    print(all_values)

    print("Today Values")
    print("---------------------------")
    print(today_values)

    share_cost = dailytable.get_share_cost()
    total_portfolio = dailytable.get_tot_portfolio()
    print("ShareCost= " + str(share_cost))
    print("TotalPortfolio= " + str(total_portfolio))


# -------------------------------------------------------------------------
# Print Inheritance Table
# -------------------------------------------------------------------------
def test_print_inheritance_table():
    dbh = Dbhandles.get_instance()
    inheritance = dbh.get_inheritedtable()
    all_values = inheritance.get_all_tables()
    print(all_values)


# -------------------------------------------------------------------------
# Simulate FMV docker (update all user's FMV)
# -------------------------------------------------------------------------
def test_update_all_users_fmv():
    fmv = FirmMarketValue()
    fmv.get_and_update()


# -------------------------------------------------------------------------
# Print the FMV of all users
# -------------------------------------------------------------------------
def test_print_all_users_fmv():
    dbh = Dbhandles.get_instance()
    usertable = dbh.get_usertables()
    fmvs = usertable.get_all_fmvs()
    print("User's FMV")
    print("-----------")
    print(fmvs)


# -------------------------------------------------------------------------
# Set User7 as dead
# -------------------------------------------------------------------------
def test_set_user7_dead():
    dbh = Dbhandles.get_instance()
    usertable = dbh.get_usertables()
    user_info = guser_list[3]
    usertable.set_statusflag_deceased(user_info[0])


# -------------------------------------------------------------------------
# Print the sum of DPs and shares
# -------------------------------------------------------------------------
def test_calculate_dead_shares_user7_distribution():
    user_info = guser_list[3]
    deaduser_distribute_shares(user_info[0], gshare_price)


# -------------------------------------------------------------------------
# Print bank API Info
# -------------------------------------------------------------------------
def test_print_bank_api_info():
    bankapi = BankAPI.get_instance()
    savvlybank = bankapi.get_savvly_object()
    api_info = savvlybank.get_api_info()
    test_print_result("API Info", api_info)


# -------------------------------------------------------------------------
# Print Account IDs
# -------------------------------------------------------------------------
def test_print_account_IDs():
    bankapi = BankAPI.get_instance()
    savvlybank = bankapi.get_savvly_object()
    account_ids = savvlybank.get_account_ids()
    test_print_result("Account IDs", account_ids)


# -------------------------------------------------------------------------
# Print all Transactions
# -------------------------------------------------------------------------
def test_print_all_transactions():
    bankapi = BankAPI.get_instance()
    savvlybank = bankapi.get_savvly_object()
    transactions = savvlybank.get_all_transactions()
    test_print_result("All Transactions", transactions)


# -------------------------------------------------------------------------
# Print Deposit Transactions
# -------------------------------------------------------------------------
def test_print_deposit_transactions():
    bankapi = BankAPI.get_instance()
    savvlybank = bankapi.get_savvly_object()
    deposit_transactions = savvlybank.get_deposit_transactions()
    test_print_result("Deposit Transactions", deposit_transactions)


# -------------------------------------------------------------------------
# Print Withdrawal Transactions
# -------------------------------------------------------------------------
def test_print_withdrawal_transactions():
    bankapi = BankAPI.get_instance()
    savvlybank = bankapi.get_savvly_object()
    withdrawal_transactions = savvlybank.get_withdrawal_transactions()
    test_print_result("Withdrawal Transactions", withdrawal_transactions)


# -------------------------------------------------------------------------
# Print Savings Transactions
# -------------------------------------------------------------------------
def test_print_savings_transactions():
    bankapi = BankAPI.get_instance()
    savvlybank = bankapi.get_savvly_object()
    account_transactions = savvlybank.get_account_transactions(savvlybank.account_type_savings)
    test_print_result("Account Saving Transactions", account_transactions)


# -------------------------------------------------------------------------
# Print Specific transaction: ttx_11h5sxvp9ksxj8
# -------------------------------------------------------------------------
def test_print_specific_transaction1():
    bankapi = BankAPI.get_instance()
    savvlybank = bankapi.get_savvly_object()
    specific_tran1 = savvlybank.get_specific_transaction("ttx_11h5sxvp9ksxj8")
    test_print_result("Specific Transaction1", specific_tran1)


# -------------------------------------------------------------------------
# Print Specific transaction: ttx_11h5sxta9ksx6f
# -------------------------------------------------------------------------
def test_print_specific_transaction2():
    bankapi = BankAPI.get_instance()
    savvlybank = bankapi.get_savvly_object()
    specific_tran2 = savvlybank.get_specific_transaction("ttx_11h5sxta9ksx6f")
    test_print_result("Specific Transaction2", specific_tran2)


# -------------------------------------------------------------------------
# Print Sweep Account
# -------------------------------------------------------------------------
def test_print_sweep_account():
    bankapi = BankAPI.get_instance()
    savvlybank = bankapi.get_savvly_object()
    sweep_account = savvlybank.get_sweep_account()
    test_print_result("Sweep Account", sweep_account)


# -------------------------------------------------------------------------
# Lock the sweep account
# -------------------------------------------------------------------------
def test_lock_sweep_account():
    bankapi = BankAPI.get_instance()
    savvlybank = bankapi.get_savvly_object()
    lock_sweep = savvlybank.lock_account(
        savvlybank.account_type_sweep)  # Requires additional permissions in the Treasury Prime API
    test_print_result("Lock Account", lock_sweep)


# -------------------------------------------------------------------------
# Transfer money from the Checking Account to the Savings Account
# -------------------------------------------------------------------------
def test_transfer_money_from_checking_saving():
    bankapi = BankAPI.get_instance()
    savvlybank = bankapi.get_savvly_object()
    checking_account = savvlybank.get_checking_account()
    test_print_result("Checking Account", checking_account)
    saving_account = savvlybank.get_saving_account()
    test_print_result("Saving Account", saving_account)
    if checking_account and saving_account:
        acc1 = checking_account["id"]
        acc2 = saving_account["id"]
        amount = 1000.00000
        print("Transfering %f$ from %s to %s" % (amount, acc1, acc2))
        money_transfer = savvlybank.transfer_money(acc1, acc2, amount)
        test_print_result("Money Transfer", money_transfer)


# -------------------------------------------------------------------------
# Print all Transfers
# -------------------------------------------------------------------------
def test_print_all_transfers():
    bankapi = BankAPI.get_instance()
    savvlybank = bankapi.get_savvly_object()
    all_transfers = savvlybank.get_all_transfers()
    test_print_result("All Transfers", all_transfers)


# -------------------------------------------------------------------------
# Process Users Transactions
# -------------------------------------------------------------------------
def test_process_users_transactions():
    bankapi = BankAPI.get_instance()
    users_transactions_list = bankapi.process_users_transactions()
    test_print_result("Users Transactions", users_transactions_list)


# -------------------------------------------------------------------------
# Share Price
# -------------------------------------------------------------------------
gshare_price = 20

# ----------------------s---------------------------------------------------
# The users list added to the database
# -------------------------------------------------------------------------
guser_info = {
    'firstname': 'John',
    'lastname': 'Doe',
    'address': 'NYC',
    'sex': 'F',
    'birthdate': '1965-01-31',
    'ssn': '123-45-7899',
    'is_married': 'Y',
    'is_US_citizen': 'Y',
    'funding': 11,
    'payout_ages': [111, 65, 70, 100],
    'ETF': 'default',
    # optional
    'spouse_firstname': 'Mary',
    'spouse_lastname': 'Jane',
    'spouse_sex': 'F',
    'spouse_birthdate': '1980-12-22',
    'spouse_ssn': '121-45-7777',
    'spouse_email': 'mail@gmail.com',
    # must in case of non US citizen
    'passport_data': 'passport data',
    'alien_id_or_visa': '123123123',
}
# guser_list = [
#     # 0         1        2             3        4     5            6                  7
#     # idx     social    DOB         Address    Sex  Parent      Deposit            Withdraw
#     ["Usr_1", "100001", "1/4/1957", "Address1", "M", "advisor1", 69.69, -500],
#     ["Usr_2", "100002", "1/4/1956", "Address2", "M", "advisor1", 22 * gshare_price, -500],
#     ["Usr_3", "100003", "1/4/1955", "Address3", "M", "advisor2", 55 * gshare_price, -500],
#     ["Usr_4", "100004", "1/4/1954", "Address4", "F", "advisor1", 32 * gshare_price, -500],
#     ["Usr_5", "100005", "1/4/1953", "Address5", "M", "advisor2", 44 * gshare_price, -500],
#     ["Usr_6", "100006", "1/4/1952", "Address6", "M", "advisor3", 24 * gshare_price, -500],
#     ["Usr_7", "100007", "1/4/1951", "Address7", "M", "advisor3", 66 * gshare_price, -500],
#     ["Usr_8", "100008", "1/4/1950", "Address8", "F", "advisor3", 32 * gshare_price, -500],
#     ["Usr_9", "100009", "1/4/1949", "Address9", "M", "advisor3", 49 * gshare_price, -500],
#     ["Usr_10", "100010", "1/4/1948", "AddressX", "M", None, 33 * gshare_price, -500],
# ]
guser_list = [
    # 0         1        2             3        4
    # idx     userinfo   Parent       Deposit   Withdraw
    ["Usr_1", guser_info, "advisor1", 69.69, -500],
    ["Usr_2", guser_info, "advisor1", 22 * gshare_price, -500],
    ["Usr_3", guser_info, "advisor2", 55 * gshare_price, -500],
    ["Usr_4", guser_info, "advisor1", 32 * gshare_price, -500],
    ["Usr_5", guser_info, "advisor2", 44 * gshare_price, -500],
    ["Usr_6", guser_info, "advisor3", 24 * gshare_price, -500],
    ["Usr_7", guser_info, "advisor3", 66 * gshare_price, -500],
    ["Usr_8", guser_info,  "advisor3", 32 * gshare_price, -500],
    ["Usr_9", guser_info,  "advisor3", 49 * gshare_price, -500],
    ["Usr_10", guser_info, None, 33 * gshare_price, -500],
]

# -------------------------------------------------------------------------
# Selected User
# -------------------------------------------------------------------------
gselected_user = 0

# -------------------------------------------------------------------------
# The lookup table for the supported test functions
# -------------------------------------------------------------------------
gtest_functions = [
    ["Exit", test_exit],
    ["Delete the database tables", test_delete_tables],
    ["Create users in the database", test_create_users],
    ["Transfer money to user account", test_deposit_money],
    ["Withdraw money from user account", test_withdraw_money],
    ["Deduct a Fee", test_deduct_fee],
    ["Add Dividend", test_add_dividend],
    ["Update daily table with random share price and total portfolio", test_update_daily_table],
    ["Prints users Totals", test_print_users_totals],
    ["Prints the selected user's data", test_print_selected_user],
    ["Prints users data", test_print_users],
    ["Print Status Flags", test_print_status_flags],
    ["Print parents info", test_print_parents_info],
    ["Print death probability", test_print_death_probability],
    ["Print users transactions", test_print_user_transactions],
    ["Print transactions table", test_print_transactions_table],
    ["Print Daily Table", test_print_daily_table],
    ["Print Inheritance Table", test_print_inheritance_table],
    ["Select a user to operate on", test_select_user],
    ["Deposit Money: Simulate User", test_simulate_deposit_by_user],
    ["Deposit Money: Simulate BankAdaptor", test_simulate_deposit_by_bankadaptor],
    ["Deposit Money: Simulate Trader", test_simulate_deposit_by_trader],
    ["Withdrawal Money: Simulate User", test_simulate_withdrawal_by_user],
    ["Withdrawal Money: Simulate BankAdaptor", test_simulate_withdrawal_by_bankadaptor],
    ["Withdrawal Money: Simulate Trader", test_simulate_withdrawal_by_trader],
    ["Simulate FMV (update all user's FMV)", test_update_all_users_fmv],
    ["Print the FMV of all users", test_print_all_users_fmv],
    ["Set User7 dead", test_set_user7_dead],
    ["Calculate the shares of a dead user7 distribution", test_calculate_dead_shares_user7_distribution],
    # ["(BankAPI) Print bank API Info",                                       test_print_bank_api_info],
    # ["(BankAPI) Print Account IDs",                                         test_print_account_IDs],
    # ["(BankAPI) Print all Transactions",                                    test_print_all_transactions],
    # ["(BankAPI) Print Deposit Transactions",                                test_print_deposit_transactions],
    # ["(BankAPI) Print Withdrawal Transactions",                             test_print_withdrawal_transactions],
    # ["(BankAPI) Print Savings Transactions",                                test_print_savings_transactions],
    # ["(BankAPI) Print Specific transaction: ttx_11h5sxvp9ksxj8",            test_print_specific_transaction1],
    # ["(BankAPI) Print Specific transaction: ttx_11h5sxta9ksx6f",            test_print_specific_transaction2],
    # ["(BankAPI) Print Sweep Account",                                       test_print_sweep_account],
    # ["(BankAPI) Lock the sweep account",                                    test_lock_sweep_account],
    # ["(BankAPI) Transfer money from Checking Account to Savings Account",   test_transfer_money_from_checking_saving],
    # ["(BankAPI) Print all Transfers",                                       test_print_all_transfers],
    # ["Process Users Transactions",                                          test_process_users_transactions],
    ["Reserved", test_stub],
]

# -------------------------------------
# The program starts here
# -------------------------------------
if __name__ == "__main__":
    test_run_menu(gtest_functions)
