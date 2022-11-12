import sys
from common.util.config_wrapper import config_wrapper_init

# ----------------------------------------------
# Read the configuration
# ----------------------------------------------
config_wrapper_init("common/")


# -------------------------------------------------------------------------
# Print Result
# -------------------------------------------------------------------------
def test_print_result(header, data):
    print("------------------------------------")
    print(header)
    print("------------------------------------")
    if isinstance(data, type([])):
        print(*data, sep='\n')
    else:
        print(data)


# -------------------------------------------------------------------------
# Get integer input from the user
# -------------------------------------------------------------------------
def test_get_integer_input(message, limit):
    selection = input(message)
    try:
        selection = int(selection)
    except Exception as err:
        print("Invalid input. Please type an integer")
        selection = -1
    if selection < 0:
        print("Invalid input. Please type a valid positive integer")
        selection = -1
    if selection > limit:
        print("Invalid input. Please type a valid integer (up to: %d)" % limit)
        selection = -1
    return selection


# -------------------------------------------------------------------------
# Show the menu of functions
# -------------------------------------------------------------------------
def test_show_menu(test_functions: list):
    print("")
    for funcinx in range(0, len(test_functions), 2):
        rec1 = test_functions[funcinx]
        rec2 = test_functions[funcinx + 1]
        print("%2d. %-52s\t\t\t%2d. %-52s" % (funcinx, rec1[0], funcinx + 1, rec2[0]))
    print("")


# -------------------------------------------------------------------------
# Process the selection
# -------------------------------------------------------------------------
def test_process_selection(test_functions: list, selection):
    funcinfo = test_functions[selection]
    func = funcinfo[1]  # Get the function
    func()


# -------------------------------------------------------------------------
# Get user selection
# -------------------------------------------------------------------------
def test_get_user_selection(test_functions: list):
    selection = test_get_integer_input("Select action (type the function index): ", len(test_functions) - 1)
    return selection


# -------------------------------------------------------------------------
# Run the menu and process the selection
# -------------------------------------------------------------------------
def test_run_menu(test_functions: list):
    while True:
        test_show_menu(test_functions)
        selection = test_get_user_selection(test_functions)
        if selection < 0:
            continue
        test_process_selection(test_functions, selection)


# -------------------------------------------------------------------------
# Exit the test program
# -------------------------------------------------------------------------
def test_exit():
    print("Exiting....")
    sys.exit(1)


# -------------------------------------------------------------------------
# Stub Function
# -------------------------------------------------------------------------
def test_stub():
    print(" Nothing happend")
