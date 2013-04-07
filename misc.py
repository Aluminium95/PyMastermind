# -*- coding: utf-8 -*-
# ensemble de fonctions...
# 03/04/2013
# prend une chaine de caractère et le traduit str à bool.

def question_fermee (chaine):
	""" Dit si la réponse à une question fermée 
		est oui où non 

		@chaine : string = la réponse à la question 

		@return : bool = True si oui, False si autre chose (attention !)
	"""

	# chaine.upper () permet de tout mettre en majuscule
	# ce qui premet à « OuI » de devenir « OUI » et de 
	# bien correspondre ... On sait jamais !
	if chaine.upper () == "OUI" or chaine.upper () == "O":
		return True
	else:
		return False

