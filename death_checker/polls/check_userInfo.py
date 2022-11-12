from user_list import dead_users

def death_checker(id):

    if id in dead_users:
        print(f'The user {id} is dead')
    else:
        print('User is still alive!')

user_input = input('verify id: ')

death_checker(user_input)
print(dead_users)

    