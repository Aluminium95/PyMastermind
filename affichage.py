#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Desmarais Yann
#
# Description:
#
# Gère tout ce qui est affichage. Soit le fond courant correspondant au thème (gestion des thèmes) et les cases colorées.

import couleurs
import persistance
from primitives import * 

y = -245
x = -125

def init (theme = ""):
	""" Initialise la fonction, affiche le fond sélectionné
	
		@thème : str
		@return : None
	"""
	
	# Crée la fenêtre :-)
	setup (width=600,height=600,startx=400,starty=300)
	sc = getscreen ()
	sc.title ("PyMastermind")
	# plateau () # Ce n'est pas à lui de le faire

def generateur_reponse (answer):
	""" Retourne un générateur
		qui permet de faire à chaque 
		étape le dessin d'un point 
		d'une couleur, le tout correspondant 
		au nombres (a,b) de la réponse !
	"""
	a,b = answer
	
	while a + b > 0: # On s'arrête après
		if a > 0: # Si a > 0, on enlève du a
			dot (10, "red") # Affiche un point rouge
			a -= 1 # Enlève du a
		elif b > 0: # Si b > 0 on enlève du b
			dot (10, "black") # Affiche un point noir
			b -= 1 # Retire du b
		
		yield # Yield à chaque point !
    
def plateau ():
	""" Affiche un plateau vierge
		et définit toutes les constantes 
		pour afficher les coups sur le plateau
		
		@return : None
	"""
	global y,x

	raz ()
	
	th = persistance.get_propriete ("backgrounds","theme:courant")

	path = "Images/Theme" + th + "/fond.gif"
	bgpic (path)
	
	y = int (persistance.get_propriete ("backgrounds", "theme:" + th + ":y:plateau"))
	x = int (persistance.get_propriete ("backgrounds", "theme:" + th + ":x:plateau"))
	
	
	goto(x,y)

	speed (0)    

def win (score):
	""" Affiche l'écran de victoire (fond choisi)
		
		@bg : str
		@return : None 
	"""
	raz () # Ou pas ?

	th = persistance.get_propriete ("backgrounds", "theme:courant")
	y = int (persistance.get_propriete ("backgrounds", "theme:" + th + ":y:plateau"))
	x = int (persistance.get_propriete ("backgrounds", "theme:" + th + ":x:plateau"))
	
	path = "Images/Theme" + th + "/gagne.gif"
	bgpic(path)
	
	aller_a (-125, -70) # On centre la réponse
	
	color ("white")
	begin_fill ()
	rectangle (250,110)
	end_fill ()
	
	aller_a (-110,0)
	color ("black")
	texte ("Votre score final","important")
	
	aller_a (-9 * len (str (score)),-50)
	color ("black")
	texte (score)
	
def loose (code):
	""" Affiche l'écran de défaite
		
		@bg : str
		@return : None
	"""
	raz () # Ou pas ?
	
	th = persistance.get_propriete ("backgrounds", "theme:courant")
	y = int (persistance.get_propriete ("backgrounds", "theme:" + th + ":y:plateau"))
	x = int (persistance.get_propriete ("backgrounds", "theme:" + th + ":x:plateau"))
	
	path = "Images/Theme" + th + "/perdu.gif"
	bgpic(path)
	
	
			
	aller_a (-125, -70) # On centre la réponse
	
	color ("white")
	begin_fill ()
	rectangle (250,110)
	end_fill ()

	aller_a (-95, -65) # On centre la réponse

	for i in code:
		color (couleurs.couleur_to_hexa (i))
		begin_fill ()
		carre (40)
		end_fill ()
		fd(50)

	
	aller_a (-110,0)
	color ("black")
	texte ("La solution était","important")


def afficher_couleurs(nbr_case,couleurs,answer):
	""" dessine une ligne du plateau du mastermind avec en argument les donnée envoyé par les autres modules:
    	les couleurs saisies par l'utilisateur et la réponse de l'ordinateur à partir du code secret. Composée de la fonction carré et de la fonction answer
        
		@nbr_case : int = le nombre de cases du tableau
		@couleurs : list de string = liste des couleurs proposées en hexadécimal
		@answer : tuple (a,b) = couple de nombre, proposition exacte et couleurs uniquement exacte.
		
        	@return : None
    """
	global y, x
	up ()
	goto (x, y)
	i = 0
	while i < nbr_case:
		color (couleurs[i])
		begin_fill ()
		carre (40)
		end_fill ()
		fd (50)
		i = i + 1
	
	# Se positionne pour 
	# permettre de faire les 
	# points rouge et noir de réponse
	up ()
	fd (20)
	left (90)
	fd (30)
	right (90)
	
	lignes (2, 20, 20, generateur_reponse (answer))
	# dessiner_answer (answer)
	up ()
	
	seth (0) # remet la tortue à un angle absolu de zéro !

	y = y + 50

def generer_score():
	
	for i in range (1,6):
		seth (0)
		
		
		up ()
		forward (40)
		color ("red")
		begin_fill ()
		polygone (6,20)
		end_fill ()
		up ()
		forward (3)
		left (90)
		forward (5)
		color ("black")
		texte (str (i))
		yield
	
	# TODO: utilisation de scores.py
	for i in range(0,5):
		down()
		score = persistance.get_propriete ("scores", str (i) + ":score")
		texte (score)
		up ()
		yield

	for i in range(0,5):
		down ()
		nom = persistance.get_propriete ("scores", str (i) + ":nom")
		texte (nom)
		up ()
		yield
        
def high_score ():
	""" Fonction qui affiche l'écran des meilleurs 
		scores 
	"""
	raz ()
	aller_a (-200, 200)
	texte ("Meilleurs scores", "important")
	aller_a (-200, 150)
	colonnes(5, 50, 100, generer_score () )
	
if __name__ == "__main__":
	persistance.init ()
	couleurs.init ()
	
	win (8)
	mainloop ()
