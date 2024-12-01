from rells_lib import Server
srv = Server()
while True:
    print("What would you like to do?")
    print("1: Modify Server Config file")
    print("2: Modify user profiles file")
    task = input("> ")
    if task == "2":
        print("1: Show current user profiles")
        print("2: Add a new user profile")
        task = input("> ")
        if task == "1":
            credentials_db = srv.loadUserProfiles("user_profiles.json")
            print(credentials_db)
        if task == "2":
            profile = {input("Username of the new profile: "): input("Password of the new profile: ")}
            srv.addUserProfile()
    if task == "1":
        print("1: Show current user profiles")
        print("2: Save a new config file")
        if task == "1":
            cfg = srv.loadConfig("config.json")
            print(cfg)
        if task == "2":
            cfg = [input("Input the server IP > "), int(input("Input your server port > "), input("Input your server password > "))]
            srv.saveConfig(cfg)