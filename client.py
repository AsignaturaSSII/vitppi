# -*- coding: utf-8 -*-
# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
from operaciones import * #Importamos el módulo operaciones

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 4: 
	print "[ERROR] La sintáxis escrita es incorrecta. Pruebe con: 'python ip.value port.value key.value'"
	exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
Key = sys.argv[3]
server.connect((IP_address, Port)) 

while True: 

	# maintains a list of possible input streams 
	sockets_list = [sys.stdin, server] 

	""" There are two possible input situations. Either the 
	user wants to give manual input to send to other people, 
	or the server is sending a message to be printed on the 
	screen. Select returns from sockets_list, the stream that 
	is reader for input. So for example, if the server wants 
	to send a message, then the if condition will hold true 
	below.If the user wants to send a message, the else 
	condition will evaluate as true"""
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

	for socks in read_sockets: 
		if socks == server: 
			##Del servidor nunca se van a recibir datos realmente. No sé si es buena idea dejarlo así o poner otra cosa.
			##ya que también tenemos que tener en cuenta que puede llegar algún mensaje del Servidor y por tanto, debemos
			##lanzar una excepción
			message = socks.recv(2048) 
			print message 
		else: 
			message = sys.stdin.readline() 
			##Aquí debemos meter la función getMac(mensaje, key)
			mac = getMac(message, Key)
			print "El mac es: "+mac

			unir = unirOSepararMacYMensaje(message, mac, True)
			print "La unión del mac y el mensaje es: "+unir[0]

			##Unimos el mensaje y el mac en un mismo texto con un carácter especial, ':'
			#res_ret = mensaje + ":" + mac
			server.send(message) 
			sys.stdout.write("<You>") 
			sys.stdout.write(message) 
			sys.stdout.flush() 
server.close() 

