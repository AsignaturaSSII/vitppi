# -*- coding: utf-8 -*-
##Este módulo contendrá la programación de todo el código de cifrado tanto del Servidor como del Cliente.
from Crypto.Cipher import DES

def getMac(mensaje, key):

    ##Pasamos la clave:
    cipher = DES.new(key)

    ##Una vez con la clave, ciframos el mensaje:
    mac = cipher.encrypt(mensaje)

    ##Unimos mensaje + mac: 
    #res_ret = mensaje + ":" + mac

    return mac

def getNonce():

    return null

def compareMac(mac1, mac2):
    return mac1 == mac2

def unirOSepararMacYMensaje(mensaje, mac, unir):
    res_ret = []
    if unir:
        aux_mensaje = mensaje + ":" + mac
        res_ret.append(aux_mensaje)
        print "El resultado de unirOSepararMacYMensaje(mensaje, mac, True) es: Mensaje["+ res_ret[0] + "]"
    
    else:
        aux_mensaje = mensaje.split(":")
        res_ret.append(aux_mensaje[0])
        res_ret.append(aux_mensaje[1])
        print "El resultado de unirOSepararMacYMensaje(mensaje, mac, False) es: Mensaje["+ res_ret[0] + "] y Mac["+ res_ret[1] +"]"
    return res_ret

