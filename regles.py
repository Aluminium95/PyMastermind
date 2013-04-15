# -*- coding: utf-8 -*-
#règles du jeu (mode facile, normal et difficile)
#014/04/2013

from turtle import *
import persistance
import couleurs



def texte_normal (text):
	write(text, False, "center", ("calibri",16,"normal"))


def texte_petit (text):
	write(text, False, "left", ("calibri",12,"normal"))

def niveau(niveau):
	text="Voici les regles du mastermind mode " + niveau + ":"
	write(text, False, "center", ("calibri",16,"underline"))

def main_text():
	goto(50,150)
	text2="- Vous devez deviner le code couleur du jeu."
	texte_normal (text2)
	goto(-132,120)
	dot(10,"red")
	goto(80,110)
	text3=" : Signifie que la couleur est juste et bien placée."
	texte_normal (text3)
	goto(-132,90)
	dot(10,"black")
	goto(90,80)
	text4=" : Signifie que la couleur est juste mais mal placée."
	texte_normal (text4)
	goto(9,50)
    

def nombre_coup(coups):
	text5="- Il y a " + coups + " couleurs selectionnables." 
	texte_normal (text5)

def main_text2():
	text6="- Le code à trouver est composé de 4 couleurs."
	texte_normal (text6)
	goto(69,-10)
	text7="- Vous avez 10 essais maximum pour le deviner."
	texte_normal (text7)
	goto(50,-40)
	color("red")
	begin_fill()
	text8="Attention,"
	texte_normal (text8)
	end_fill()
	color("black")
	goto(80,-60)
	text9="si rien n'est indiqué, alors votre réponse est fausse."
	texte_normal (text9)
	goto(-185,-130)
	text10="Panel de couleurs :"
	write(text10, False, "center", ("calibri",15,"underline"))
	goto(-285,-280)

def carre(taille):
	c = 0
	down ()
	while c<4:
		forward(taille)
		left(90)
		c = c + 1
	up ()

def carre_facile():
	li = couleurs.liste_couleurs ()
	print li
	for i in li:
		color (couleurs.string_to_hexa (i))
		begin_fill ()
		carre(10)
		end_fill ()
		left (90)
		fd (10)
		texte_petit(i)
		right(90)
		fd (38)
        
def carre_normal ():
	li = couleurs.liste_couleurs ()
	print li
	
	k = 0 # Compteur
	# Dit combien de couleurs 
	# ont été dessinées sur une colonne 

	for i in li:
		if k == 4: # Quand on a fait 4 couleurs
			k = 0 # On repart à zéro
			left (90) # Et on se place sur la colonne suivante 
			fd (120)
			right (90)
			fd (120)

		color (couleurs.string_to_hexa (i))
		begin_fill ()
		carre (10)
		end_fill ()
		fd (20)

		right (90)
		fd (5)
		texte_petit(i)
		fd (-5)
		left (90)

		fd (-20)
		right(90)
		fd (30)
		left (90)
		
		k += 1

def carre_difficile():
	li = couleurs.liste_couleurs ()
	print li
	for i in li:
		color (couleurs.string_to_hexa (i))
		begin_fill ()
		carre(10)
		end_fill ()
		left (90)
		fd (10)
		texte_petit(i)
		right(90)
		fd (38)

def regles_facile(couleur):
	"""Affiche les règles ainsi que les aides du jeu. En mode facile.
	(un fond y est inséré)"""
	screensize(600,600,"white")
	bgpic("ff.gif")
	up()
	goto(30,220)
	color(couleur)
	niveau('facile')
	main_text()
	goto(8,50)
	nombre_coup('8')
	goto(64,20)
	main_text2()
	carre_facile()


def regles_normal(couleur):
	"""Affiche les règles ainsi que les aides du jeu. En mode normal.
	(un fond y est inséré)"""
	screensize(600,600,"white")
	th = persistance.get_propriete ("backgrounds", "theme:courant")
	bgpic("Images/Regles/fn.gif")
	up()
	goto(30,220)
	color(couleur)
	niveau('normal')
	main_text()
	goto(14,50)
	nombre_coup('12')
	goto(63,20)
	main_text2()
	
	goto (-245,-160)

	carre_normal()

def regles_difficile(couleur):
	"""Affiche les règles ainsi que les aides du jeu. En mode difficile.
	(un fond y est inséré)"""
	screensize(600,600,"white")
	th = persistance.get_propriete ("backgrounds", "theme:courant")
		

	bgpic ("Images/Theme" + th + "/fd.gif")
	up()
	goto(30,220)
	color(couleur)
	niveau('difficile')
	main_text()
	goto(14,50)
	nombre_coup('16')
	goto(63,20)
	main_text2()
	carre_difficile()


# Cette partie de code ne s'exécute que
# quand le programme est lancé directement 
# ce n'est pas exécuté quand le module 
# est importé, ou quand on génère la doc 
# ... Très utile cette petite astuce !
if __name__ == '__main__':
	persistance.init ()
	couleurs.init ()
	
	regles_normal ("#000")
	
	mainloop ()
