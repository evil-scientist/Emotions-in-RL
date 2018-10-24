import socket
#from util import check_exit, encrypt, decrypt
import sys


HOST = '127.0.0.1'
PORT = 4000


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	print("Socket Connected.")
	print("Enter # to disconnect....")
	while (1):
		print("Client:")
		d = str.encode(input())
		s.sendall(d)#s.sendall(encrypt(d))
		# check_exit(d)
		data = s.recv(1024)#data = decrypt(s.recv(1024))
		print("Server:", data.decode())
		#check_exit(data)
