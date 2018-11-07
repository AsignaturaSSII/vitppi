# -*- coding: utf-8 -*-
##Este módulo contendrá la programación de todo el código de cifrado tanto del Servidor como del Cliente.
from Crypto.Cipher import DES
import time
import random
import hmac
import hashlib, binascii
import os
import time
import threading

def getMac(mensaje, key):

    ##Pasamos la clave:
    ##hmac_new = hmac.new("holaa")
    ##cipher = DES.new(key)

    ##Una vez con la clave, ciframos el mensaje:
    ##hmac_new.update(mensaje)
    ##mac = hmac_new.digest()

    b = key.encode()
    print "Key en Bytes => [",b,"]"
    s = mensaje.encode()
    print "Mensaje en Bytes => [",s,"]"
    dk = hashlib.pbkdf2_hmac('sha256', b, s, 100000)
    return binascii.hexlify(dk)
    ##mac = cipher.encrypt(mensaje)

    ##Unimos mensaje + mac: 
    #res_ret = mensaje + ":" + mac

    return mac

def getNonce():
    year = int(time.strftime("%Y"))
    #month = int(time.strftime("%B"))
    day = int(time.strftime("%d"))
    hour = int(time.strftime("%H"))
    minutes = int(time.strftime("%M"))
    seconds = int(time.strftime("%S"))
    numero_random = random.randrange(10000)
    res_ret = year * day * hour * minutes * seconds * numero_random
    print "año => ",year
    #print "month => ",month
    print "day => ",day
    print "hour => ",hour
    print "minutes => ",minutes
    print "seconds => ",seconds
    print "Nonce => ",res_ret
    return res_ret

def compareMac(mac1, mac2):
    return mac1 == mac2

def unirOSepararMacYMensaje(mensaje, mac, nonce, unir):
    res_ret = []
    if unir:
        aux_mensaje = mensaje + ":" + mac + ":" + nonce
        res_ret.append(aux_mensaje)
        print "El resultado de unirOSepararMacYMensaje(mensaje, mac, True) es: Mensaje["+ res_ret[0] + "]"
    
    else:
        aux_mensaje = mensaje.split(":")
        res_ret.append(aux_mensaje[0]) #Mensaje
        res_ret.append(aux_mensaje[1]) #MAC
        res_ret.append(aux_mensaje[2]) #Nonce
        print "El resultado de unirOSepararMacYMensaje(mensaje, mac, False) es: Mensaje["+ res_ret[0] + "] y Mac["+ res_ret[1] +"]"
    return res_ret

    #Crea el fichero con el número de mensajes enviados,errores, el porcentaje de integridad

def creacionFicheroKPIDiario(totalMensajes,mensajesCorrectos,contadorNonceError,
								contadorMacError,errorAmbos):
    while True:
    
        time.sleep(30)    #cada dia crea este archivo                       
        ahora = time.strftime("%c")
        division = float(mensajesCorrectos) / float(totalMensajes)
        porcentaje = division * 100

        file = open("./KPIDocument"+ahora+".txt", "w")

        file.write("Nº de mensajes enviados en total: " + str(totalMensajes) + os.linesep)
        file.write("Nº de mensajes con errores en la mac: " +str(contadorMacError)  + os.linesep)
        file.write("Nº de mensajes con errores en el nonce: " + str(contadorNonceError) + os.linesep)
        file.write("Nº de mensajes con errores en el nonce y en el mac: " + str(errorAmbos) + os.linesep)
        file.write("Nº de mensajes enviados correctamente: " +str(mensajesCorrectos) + os.linesep)
        file.write("Porcentaje de integridad de los mensajes: " +str(porcentaje) +  os.linesep)
        file.close()
        

def creacionFicheroKPIMensual(totalMensajes,mensajesCorrectos,contadorNonceError,
								contadorMacError,errorAmbos,tendencia):
    while True:
    
        time.sleep(400)    #cada mes crea este archivo
        print "-----------------La tendencia para mensual es:----------------",tendencia                      
        ahora = time.strftime("%c")
        division = float(mensajesCorrectos) / float(totalMensajes)
        porcentaje = division * 100

        file = open("./KPIDocumentMensual"+ahora+".txt", "w")

        file.write("Nº de mensajes enviados en total: " + str(totalMensajes) + os.linesep)
        file.write("Nº de mensajes con errores en la mac: " +str(contadorMacError)  + os.linesep)
        file.write("Nº de mensajes con errores en el nonce: " + str(contadorNonceError) + os.linesep)
        file.write("Nº de mensajes con errores en el nonce y en el mac: " + str(errorAmbos) + os.linesep)
        file.write("Nº de mensajes enviados correctamente: " +str(mensajesCorrectos) + os.linesep)
        file.write("Porcentaje de integridad de los mensajes(Tendencia): " +str(tendencia) +  os.linesep)
        file.close()
        print "------------------------------KPI MENSUAL CREADO-----------------"

#TODO esto me queda de codigo
def actualizarTendenciaDiaria(lista,porcentaje):

    while True:
        time.sleep(10) #un dia,para la prueba actualizamos cada 10 segundos 
        lista.append(porcentaje)
        print "Actualizacion Diaria realizada",porcentaje

def tendenciaMensual(lista,tendencia):
    sumatorio = 0
    res = 0
    while True:
        time.sleep(10*30 ) #1mes
        for porcentaje in range(len(lista) - 30,len(lista)):
            sumatorio += lista[porcentaje]
        tendencia = sumatorio/30.0
        
        print "Actualizacion Mensual realizada"

        
    

        
