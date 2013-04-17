#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
# Lopez Aliaume
# 06/04/2013
#
# Un utilitaire de modification
# des fichiers de configuration
#
#
# Ce code a pour vocation d'être simple 
# et compréhensible, afin de servir de modèle
# pour l'utilisation des modules « persistance »
# et l'utilisation des générateurs comme « fsm »
#
#
# Chaque ligne de code est comméntée le mieux possible,
# afin de vous permettre de comprendre les buts et 
# moyens !
#
#
# OBJECTIF: permettre l'édition par un programme des 
# 	variables de configuration, écrites dans des fichiers
# 	« illisibles » par l'utilisateur normal ... Permettant
# 	ainsi de configurer des comportements, en utilisant un 
#	outil adapté, qui empêche de faire n'importe quoi

import persistance
import iconsole


"""
	Une FSM :
		Variables:
			- fichier
		
		États:
			- sélection fichier
				* « help »
				* « entrer »
				* « liste »
			- sélection variable
				+ sélection fichier : « up »
				+ sélection variable :
					* « éditer »
					* « liste »
					* « ou »
					* « help »
"""


def gen_fsm ():
	""" Crée la FSM ... c'est toute la fonction la plus importante """
	
	# Variables de la FSM
	fichier = ""
	st = "menu-fichier"

	
	while True:

		# Là est toute la magnificience 
		# on rend la main avec l'état actuel (comme ça les gens peuvent
		# savoir où on est) 
		# mais la prochaine exécution ... demande une action à faire
		# (et comme la boucle est infinie ... on revient toujours attendre 
		# à ce point exact de la boucle :-P.
		req = (yield st) # on sauve dans une variable 
		
		if st == "menu-fichier": # Si on est dans le menu-fichier les commandes sont 
			if req == "list":
				# On affiche la liste des fichiers 
				# disponnibles 
				iconsole.afficher (st, persistance.liste_fichiers ())
			elif req == "entrer":
				# Yop, on transite vers l'état menu-variable
				# SI ET SEULEMENT SI l'utilisateur 
				# a sélectionné un fichier !!!
				if fichier != "":
					st = "menu-variable"
				else:
					iconsole.afficher (st,"Vous n'avez pas sélectionné un fichier ...")
			elif req == "help":
				# L'aide affiche la liste des commandes possibles 
				iconsole.afficher (st, "Les commandes sont : « quit », « list », « entrer », « help » et @Fichier")
			else: # C'est un nom de fichier 
				# On suppose que si ce n'est pas une commande, 
				# c'est un nom de fichier, et on change donc 
				# le fichier sélectionné
				fichier = req
				iconsole.afficher (st,"Vous avez sélectionné " + req)
				
		else: # il n'existe que deux états, celui là est donc menu-variable
			# On a forcément définit un fichier,
			# vu que l'on ne peut être arrivé à cet état 
			# QUE par une transition !
			if req == "list":
				# On affiche simplement la liste des variables disponnibles 
				iconsole.afficher (st, persistance.liste_variables (fichier))
			elif req == "up":
				# On retourne au menu fichier ... tout con 
				st = "menu-fichier"
			elif req == "ou":
				# On dit à l'utilisateur où il se trouve, c'est à dire le fichier courant 
				iconsole.afficher (st, "Le fichier courant est : "+ fichier)
			elif req == "help":
				# On affiche la liste des commandes disponnibles 
				iconsole.afficher (st, "Les commandes sont : « quit », « ou », « list », « help », « up » et @Variable")
			else: # C'est une variable 
				# On suppose que si ce n'est pas une commande c'est une variable 
				# à modifier ... Donc on demande la nouvelle valeur 
				# et on modifie ... 
				iconsole.afficher (st, "Valeur actuelle : " + str (persistance.get_propriete (fichier,req)))
				
				val = iconsole.demander (st,"Nouvelle valeur : ")
				persistance.set_propriete (f,req,val)
				iconsole.afficher (st,"Bien modifié !")

		

if __name__ == '__main__':

	# On initalise la persistance, pour 
	# avoir accès et charger les fichiers 
	persistance.init ()

	# On crée une machine comme définit en début de fichier 
	machine = gen_fsm ()
	
	st = machine.next () # premier yield, pour savoir le nom de l'état et initialiser le générateur
	
	# La boucle infinie ... moche !
	while True:
		# On actualise l'état courant à chaque
		# tour de boucle ... 
		
		# Un prompt personnalisé, demande une commande 
		req = iconsole.demander (st, "Commande")
		
		# Ici on fait un switch entre les états 
		# C'est là que se déroule toutes les 
		# redirections ... Je ne sais pas trop comment 
		# faire cela autrement :-)
		
		# Quelque soit l'état ... on peut quitter ! :-)
		if req == "quit":
			break # On sort de la boucle, sauve, et quitte le programme 
		
		st = machine.send (req) # on l'envoie à la machine
	# Une fois la boucle terminée, on doit 
	# sauver les modifications (sinon c'est con nan ?)
	persistance.save ()
