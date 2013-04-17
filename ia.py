#-*- coding: utf-8 -*-
# Les fonctions de l'ia
# ...

import couleurs
import moteur
import iconsole
import persistance
import chargement
from turtle import goto
from random import choice # faire un choix aléatoire dans une liste 

def generer_couleurs_aleatoires ():
	""" Génère un code aléatoire de couleurs, complètement !

		@return : list of couleurs (Français)
	"""

	sortie = [] # le tableau de sortie 

	# On récupère la liste des couleurs possibles
	lst = couleurs.liste_couleurs ()

	# On récupère le nombre de cases demandées
	n = persistance.get_propriete ("config","nombre_cases")

	# On définit n couleurs au hasard ... 
	for i in xrange (int (n)):
		sortie.append (choice (lst))
	
	return sortie
	
def create_list(S):
	"""Créé une liste de toutes les combinaison possibles des objets dans S (une même couleur peux se retrouver plusieurs fois)
		len(li) = n^(4) à l'issue de cette fonction (où n est len(S))
		
		@S : list = L'univers, l'ensemble des possibilités, pour le mastermind, le nombre de couleurs
		@return : list = li la liste de toutes les combinaison
	"""
	li=[]
	for i in S:
		temp = [0,0,0,0]
		temp[0] = i
		for j in S:
			temp[1] = j
			for k in S:
				temp[2] = k
				for l in S:
					temp[3] = l
					li.append(list(temp))
	return li

# L'IA définit le code 
def choisir_code (mode="aleatoire"):
	""" Définit le code à trouver pour la partie 
		de mastermind, de manière aléatoire 

		@return : None
	"""
	
	# les fonctions définies ici ne sont pas visibles 
	# depuis l'extérieur ! C'est le but !

	def ia_alea ():
		# BRUTE FORCE !!!!
		# On crée des listes aléatoires 
		# et on teste, jusqu'au jour où
		# le code secret proposé est valide 
		# par rapport à la difficulté 
		condition = True
	
		while condition:
			r = moteur.definir_code (generer_couleurs_aleatoires ())
			if r != False:
				condition = False

	# fin def ia_alea ici 

	if mode == "aleatoire":
		ia_alea ()
	else:
		return False 

# L'IA joue, avec un mode 
def jouer (mode = "aleatoire"):
	""" Fait jouer l'IA pour deviner le code 

		@mode : string (aleatoire | knuth | matrice) = 
			le mode de résolution 

		@return : None
	"""

	def ia_alea ():
		# On fait pas dans la finesse ici 
		# Il faut plus de rafinement --"
		while True:
			prop = generer_couleurs_aleatoires ()
			r = moteur.verification_solution (prop)
		
			# On affiche que si le coup était valide
			# (sinon on a plein de trucs nuls :-P)
			if r != False:
				iconsole.afficher ("IA", "Joue {0} -> {1}".format (prop,r))
	
			if r == "perdu" or r == "gagne":
				return


	def ia_knuth ():
		univers = couleurs.liste_couleurs ()[0:8] # Prend les 8 premières couleurs 
		li = create_list (univers) # Crée la liste de toutes les possibilités 
		
		while True: # On boucle ! Youhou ...
			proposition = choice (li) # On propose un truc de la liste 
			li.remove (proposition) # Retire la proposition de la liste 
			
			goto (-200,-200)
			chargement.animation (2,"cercle",10)
			reponse = moteur.verification_solution (proposition) # Et récupère la réponse du moteur 
			
			if reponse == False: # Si la solution est « faux » ... l'univers est corrompu !
				return False # On quitte !
			if reponse == "gagne": # Si la solution est « gagne » ... fin
				return "gagne" 
			if reponse == "perdu": # Si la solution est « perdu » ... idem 
				return "perdu"
			else: # Sinon, c'est un tuple (a,b) (par définition de la fonction)
				nli = []
				for i in li: # Pour chaque élément de la liste 
					reponse_tmp = moteur.proposition_solution (proposition, i)
					if reponse_tmp == reponse: # Si l'élément « i » donne bien le même résultat
						nli.append (i) # On le garde ... sinon on le laisse 
				li = nli # On remplace l'ancienne liste 
	ia_knuth ()
	"""
	if mode == "aleatoire":
		ia_alea ()
	elif mode == "knuth":
		ia_knuth ()
	else:
		return False
	"""
