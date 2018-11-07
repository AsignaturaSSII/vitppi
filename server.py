# -*- coding: utf-8 -*-
import socket 
import select 
import sys 
from thread import *
from operaciones import * #Importamos el módulo operaciones


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


server.bind((IP_address, Port)) 


server.listen(100) 

list_of_clients = [] 

list_nonce = {}

#Definimos variables
totalMensajes = 0
mensajesCorrectosGlobal = 0
contadorNonceErrorGlobal = 0	
contadorMacErrorGlobal = 0
errorAmbosGlobal = 0
tendencia = 0
porcentajeIntegridadDiario = []



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
	global porcentajeIntegridadDiario
	global tendencia
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
				print "-----------------Indicadores------------------"
				print "Total de mensajes enviados:",totalMensajes
				print "Total de mensajes enviados correctamente:",mensajesCorrectosGlobal

				print "Total de mensajes con error en el nonce:",contadorNonceErrorGlobal
				print "Total de mensajes con error en la mac:",contadorMacErrorGlobal
				print "Total de mensajes con error en la mac y en el nonce:",errorAmbosGlobal
				division = float(mensajesCorrectosGlobal) / float(totalMensajes)
				porcentaje = division*100
				print "Porcentaje de integridad de los mensajes: ",porcentaje

				#creacionFicheroKPI(totalMensajes,mensajesCorrectosGlobal,contadorNonceErrorGlobal,
				#				contadorMacErrorGlobal,errorAmbosGlobal)


				
		
				##Mensajes de despedida:
				print "La conexión con [",addr[0],"] ha concluido."
				
				
				print "Porcentaje de integridad de los mensajes: ",porcentaje
				
				#creamos hilos para automatizar las diferentes tareas
				# t1 crea fichero de kpi cada 24 horas
				# t2 calcula la tendencia mensual sumatorio de porcentajes diarios/30
				# t3 cada 24h añade el porcentaje del dia a una lista global donde se almacenan todos los porcentajes
				# t3 crea un fichero de kpi cada 30 días 
				t1 = threading.Thread(name='creacionFicheroKPIDiario', target=creacionFicheroKPIDiario ,args =(totalMensajes,mensajesCorrectosGlobal,contadorNonceErrorGlobal,
								contadorMacErrorGlobal,errorAmbosGlobal))
				t2 = threading.Thread(name='tendenciaMensual', target=tendenciaMensual,args=(porcentajeIntegridadDiario,tendencia))

				t3 = threading.Thread(name='actualizarTendenciaDiaria', target=actualizarTendenciaDiaria ,
						args=(porcentajeIntegridadDiario,porcentaje))

				t4 = threading.Thread(name='creacionFicheroKPIMensual', target=creacionFicheroKPIMensual ,
						args =(totalMensajes,mensajesCorrectosGlobal,contadorNonceErrorGlobal,
								contadorMacErrorGlobal,errorAmbosGlobal,tendencia))
				t1.start()
				t2.start()
				t3.start()
				t4.start()

			except: 
				continue


def broadcast(message, connection): 
	for clients in list_of_clients: 
		if clients!=connection: 
			try: 
				clients.send(message) 
			except: 
				clients.close() 

				remove(clients) 



def remove(connection): 
	if connection in list_of_clients: 
		list_of_clients.remove(connection) 

while True: 

	
	conn, addr = server.accept() 

	list_of_clients.append(conn) 

	#Muestra la ip del cliente que se ha conectado
	print addr[0] + " connected"
	start_new_thread(clientthread,(conn,addr))	 

conn.close() 
server.close() 

