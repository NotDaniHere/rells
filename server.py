import threading
import socket

host = '127.0.0.1' #localhost
port = 40132

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
server_password = "RELLSFTW"


credentials_db = {"Dani": "VatraDunarii2016", "PLACEHOLDER_NICKNAME": "CLEAR"}

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
        nickname = "PLACEHOLDER_NICKNAME"
        password = "clear"
        client.send('LOGIN'.encode('ascii'))
        credentials = client.recv(1024).decode('ascii')
        for i, j in enumerate(credentials):
            if j == "/":
                if credentials[i+1] == "S":
                    if credentials[i+2] == "E":
                        if credentials[i+3] == "R":
                            if credentials[i+4] == "V":
                                if credentials[i+5] == "E":
                                    if credentials[i+6] == "R":
                                        if credentials[i+7] == "_":
                                            if credentials[i+8] == "S":
                                                if credentials[i+9] == "E":
                                                    if credentials[i+10] == "P":
                                                        if credentials[i+11] == '/':
                                                            server_sep_index = i
                                                            user_server_password = credentials[server_sep_index+12:-1]
                                                            if not user_server_password == sv_password:
                                                                client.close()
                                                                clients.remove(client)

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
                                                            password = credentials[i+12:server_sep_index]
                                                            nickname = credentials[0:i]
                                                            
        if nickname in credentials_db:
            if credentials_db[nickname] == password:
                print(f"Connected with {str(address)}.")
                nicknames.append(nickname)
                clients.append(client)

                print(f'{nickname} has logged on the server.')
                broadcast(f'{nickname} has joined the chat'.encode('ascii'))
                client.send('Connected to the server.'.encode('ascii'))

                thread = threading.Thread(target = handle, args = (client,))
                thread.start()
            else:
                client.send('LOGIN_ERROR'.encode('ascii'))
        else:
            client.send('LOGIN_ERROR'.encode('ascii'))


receive(server_password)

