# -*- coding: utf-8 -*-
##Este módulo contendrá la programación de todo el código de cifrado tanto del Servidor como del Cliente.
from Crypto.Cipher import DES
import time
import random
import hmac

def getMac(mensaje, key):

    ##Pasamos la clave:
    hmac_new = hmac.new(key)
    ##cipher = DES.new(key)

    ##Una vez con la clave, ciframos el mensaje:
    hmac_new.update(mensaje)
    mac = hmac_new.hexdigest()
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

