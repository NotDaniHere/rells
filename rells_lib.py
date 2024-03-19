import socket
class Client():
    def __init__(self, host, port, server_password, nickname, user_password):
        self.host = host
        self.port = port
        self.server_password = server_password
        self.nickname = nickname
        self.user_password = user_password
        self.credentials = f'{self.nickname}/PASSWD_SEP/{self.password}/SERVER_SEP/{self.server_password}'
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
                    break
                elif message.startswith(f'{self.nickname}: '):
                    continue      
                else:
                    print(message)
            except:
                print("An error has occurred.")
                self.client.close()
                break
            
    def write(self):
        while True:
            message = f'{self.nickname}: {input("")}'
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
    def editProfile(self, prop, rect):
        self.profile[prop] = rect
        


