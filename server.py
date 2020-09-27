from socket import *
import threading

HOST = ''
PORT = 55555
ADDR = (HOST, PORT)

server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)
server.listen()

clients = {}

def send_all(message, sender=None):
	try:
		byte_format = type(message) == bytes
		if sender:
			header = f'{sender}: '
			if byte_format: header = header.encode()
			message = header + message
		if not byte_format: message = message.encode()
		for client in clients:
			client.send(message)
	except Exception as e:
		print(f'Unable to send message. Error {str(e)}')


def receive_message(client):
	while True:
		try:
			message = client.recv(2048)
			send_all(message, clients[client])
		except Exception as e:
			print(str(e))
			send_all(f'disconnected {clients[client]} from chatroom')
			del clients[client]
			break

def open():
	print("Server listening...")
	while True:
		client, addr = server.accept()
		print(f'User with {addr} has joined.')
		nickname = client.recv(1024).decode()
		clients[client] = nickname

		send_all(f'{nickname} has joined the chatroom')
		print(clients)
		thread = threading.Thread(target=receive_message, args=(client,))
		thread.start()

open()