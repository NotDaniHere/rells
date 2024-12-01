import socket
import json
'''
This is the Rells Library, made to ease the production process of creating the Client Software and Server Software for the Rells CLI Project. RLS LIB VERSION: 31.08.24
'''
class Client:
    def __init__(self, host, port, server_password, nickname, user_password):
        self.host = host
        self.port = port
        self.server_password = server_password
        self.nickname = nickname
        self.user_password = user_password
        self.credentials = f'{self.nickname}/PASSWD_SEP/{self.user_password}/SERVER_SEP/{self.server_password}'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True  # Control flag for managing connection state
        self.client.connect((self.host, self.port))

    def receive(self):
        while self.running:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'LOGIN':
                    print("Logging in...")
                    self.client.send(self.credentials.encode('ascii'))
                elif message == "LOGIN_ERROR":
                    print("Unable to connect to the server (wrong login details)")
                    self.stop_client()
                elif message == "SIGNUP_END":
                    print("You may now login with your newly created account.") 
                    self.stop_client()
                elif message.startswith(f'{self.nickname}: '):
                    continue 
                else:
                    print(message)
            except Exception as e:
                print(f"An error occurred: {e}")
                self.stop_client()
            
    # Client class (in rells_lib)
    def write(self):
        while True:
            try:
                message = f'{self.nickname}: {input("")}'
                self.client.send(message.encode('ascii'))
            except Exception as e:
                print(f"Error in write: {e}")
                self.client.close()
                break


    def stop_client(self):
        """Gracefully stops the client."""
        self.running = False
        self.client.close()
        print("Connection closed.")
class Profile():
    def __init__(self, profile_name, server_ip, server_port, server_password, user_nickname, user_password):
        self.profile_name = profile_name
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_password = server_password
        self.user_nickname = user_nickname
        self.user_password = user_password
        self.profile = [profile_name, server_ip, server_port, server_password, user_nickname, user_password]
    def getProfile(self):
        return self.profile
    def loadJsonDataClient(self, path):
        with open(path, 'r') as file:
            data = json.load(file)
        return data
    def saveJsonDataClient(self, path, profiles):
        json_object = json.dumps(profiles, indent=4)

        with open(path, "w") as outfile:
            outfile.write(json_object)
class Server():
    def __init__(self) -> None:
        pass
    def validateCredentials(self, credentials):
        try:
            # Split the credentials into username, user_password, and server_password
            username, remainder = credentials.split('/PASSWD_SEP/')
            user_password, server_password = remainder.split('/SERVER_SEP/')
            return username, user_password, server_password
        except ValueError as e:
            print(f"Error in validateCredentials: {e}")
            print(f"Malformed credentials: {credentials}")
            return None

    def loadConfig(self, path):
        #Function loads the server config file.
        #Server config file contains the IP (default, localhost), server port and also the server password.
        with open(path, 'r') as file:
            data = json.load(file)
        config = data['RELLS_SERVER_CONFIG']
        return config
    
    def saveConfig(self, path, cfg):
        #Function saves the parsed in server config file.
        #Server config format goes like this: {"RELLS_SERVER_CONFIG": [IP, PORT, SV_PASSWORD]}
        config_file = json.dumps({"RELLS_SERVER_CONFIG": cfg}, indent=4)
        with open(path, "w") as outfile:
            outfile.write(config_file)


    def loadUserProfiles(self, path):
        #Function gets all of the user profiles in the parsed path, and uses them as the credentials_db folder.
        with open(path, 'r') as file:
            data = json.load(file)
        return data
    
    def saveUserProfiles(self, path, profiles):
        #This function saves current user profiles.
        #It removes all previous user profiles and replaces it with whatever credentials_db you parse.
        #Credentials_db format goes as follows: {"Username": "Password", "Username2": "Password2"}
        user_profiles = json.dumps(profiles, indent=4)

        with open(path, "w") as outfile:
            outfile.write(user_profiles)

    def addUserProfile(self, path, profile):
        #This function adds a new user profile. 
        #The user profile object is a dictionary that uses the username as the key and the password is its contents
        with open(path, 'r') as file:
            data = json.load(file)
        data.update(profile)
        user_profiles = json.dumps(data, indent=4)

        with open(path, "w") as outfile:
            outfile.write(user_profiles)


                                                                                                                




