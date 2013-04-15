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
	""" Initialise le module """
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
		
def calcul_score ():
	""" Calcul le score actuel a partir du nombre de coups et de la difficulté
		
		@return : int = le score calculé 
	"""
	
	coups = restant # Le nombre de coup qu'il reste à jouer ... donc plus il y en a mieux c'est !
	mode = get_mode()
	if mode == "facile":
		score = coups
	elif mode == "moyen":
		score = coups + 2
	else:
		score = coups + 5
	
	return score

def recup_score():
	""" Recupere la liste des 5 meilleurs scores
		
		@return : [ int ... ] = les 5 meilleurs scores 
	"""
      
	score = []
	i = 0
	while i < 5:
		score.append(persistance.get_propriete ("scores",str(i)))
		i = i+1
	return score

def enregistre_score (): 
	""" Enregistre le score actuel dans le top 5 des scores s'il est superieur a un de ces derniers
		
		@return : None
	"""
		score_actuel = calcul_score ()

		top_score = recup_score ()

    	i = 0

    	while i < 5:
        	if score_actuel > top_score[i]:
            		top_score.insert(i, score_actuel)
            		i = i+1
            
    	i = 0
    	while i < 5:
        	persistance.set_propriete ("scores",str(i),top_score[i])
		i = i+1
		
def get_historique():
	""" Retourne une copie de l'historique 
		
		@return : 
			[ 
				[ ["couleur", ...], (a,b) ] 
				... 
				[ COUP , RESULTAT ] 
			]
	"""
	return list (historique) # Retourne une copie de l'historique

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
			if solution[j] != "*" and solution[j] == proposition_copie[i]:
				b = b+1
				solution[j] = "*"
				proposition_copie[i] = "*"
				break
			j = j + 1
		i = i+1
	
	historique.append([proposition_copie, (a,b)])
	
	restant -= 1
	l = []
	for i in proposition: # alala, c'est trop con sinon 
		l.append (couleurs.string_to_hexa (i))
	
	affichage.afficher_couleurs (4,l,(a,b))
	
	if a == 4: #si proposition est identique àsolution	
		affichage.win ("red") 
		return "gagne"
	elif restant <= -1: #si le nombre de coups restants est de 0
		affichage.loose ("red") 
		return "perdu"
	else:
		return (a,b) #retourne a, le nombre de justes bien placées, et b le nombre de justes mal placées.

def proposition_ia (proposition, code_secret): 
	""" Fonction qui effectue un coup du joueur !
		comme la fontion proposer_solution, sans s'occuper des autres paramètres, tel que le score,
		les coups restant ... ne renvoie que (a,b)

		@proposition : [couleur (français) ...] = la proposition du joueur

		@return : (a,b)
			- (a,b) : a couleurs justes et bien placées, b couleurs justes et mal placées 
	"""
	
	

	# couleurs.is_string (c) 
	# il faut verifier que la couleur est valide 

	a = 0
	b = 0
	i = 0
	
	proposition_copie = list (proposition) # Création d'une nouvelle liste par copie
	
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
			if solution[j] != "*" and solution[j] == proposition_copie[i]:
				b = b+1
				solution[j] = "*"
				proposition_copie[i] = "*"
				break
			j = j + 1
		i = i+1
		
	return (a,b) #retourne a, le nombre de justes bien placées, et b le nombre de justes mal placées.

