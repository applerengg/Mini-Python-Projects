# Server for multithreaded (asynchronous) chat application.

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# client name and client address dicts
clients = {}
addresses = {}

# some constants to use later
HOST = ""
PORT = 33000
BUFSIZ = 4096
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def accept_incoming_connections():
	# sets up handling for incoming clients.
	while True:
		client, client_addr = SERVER.accept()
		print("%s:%s has connected." % client_addr )
		client.send(bytes("Hello Stranger! " + 
			"Please enter your name in the input box below.","utf8"))
		addresses[client] = client_addr
		Thread(target=handle_client, args=(client,)).start()


def handle_client(client):	# takes client socket as argument
	# handles a single client connection.
	name = client.recv(BUFSIZ).decode("utf8")
	welcome = "Welcome %s! When you want to quit, type '*quit' to exit."%name
	client.send(bytes(welcome,"utf8"))
	client.send(bytes("*"*100,"utf8"))

	msg = "***** %s has joined the chat! *****" % name
	broadcast(bytes(msg, "utf8"))
	clients[client] = name
	while True:
		msg = client.recv(BUFSIZ)
		if msg != bytes("*quit", "utf8"):
			broadcast(msg, name+": ")
		else:
			client.send(bytes("*quit", "utf8"))
			client.close()
			del clients[client]
			broadcast(bytes("***** %s has left the chat. *****" % name,
				"utf8"))
			print("%s:%s has disconnected." % addresses[client] )
			del addresses[client]
			break


def broadcast(msg, prefix=""):	# prefix is for name identification
	# broadcasts a message to all clients.
	for sock in clients:
		sock.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
	SERVER.listen(8)	# listens at most 8 connections.
	print("Waiting for connection...")
	ACCEPT_THREAD = Thread(target=accept_incoming_connections)
	ACCEPT_THREAD.start()	# starts the infinite loop
	ACCEPT_THREAD.join()
	SERVER.close()


