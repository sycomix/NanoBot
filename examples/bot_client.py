import socket

# Put the data into a JSON string
msg = 'Hello, NanoBot!'

# Create TCP socket and send msg
s = socket.socket()         # Create a socket object
host = socket.gethostname()  # 'localhost' #
port = 8008
s.connect((host, port))

s.send(bytes(msg, 'UTF-8'))

s.close()
