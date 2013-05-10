#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Un serveur basique
# qui permet de jouer 
# avec un ordinateur 
# distant !
#
# Protocole :
#	(>)(.*) : afficher du texte sur la console
#   (<)(.*) : pose une question (attends une réponse)
#   (h)     : retourne une liste de commandes disponibles

HOST = 'localhost' # fonctionne ?
PORT = 3500 

import socket, sys, threading

clients = {} # Tableau des clients

# Thread qui gère un client
class ThreadClient (threading.Thread):
	def __init__ (self, conn):
		threading.Thread.__init__ (self)
		self.connection = conn # Enregistre la connection client

	def run (self):
		while True:
			m = self.connection.recv (1024)
			print (m)
			self.connection.send ("Message reçu !")
		
		self.connection.close ()

# Création de la SOCKET
mySocket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind ((HOST, PORT))

mySocket.listen(5)
# Fin Création SOCKET


while True: # Accepteur
	connexion, adresse = mySocket.accept ()
	th = ThreadClient (connexion)
	th.start ()
	
	clients[th.getName ()] = connexion
