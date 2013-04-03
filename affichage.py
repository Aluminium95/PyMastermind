#-*- coding: utf-8 -*-
# 03/04/2013
# Desmarais Yann
#
# Description:

from turtle import *

y = 120
couleurs=["red","yellow","purple","green","black"]#une petite liste pour tester ma fonction

a=(3,1)#un petit tuple pour tester une autre fonction

def init ():
	up ()
	# bgpic ...
	# etc ...
	

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

    

def win():
	""" Affiche l'écran de victoire
		
		@return : None 
	"""
	reset()
	#bgpic(fondMarie.Gagner)
	
def loose():
	""" Affiche l'écran de défaite
	
		@return : None
	"""
	reset()
	#bgpic(fondMarie.Perdre)


            
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

	y = y - 60
