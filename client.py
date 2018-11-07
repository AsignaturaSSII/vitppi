# -*- coding: utf-8 -*- 
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
nonce_aux = ""
mensaje_enviado = False

while True: 


	sockets_list = [sys.stdin, server] 

	
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

	for socks in read_sockets: 
		if socks == server: 
			##Recibimos el mensaje de bienvenida del servidor junto con el NONCE que ya nos viene 
			##tras hacer la primera conexión
			message = socks.recv(2048) 
			print message.split("-")[0] 
			##GET al NONCE:
			#En el mensaje de bienvenida nos manda el nonce también
			nonce_aux = message.split("-")[1]
			print "nonce => ",nonce_aux
		else: 
			message = sys.stdin.readline() 
			message_aux = message+":"+nonce_aux

			##Aquí debemos meter la función getMac(mensaje, key)
			mac = getMac(str(message), str(Key))
			print "El mac es: "+mac
			print "La key es => ",Key
			print "Mensaje que se cifra => ",message
			
			#Unimos el HMAC, el mensaje y el NONCE
			unir = unirOSepararMacYMensaje(message, mac, nonce_aux, True)
			print "La unión del mac, el mensaje y el nonce es: "+unir[0]
			
			#Enviamos los datos al servidor
			server.send(unir[0]) 
			sys.stdout.write("Transacción realizada correctamente.\n") 
			sys.stdout.write("Muchas gracias por usar VITPPI para mejorar su seguridad.\n") 
			sys.stdout.write("Conexión terminada.\n")
			mensaje_enviado = True
			sys.stdout.flush() 
	if mensaje_enviado:
		break
server.close()  

