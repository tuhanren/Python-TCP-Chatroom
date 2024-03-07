import threading
import socket

host = '127.0.0.1'  # localhost - local desktop
port = 55555  # a free port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creation of socket
server.bind((host, port))  # bind the server with the host
server.listen()  # turn the server to listening mode

clients = []  # all clients connected
usernames = []  # users


def broadcast(message):
    for client in clients:
        client.send(message)


# receive message from a client and broadcast to all other clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            usernames.remove(username)
            broadcast(f'{username} has left the chat.'.encode('ascii'))
            break


# receive method
def receive():
    while True:
        client, address = server.accept()  # accept clients connection
        print(f'{str(address)} connection established.')  # notice on the server console

        client.send('USERNAME'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        print(f'Client name is {username}')  # notice on the server console
        broadcast(f'{username} is connected to the chat!'.encode('ascii'))  # notice the chat room members
        client.send('You are connected to the chat room!'.encode('ascii'))  # notice the new joined client

        thread = threading.Thread(target=handle, args={client})
        thread.start()


print('Chat server is on...')
receive()