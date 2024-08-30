import socket
import json
'''
This is the Rells Library, made to ease the production process of creating the Client Software and Server Software for the Rells CLI Project. RLS LIB VERSION: 31.08.24
'''
class Client():
    def __init__(self, host, port, server_password, nickname, user_password):
        self.host = host
        self.port = port
        self.server_password = server_password
        self.nickname = nickname
        self.user_password = user_password
        self.credentials = f'{self.nickname}/PASSWD_SEP/{self.user_password}/SERVER_SEP/{self.server_password}+'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'LOGIN':
                    print("Logging in...")
                    self.client.send(self.credentials.encode('ascii'))
                elif message == "LOGIN_ERROR":
                    print("Unable to connect to the server (wrong login details)")
                    self.client.close()
                    exit()
                elif message.startswith(f'{self.nickname}: '):
                    continue      
                else:
                    print(message)
            except:
                print("An error has occurred.")
                self.client.close()
                exit()
            
    def write(self):
        while True:
            message = f'<{self.nickname}>: {input(f"")}'
            self.client.send(message.encode('ascii'))
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
        for i, j in enumerate(credentials):
            if j == "/":
                if credentials[i+1] == "P":
                    if credentials[i+2] == "A":
                        if credentials[i+3] == "S":
                            if credentials[i+4] == "S":
                                if credentials[i+5] == "W":
                                    if credentials[i+6] == "D":
                                        if credentials[i+7] == "_":
                                            if credentials[i+8] == "S":
                                                if credentials[i+9] == "E":
                                                    if credentials[i+10] == "P":
                                                        if credentials[i+11] == '/':
                                                            username = credentials[0:i]
                                                            credentials_no_user = credentials[i+12:-1]
                                                            print(credentials_no_user)
                                                            for i, j in enumerate(credentials_no_user):
                                                                if credentials_no_user[i] == "/":
                                                                    if credentials_no_user[i+1] == "S":
                                                                        if credentials_no_user[i+2] == "E":
                                                                            if credentials_no_user[i+3] == "R":
                                                                                if credentials_no_user[i+4] == "V":
                                                                                    if credentials_no_user[i+5] == "E":
                                                                                        if credentials_no_user[i+6] == "R":
                                                                                            if credentials_no_user[i+7] == "_":
                                                                                                if credentials_no_user[i+8] == "S":
                                                                                                    if credentials_no_user[i+9] == "E":
                                                                                                        if credentials_no_user[i+10] == "P":
                                                                                                            if credentials_no_user[i+11] == '/':
                                                                                                                user_password = credentials_no_user[0:i]
                                                                                                                server_password = credentials_no_user[i+12:]
                                                                                                                return(username, user_password, server_password)
    def loadConfig(self, path):
        with open(path, 'r') as file:
            data = json.load(file)
        config = data['RELLS_SERVER_CONFIG']
        return config
    
    def saveConfig(self, path, cfg):
        config_file = json.dumps({"RELLS_SERVER_CONFIG": cfg}, indent=4)

        with open(path, "w") as outfile:
            outfile.write(config_file)


    def loadUserProfiles(self, path):
        with open(path, 'r') as file:
            data = json.load(file)
        return data
    
    def saveUserProfiles(self, path, profiles):
        user_profiles = json.dumps(profiles, indent=4)

        with open(path, "w") as outfile:
            outfile.write(user_profiles)

    def addUserProfile(self, path, profile):
        with open(path, 'r') as file:
            data = json.load(file)
        data.update(profile)
        user_profiles = json.dumps(data, indent=4)

        with open(path, "w") as outfile:
            outfile.write(user_profiles)


                                                                                                                




