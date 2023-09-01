import socket
import threading
import random

IP_ADDRESS = "127.0.0.1"
PORT = 8000

questions = [
    "What is the capital of France?",
    "Which planet is known as the Red Planet?",
    "What is the largest mammal in the world?"
]

answers = [
    "Paris",
    "Mars",
    "Blue Whale"
]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((IP_ADDRESS, PORT))
server_socket.listen(5)

clients = []

def send_instructions(client_socket):
    instructions = "Welcome to the Quiz Game!\nAnswer the questions and earn points.\n"
    instructions += "Type your answer and press Enter to submit.\n"
    client_socket.send(instructions.encode('utf-8'))

def get_random_question_answer(client_socket):
    index = random.randint(0, len(questions) - 1)
    question = questions[index]
    answer = answers[index]
    client_socket.send(question.encode('utf-8'))
    return index, question, answer

def remove_question(index):
    del questions[index]
    del answers[index]

def client_thread(client_socket):
    send_instructions(client_socket)
    score = 0

    while True:
        index, question, answer = get_random_question_answer(client_socket)

        client_answer = client_socket.recv(1024).decode('utf-8')

        if client_answer.strip().lower() == answer.lower():
            score += 1
            client_socket.send(f"Correct! Your score is {score}".encode('utf-8'))
            remove_question(index)
        else:
            client_socket.send("Incorrect. Try the next question.".encode('utf-8'))
            remove_question(index)

        if not questions:
            client_socket.send("Quiz over. Thanks for playing!".encode('utf-8'))
            break

    client_socket.close()
    clients.remove(client_socket)


while True:
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print(f"Connected to {client_address}")
    clients.append(client_socket)
    
    client_thread_handler = threading.Thread(target=client_thread, args=(client_socket,))
    client_thread_handler.start()
