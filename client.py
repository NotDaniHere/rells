from rells_lib import Client
from rells_lib import Profile
import threading
placeholder_profile = Profile("a", "a", "a", "a", "a", "a")
jsonPath = "profiles.json"
profiles = placeholder_profile.loadJsonDataClient(jsonPath)
noProfiles = False
if profiles == {}:
    noProfiles = True
def create_profile():
    profile_name = input("What's this new profile's name? > ")
    server_ip = input("What is the server's ip? > ")
    server_port = input("What is the server port? > ")
    server_password = input("What is the server password? > ")
    nickname = input("What's the nickname you're going to be using? > ")
    nickname_password = input("What's your nick's password? > ")
    a = Profile(profile_name, server_ip, server_port, server_password, nickname, nickname_password) 
    profiles.update({f'{len(profiles)+1}': a.getProfile()})
    placeholder_profile.saveJsonDataClient(jsonPath, profiles)
def lsProfiles():
    for i in profiles:
        counter = 1
        print(f'{profiles[i][0]} ({i})')
        for _ in profiles[i]:
            if counter == 0:
                continue
            elif counter == 1:
                print(f"IP:    {profiles[i][counter]}")
            elif counter == 2:
                print(f"Port:    {profiles[i][counter]}")
            elif counter == 3:
                print(f"Server password:    {profiles[i][counter]}")
            elif counter == 4:
                print(f"Logging Nickname:    {profiles[i][counter]}")
            elif counter == 5:
                print(f"Nickname password:    {profiles[i][counter]}")
            counter += 1
if noProfiles:
    print("Create a new profile to get started!")
    create_profile()
    noProfiles = False
usr_input = "new"
while usr_input == "new":
    print("Here are all of your saved profiles (choose by typing in the number next to your profile name, or type new to create a new profile):")
    lsProfiles()
    print("Or create a new account to use for a server (signup)")
    usr_input = input("> ")
    if usr_input == "new":
        create_profile()

# Use the updated `Client` class from the fixed `rells_lib` with proper `stop_client` handling

if not usr_input == "signup":
    current_profile = profiles[usr_input]
else:
    # Collect signup data
    server_ip = input("What is the server IP? > ")
    server_port = input("What is the server port? > ")
    signup_password = input("What is the signup password? > ")
    nickname = input("What is the nickname you're creating? > ")
    nickname_password = input("What is the nickname password you'll use? > ")

    current_profile = ["signup", server_ip, server_port, signup_password, nickname, nickname_password]

# Create the client
use_client = Client(current_profile[1], int(current_profile[2]), current_profile[3], current_profile[4], current_profile[5])

# Start threads for receive and write
receive_thread = threading.Thread(target=use_client.receive)
write_thread = threading.Thread(target=use_client.write)

receive_thread.start()
write_thread.start()

receive_thread.join()
write_thread.join()
