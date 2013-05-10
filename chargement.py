#!/usr/bin/env python
#-*- coding: utf-8 -*-
# 
# Affiche un écran qui fait une barre
# de chargement !
# Permet aussi de faire des chargements
# plus petits sur une portion de l'écran

# Nos modules à nous 
import persistance
import couleurs
import themes
import primitives 

# Python standard
from random import randint
from random import choice

def init ():
	""" Initialise le module """
	pass # ne fait rien 

def generer_couleurs (col,n, t = 40):
	""" Génère des ronds de plus en plus clair 
		de la teinte de départ, avec n ronds,
		de taille t

		@col : couleur (fr) = couleur de départ
		@n : int = nombre de ronds
		@t : int = rayon du rond

		@return : generator
	"""
	current_color = col
	for i in range (0,n):
		try:
			# Pour le moment la fonction éclaircir 
			# n'est pas fonctionnelle, mais elle le 
			# sera bientôt, et la couleur 
			# princpale sera dégradée !!!
			current_color = couleurs.eclaircir (current_color, "11")
		except:
			pass # un erreur ...
		primitives.dot (t, current_color)
		yield


def animation (t,mode = "cercle",taille = 40):
	""" Fait une animation en partant de la position 
		actuelle du pointeur ...

		@t : int = le nombre de tours
		@mode : str (cercle|arc|ligne) = le mode de chargement

		@return : None
	"""
	x,y = primitives.get_position ()
	
	# En fonction du nombre de « cycles » 
	# on peut définir des couleurs différentes
	# qui sont représentatives d'une progression
	if t % 5 == 0:
		liste = ["rouge","carmin","or","vert","chartreuse"]
	elif t % 3 == 0:
		liste = ["carmin","or","chartreuse"]
	elif t % 2 == 0:
		liste = ["carmin","chartreuse"]
	else: # Un nombre indéterminé 
		liste = ["zinzolin","indigo"]

	# speed (0) est déjà activé normalement 
	for i in range (t):
		# Définit la couleur de ce tour de boucle 
		current_color = couleurs.string_to_hexa (liste[i % len (liste)])

		if mode == "cercle":
			# Fait un cercle ... mouhaha
			primitives.cercle (6,taille * 2 + 20,generer_couleurs (current_color,6, taille))
		elif mode == "arc":
			primitives.arc (20,taille + 10,generer_couleurs (current_color,5, taille))
		else: # mode == "ligne"
			primitives.colonnes (1,taille + 10, taille + 10,generer_couleurs (current_color,4,taille))

# TODO: bouger cette fonction ailleurs 
def try_load_int (fichier,variable):
	""" Tente de charger un nombre dans un fichier 
		de configuration ...

		@fichier : str = le nom du fichier 
		@variable : str = le nom de la variable

		@return : int = la valeur convertie en int

		@throw : persistance.FichierInvalide
				 persistance.CleInvalide
				 persistance.ValeurInvalide (chemin,fichier)
	"""
	try:
		m = persistance.get_propriete (fichier, variable)
		k = int (m)
		return k
	except ValueError:
		raise persistance.ValeurInvalide (fichier,variable)

def run (t,mode = "cercle"):
	""" Fait un chargement d'une durée
		de t secondes ... Un super écran ! 

		@t : int = secondes
		@mode : str (cercle|arc|ligne) = le mode d'affichage de la barre de chargement

		@return : None 
		
		@throw : persistance.FichierInvalide
				 persistance.CleInvalide
				 persistance.ValeurInvalide (chemin,fichier)
	"""
	
	primitives.raz ()
	primitives.speed (0)
	
	# Affiche le fond d'écran approprié
	th = themes.actuel () # le thème actuel 
	
	# TODO: gérer ça autrement ...
	primitives.bgpic ("Images/Theme{0}/chargement.gif".format (th))
	
	# Affiche une astuce
	# Récupère une astuce au hasard dans celles disponibles
	maximum = try_load_int ("phrases","max")
	numero = randint (0,maximum - 1)
	
	# Cette ligne est susceptible de planter ... Il faut que le type récupère l'erreur !
	astuce = persistance.get_propriete ("phrases", str (numero))
	
	# Ces lignes redirigent les erreurs de « persistance »
	# vers l'appelant, en ajoutant la gestion du fait 
	# que la variable peut être invalide, c'est à dire 
	# qu'elle n'est pas convertible en int 
	r = themes.get_theme_opts (th, "x:astuce", "y:astuce", "x:chargement", "y:chargement")
	
	r = list (map (int, r))
	xa,ya,xc,yc = r

	primitives.aller_a (xa,ya)
	primitives.color ("red")
	primitives.texte (astuce,"petit")
	
	primitives.aller_a (xc,yc)
	
	primitives.down ()
	animation (t,mode)
	
	primitives.aller_a (0,0)
	primitives.seth (0)

if __name__ == '__main__':
	# Si on lance le module seul
	persistance.init ()
	couleurs.init ()

	init ()
	run (2,"cercle")
	primitives.raz ()
	run (2,"arc")
	primitives.raz ()
	run (2,"ligne")
