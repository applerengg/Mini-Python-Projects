# Script for Tkinter GUI chat client.

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from random import choice

NUM_MESSAGES = 2
POSSIBLE_COLORS = ["#0000bf","#0000ff","#00bf00","#00ff00","#bf0000",
	"#ff0000","#00bfff","#bf00ff","#bfff00","#00ffbf","#ff00bf","#ffbf00"]

def receive():
	# Handles receiving of messages
	while True:
		try:
			msg = client_socket.recv(BUFSIZ).decode("utf8")
			msg_list.insert(tkinter.END, msg)
			global NUM_MESSAGES
			NUM_MESSAGES += 1
			msg_list.see(NUM_MESSAGES)
		except OSError:	# Possibly client has left the chat
			break


def send(event=None):	# event is passed by binders 
	# Handles sending of messages
	msg = my_msg.get()
	my_msg.set("")	# clears input field
	client_socket.send(bytes(msg, "utf8"))
	if msg == "*quit":
		#client_socket.close()
		top.quit()


def on_closing(event=None):
	# This function is to be called when the window is closed
	my_msg.set("*quit")
	send()

# top level widget:
top = tkinter.Tk()
top.title("Mesajlaşma")

# frame for holding list of messages and string variable for message
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()	# for the messages to be sent
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)	# to navigate through messages.	

# create message list and pack everything
LISTBOX_HEIGHT = 20
LISTBOX_WEIGHT = 100
msg_list = tkinter.Listbox(messages_frame, height=LISTBOX_HEIGHT,
	width=LISTBOX_WEIGHT, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()	


# create input field and bind it to the string variable above
entry_field = tkinter.Entry(top, textvariable=my_msg, width=30)
entry_field.bind("<Return>", send)	# send message when pressed enter
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send,	# send message
	height=2, width=30)	                                 # when clicked button 
                                                         
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)


# connecting to the server: ---sockets part---
HOST = input("Enter host:")
PORT = input("Enter port:")
if not PORT:
	PORT = 33000	# default value.
else:
	PORT = int(PORT)
if not HOST:
	HOST = "127.0.0.1"

BUFSIZ = 4096
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()	# starts GUI execution

