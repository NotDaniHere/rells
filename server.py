import threading
import socket
import random
from rells_lib import Server
srv = Server()
cfg = srv.loadConfig("config.json")
host = cfg[0]
port = cfg[1]
server_password = cfg[2]
acc_create_pass = cfg[3]
clients = []
nicknames = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
cred_path = "user_profiles.json"
credentials_db = srv.loadUserProfiles(cred_path)

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
def receive(sv_password, acc_create_pass):
    while True:
        client, address = server.accept()
        client.send('LOGIN'.encode('ascii'))
        credentials = client.recv(1024).decode('ascii')
        unpacked_information = srv.validateCredentials(credentials)
        print(f"Raw credentials received: {credentials}")

        if unpacked_information is None:
            client.send('LOGIN_ERROR'.encode('ascii'))
            client.close()
            continue

        username, user_password, provided_password = unpacked_information

        # Handle signup
        if provided_password == acc_create_pass:
            if username in credentials_db:
                client.send('LOGIN_ERROR'.encode('ascii'))  # User already exists
            else:
                # Add the new user and save profiles
                credentials_db[username] = user_password
                srv.saveUserProfiles(cred_path, credentials_db)

                # Generate new signup password
                acc_create_pass = str(random.randint(1000, 9999))
                srv.saveConfig("config.json", [host, port, sv_password, acc_create_pass])

                client.send('SIGNUP_END'.encode('ascii'))
                print(f"New user '{username}' created successfully.")
            client.close()
            continue


        # Handle login
        elif provided_password == sv_password:
            if username in credentials_db:
                if credentials_db[username] == user_password:
                    print(f"Connected with {str(address)}.")
                    nicknames.append(username)
                    clients.append(client)

                    broadcast(f'{username} has joined the chat.'.encode('ascii'))
                    print(f'{username} has logged on the server.')

                    thread = threading.Thread(target=handle, args=(client,))
                    thread.start()
                else:
                    client.send('LOGIN_ERROR'.encode('ascii'))  # Wrong password
                    client.close()
            else:
                client.send('LOGIN_ERROR'.encode('ascii'))  # User does not exist
                client.close()


        # Invalid credentials
        else:
            client.send('LOGIN_ERROR'.encode('ascii'))
            client.close()

receive(server_password, acc_create_pass)