#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Un serveur basique
# qui permet de jouer 
# avec un ordinateur 
# distant !
#
# Protocole :
#   Entrées :
# 	  (t)(.*) : chatter (envoyer du texte)
#     (>)(.*) : envoie une réponse au seveur
# 	  (<)(.*) : pose une question au serveur
#     (h)     : demande l'aide
#   Sorties :
#	  (>)(.*) : afficher du texte sur la console du client
#     (t)(.*) : envoyer un message (chat) au client
#	  (<)(.*) : pose une question (attends une réponse)

HOST = 'localhost' # fonctionne ?
PORT = 3500 

import socket, sys, threading

class ClientProtocol:
	def __init__ (self):
		pass
	def parse (self,msg):
		pass
	def send (self,t,msg):
		pass

clients = {} # Tableau des clients

# Thread qui gère un client
class ThreadClient (threading.Thread,ClientProtocol):
	def __init__ (self, conn):
		threading.Thread.__init__ (self)
		ClientProtocol.__init__ (self)

		self.connection = conn # Enregistre la connection client

	def run (self):
		while True:
			m = self.connection.recv (1024)
			print (m.decode ("utf-8"))
			self.connection.send ("Message reçu !".encode ("utf-8"))
			
			for i,j in clients.items ():
				j.send (m)

		self.connection.close ()

class ThreadServeur (threading.Thread):
	def __init__ (self):
		threading.Thread.__init__ (self)
		
		self.mySocket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
		
	def run (self):

		# Création de la SOCKET
		self.mySocket.bind ((HOST, PORT))

		self.mySocket.listen (5)
		# Fin Création SOCKET


		while True: # Accepteur
			connexion, adresse = self.mySocket.accept ()
			th = ThreadClient (connexion)
			th.start ()
			
			clients[th.getName ()] = connexion

if __name__ == '__main__':
	serveur = ThreadServeur ()
	serveur.start ()

