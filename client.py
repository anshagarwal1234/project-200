import socket
import threading

nickname = input("Choose your nickname: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = "127.0.0.1" 
server_port = 8000     

client_socket.connect((server_ip, server_port))

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'NICKNAME':
                client_socket.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred.")
            client_socket.close()
            break
def write():
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))
receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)

receive_thread.start()
write_thread.start()
