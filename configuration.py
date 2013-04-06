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
# et « fsm » de mon cru !
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
import fsm


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

def fichier_variable (m):
	""" Éffectue la transition 
		de la sélection du fichier vers la 
		sélection de la variable 
		
		@m : fsm = la machine qui effectue la transition

		@return : None
	"""
	# On prend le fichier sélectionné
	# dans l'état « menu-fichier »
	f = fsm.get_state_property (m,"fichier")
	
	iconsole.afficher ("Main","Vous avez sélectionné le fichier " + f)
	iconsole.afficher ("Main","Vous êtes maintenant dans le menu « variable »")
	
	# Et on le définit comme une propriété
	# globale à tous les états (accessible partout)
	# car les variables d'état sont DÉTRUITES
	# après chaque transition !
	fsm.set_special_property (m,"fichier",f)
	
def variable_fichier (m):
	""" Effectue la transition de
		la sélection des variables à
		la sélection des fichiers

		@m : fsm = la machine qui effectue la transition

		@return : None
	"""
	# On informe juste que l'on revient dans le menu-fichier ... 
	# rien de bien complexe 
	iconsole.afficher ("Main","Vous êtes maintenant dans le menu « fichier »")

if __name__ == '__main__':

	# On initalise la persistance, pour 
	# avoir accès et charger les fichiers 
	persistance.init ()

	# On crée une machine comme définit en début de fichier 
	machine = fsm.new ()
	
	# On définit les transitions possibles entre les états 
	# Si les états n'existent pas, fsm les crée !!
	# « état de départ » -> transition -> « état d'arrivée »
	# transition est une fonction qui prend en argument
	# la machine qui effectue la transition, AVANT
	# que le changement d'état ai lieu !
	fsm.set_transition (machine, "menu-fichier","menu-variable", fichier_variable)
	fsm.set_transition (machine, "menu-variable","menu-fichier", variable_fichier)
	
	# On définit l'état de départ !
	# L'état sans rien étant « None »
	# Aucune fonction de transition n'est déclenchée
	# (logique ...)
	fsm.transition (machine, "menu-fichier")
	
	# La boucle infinie ... moche !
	while True:
		# On actualise l'état courant à chaque
		# tour de boucle ... 
		
		st = fsm.get_state (machine)
		
		# Un prompt personnalisé, demande une commande 
		req = iconsole.demander (st, "Commande : ")
		
		# Ici on fait un switch entre les états 
		# C'est là que se déroule toutes les 
		# redirections ... Je ne sais pas trop comment 
		# faire cela autrement :-)
		
		# Quelque soit l'état ... on peut quitter ! :-)
		if req == "quit":
			break # On sort de la boucle, sauve, et quitte le programme 
		
		
		# Ici on définit les deux menus possibles
		# En prenant les réactions aux évènements 
		# En fonction de l'état de la machine
		if st == "menu-fichier": # Si on est dans le menu-fichier les commandes sont 
			if req == "list":
				# On affiche la liste des fichiers 
				# disponnibles 
				iconsole.afficher (st, persistance.liste_fichiers ())
			elif req == "entrer":
				# Yop, on transite vers l'état menu-variable
				# SI ET SEULEMENT SI l'utilisateur 
				# a sélectionné un fichier !!!
				if fsm.get_state_property (machine, "fichier") != "":
					fsm.transition (machine,"menu-variable")
				else:
					iconsole.afficher (st,"Vous n'avez pas sélectionné un fichier ...")
			elif req == "help":
				# L'aide affiche la liste des commandes possibles 
				iconsole.afficher (st, "Les commandes sont : « quit », « list », « entrer », « help » et @Fichier")
			else: # C'est un nom de fichier 
				# On suppose que si ce n'est pas une commande, 
				# c'est un nom de fichier, et on change donc 
				# le fichier sélectionné
				fsm.set_state_property (machine,"fichier",req)
				iconsole.afficher (st,"Vous avez sélectionné " + req)
				
		else: # il n'existe que deux états, celui là est donc menu-variable
			# On a forcément définit un fichier,
			# vu que l'on ne peut être arrivé à cet état 
			# QUE par une transition !
			
			# On récupère le fichier à éditer ... 

			f = fsm.get_special_property (machine, "fichier")
			if req == "list":
				# On affiche simplement la liste des variables disponnibles 
				iconsole.afficher (st, persistance.liste_variables (f))
			elif req == "up":
				# On retourne au menu fichier ... tout con 
				fsm.transition (machine,"menu-fichier")
			elif req == "ou":
				# On dit à l'utilisateur où il se trouve, c'est à dire le fichier courant 
				iconsole.afficher (st, "Le fichier courant est : "+ f)
			elif req == "help":
				# On affiche la liste des commandes disponnibles 
				iconsole.afficher (st, "Les commandes sont : « quit », « ou », « list », « help », « up » et @Variable")
			else: # C'est une variable 
				# On suppose que si ce n'est pas une commande c'est une variable 
				# à modifier ... Donc on demande la nouvelle valeur 
				# et on modifie ... 
				iconsole.afficher (st, "Valeur actuelle : " + persistance.get_propriete (f,req))
				
				val = iconsole.demander (st,"Nouvelle valeur : ")
				persistance.set_propriete (f,variable,val)
				iconsole.afficher (st,"Bien modifié !")
	
	# Une fois la boucle terminée, on doit 
	# sauver les modifications (sinon c'est con nan ?)
	persistance.save ()
