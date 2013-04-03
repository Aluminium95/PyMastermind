#-*- coding: utf-8 -*-

# 29/03/13
#derniere maj 3/4

import persistance
import couleurs
import affichage

code_secret = False
mode = "moyen"
restant = persistance.get_propriete ("config","coups:facile")
liste_mode = ["facile","moyen","difficile"]

def get_mode ():
	return mode

def set_mode (m):
	global mode,restant
	
	if m in liste_modes:
		mode = m
		restant = persistance.get_propriete ("config","coups:"+m)
		return True
	else:
		return False

def get_restant ():
    return restant

def double_couleur (test):
	liste_test = []
	for i in test:
		if i in liste_test:
			return False
		else:
			liste_test.append(i)
	return True

def definir_code (tableau):
                        
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
	global restant

	# couleurs.is_string (c) 
	# il faut verifier que la couleur est valide 

	a = 0
	b = 0
	i = 0

	solution = list (code_secret)

	while i < len (code_secret):
		if solution[i] == proposition[i]:
			a = a+1
			solution[i] = "*"
		i = i+1
	i = 0

	while i < len (code_secret):
		j = 0
		while j < len (solution):
			if solution[j] != "*" and solution[j] == proposition[i]:
				b = b+1
				solution[j] = "*"
				break
			j = j + 1
		i = i+1

	restant -= 1
	if a == 4:
		affichage.win ("red")
		return "gagne"
	elif restant == 0:
		affichage.perdu ()
		return "perdu"
	else:
		l = []
		for i in proposition:
			l.append (couleurs.string_to_hexa (i))
		
		affichage.afficher_couleurs (4,l,(a,b))
		return (a,b)

