#-*- coding: utf-8 -*-
# 03/04/2013
# Desmarais Yann
#
# Description:

from turtle import *
from couleurs import *
import persistance

y = 245


def init (theme = ""):
	""" Initialise la fonction, affiche le fond sélectionné
	
		@thème : str
		@return : None
	"""
	# yop ... ça plante --"
	up ()
	# selected_theme = persistance.get_propriete ("background",theme)
	# bgpic(picname = selected_theme)
	

def dessiner_carre (taille,couleur):
	up ()
	if couleur != False:
		down()
		color(couleur)
		begin_fill()
	for i in range (0,4):
		forward(taille)
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
    
def reset():
	""" Remet à zéro !
		
		@return : None
	"""
	global y
	clear()
	y=120
	goto(-125,y)

    

def win(bg):
	""" Affiche l'écran de victoire (fond choisi)
		
		@bg : str
		@return : None 
	"""
	reset()
	#selected_bg = persistance.get_propriete ("background",bg)
	#bgpic(picname = selected_bg)
	
def loose(bg):
	""" Affiche l'écran de défaite
		
		@bg : str
		@return : None
	"""
	reset()
	#selected_bg = persistance.get_propriete ("background",bg)
	#bgpic(picname = selected_bg)


            
def afficher_couleurs(nbr_case,couleurs,answer):
	""" dessine une ligne du plateau du mastermind avec en argument les donnée envoyé par les autres modules:
    	les couleurs saisies par l'utilisateur et la réponse de l'ordinateur à partir du code secret. Composée de la fonction carré et de la fonction answer
        
		@nbr_case : int = le nombre de cases du tableau
		@couleurs : list de string = liste des couleurs proposées en hexadécimal
		@answer : tuple (a,b) = couple de nombre, proposition exacte et couleurs uniquement exacte.
		
        	@return : None
    """
	global y
	up ()
	goto(-125,y)
	i=0
	while i<nbr_case:
		dessiner_carre(40,couleurs[i])
		fd(50)
		i=i+1
	dessiner_answer(answer)
	up ()
	
	seth (0) # remet la tortue à un angle absolu de zéro !

	y = y - 60

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
	goto ( x + l + 20, (y - l) / 2)
	down ()
	write (texte)
	up ()
