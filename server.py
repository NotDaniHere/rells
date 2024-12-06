import threading
import socket
import random
import os
import json
from rells_lib import Server

srv = Server()

# Paths for configuration and user profiles
config_path = "config.json"
cred_path = "user_profiles.json"

# Ensure config.json exists with default values
default_config = {
    "RELLS_SERVER_CONFIG": ["127.0.0.1", 5000, "default_server_password", "default_signup_password"]
}

if not os.path.exists(config_path):
    print(f"{config_path} not found. Creating default configuration.")
    with open(config_path, "w") as f:
        json.dump(default_config, f, indent=4)

# Load server configuration
cfg = srv.loadConfig(config_path)
host = cfg[0]
port = cfg[1]
server_password = cfg[2]
acc_create_pass = cfg[3]

# Ensure user_profiles.json exists
if not os.path.exists(cred_path):
    print(f"{cred_path} not found. Creating an empty user profile database.")
    with open(cred_path, "w") as f:
        json.dump({}, f, indent=4)

# Load user profiles
credentials_db = srv.loadUserProfiles(cred_path)

# Initialize server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

# Broadcast function
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle individual clients
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

# Accept new clients and handle login/signup
def receive(sv_password, acc_create_pass):
    while True:
        client, address = server.accept()
        client.send('LOGIN'.encode('ascii'))
        credentials = client.recv(1024).decode('ascii')
        try:
            unpacked_information = srv.validateCredentials(credentials)
            username = unpacked_information[0]
            user_password = unpacked_information[1]
            server_password = unpacked_information[2]

            if server_password == acc_create_pass:
                # Handle signup
                credentials_db.update({username: user_password})
                srv.saveUserProfiles(cred_path, credentials_db)
                acc_create_pass += str(random.randint(0, 9))
                srv.saveConfig(config_path, [host, port, sv_password, acc_create_pass])
                client.send('SIGNUP_END'.encode('ascii'))
            elif username in credentials_db and credentials_db[username] == user_password:
                # Handle login
                clients.append(client)
                nicknames.append(username)
                broadcast(f'{username} has joined the chat.'.encode('ascii'))
                thread = threading.Thread(target=handle, args=(client,))
                thread.start()
            else:
                client.send('LOGIN_ERROR'.encode('ascii'))
                client.close()
        except Exception as e:
            print(f"Error processing credentials from {address}: {e}")
            client.send('LOGIN_ERROR'.encode('ascii'))
            client.close()

# Start the server
print(f"Server is running on {host}:{port}")
receive(server_password, acc_create_pass)
