#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Un serveur basique
# qui permet de jouer 
# avec un ordinateur 
# distant !
#
# Protocole :
#   Entrées (Client envoie) :
# 	  (t)(.*) : chatter (envoyer du texte)
# 	  (<)(.*) : commande (demande un truc au serveur)
#   Sorties (Client reçoit) :
#	  (t)(.*) : chatter (le serveur envoie du texte)
#	  (>)[(.+)](*.) : le serveur répond (\1 : état, \2, réponse)
#

HOST = 'localhost' # fonctionne ?
PORT = 3500 

import socket, sys, threading, json

class ClientProtocol:
	""" Protocole basique de comunication avec 
		le client, met en place toutes les fonctions
		bas niveau pour communiquer, permettant une 
		abstraction des choses comme l'encodage, 
		la gestion des autres clients etc ...
	"""
	messages = [] # Liste des messages
	users = {} # Users ...
	def __init__ (self,identifiant,connexion):
		
		self.identifiant = identifiant
		self.connexion = connexion
		
		ClientProtocol.users[identifiant] = connexion

	def receive (self):
		m = self.connexion.recv (1024).decode ("utf-8")
		try:
			return json.loads (m)
		except:
			return m

	def broadcast (self,msg):
		for i,j in ClientProtocol.users.items ():
			if i != self.identifiant:
				self.send (j,msg)

	def send (self,conn,msg):
		try:
			conn.send (json.dumps (msg).encode ("utf-8"))
		except:
			conn.send (msg.encode ("utf-8"))

	def reply (self,msg):

		self.send (self.connexion, msg)

# Thread qui gère un client
class ThreadClient (threading.Thread,ClientProtocol):
	""" Thread qui gère la connexion avec un client,
		c'est tout ce qui fait le lien entre 
		le client et le serveur
	"""
	def __init__ (self, conn):
		threading.Thread.__init__ (self)

		ClientProtocol.__init__ (self, self.getName (), conn)

	def run (self):
		while True:
			m = self.receive () # Attends une reponse !
			
			try:
				context,message = m
			except:
				break # Message invalide

			if context == "request": # Le client fait une requête
				# Insérer une state machine ici 
				self.reply (["response","Etat","Message"])
			elif context == "chat": # Le client veut chatter
				self.broadcast (["chat",message])
			else:
				print ("Mauvaise gestion des paquets ...")
				break # Quitte la boucle, on suppose qu'une mauvaise gestion est fatale
		self.connexion.close ()

class ThreadServeur (threading.Thread):
	""" Thread du serveur .... C'est tout ce qui 
		est au niveau de la gestion de 
		la réception des clients et du démarrage 
		de nouveaux threadsClients
		
		Il possède donc la Socket
	"""
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
			

if __name__ == '__main__':
	serveur = ThreadServeur ()
	serveur.start ()

