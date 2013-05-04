


boutons = [] # Tableau des boutons

def ajouter_bouton (nom,cote,position):
	global boutons
	boutons.append ([nom,cote,position])

def click_to_bouton (x,y):
	
	for i in boutons:
		w = i[1]
		xb,yb = i[2]
		if xb < x < xb + w and yb < y < yb + w:
			return i[0] # le nom 
		
def callback (x,y):
	print (click_to_bouton (x,y))
	
def init ():
	""" Constructeur 
		
		@initial : str = l'état de départ 
		
		@return : Mastermind 
	"""
	set_etat ("Menu")
	set_ecran ("plateau")
	
	sc = getscreen ()
	sc.onclick (callback)


def afficher_boutons_couleurs ():
	""" Affiche la liste des couleurs disponibles 
		actuellement si possible, ou 
		future si on n'est pas en cours de partie
		
		@return : None
	"""
	nombre_couleurs = False
	try:
		nombre_couleurs = moteur.get_nombre_couleurs ()
	except moteur.PasEnCoursDePartie:
		nombre_couleurs = moteur.get_nombre_couleurs_next ()
	
	def generateur_liste_couleurs (nbr):
		c = couleurs.liste_couleurs ()[0:nbr] # Prend le bon nombre de couleurs
		
		for i in c:
			color (couleurs.string_to_hexa (i))
			begin_fill ()
			carre (40)
			end_fill ()
			ajouter_bouton (i,40,position ()) # Ajoute un bouton
			yield
		
	aller_a (140,200)
	lignes (3, 50, 50, generateur_liste_couleurs (nombre_couleurs))
