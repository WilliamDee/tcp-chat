from socket import *
import threading

HOST = 'localhost'
PORT = 55555
ADDR = (HOST, PORT)

nickname = input('input a nickname: ')

client = socket(AF_INET, SOCK_STREAM)
client.connect(ADDR)
client.send(nickname.encode())

def receive():
	while True:
		try:
			message = client.recv(1024).decode()
			print(message)
		except:
			print("An error occured!")
			client.close()
			break

def send():
	while True:
		message = input('')
		client.send(message.encode())

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=send)
write_thread.start()