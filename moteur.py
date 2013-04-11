#-*- coding: utf-8 -*-

# 29/03/13
#derniere maj 3/4

import persistance
import couleurs
import affichage

historique = []
code_secret = False
mode = "moyen"
restant = 10
liste_mode = ["facile","moyen","difficile"]

def init ():
	global restant
	restant = persistance.get_propriete ("config","coups:" + mode)
	restant = int (restant)

def get_mode ():
	""" Retourne le mode de jeu actuel 
		
		@return : str (facile | moyen | difficile)
	"""
	return mode

def set_mode (m): 
	""" Change le mode de jeu 
		
		@m : str (facile | moyen | difficile) = Le nouveau mode de jeu 

		@return : bool = si c'est bon 
	"""
	global mode,restant
	
	if m in liste_modes:
		mode = m
		restant = persistance.get_propriete ("config","coups:"+m)
		return True
	else:
		return False
		
def get_historique():
	return historique

def get_restant (): 
	""" Retourne le nombre de coups restants 
		
		@return : int
	"""
    return restant

def double_couleur (test):
	""" Vérifie si une liste contient deux fois un élément identique
		
		@test : [? ...] = la liste à tester

		@return : bool 
	"""
	liste_test = []
	for i in test:
		if i in liste_test:
			return False
		else:
			liste_test.append(i)
	return True

def definir_code (tableau): 
	""" Définit le code à trouver pour la partie !
		
		@tableau : [couleurs (français) ...] = le code à trouver

		@return : bool = si tout s'est bien passé
	"""
	global code_secret
	if len (tableau) == int (persistance.get_propriete ("config", "nombre_cases")):
		for i in tableau:
			if couleurs.is_string (i) == False:
				return False
		code_secret = tableau
		return True
	else:
		return False

def proposer_solution (proposition): 
	""" Fonction qui effectue un coup du joueur !
		Si le coup est invalide, on n'enlève pas de vie ni ne diminue 
		le score !

		@proposition : [couleur (français) ...] = la proposition du joueur

		@return : False | "gagne" | "perdu" | (a,b)
			- False : il y a eu un problème dans le code proposé
			- "gagne" : l'utilisateur a gagné la partie
			- "perdu" : l'utilisateur a perdu la partie
			- (a,b) : a couleurs justes et bien placées, b couleurs justes et mal placées 
	"""
	
	global restant
	

	# couleurs.is_string (c) 
	# il faut verifier que la couleur est valide 

	a = 0
	b = 0
	i = 0
	
	proposition_copie = list (proposition) # Création d'une nouvelle liste par copie
	
	""" Le code ici est un peu « barbare » 
	while i < len(proposition):
		proposition_copie.append(proposition[i])
		i = i+1
	
	i = 0
	"""

	solution = list (code_secret) # Création d'une copie de la liste :-) 

	while i < len (code_secret): #cherche les bonnes couleurs bien placées.
		if solution[i] == proposition_copie[i]:
			a = a+1
			solution[i] = "*"
			proposition_copie[i] = "*"
		i = i+1
	i = 0

	while i < len (code_secret):
		j = 0
		while j < len (solution): #cherche les bonnes couleurs mal placées
			if solution[j] != "*" and solution[j] == proposition[i]:
				b = b+1
				solution[j] = "*"
				proposition_copie[i] = "*"
				break
			j = j + 1
		i = i+1
	
	historique.append([proposition_copie, (a,b)])
	
	restant -= 1
	if a == 4: #si proposition est identique àsolution
		affichage.win ("red") 
		return "gagne"
	elif restant <= -1: #si le nombre de coups restants est de 0
		affichage.loose ("red") 
		return "perdu"
	else:
		l = []
		for i in proposition_copie:
			l.append (couleurs.string_to_hexa (i))
		
		affichage.afficher_couleurs (4,l,(a,b))
		return (a,b) #retourne a, le nombre de justes bien placées, et b le nombre de justes mal placées.

