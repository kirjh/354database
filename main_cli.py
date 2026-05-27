import python.sqlserver as sql

conn = sql.connect()
user_id = None
user_name = None

#user_id = 'D__iHPVDEhqQr0ZkGt___Q' # FOR TESTING ONLY. REMOVE LATER
#user_name = 'Sara'


print("#-----------------------------------#\n\
Welcome to the command line interface. To begin, type the command 'login'. To exit, type 'exit'.\n\
For a list of commands, type 'help'.")

cmd_list = {
    'business': 'Search for (a) business(es).',
    'exit': 'Exit the program.',
    'friend' : 'Add a friend.',
    'help': 'Get list of commands.',
    'login' : 'Log into the database.',
    'logout' : 'Log out of the database.',
    'review' : 'Leave a review for a business',
    'user' : 'Search for (a) user(s).'
}

def login(conn, user_id, user_name):
    if user_id:
        print("Already logged in!")
        return user_id, user_name
    print("Type in your user ID or type 'c' to cancel.")
    while True:
        uin = input("CLI:Home/Login> ")
        try:
            user = sql.login(conn, uin)
            uid = user[0]
            un = user[1]
        except Exception as e:
                print(e)
                print("An error has occured.")
                uin = 'c'
        if uin == 'c':
            return user_id, user_name
        elif uid != None:
            print(f"Successfully logged in as {un}.")
            return uid, un 
        else:
            print("Failed to log in. Please try again or type 'c' to cancel.")

def search_business(conn):
    while True:
        uin = [0,0,0,0]
        while True:
            uin[0] = input("Enter the business name. Leave blank to search all.\nCLI:Home/Search> ")
            uin[1] = input("Enter the city. Leave blank to search all.\nCLI:Home/Search> ")
            uin[2] = input("Enter the minimum number of stars. Leave blank to search all.\nCLI:Home/Search> ")
            uin[3] = input("Enter the search ordering(name, city, stars).\nCLI:Home/Search> ")
            a = input("Search database with these values? (y/n) or type 'c' to cancel.\nCLI:Home/Search> ")
            if a == 'y':
                break
            elif a == 'c':
                return
            
        if uin[2] == '':
            uin[2] = 1
        try:
            float(uin[2])
        except:
            uin[2] = -1

        if float(uin[2]) > 5 or float(uin[2]) < 1:
            print("Invalid value for stars. Must be a float between 1 and 5 inclusive.")
        elif uin[3] not in ['name', 'city', 'stars']:
            print("Invalid value for ordering value. Must be either of 'name', 'city', or 'stars'.")
        else:
            try:
                arr = sql.search_business(conn, uin[0], uin[1], uin[2], uin[3])
            except Exception as e:
                print(e)
                print("An error has occured.")
                break
            if arr == None:
                print("No results found")
            else:
                print("business_id, name, address, city, stars")
                for i in arr:
                    print(f"{i[0]}, {i[1]}, {i[2]}, {i[3]}, {i[4]}")
                print(f"Businesses found: {len(arr)}")
            break

def search_user(conn):
    while True:
        uin = [0,0,0]
        while True:
            uin[0] = input("Enter the name. Leave blank to search all.\nCLI:Home/Search> ")
            uin[1] = input("Enter the minimum review count. Leave blank to search all.\nCLI:Home/Search> ")
            uin[2] = input("Enter the minimum average stars. Leave blank to search all.\nCLI:Home/Search> ")
            a = input("Search database with these values? (y/n) or type 'c' to cancel.\nCLI:Home/Search> ")
            if a == 'y':
                break
            elif a == 'c':
                return
        
        if uin[1] == '':
            uin[1] = 0
        if uin[2] == '':
            uin[2] = 1
        try:
            int(uin[1])
        except:
            uin[1] = -1
        try:
            float(uin[2])
        except:
            uin[2] = -1
        if int(uin[1]) < 0:
            print("Invalid value for minimum review count. Must be an integer greater than 0.")
        elif float(uin[2]) > 5 or float(uin[2]) < 1:
            print("Invalid value for stars. Must be a float between 1 and 5 inclusive.")
        else:
            try:
                arr = sql.search_user(conn, uin[0], uin[1], uin[2])
            except Exception as e:
                print(e)
                print("An error has occured.")
                break
            if arr == None:
                print("No results found")
            else:
                print("user_id, name, review_count, useful, funny, cool, average_stars, yelping_since")
                for i in arr:
                    print(f"{i[0]}, {i[1]}, {i[2]}, {i[3]}, {i[4]}, {i[5]}, {i[6]}, {i[7]}")
                print(f"Users found: {len(arr)}")
            break

def make_friend(conn):
    while True:
        uin = input("Enter the user_id of the person you wish to friend.\nCLI:Home/Friend> ")
        try:
            sql.make_friend(conn,user_id, uin)
            print("Successfully added friend.")
            break
        except Exception as e:
            print(e)
            print("Friendship failed. Try again.")

def leave_review(conn):
    while True:
        uin = [0,0]
        while True:
            uin[0] = input("Enter the business_id.\nCLI:Home/Review> ")
            uin[1] = input("Enter the number of stars.\nCLI:Home/Review> ")
            a = input("Submit review with these values? (y/n) or type 'c' to cancel.\nCLI:Home/Review> ")
            if a == 'y':
                break
            elif a == 'c':
                return
        try:
            int(uin[1])
        except:
            uin[1] = -1
        if int(uin[1]) > 5 or int(uin[1]) < 1:
            print("Invalid value for stars. Must be an integer between 1 and 5 inclusive.")
        else:
            try:
                sql.review_business(conn,user_id, uin[0], uin[1])
                print("Successfully left review.")
                break
            except Exception as e:
                print(e)
                print("Failed to leave review. Try again.")

while True:
    print("#-----------------------------------#\nStatus: " + (f"Logged in as {user_name}." if user_id != None else "Not logged in."))
    user_input = input("CLI:Home> ")
    match user_input:
        case 'exit' | 'e':
            break
        case 'help' | 'h':
            print("Commands:")
            for key in cmd_list:
                print(f"| {key} :: {cmd_list[key]}")
        case 'login' | 'l':
            user_id, user_name = login(conn, user_id, user_name)
        case 'logout' | 'o':
            if user_id:
                user_id, user_name = (None, None)
                print("Successfully logged out.")
            else:
                print("Already logged out!")
        case 'business' | 'b':
            if user_id:
                search_business(conn)
            else:
                print("You must log in to perform this action.")
        case 'user' | 'u':
            if user_id:
                search_user(conn)
            else:
                print("You must log in to perform this action.")
        case 'friend' | 'f':
            if user_id:
                make_friend(conn)
            else:
                print("You must log in to perform this action.")
        case 'review' | 'r':
            if user_id:
                leave_review(conn)
            else:
                print("You must log in to perform this action.")
        case _:
            print("Unknown command. For a list of commands, type 'help'.")

conn.close()