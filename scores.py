#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Scores.py
# Gère tout ce qui s'apparente
# aux scores !
# Bien entendu, il dépend 
# du moteur ... il faut donc 
# faire attention, certaines
# fonctions ne peuvent être 
# appellées que si on est en cours
# de partie !

import persistance
import moteur

def recup_score ():
	""" Recupere la liste des 5 meilleurs scores
		
		@return : [ int ... ] = les 5 meilleurs scores 
		
		@throw : 
			persistance.CleInvalide
			persistance.FichierInvalide
	"""
      
	score = []
	i = 0
	while i < 5:
		score.append (persistance.get_propriete ("scores",str(i)+":score"))
		i = i + 1
	return score

def recup_nom (): #recupere les noms des joueurs des 5 meilleurs scores
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
		nom.append (persistance.get_propriete ("scores",str(i)+":nom"))
		i = i + 1
	return nom

def calcul_score ():
	""" Calcul le score actuel a partir du nombre de coups et de la difficulté
		
		@return : int = le score calculé 
	"""
	
	if moteur.est_en_partie () != True:
		raise moteur.PasEnCoursDePartie
	
	coups = moteur.get_restant () # Le nombre de coup qu'il reste à jouer ... donc plus il y en a mieux c'est !
	mode = get_mode()
	if mode == "facile":
		score = 10 * (coups - 1) / 2
	elif mode == "moyen":
		score = 10 * (coups - 1) / 1.5
	else:
		score = 10 * (coups - 1)
	
	return int (score) # On retourne un entier
	
def enregistre_score (nom_du_joueur = "AAA"):
	""" Enregistre le score actuel dans le top 5 des scores s'il est superieur a un de ces derniers
		
		@return : None
		
		@throw : 
			moteur.PasEnCoursDePartie
			persistance.CleInvalide
			persistance.FichierInvalide
	"""
	score_actuel = calcul_score () # Throw PasEnCoursDePartie si besoin ... 

	top_score = recup_score ()
	nom = recup_nom ()

	i = 0
	while i < 5:
		try:
			sc = int (top_score[i])
		except ValueError:
			raise persistance.ValeurInvalide ("scores",str (i) + ":score")
		else:
			if score_actuel > int(top_score[i]):
				top_score.insert(i, str (score_actuel))
				nom.insert(i, nom_du_joueur)
				break
			i = i + 1

	i = 0
	while i < 5:
		persistance.set_propriete ("scores",str(i)+":score",top_score[i])
		persistance.set_propriete ("scores",str(i)+":nom",nom[i])
		i = i + 1

