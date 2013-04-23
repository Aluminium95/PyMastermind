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
		
		univers = couleurs.liste_couleurs ()[0:moteur.get_nombre_couleurs ()]
		
		m = matrice.make (4, len (univers), lambda x,y: 0) # une matrice couleur/case

		def coup_alea ():
			coup = []
			while coup == []:
				coup = generer_couleurs_aleatoires (univers)
				valide = True
				for i,j in enumerate (coup):
					if matrice.get (m,i, univers.index (j)) == "F":
						valide = False
				
				hi = moteur.get_historique ()
				for h in hi:
					if h[0] == coup:
						valide = False

				if valide == False:
					coup = []
			return coup

		def coup_tentative ():
			coup = []
			for i in matrice.parcourir_lignes (m):
				maximum = 0
				maximum_pos = 0
				for j,k in enumerate (i):
					if k != "F" and k >= maximum:
						maximum = k
						maximum_pos = j
				coup.append (univers[maximum_pos])
				
			for h in moteur.get_historique ():
				if h[0] == coup:
					return coup_alea ()
		
			return coup
	
		while True:
			coup = []
			if moteur.get_restant () < 5:
				coup = coup_tentative ()
			else:
				coup = coup_alea ()
			
			reponse = moteur.verification_solution (coup)

			if reponse == "gagne" or reponse == "perdu":
				return reponse
			else:
				a,b = reponse
				if a == 0:
					for i,j in enumerate (coup):
						matrice.set (m,i,univers.index (j), "F") # Met faux dans les cases 
						if b == 4:
							k = 0
							for element in matrice.parcourir_colonne (m, univers.index (j)):
								if element != "F":
									matrice.set (m, k, univers.index (j), element + 4)
								k += 1
						elif b == 0:
							k = 0
							for element in matrice.parcourir_colonne (m, univers.index (j)):
								matrice.set (m, k, univers.index (j), "F")
								k += 1
				else:
					sc = 10 * a + b
					for i,j in enumerate (coup):
						old = matrice.get (m,i,univers.index (j))
						if old != "F":
							matrice.set (m,i,univers.index (j), old + sc)

				for i in matrice.parcourir_lignes (m):
					print (i)
				


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
