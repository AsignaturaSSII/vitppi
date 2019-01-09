# Uso

## Servidor
Para usar el chat de mensajes abre un terminal, busca la ruta donde estén los archivos, y ejecuta:

```
python server.py dirección_ip puerto key

ex: python server.py 10.101.10.11 8180 "mi_key"
```

## Cliente
Tras montar el servidor, abre otro terminal y ejecuta el archivo client.py de la siguiente forma:

```
python client.py dirección_ip(misma arriba) puerto key

ex: python client.py 10.101.10.11 8180 "mi_key"
```

## Extras:

Para obtener tu dirección ip puedes hacerlo con `ifconfig`


