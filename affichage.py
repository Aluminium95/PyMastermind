#-*- coding: utf-8 -*-
# 03/04/2013
# Desmarais Yann
#
# Description:
#
# Gère tout ce qui est plateau

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
	plateau ()
	

def dessiner_carre (taille,couleur):
	up ()
	if couleur != False:
		down()
		color(couleur)
		begin_fill()
	for i in range (0,4):
		forward(taille - 1)
		right(90)
	if couleur != False:
		end_fill()
		up()



def dessiner_answer(answer):
	""" Affiche le score de la proposition du joueur, 
		answer étant un tuple (a,b)
		
		@answer : (a,b) int × int = 
			a - le nombre de couleurs bonne et à la bonne place
			b - le nombre de couleurs bonne et à la mauvaise place
	
		@return : None
	"""
	up ()
	fd(10)
	a,b=answer
	fd(10)
	right(90)
	fd(10)
	down()
	if a>0:
		a=a-1
		dot(10,"red")
	elif b>0:
		b=b-1
		dot(10,"grey")
	else:
		return
	up()
	left(90)
	fd(20)
	if a>0:
		a=a-1
		dot(10,"red")
	elif b>0:
		b=b-1
		dot(10,"grey")
	else:
		return
	up()
	right(90)
	fd(20)
	if a>0:
		a=a-1
		dot(10,"red")
	elif b>0:
		b=b-1
		dot(10,"grey")
	else:
		return
	right(90)
	fd(20)
	if a>0:
		a=a-1
		dot(10,"red")
	elif b>0:
		b=b-1
		dot(10,"grey")
	else:
		return
    
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

	aller_a (-95, -25) # On centre la réponse

	for i in code:
		dessiner_carre (40, couleurs.couleur_to_hexa (i))
		fd(50)

	
	aller_a (-110,0)
	color ("black")
	texte ("La solution était","important")


def choix_theme(nbr_theme = 1):
	""" Sélectionne un thème (modifie le fichier de configuration)
		
		@nbr_theme : int = le numéro du nouveau thème sélectionné
		
		@return : None
		
		@throw :
			persistance.CleInvalide
			persistance.FichierInvalide
			ValueEror # si jamais il y a une valeur erronée dans backgrounds -> theme:max
	"""
	if not isinstance (nbr_theme, int):
		nbr_theme = 1
	
	max_theme = persistance.get_propriete ("backgrounds","theme:max")
	
	if nbr_theme > int (max_theme):
		nbr_theme = 1
	
	persistance.set_propriete ("backgrounds","theme:courant",str (nbr_theme))

def liste_themes ():
	# C'est con ... ça génère ["1", "2", ..., "max"]
	max_theme = persistance.get_propriete ("backgrounds", "theme:max")
	
	l = []

	i = 1
	while i <= int (max_theme):
		l.append (str (i))
		i += 1
	return l

def afficher_couleurs(nbr_case,couleurs,answer):
	""" dessine une ligne du plateau du mastermind avec en argument les donnée envoyé par les autres modules:
    	les couleurs saisies par l'utilisateur et la réponse de l'ordinateur à partir du code secret. Composée de la fonction carré et de la fonction answer
        
		@nbr_case : int = le nombre de cases du tableau
		@couleurs : list de string = liste des couleurs proposées en hexadécimal
		@answer : tuple (a,b) = couple de nombre, proposition exacte et couleurs uniquement exacte.
		
        	@return : None
    """
	global y,x
	up ()
	goto(x,y)
	i=0
	while i<nbr_case:
		dessiner_carre(40,couleurs[i])
		fd(50)
		i=i+1
	dessiner_answer(answer)
	up ()
	
	seth (0) # remet la tortue à un angle absolu de zéro !

	y = y + 50

def creer_bouton (x,y,l,couleur,texte):
	""" Crée un bouton de couleur avec du texte à côté
		
		@x : int = position x
		@y : int = position y
		@l : int = taille du côté
		@couleur : string = la couleur en hexa ou en français
		@texte : string = le texte descriptif 

		@return : None
	"""
	up ()
	goto (x,y)
	down ()
	dessiner_carre (l,couleur)
	up ()
	goto ( x + l + 20, y - (l / 2))
	down ()
	write (texte)
	up ()
	
def generer_score():
	
	for i in range (1,6):
		seth (0)
		
		
		up ()
		forward (40)
		polygone (6,20)
		up ()
		forward (3)
		left (90)
		forward (5)
		texte (str (i))
		yield
	
	for i in range(0,5):
		down()
		score = persistance.get_propriete("scores",str (i) + ":score")
		texte(score)
		up()
		yield

	for i in range(0,5):
		down()
		nom = persistance.get_propriete("scores",str (i) + ":nom")
		texte(nom)
		up()
		yield
        
def high_score ():
	raz ()
	aller_a (-200,200)
	texte ("Meilleurs scores","important")
	aller_a (-200,150)
	colonnes(5, 50, 100, generer_score () )
	
if __name__ == "__main__":
	persistance.init ()
	couleurs.init ()
	
	win (8)
	mainloop ()
