import threading
import socket

username = input('Please enter your username: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))  # connect to the server


#  client receives messages from server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'USERNAME':
                client.send(username.encode('ascii'))  # client send chosen name to server
            else:
                print(message)
        except:
            print('An error occurred, connection closed!')
            client.close()
            break


def write():
    while True:
        message = f'{username}: {input("")}'  # constantly ask user to input new message line by line
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
