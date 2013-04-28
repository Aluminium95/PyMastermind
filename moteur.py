#-*- coding: utf-8 -*-
# 29/03/13
#derniere maj 3/4

import persistance
import couleurs
import affichage

# EXCEPTIONS 

class TableauInvalide (Exception):
	def __init__ (self,msg):
		self.message = msg
		
class ModeInvalide (Exception):
	pass

class PasEnCoursDePartie (Exception):
	pass

# FIN EXCEPTIONS

liste_mode = ["facile","moyen","difficile"] # Les modes disponibles 
en_cours_de_partie = False # Est on en train de jouer ?

# Variables relatives à une partie 
historique = False # Les coups joués 
code_secret = False # Le code secret 
restant = False # Le nombre de coups restants
mode_partie = False # Le mode de la partie actuelle


def est_en_partie ():
	""" Dit si on est en cours de partie ou non 
		
		@return : bool
	"""
	global en_cours_de_partie
	
	return en_cours_de_partie

def get_nombre_couleurs ():
	""" Retourne le nombre de couleurs disponibles dans 
		le niveau de difficulté courant 

		@return : int 
		
		@throw :
			PasEnCoursDePartie
			persistance.CleInvalide
			persistance.FichierInvalide
			ValueError
	"""
	global mode_partie
	
	if est_en_partie () != True:
		raise PasEnCoursDePartie
	
	return int (persistance.get_propriete ("config","couleurs:" + mode_partie))

def get_nombre_couleurs_next ():
	""" Retourne le nombre de couleurs disponibles dans 
		le futur niveau de difficulté 
		
		@return : int 
		
		@throw :
			persistance.CleInvalide
			persistance.FichierInvalide
			ValueError
	"""
	cle = "couleurs:{0}".format (get_next_mode ())
	
	return int (persistance.get_propriete ("config", cle))

def init ():
	""" Initialise le module """
	pass 

def nouvelle_partie ():
	""" Commence une nouvelle partie,
		nécessaire pour pouvoir utilser les 
		fonctions relatives à une partie ... afin 
		de bien savoir ce qui se passe 
		
		@return : None
		
		@throw : 
			persistance.CleInvalide # pour le nombre de coups
			persistance.FichierInvalide # « config »
			persistance.ValeurInvalide (fichier,clé) # nombre de coups 
	"""
	global en_cours_de_partie,historique,restant,code_secret,mode_partie
	
	en_cours_de_partie = True
	historique = [] # Initialise l'historique
	
	mode_partie = get_next_mode () # susceptible de planter 
	
	restant = persistance.get_propriete ("config", "coups:" + mode_partie)
	
	try:
		restant = int (restant)
	except ValueError:
		raise persistance.ValeurInvalide ("config", "coups:" + mode_partie)
	
	affichage.plateau () # Remet l'affichage du plateau

def reprendre_partie ():
	""" Réaffiche le plateau et les coups joués précédement dans 
		la partie sur l'écran Turtle 
		
		@return : None
		
		@throw : PasEnCoursDePartie
	"""
	global historique
	
	if est_en_partie () != True:
		raise PasEnCoursDePartie
	affichage.plateau () # Remet l'affichage du plateau

	for coup in historique:
		couleurs_hexa = []
		
		for couleurplacee in coup[0]: # alala, c'est trop con sinon 
			couleurs_hexa.append (couleurs.couleur_to_hexa (couleurplacee))
			
		affichage.afficher_couleurs (4,couleurs_hexa,coup[1])
	
def get_mode ():
	""" Retourne le mode de jeu actuel 
		
		@return : str (facile | moyen | difficile)
		
		@throw : PasEnCoursDePartie
	"""
	global mode_partie
	
	if est_en_partie () != True:
		raise PasEnCoursDePartie
	
	return mode_partie

def get_next_mode ():
	""" Retourne le mode de jeu de la prochaine partie
		(comme définit dans le fichier de configuration)
		
		@return : str (facile | moyen | difficile)
		
		@throw :
			persistance.CleInvalide
			persistance.FichierInvalide
	"""
	return persistance.get_propriete ("config", "niveau")

def get_liste_modes ():
	""" Retourne la liste des modes disonibles 

		@return : list [str ...] = la liste
	"""

	return list (liste_mode)

def set_mode (m): 
	""" Change le mode de jeu pour la PROCHAINE partie jouée
		
		@m : str (facile | moyen | difficile) = Le nouveau mode de jeu 

		@return : None
		
		@throw : 
			ModeInvalide
			persistance.FichierInvalide
	"""
	global restant
	
	if m in liste_mode:
		persistance.set_propriete ("config","niveau",m)
	else:
		raise ModeInvalide
		
def calcul_score ():
	""" Calcul le score actuel a partir du nombre de coups et de la difficulté
		
		@return : int = le score calculé 
	"""
	global restant
	
	if est_en_partie () != True:
		raise PasEnCoursDePartie
	
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
		
		@throw : 
			persistance.CleInvalide
			persistance.FichierInvalide
	"""
      
	score = []
	i = 0
	while i < 5:
		score.append(persistance.get_propriete ("scores",str(i)+":score"))
		i = i+1
	return score

def recup_nom(): #recupere les noms des joueurs des 5 meilleurs scores
	""" Récupère les noms des joueurs des 5 meilleurs scores 
		dans le fichier de scores
		
		@return : [str ... ] = les 5 meilleurs noms
		
		@throw : 
			persistance.CleInvalide
			persistance.FichierInvalide
	"""
	nom = []
	i = 0
	while i < 5:
		score.append(persistance.get_propriete ("scores",str(i)+":nom"))
		i = i+1
	return nom

def enregistre_score (nom_du_joueur = "AAA"):
	""" Enregistre le score actuel dans le top 5 des scores s'il est superieur a un de ces derniers
		
		@return : None
		
		@throw : 
			PasEnCoursDePartie
			persistance.CleInvalide
			persistance.FichierInvalide
	"""
	score_actuel = calcul_score () # Throw PasEnCoursDePartie si besoin ... 

	top_score = recup_score ()
	nom = recup_nom()

	i = 0
	while i < 5:
		if score_actuel > top_score[i]:
			top_score.insert(i, score_actuel)
			nom.insert(i, nom_du_joueur)
			break
		i = i+1

	i = 0
	while i < 5:
		persistance.set_propriete ("scores",str(i)+":score",top_score[i])
		persistance.set_propriete ("scores",str(i)+":nom",nom[i])
		i = i+1

def get_historique():
	""" Retourne une copie de l'historique 
		
		@return : 
			[ 
				[ ["couleur", ...], (a,b) ] 
				... 
				[ COUP , RESULTAT ] 
			]
			
		@throw :
			PasEnCoursDePartie
	"""
	global historique
	
	if est_en_partie () != True:
		raise PasEnCoursDePartie
	
	return list (historique) # Retourne une copie de l'historique

def get_restant (): 
	""" Retourne le nombre de coups restants 
		
		@return : int
		
		@throw : PasEnCoursDePartie
	"""
	global restant
	
	if est_en_partie () != True:
		raise PasEnCoursDePartie
	
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

		@return : None

		@throw : TableauInvalide (msg) 
				PasEnCoursDePartie
	"""
	global code_secret
	
	if est_en_partie () != True:
		raise PasEnCoursDePartie
	
	if len (tableau) == int (persistance.get_propriete ("config", "nombre_cases")):
		for i in tableau:
			if couleurs.is_string (i) == False:
				raise TableauInvalide ("La couleur {0} est invalide".format (i))
		code_secret = tableau
	else:
		raise TableauInvalide ("Le tableau ne contient pas le bon nombre de cases")

def verification_solution (proposition): 
	""" Fonction qui effectue un coup du joueur !
		Si le coup est invalide, on n'enlève pas de vie ni ne diminue 
		le score !

		@proposition : [couleur (français) ...] = la proposition du joueur

		@return : "gagne" | "perdu" | (a,b)
			- "gagne" : l'utilisateur a gagné la partie
			- "perdu" : l'utilisateur a perdu la partie
			- (a,b) : a couleurs justes et bien placées, b couleurs justes et mal placées 
		
		@throw : TableauInvalide (msg)
				PasEnCoursDePartie
	"""
	
	if est_en_partie () != True:
		raise PasEnCoursDePartie
	
	i = 0
	reponse = proposition_solution(proposition, code_secret)
	
	global restant
	

	univers = couleurs.liste_couleurs()[0:get_nombre_couleurs ()]
	for i in proposition:
		if i not in univers:
			raise TableauInvalide ("La couleur {0} n'est pas bonne".format (i))

	a,b = proposition_solution (proposition,code_secret)
	
	historique.append([ list (proposition) , reponse])
	
	restant -= 1
	l = []
	for i in proposition: # alala, c'est trop con sinon 
		l.append (couleurs.string_to_hexa (i))
	
	# Affiche la proposition à l'écran
	affichage.afficher_couleurs (4,l,reponse)
	
	if a == 4: #si proposition est identique à solution
		score = calcul_score()
		affichage.win (score)
		
		en_cours_de_partie = False
		return "gagne"
	elif restant <= 0: #si le nombre de coups restants est de 0
		affichage.loose (list(code_secret))
		
		en_cours_de_partie = False
		return "perdu"
	else:
		return reponse #retourne a, le nombre de justes bien placées, et b le nombre de justes mal placées.

def proposition_solution (proposition, code): 
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
	
	solution = list (code) # Création d'une copie de la liste :-) 

	while i < len (code): # cherche les bonnes couleurs bien placées.
		if solution[i] == proposition_copie[i]:
			a = a+1
			solution[i] = "*"
			proposition_copie[i] = "*"
		i = i+1
	i = 0

	while i < len (code):
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

