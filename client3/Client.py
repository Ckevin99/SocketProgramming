import socket
import threading
from tkinter import *
import tkinter as tk
import sys
import rsa

with open("private.pem", "rb") as r:
    private_key = rsa.PrivateKey.load_pkcs1(r.read())
with open("public.pem", "rb") as r:
    public_key = rsa.PublicKey.load_pkcs1(r.read())


screen = Tk()
screen.geometry("480x480")
screen.resizable(False, False)
username_text = Label(screen, height=1,text="nickname", width=15)
username_text.place(relx=0.5, rely=0.1, anchor="center")


username_area = Text(screen, height=1, width=15)
username_area.place(relx=0.5, rely=0.2, anchor="center")


ip_text = Label(screen, height=1,text="ip", width=15)
ip_text.place(relx=0.5, rely=0.3, anchor="center")

ip_area = Text(screen, height=1, width=15)
ip_area.place(relx=0.5, rely=0.4, anchor="center")


port_text = Label(screen, height=1,text="port", width=15)
port_text.place(relx=0.5, rely=0.5, anchor="center")

port_area = Text(screen, height=1, width=15)
port_area.place(relx=0.5, rely=0.6, anchor="center")





def generate():
    server_ip = ip_area.get("1.0", "end-1c")
    port = int(port_area.get("1.0", "end-1c"))

    ip = (server_ip, port)

        
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip,port))
    public_key_pem = public_key.save_pkcs1(format='PEM')
    sock.sendall((public_key_pem))
    server_pb = sock.recv(4096)
    server_pb = rsa.PublicKey.load_pkcs1(server_pb, format='PEM')

    
    #  encript = message.encode()
    #         encript= rsa.encrypt(encript,connections[con][1])
    #         print("live2")
    #         print(encript)
    #         con.sendall(encript)
    message = username_area.get("1.0", "end-1c")
    message = message.encode()
    encript = rsa.encrypt(message,server_pb)
    sock.sendall(encript)



    username_text.destroy()
    buttonc.destroy()
    username_area.destroy()
    ip_text.destroy()
    ip_area.destroy()
    port_text.destroy()
    port_area.destroy()
    # Create and place the chat area


    chat_area = Text(screen, height=15, width=50)
    chat_area.grid(row=0, column=1, columnspan=1, padx=35, pady=10)

    # Create and place the write area
    write_area = Text(screen, height=2, width=30)
    write_area.grid(row=1, column=1, columnspan=1, padx=10, pady=10)
    def sendmessage(event=None):
            message = write_area.get("1.0", "end-1c")
            message = message.encode("utf-8")
            message = rsa.encrypt(message, server_pb)                
            sock.sendall(message)
            write_area.delete("1.0", tk.END)
            pass
    def connected(sock):
        while True:
            response = sock.recv(4096)
            if response != "":

                response = rsa.decrypt(response, private_key)                  
                chat_area.insert(tk.END, response)
                chat_area.insert(tk.END, "\n")
    button = Button(screen, text="Send Message", command=sendmessage)
    thread = threading.Thread(target=connected, args=(sock,))
    thread.start()
    screen.bind('<Return>', sendmessage)
    def quit():
        sock.sendall(bytes("/quit", "UTF-8"))
        sock.close()
        sys.exit()
        pass


    # Place the button in the window using grid
    button.grid(row=2, column=1, padx=10, pady=10)

    buttonquit = Button(screen, text="Disconnect", command=quit)

    # Place the button in the window using grid
    buttonquit.grid(row=3, column=1, padx=10, pady=10)



buttonc = Button(screen, text="Connect", command=generate)


buttonc.place(relx=0.5, rely=0.7, anchor="center")
screen.mainloop()




        
    
