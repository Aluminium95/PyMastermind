#-*- coding: utf-8 -*-
# 03/04/2013

import persistance
import affichage
import moteur
import iconsole
import joueur
import ia
import couleurs
import misc
import regles

import primitives 
import chargement 

from random import randint

# C'est un gros paquet d'aide !
aide = {
	"global" : {
		"quit" : "Quitte le programme ...",
		"regles" : "Affiche les règles du jeu ...",
		"scores" : "Affiche les meilleurs scores du jeu ...",
		"fortune" : "Affiche une petite phrase aléatoire sympa ...",
		"score" : "Affiche le score actuel ..."
	},
	"Menu" : {
		"ia-code" : "Fait décider un code à trouver par une IA",
		"ia-joue" : "Fait trouver le code par une IA (nécessite qu'un code ai été défini avant)",
		"humain-code" : "Fait rentrer un code à l'utilisateur",
		"humain-joue" : "Fait trouver le code à l'utilisateur",
		"theme" : "Permet à l'utilisateur de chosir un thème",
		"niveau" : "Permet à l'utilisateur de changer de niveau de difficulté"
	},
	"Niveau" : {
		"list" : "Fait la liste des niveaux disponibles",
		"actuel" : "Affiche le niveau actuel de difficulté",
		"fin" : "Enregistre le niveau sélectionné et revient au menu",
		"@" : "Une autre chaine de caractère est prise comme un niveau"
	},
	"Theme" : {
		"list" : "Fait la liste des thèmes disponibles",
		"actuel" : "Affiche le thème actuel ...",
		"fin" : "Engeristre le thème sélectionné et revient au menu",
		"@" : "Sélectionne le texte rentré comme un thème"
	},
	"Humain-Joue" : {
		"proposer" : "Permet de faire une proposition, si et seulement si le plateau est affiché",
		"plateau" : "Permet de réafficher le plateau de jeu",
		"score" : "Permet de savoir le score actuel", # Pour l'instant c'est faux
		"abandon" : "Permet de revenir au menu, et abandonner la partie"
	}
}

class Mastermind:
	""" La classe princpale du mastermind : c'est le jeu en lui même !
	"""
	def __init__ (self,initial):
		""" Constructeur 
			
			@initial : str = l'état de départ 
			
			@return : Mastermind 
		"""
		self.etat = initial
		self.ecran = "plateau" # Quel est l'écran actuel ?
		
	def afficher (self, quelquechose, t = 0):
		""" Une surcouche de iconsole.afficher 
			qui met automatiquement l'état courant 
			en « acteur »
			
			@quelquechose : str = un truc à afficher 
			@t : int = nombre de tabulations 
			
			@return : None
		"""
		iconsole.afficher (self.get (), quelquechose, t)
	
	def afficher_liste (self, quelquechose, generateur, t = 0):
		""" Encore une surcouche qui englobe iconsole.afficher_liste
			
			@quelquechose : str = texte
			@generateur : generator = générateur de liste
			@t : int = tabulations 
			
			@return : None
		"""
		iconsole.afficher_liste (self.get (), quelquechose, generateur, t)
	
	def demander (self, quelquechose, t = 0):
		""" Une surcouche de iconsole.demander 
			qui met l'état actuel en « acteur »
			
			@quelquechose : str = un truc à afficher 
			@t : int = nombre de tabulations 
			
			@return : str
		"""
		return iconsole.demander (self.get (), quelquechose, t)
		
	def get (self):
		""" Retourne l'état courant 
			
			@return : str 
		"""
		return self.etat
	
	def set (self, state):
		""" Définit l'état courant 
			
			@state : str = le nouvel état 
			
			@return : None
		"""
		self.etat = state 
		# petits trucs ici pour les transitions 
		iconsole.separateur ()
		self.afficher ("Vous êtes maintenant dans un nouveau mode")
		self.aide () # Affiche l'aide du nouvel état 
	
	def aide (self):
		""" Affiche l'aide globale ainsi que celle de l'état courant 
			
			@return : None
		"""
		# On Crée un générateur de l'aide actuelle
		# pour personnaliser un peu l'affichage de la liste 
		def gen_help ():
			yield "Commandes globales ..."
			for i,j in aide["global"].items ():
				yield ("\t" + i,j)
			
			yield "Commandes d'état"
			for i,j in aide[self.get ()].items ():
				yield ("\t" + i,j)
		# On l'affiche avec le magnifique module iconsole
		self.afficher_liste ("Aide : ", gen_help ())
	
	def send (self,rep):
		""" Envoie une requête utilisateur au Mastermind
			qui va gérer la redirection et les actions 
			nécessaires
			
			@rep : str = la requête
			
			@return : str = l'état actuel 
		"""
		if rep == "help": # Commande indépendante de l'état courant !
			self.aide ()
		elif rep == "regles": # Commande indépendante de l'état courant !
			self.afficher ( "Affichage des règles sur la fenêtre graphique ...")
			chargement.run (2,"ligne")
			regles.regles ()
			self.ecran = "regles"
		elif rep == "scores": # Commande indépendante de l'état courant !
			self.afficher ("Affichage des scores sur la fenêtre graphique ...")
			# primitives.raz ()
			affichage.high_score ()
			self.ecran = "scores"
		elif rep == "fortune":
			try:
				maximum = persistance.get_propriete ("phrases", "max")
				maximum = int (maximum)
				aleatoire = randint (0,maximum - 1)
				self.afficher (persistance.get_propriete ("phrases", str (aleatoire)))
			except persistance.CleInvalide:
				self.afficher ( "Il est impossible de récupérer la fortune ... le fichier « phrases » doit être corrompu »")
			except persistanec.FichierInvalide:
				self.afficher ( "Le fichier est introuvable ... Cela implique un problème dans le CODE SOURCE ... revenez plus tard ...")
			except ValueError:
				self.afficher ( "La valeur de « max » dans « phrases » est fausse et ne représente pas un nombre valide ...")
			except:
				self.afficher ( "Une erreur inconnue est survenue ... ")
		elif self.get () == "Humain-Joue":
			self.humain_joue (event)
		elif self.get () == "Menu":
			self.menu (event)
		
		else:
			raise ValueError
		
		return self.get ()
	
	def humain_joue (self,rep):
		""" Une fonction qui permet de faire jouer 
			l'humain quand on est dans l'état 
			« Humain-Joue »
			
			@rep : str = l'évènement à gérer
			
			@return : None
		"""
		if self.get () != "Humain-Joue":
			raise ValueError
		
		if rep == "abandon": # Abandon de la partie -> retour au menu
			self.afficher ("Vous avez abandonné la partie ...")
			self.set ("Menu")
		if rep == "plateau":
			self.afficher ("Le plateau est affiché, vous pouvez proposer des solutions")
			moteur.reprendre_partie ()
		elif rep == "proposer":
			if self.ecran != "plateau":
				affichage.reset ()
			
			Li = iconsole.demander_tableau ()
			try:
				r = moteur.verification_solution (Li)
				if r == "gagne":
					self.afficher ("Vous avez gagné !!!")
					self.set ("Menu")
				elif r == "perdu":
					self.afficher ("Vous avez perdu !!!")
					self.set ("Menu")
				elif r == False:
					self.afficher ("Votre proposition n'a pas de sens ...")
				else:
					a,b = r
			
					# On fait un joli affichage qui dit si on doit mettre un S ou pas ...
					sa = ""
					sb = ""

					if a > 1:
						sa = "s"

					if b > 1:
						sb = "s"
			
					messaga = "Il y a {0} bonne{1} couleur{1} bien placée{1}".format (a,sa)
					messagb = "Il y a {0} bonne{1} couleur{1} mal placée{1}".format (b,sb)

					self.afficher(messaga)
					self.afficher(messagb)
			except moteur.TableauInvalide as exception:
				self.afficher ("Le tableau est invalide : {0}".format (exception.message))
			except:
				self.afficher ("Une erreur inconnue est survenue ...")
		else:
			self.afficher ("Requête invalide ...")
				
	
	def theme (self,rep):
		""" Fonction qui premet de faire réagir le menu Theme
			
			@rep : str = l'évènement
			
			@reutrn : None
		"""
		if self.get () != "Theme":
			raise ValueError
		
		if rep == "list":
			def gen_liste_theme ():
				for i in affichage.liste_themes ():
					desc = persistance.get_propriete ("backgrounds", "theme:" + i + ":description")
					yield (i,desc)

			self.afficher_liste ("Themes",gen_liste_theme ())
		elif rep == "fin":
			self.afficher ("Theme modifié ... ")
			self.set ("Menu")
		else:
			try:
				
				affichage.choix_theme (int (rep)) # un truc qui peut facilement planter a cause du int
				self.afficher ("Selection theme : " + rep)
				primitives.raz ()
				path = "Images/Theme" + rep + "/fond.gif"
				primitives.bgpic (path)
			except ValueError:
				self.afficher ("Il faut entrer le numéro du thème ...")
			except persistance.CleInvalide:
				self.afficher ("Euh ... ce thème ne peut être chargé ...")
			except persistance.FichierInvalide:
				self.afficher ("Priez pauvres fous, le fichier de configuration est introuvable !")
	
	def niveau (self, rep):
		""" Fonction qui fait réagir le menu Niveau
			
			@rep : str = l'évènement
			
			@return : None
		"""
		if self.get () != "Niveau":
			raise ValueError
		
		if rep == "list":
			self.afficher (str (moteur.get_liste_modes ()))
		elif rep == "actuel":
			self.afficher ("Le mode de la prochaine partie est " + moteur.get_next_mode ())
		elif rep == "fin":
			self.afficher ("Niveau modifié pour la prochaine partie")
			self.set ("Menu")
		else:
			if rep in (moteur.get_liste_modes ()):
				self.afficher ("Vous avez sélectionné le niveau : " + rep)
				moteur.set_mode (rep)
				regles.regles () # affiche les règles 
				self.ecran = "regles"
			else:
				self.afficher ("Ce niveau est invalide ...")

	def menu (self, rep):
		""" Fonction qui permet de faire réagir le menu 
			à des actions 
			
			@rep : str = l'évènement
			
			@return : None
		"""
		if self.get () != "Menu":
			raise ValueError
		
		if rep == "ia-code":
			moteur.nouvelle_partie ()
			self.afficher ( "L'IA va choisir un code, on commence une nouvelle partie")
			chargement.run (5,"ligne")
			primitives.raz ()
			ia.choisir_code ()
			self.afficher ( "L'IA a déterminé un code")
		elif rep == "humain-code":
			moteur.nouvelle_partie ()
			self.afficher ( "L'humain va choisir un code, on commence une nouvelle partie")
			self.afficher ( "Le niveau actuel est : " + moteur.get_mode ())
			iconsole.afficher_liste (etat, "Les couleurs disponibles sont : ", couleurs.liste_couleurs ()[0:moteur.get_nombre_couleurs ()])
			joueur.choisir_code ()
			self.afficher ( "L'humain a déterminé un code")
		elif rep == "humain-joue":
			try:
				self.afficher ( "Le niveau actuel est : " + moteur.get_mode ())
				self.afficher_liste ("Les couleurs disponibles sont : ", couleurs.liste_couleurs ()[0:moteur.get_nombre_couleurs ()])
					
				chargement.run (10,"arc")
				affichage.reset ()
				
				self.set ("Humain-Joue")
				
				
			except moteur.PasEnCoursDePartie:
				self.afficher ( "Mmmh ... vous n'êtes pas en cours de partie ... il faut définir un code !")
			except:
				self.afficher ( "Une erreur inconnue est survenue ... ")
		elif rep == "ia-joue":
			self.afficher ("L'IA va jouer une partie")
			try:
				self.afficher ("Le niveau actuel est : " + moteur.get_mode ())
				self.afficher_liste ("Les IAs sont", [("knuth", "Une IA très forte"), ("aleatoire", "Une ia ... mauvaise !")])
				
				ia_mode = ""
				demander_ia = True
				while demander_ia == True:
					ia_mode = self.demander ("Quelle IA")
					if ia_mode in ["matrice", "aleatoire", "knuth"]:
						demander_ia = False
					else:
						self.afficher ("Ce mode d'IA est invalide !")
				self.afficher_liste ("Les couleurs disponibles sont : ", couleurs.liste_couleurs ()[0:moteur.get_nombre_couleurs ()])
				chargement.run (5,"cercle")
				affichage.reset ()
				ia.jouer (ia_mode)
			except moteur.PasEnCoursDePartie:
				self.afficher ("Vous n'êtes pas en cours de partie ... il faut définir un code !")
			except:
				self.afficher ("Une erreur inconnue est survenue dans l'IA ...")
		elif rep == "theme":
			self.set ("Theme")
		elif rep == "niveau":
			self.set ("Niveau")
		else:
			self.afficher ("Cette requête est invalide dans le menu ...")

if __name__ == '__main__':
	# Initialisations des modules dans le bon ordre !
	persistance.init ()
	couleurs.init ()
	affichage.init ()
	moteur.init ()
	
	iconsole.afficher ("Programme", "Bienvenue dans le mastermind !")

	e = "Menu"
	machine = Mastermind (e)

	iconsole.afficher (e, "Tapez « help » pour obtenir de l'aide ...")

	continuer = True
	while continuer == True:
		# Les commandes sont 
		# help, humain-code, humain-joue, quit, ia-joue, ia-code
		rep = iconsole.demander (e,"Commande")
		
		if rep == "quit":
			continuer = False
			iconsole.afficher ("Programme", "Quitte ...")
		else:
			e = machine.send (rep)
	
	try:
		persistance.save ()
	except persistance.EcritureImpossible:
		iconsole.afficher ("Erreur", "Il est impossible de sauvgarder les modifications de paramètres ...")
