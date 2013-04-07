# -*- coding: utf-8 -*-
# ensemble de fonctions...
# 03/04/2013
# prend une chaine de caract�re et le traduit str � bool.

def question_fermee (chaine):
	""" Dit si la r�ponse � une question ferm�e 
		est oui o� non 

		@chaine : string = la r�ponse � la question 

		@return : bool = True si oui, False si autre chose (attention !)
	"""

	# chaine.upper () permet de tout mettre en majuscule
	# ce qui premet � � OuI � de devenir � OUI � et de 
	# bien correspondre ... On sait jamais !
	if chaine.upper () == "OUI" or chaine.upper () == "O":
		return True
	else:
		return False

