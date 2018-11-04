# -*- coding: utf-8 -*-
# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
from thread import *
from operaciones import * #Importamos el módulo operaciones

"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# checks whether sufficient arguments have been provided 
if len(sys.argv) != 4: 
	print "[ERROR] La sintáxis escrita es incorrecta. Pruebe con: 'python ip.value port.value key.value'"
	exit() 

# takes the first argument from command prompt as IP address 
IP_address = str(sys.argv[1]) 

# takes second argument from command prompt as port number 
Port = int(sys.argv[2]) 

Key = sys.argv[3]

""" 
binds the server to an entered IP address and at the 
specified port number. 
The client must be aware of these parameters 
"""
server.bind((IP_address, Port)) 

""" 
listens for 100 active connections. This number can be 
increased as per convenience. 
"""
server.listen(100) 

list_of_clients = [] 

list_nonce = {}

totalMensajes = 0
mensajesCorrectosGlobal = 0
contadorNonceErrorGlobal = 0	
contadorMacErrorGlobal = 0
errorAmbosGlobal = 0

def clientthread(conn, addr): 

	# sends a message to the client whose user object is conn
	nonce = getNonce() 
	list_nonce[addr[0]] = nonce
	print "Mostramos la lista => ",list_nonce
	bienvenida = "Welcome to this chatroom!-"+str(nonce)
	print "mensaje de bienvenida => ",bienvenida
	conn.send(bienvenida) 
	contadorNonceError = 0 
	mensajesCorrectos = 0
	contadorMacError = 0
	macCorrecto = False
	nonceCorrecto = False
	mensajesEnviadosTotales = 0
	errorAmbos = 0
	global totalMensajes 
	global contadorNonceErrorGlobal
	global contadorMacErrorGlobal
	global errorAmbosGlobal
	global mensajesCorrectosGlobal

	while True: 
			try: 
				message = conn.recv(2048)
				##Aquí debemos partir el mensaje y el mac de tal forma que podamos comprobar todo.
				separar = unirOSepararMacYMensaje(message,"","",False)
				
				#Realizamos la comprobación del NONCE
				if int(separar[2]) == int(list_nonce.get(addr[0])):
					print "El nonce es correcto"
					nonceCorrecto = True
				else: 
					print "El nonce es incorrecto"
					##CARLOS: Aquí debes tener en cuenta de coger un valor para saber que el nonce no es correcto

				##Obtenemos la mac del mensaje
				#Con la función strip(" ") lo que hacemos es quitar los espacios de los String.
				mac = getMac(str(separar[0].strip(" ")),str(Key.strip("")))
				print "Mensaje que se cifra => [",separar[0].strip(" "),"]"
				print "Cifrado con la clave => ",Key
				print "Mac nueva => ",mac
				print "Mac de la lista => [",separar[1],"]"

				##Comparamos la mac
				##Damos el veredicto de la mac
				if(mac == separar[1]):
					print "Las macs son iguales"
					macCorrecto = True
				else:
					print "Las macs son diferentes"
					##CARLOS: Aquí ocurre parecido a lo del NONCE

				##Actualizar indicadoress de verificación
				##mensaje correcto
				if((macCorrecto == True) and (nonceCorrecto == True)):
					mensajesCorrectos += 1
				elif((macCorrecto == True) and (nonceCorrecto == False)):
					contadorNonceError += 1
				elif((macCorrecto == False ) and (nonceCorrecto == True)):
					contadorMacError += 1
				elif((macCorrecto == False) and (nonceCorrecto == False)):
					errorAmbos += 1
				totalMensajes = totalMensajes + mensajesCorrectos + contadorNonceError + contadorMacError + errorAmbos
				mensajesCorrectosGlobal = mensajesCorrectosGlobal + mensajesCorrectos
				contadorNonceErrorGlobal = contadorNonceErrorGlobal + contadorNonceError
				contadorMacErrorGlobal = contadorMacErrorGlobal + contadorMacError
				errorAmbosGlobal = errorAmbosGlobal + errorAmbos
				print "-----------------Validadores------------------"
				print "Total de mensajes enviados:",totalMensajes
				print "Total de mensajes enviados correctamente:",mensajesCorrectosGlobal

				print "Total de mensajes con error en el nonce:",contadorNonceErrorGlobal
				print "Total de mensajes con error en la mac:",contadorMacErrorGlobal
				print "Total de mensajes con error en la mac y en el nonce:",errorAmbosGlobal


				

				##Mensajes de despedida:
				print "La conexión con [",addr[0],"] ha concluido."
			except: 
				continue

"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, connection): 
	for clients in list_of_clients: 
		if clients!=connection: 
			try: 
				clients.send(message) 
			except: 
				clients.close() 

				# if the link is broken, we remove the client 
				remove(clients) 

"""The following function simply removes the object 
from the list that was created at the beginning of 
the program"""
def remove(connection): 
	if connection in list_of_clients: 
		list_of_clients.remove(connection) 

while True: 

	"""Accepts a connection request and stores two parameters, 
	conn which is a socket object for that user, and addr 
	which contains the IP address of the client that just 
	connected"""
	conn, addr = server.accept() 

	"""Maintains a list of clients for ease of broadcasting 
	a message to all available people in the chatroom"""
	list_of_clients.append(conn) 

	# prints the address of the user that just connected 
	print addr[0] + " connected"

	# creates and individual thread for every user 
	# that connects 
	start_new_thread(clientthread,(conn,addr))	 

conn.close() 
server.close() 

