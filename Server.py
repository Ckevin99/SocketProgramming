import socket
import threading
import rsa

with open("private.pem", "rb") as r:
    private_key = rsa.PrivateKey.load_pkcs1(r.read())


with open("public.pem", "rb") as r:
    public_key = rsa.PublicKey.load_pkcs1(r.read())






server_ip = "127.0.0.1"
port = 10000

ip = (server_ip, port)
connections = {}
lock = threading.Lock()

def returnmessage(message):

    with lock:
        for con in connections.keys():
            print("live")
            encript = message.encode()
            encript= rsa.encrypt(encript,connections[con][1])
            print("live2")
            print(encript)
            con.sendall(encript)
            

def connected(sock, connection, address):

    pk = connection.recv(4096)

    pk= rsa.PublicKey.load_pkcs1(pk, format='PEM')

    server_public_key = public_key.save_pkcs1(format='PEM')

    connection.sendall(server_public_key)

    
    
    with lock:
        connections[connection] = [address, pk]
    
        nickname = connection.recv(4096)
        nickname = rsa.decrypt(nickname, private_key)
        nickname = nickname.decode("utf-8")



    while True:
        data = connection.recv(4096)
        try:
            data = rsa.decrypt(data, private_key)

        except rsa.pkcs1.DecryptionError as e:
            print(f"Decryption failed: {e}")
        data = data.decode("utf-8")
        

        if data == "/quit":
            connections.pop(connection)
            message = f"{nickname} leaved the chat"
            returnmessage(message)
            return

        
        message = f"{nickname} - {data}"
        returnmessage(message)
        


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((server_ip,port))
    while True:
        sock.listen()
        connection, address = sock.accept()
        print(f"Server listening in port :{port}")
        thread = threading.Thread(target=connected, args=(sock,connection, address))
        thread.start()

