import threading
import socket
from rells_lib import Server
srv = Server()
cfg = srv.loadConfig("config.json")
host = cfg[0]
port = cfg[1]
server_password = cfg[2]
clients = []
nicknames = []
config_path = ""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
credentials_db = srv.loadUserProfiles("user_profiles.json")
def broadcast(message):
    for client in clients:
        client.send(message)
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chat.'.encode('ascii'))
            nicknames.remove(nickname)
            break
def receive(sv_password):
    while True:
        client, address = server.accept()
        client.send('LOGIN'.encode('ascii'))
        credentials = client.recv(1024).decode('ascii')
        unpacked_information = srv.validateCredentials(credentials)
        username = unpacked_information[0]
        user_password = unpacked_information[1]
        server_password = unpacked_information[2]
        if not server_password == sv_password:
            client.send('LOGIN_ERROR'.encode('ascii'))
            login_error = True
        else:
            login_error = False
        if not login_error:
            if username in credentials_db:
                if credentials_db[username] == user_password:
                    print(f"Connected with {str(address)}.")
                    nicknames.append(username)
                    clients.append(client)
                    print(f'{username} has logged on the server.')
                    broadcast(f'    {username} has joined the chat.'.encode('ascii'))

                    thread = threading.Thread(target = handle, args = (client,))
                    thread.start()
                else:
                    client.send('LOGIN_ERROR'.encode('ascii'))
            else:
                client.send('LOGIN_ERROR'.encode('ascii'))
receive(server_password)