#-*- coding: utf-8 -*-
# Les fonctions de l'ia
# ...

import couleurs
import moteur
import iconsole
import persistance
import chargement

import matrice

from turtle import goto # moooooochhheeee

from random import choice # faire un choix aléatoire dans une liste 
from random import random 


# EXCEPTIONS

class ModeInvalide (Exception):
	pass 

# FIN EXCEPTIONS

def generer_couleurs_aleatoires (c = False):
	""" Génère un code aléatoire de couleurs, complètement !
		
		@c : [couleurs (fr) ...] | False = si on a un univers prédéfini !

		@return : list of couleurs (Français)
	"""

	sortie = [] # le tableau de sortie 

	# On récupère la liste des couleurs possibles
	if c == False:
		lst = couleurs.liste_couleurs ()
	else:
		lst = c
	
	# On récupère le nombre de cases demandées
	n = persistance.get_propriete ("config","nombre_cases")

	# On définit n couleurs au hasard ... 
	for i in range (int (n)):
		sortie.append (choice (lst))
	
	return sortie
	
def create_list(S):
	"""Créé une liste de toutes les combinaison possibles des objets dans S (une même couleur peux se retrouver plusieurs fois)
		len(li) = n^(4) à l'issue de cette fonction (où n est len(S))
		
		@S : list = L'univers, l'ensemble des possibilités, pour le mastermind, le nombre de couleurs
		@return : list = li la liste de toutes les combinaison
	"""
	L = []
	
	n = len (S) - 1

	rotors = [-1,0,0,0]

	while rotors != [n,n,n,n]:
		
		rotors[0] += 1
		
		i = 0
		while i < len (rotors):
			if rotors[i] == (n + 1): # Si la couleurs n'existe pas, on recommence
				rotors[i] = 0 # repart à zéro
				try: # Je pense que ça peut planter
					rotors[i + 1] += 1 # Et ajoute 1 au suivant
				except:
					# On y arrive jamais ici ... c'est con 
					print ("euh ... ici faut vérifier")
			else:
				break
			i += 1 
		
		nl = []
		for i in rotors:
			nl.append (S[i])
		
		L.append (nl)
	
	return L

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
		univers = couleurs.liste_couleurs ()[0:moteur.get_nombre_couleurs()]

		while condition:
			p = generer_couleurs_aleatoires (univers)
			try:
				r = moteur.definir_code (p)
				condition = False
			except:
				pass

	# fin def ia_alea ici 

	if mode == "aleatoire":
		ia_alea ()
	else:
		raise ModeInvalide

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
			try:
				r = moteur.verification_solution (prop)
				
				if r == "perdu" or "gagne":
					return

			except moteur.TableauInvalide as t:
				iconsole.afficher ("IA", "Erreur ... " + t.message)
	
	def ia_matrice ():
		""" Une ia qui fait une matrice probabiliste
			qui permet d'étudier quelle doit être 
			la combinaison couleurs/cases qui
			correspond au code
		"""
		# Il est pratique d'avoir l'univers sous la main 
		# (l'ensemble des couleurs disponibles dans l'ordre)
		univers = couleurs.liste_couleurs ()[0:moteur.get_nombre_couleurs ()]
		
		# On crée la matrice pondérée des coefs case/couleur (affichée en sortie !)
		m = matrice.make (4, len (univers), lambda x,y: 0) # une matrice couleur/case

		def coup_alea ():
			""" Crée un coup totalement aléatoire, tout en 
				vérifiant qu'il n'est pas dans l'historique
				et vérifiant qu'il n'utilise pas des combinaisons
				cases/couleurs qui sont impossibles 
			"""
			coup = []
			while coup == []:
				# On génère un coup aléatoire (totalement) à partir de l'univers
				coup = generer_couleurs_aleatoires (univers)
				valide = True # On présuppose que le coup est valide
				for i,j in enumerate (coup):
					if matrice.get (m,i, univers.index (j)) == "F":
						valide = False # Mais s'il utilise une valeur interdite ... il ne l'est pas
				
				hi = moteur.get_historique () # On récupère les coups déjà joués 
				for h in hi:
					if h[0] == coup: # h[0] représente le coup et h[1] la réponse
						valide = False # S'il y est ... on ne le rejoue pas !

				if valide == False: # Si c'est invalide (historique ou valeur interdite)
					coup = [] # On met à [] (donc on continue à boucler)
			return coup # On retourne le coup une fois généré !

		def coup_tentative ():
			""" Fait une tentative d'interprétation des 
				résultats !
			"""
			coup = [] # Un coup
			
			# Pour chaque numéro de ligne est une case
			# et les colonnes sont les couleurs, donc 
			# Pour chaque ligne, on trouve la colonne avec 
			# le meilleur coef, et on prend la couleur qui
			# correspond à cette colonne :-)
			for i in matrice.parcourir_lignes (m):
				maximum = 0
				maximum_pos = 0
				for j,k in enumerate (i):
					if k != "F" and k >= maximum:
						maximum = k
						maximum_pos = j
				coup.append (univers[maximum_pos])
			
			# On vérifie que le coup n'est pas déjà joué
			for h in moteur.get_historique ():
				if h[0] == coup:
					return coup_alea () # Auquel cas on retourne un coup aléatoire
		
			return coup # Sinon on retourne le coup géneré
	
		while True:
			coup = []
			
			# En fonction du nombre de coups restant
			# On a une approche différente ...

			if moteur.get_restant () < 5:
				coup = coup_tentative ()
			else:
				coup = coup_alea ()
			
			# On récupère la réponse 
			reponse = moteur.verification_solution (coup)

			if reponse == "gagne" or reponse == "perdu":
				return reponse # là c'est génial 
			else:
				a,b = reponse # là c'est le couple (a,b) !
				# ce code tente de remplir la matrice d'informations 
			 	# les plus pertinentes possibles à partir de ce couple
				# et des couleurs jouées ... Mais c'est dur !
				
				if a + b == 4:
					def une_petite_lambda (i,j,v):
						if univers[j] not in coup:
							return "F"
						else:
							return v
					matrice.apply (m, une_petite_lambda)
				elif a == 0:
					for i,j in enumerate (coup):
						matrice.set (m,i,univers.index (j), "F") # Met faux dans les cases 
						if b > 0:
							k = 0
							for element in matrice.parcourir_colonne (m, univers.index (j)):
								if element != "F":
									matrice.set (m, k, univers.index (j), element + b)
								k += 1
						elif b == 0:
							k = 0
							for element in matrice.parcourir_colonne (m, univers.index (j)):
								matrice.set (m, k, univers.index (j), "F")
								k += 1
				else: # A ≠ 0
					sc = 20 * a + b
					
					def my_little_lambda (i,j,v):
						if v == "F":
							return "F"
						else:
							return v - 5 * a

					matrice.apply (m, my_little_lambda)
	
					for i,j in enumerate (coup):
						old = matrice.get (m,i,univers.index (j))
						if old != "F":
							matrice.set (m,i,univers.index (j), old + sc)
				
				matrice.display (m,univers) # Affiche la matrice résultante !


	def ia_knuth ():
		univers = couleurs.liste_couleurs ()[0:moteur.get_nombre_couleurs ()]

		li = create_list (univers) # Crée la liste de toutes les possibilités 
		
		while True: # On boucle ! Youhou ...
			try:
				proposition = choice (li) # On propose un truc de la liste 
				li.remove (proposition) # Retire la proposition de la liste 
			except:
				iconsole.afficher ("IA","Le code utilise FORCÉMENT des couleurs qui ne sont pas disonibles ...")
			goto (200,-200)
			chargement.animation (3,"cercle",20)

			try:
				reponse = moteur.verification_solution (proposition) # Et récupère la réponse du moteur 
				iconsole.afficher ("IA","Joue {0} -> {1}".format (proposition,reponse))
				
				if reponse == "gagne" or reponse == "perdu":
					return reponse
				else:
					nli = []
					for i in li:
						reponse_tmp = moteur.proposition_solution (proposition, i)
						if reponse_tmp == reponse:
							nli.append (i)
					li = nli
			except moteur.TableauInvalide as t:
				iconsole.afficher ("IA", "Erreur ... " + t.message)

	if mode == "aleatoire":
		ia_matrice ()
	elif mode == "knuth":
		ia_knuth ()
	else:
		raise ModeInvalide
