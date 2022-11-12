from common.controllers.dbhandles import *
# from tests import test_print_result
# from tests import test_get_user_selection, test_get_integer_input, test_exit
from commontest import *  # Common to all tests in nthis repository


# -------------------------------------------------------------------------
# Create a list of users
# -------------------------------------------------------------------------
def test_create_RIAs():
    # print("testing RIA database")
    dbh = Dbhandles.get_instance()
    RIAtable = dbh.get_RIAtables()

    for userinfo in guser_list:
        idx = userinfo[0]
        crd_individual = userinfo[1]
        associated = userinfo[2]
        advisor_info = userinfo[3]
        crd_firm = userinfo[4]
        # print(f"adding user idx={idx}")
        if not RIAtable.add_new_advisor(idx, crd_individual, crd_firm, associated, advisor_info):
            break


# -------------------------------------------------------------------------
# get_all_associated_RIAs
# -------------------------------------------------------------------------
def test_get_all_associated_RIAs():
    dbh = Dbhandles.get_instance()
    RIAtable = dbh.get_RIAtables()

    advisors = RIAtable.get_all_associated_RIAs(g_associated)
    test_print_result(f"RIAs associated with '{g_associated}':", advisors)

    all_rias = '*'
    advisors = RIAtable.get_all_associated_RIAs(all_rias)
    test_print_result(f"RIAs associated with '{all_rias}':", advisors)


# -------------------------------------------------------------------------
# delete_RIA_tables
# -------------------------------------------------------------------------
def test_delete_RIA_tables():
    dbh = Dbhandles.get_instance()
    dbh.delete_RIA_tables()


# -------------------------------------------------------------------------
# is_RIA
# -------------------------------------------------------------------------
def test_is_advisor():
    dbh = Dbhandles.get_instance()
    RIAtable = dbh.get_RIAtables()
    RIAtable.is_advisor(idx=guser_list[0][0])
    RIAtable.is_advisor(idx=guser_list[0][1])

    RIAtable.is_advisor(idx='dummy_idx')
    # RIAtable.is_advisor(idx=None, crd_firm=None)


# -------------------------------------------------------------------------
# test_add_child
# -------------------------------------------------------------------------
def test_add_child():
    dbh = Dbhandles.get_instance()
    RIAtable = dbh.get_RIAtables()
    RIAtable.add_child('advisor2', 'Usr1')
    RIAtable.add_child('advisor2', 'Usr2', )
    RIAtable.add_child('advisor2', 'Usr_dummy')


# -------------------------------------------------------------------------
# get_RIA_info
# -------------------------------------------------------------------------
def test_get_RIA_info():
    dbh = Dbhandles.get_instance()
    RIAtable = dbh.get_RIAtables()
    RIAtable.get_advisor_info(guser_list[0][0])
    RIAtable.get_advisor_info('dummy_idx')


# -------------------------------------------------------------------------
# get_RIA_children
# -------------------------------------------------------------------------
def test_get_RIA_children():
    dbh = Dbhandles.get_instance()
    RIAtable = dbh.get_RIAtables()
    RIA_idx = 'advisor1'
    print(f'all childen of {RIA_idx}:')
    children = RIAtable.get_advisor_children(RIA_idx)
    print(children)


# -------------------------------------------------------------------------
# test_add_child
# -------------------------------------------------------------------------
def test_add_child():
    dbh = Dbhandles.get_instance()
    RIAtable = dbh.get_RIAtables()
    RIA_idx = 'advisor1'
    child_idx = 'Usr1'
    RIAtable.add_child(idx=RIA_idx, userid=child_idx)


# -------------------------------------------------------------------------
# test_del_child
# -------------------------------------------------------------------------
def test_del_child():
    dbh = Dbhandles.get_instance()
    RIAtable = dbh.get_RIAtables()
    RIA_idx = 'advisor1'
    child_idx = 'Usr1'
    RIAtable.del_child(idx=RIA_idx, userid=child_idx)


# -------------------------------------------------------------------------
# test_get_by_status8
# -------------------------------------------------------------------------
def test_get_by_status():
    dbh = Dbhandles.get_instance()
    RIAtable = dbh.get_RIAtables()

    users_table = dbh.get_usertables()

    statuses = [
        users_table.status_flag_active,
        users_table.status_flag_pending,
        users_table.status_flag_transfer,
        users_table.status_flag_transfer_complete,
        users_table.status_flag_purchase_pending,
        users_table.status_flag_withdrawal,
        users_table.status_flag_withdrawal_pending,
        users_table.status_flag_deceased,
        users_table.status_flag_closed,
        users_table.status_flag_transfer_cancel,
    ]
    RIA_idx = 'advisor1'
    for status in statuses:
        print(f"Children with status {status}:")
        children = RIAtable._get_all_specific_statusflag(idx=RIA_idx, status_flag_value=status)
        print(children)


# ----------------------s---------------------------------------------------
# The RIA  list added to the database
# -------------------------------------------------------------------------
guser_list = [
    # 0             1                  2           3            4
    # idx          crd_individual     associated   advisorinfo  crd_firm
    ["RIA1", "123123", "111",
     {"firstname": "Adv1", "lastname": "last1", "address": "NYC", "email": "x@y.com",
      "phone": "+1 (212) 333-4444"}, "332"],
    ["RIA2", None, "222",
     {"firstname": "Adv1", "lastname": "last1", "address": "NYC", "email": "x@y.com",
      "phone": "+1 (212) 333-4444"}, "3321"],
    ["RIA3", "123444", "111",
     {"firstname": "Adv1", "lastname": "last1", "address": "NYC", "email": "x@y.com",
      "phone": "+1 (212) 333-4444"}, "3322"],
    ["RIA4", "123555", "222",
     {"firstname": "Adv1", "lastname": "last1", "address": "NYC", "email": "x@y.com",
      "phone": "+1 (212) 333-4444"}, "3323"],
    ["advisor1", "123666", "savvly",
     {"firstname": "Adv1", "lastname": "last1", "address": "NYC", "email": "x@y.com",
      "phone": "+1 (212) 333-4444"}, "3324"],
    ["advisor2", "123777", "savvly",
     {"firstname": "Adv1", "lastname": "last1", "address": "NYC", "email": "x@y.com",
      "phone": "+1 (212) 333-4444"}, "332"],
    ["advisor3", "123888", "savvly",
     {"firstname": "Adv1", "lastname": "last1", "address": "NYC", "email": "x@y.com",
      "phone": "+1 (212) 333-4444"}, "332"],
    ["advisor4", "123999", "savvly",
     {"firstname": "Adv1", "lastname": "last1", "address": "NYC", "email": "x@y.com",
      "phone": "+1 (212) 333-4444"}, None],

]
g_associated = 'savvly'

# -------------------------------------------------------------------------
# The lookup table for the supported test functions
# -------------------------------------------------------------------------
gtest_functions = [
    ["Exit", test_exit],
    ["Create RIAs in the database", test_create_RIAs],
    ["Delete RIAs table", test_delete_RIA_tables],
    [f"Get all RIA's associated with '{g_associated}', all=4'*' ", test_get_all_associated_RIAs],
    ["test is_advisor", test_is_advisor],
    [f"get RIA children of {'advisor1'}", test_get_RIA_children],
    [f"Add to client Usr1 parent {'advisor1'}", test_add_child],
    [f"del client Usr1 parent {'advisor1'}", test_del_child],
    [f"get all clients with parent {'advisor1'} per status", test_get_by_status],
    ["Reserved", test_stub],
]

if __name__ == "__main__":
    test_run_menu(gtest_functions)
