#-*- coding: utf-8 -*-
# Les fonctions de l'ia
# ...

import couleurs
import moteur
import iconsole
import persistance
from random import choice # faire un choix aléatoire dans une liste 
from random import * #j'ai besoin de randint() !

def generer_couleurs_aleatoires ():
	""" Génère un code aléatoire de couleurs, complètement !

		@return : list of couleurs (Français)
	"""

	sortie = [] # le tableau de sortie 

	# On récupère la liste des couleurs possibles
	lst = couleurs.liste_couleurs ()

	# On récupère le nombre de cases demandées
	n = persistance.get_propriete ("config","nombre_cases")

	# On définit n couleurs au hasard ... 
	for i in xrange (int (n)):
		sortie.append (choice (lst))
	
	return sortie
	
def random_choice(S):
	""" fonction qui permet de choisir une code dans la liste des possibilités générés
		Je sais pas si generer_couleurs_aleatoires fait la même chose...
	"""
    a = randint(0,len(S)-1)
    return S[a]

def create_list(S):
    """Créé une liste de toutes les combinaison possibles des objets dans S (une même couleur peux se retrouver plusieurs fois)
        len(li) = n^(4) à l'issue de cette fonction (où n est len(S))

        @S : list = L'univers, l'ensemble des possibilités, pour le mastermind, le nombre de couleurs
        @return : list = li la liste de toutes les combinaison

    """
    li=[]
    for i in S:
        temp = [0,0,0,0]
        temp[0] = i
        for j in S:
            temp[1] = j
            for k in S:
                temp[2] = k
                for l in S:
                    temp[3] = l
                    li.append(list(temp))
    return li

# L'IA définit le code 
def choisir_code (mode="aleatoire"):
	""" Définit le code à trouver pour la partie 
		de mastermind, de manière aléatoire 

		@return : None
	"""
	
	# les fonctions définies ici ne sont pas visibles 
	# depuis l'extérieur ! C'est le but !

	def ia_alea ():
		# BRUTE FORCE !!!!
		# On crée des listes aléatoires 
		# et on teste, jusqu'au jour où
		# le code secret proposé est valide 
		# par rapport à la difficulté 
		condition = True
	
		while condition:
			r = moteur.definir_code (generer_couleurs_aleatoires ())
			if r != False:
				condition = False

	# fin def ia_alea ici 

	if mode == "aleatoire":
		ia_alea ()
	else:
		return False 

# L'IA joue, avec un mode 
def jouer (mode = "aleatoire"):
	""" Fait jouer l'IA pour deviner le code 

		@mode : string (aleatoire | knuth | matrice) = 
			le mode de résolution 

		@return : None
	"""

	def ia_alea ():
		# On fait pas dans la finesse ici 
		# Il faut plus de rafinement --"
		while True:
			prop = generer_couleurs_aleatoires ()
			r = moteur.proposer_solution (prop)
		
			# On affiche que si le coup était valide
			# (sinon on a plein de trucs nuls :-P)
			if r != False:
				iconsole.afficher ("IA", "Joue {0} -> {1}".format (prop,r))
	
			if r == "perdu" or r == "gagne":
				return
	def ia_knuth(S):
    		li = create_list(S)
    		proposition = random_choice(li)
   		sol = moteur.proposer_solution(proposition)
    		if sol == False:
			return False
    		if sol == "gagne":
        		return "gagne"
    		if sol == "perdu":
        		return "perdu"
#Autant prévenir à partir de là ça par en couille, j'ai juste essayer de faire au plus réutilisable...
    		else:
        		for i in li:
           			temp = moteur.proposer_solution(i)
            """Ou une autre punaise de fonction qui serait plus appropriée...
                Dans l'idéal un truc qui me permet de mettre en argument le code et la proposition et qui retourne un tuple uniquement"""
           			 if type(temp) == tuple:
                			if temp == sol:
                				li.remove(i)
                    

	if mode == "aleatoire":
		ia_alea ()
	elif mode == "knuth":
		ia_knuth ()
	else:
		return False
