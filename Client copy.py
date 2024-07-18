import socket
import threading
from tkinter import *


server_ip = "127.0.0.1"
port = 10000

ip = (server_ip, port)

def connected(sock):
    while True:
        response = sock.recv(2048)
        if response != "":
            print(str(f"{response}"))
        


screen = Tk()
screen.geometry("480x480")
screen.resizable(False, False)


# Create and place the chat area
chat_area = Text(screen, height=15, width=50)
chat_area.grid(row=0, column=1, columnspan=1, padx=35, pady=10)

# Create and place the write area
write_area = Text(screen, height=2, width=30)
write_area.grid(row=1, column=1, columnspan=1, padx=10, pady=10)

button = Button(screen, text="Send Message", command=connected)

# Place the button in the window using grid
button.grid(row=2, column=1, padx=10, pady=10)

button = Button(screen, text="Disconnect")

# Place the button in the window using grid
button.grid(row=3, column=1, padx=10, pady=10)


screen.mainloop()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((server_ip,port))
    thread = threading.Thread(target=connected, args=(sock,))
    thread.start()
    message = input("Your username")
    sock.sendall(bytes(message, "UTF-8"))
    while True:
        sock.sendall(bytes(message, "UTF-8"))
        
    
