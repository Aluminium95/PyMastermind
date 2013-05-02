#-*- coding: utf-8 -*-
# Fichier du joueur (némésis de ia.py)

# Charge toute l'arborescence ... on sait jamais 
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

# DEB EXCEPTIONS

class EcranInvalide (Exception): # Un problème d'écran 
	def __init__ (self, ecran):
		self.ecran = ecran 

class EtatInvalide (Exception): # Un problème d'état
	def __init__ (self, etat):
		self.etat = etat
		
class LeProgrammeurEstCon (Exception): # Ah, c'est une mauvaise utilisation d'une fonction
	pass

class ErreurFatale (Exception): # Pas la peine de continuer ...
	pass 

# FIN EXCEPTIONS

# C'est un gros paquet d'aide !
aide = {
	"global" : {
		"quit" : "Quitte le programme ...",
		"regles" : "Affiche les règles du jeu ...",
		"scores" : "Affiche les meilleurs scores du jeu ...",
		"fortune" : "Affiche une petite phrase aléatoire sympa ...",
		"couleurs" : "Affiche la liste des couleurs disponibles",
		"clear" : "Efface l'écran de la console ..."
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
		"score" : "Permet de savoir le score actuel",
		"abandon" : "Permet de revenir au menu, et abandonner la partie",
		"historique" : "Permet d'afficher l'historique des coups déjà joués et leur réponses",
		"abandon" : "Revient au mode « Humain-Joue » en ne proposant pas ce code",
		"valider" : "Propose le tableau au mastermind et affiche la réponse, revient à l'état « Humain-Joue »",
		"annuler" : "Supprime le dernier item du tableau",
		"historique" : "Permet d'afficher l'historique des coups déjà joués et leur réponses",
		"@" : "Une autre chaine est prise comme une couleur à ajouter en fin de tableau"
	},
	"Definir-Code" : {
		"abandon" : "Revient au menu en annulant la partie actuelle",
		"fin" : "Valide le code et revient au menu, la partie est lancée !",
		"annuler" : "Supprime du tableau la dernière entrée",
		"@" : "Une autre chaine de caractères est prise comme une couleur à ajouter à la fin"
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
		self.etats = ["Menu","Humain-Joue","Theme","Niveau","Proposer-Code","Definir-Code"]
		self.ecrans = ["plateau", "regles", "scores"]
		self.etat = ""
		self.ecran = "plateau" # Quel est l'écran actuel ?
		
		self.tableau_tampon = [] # Un tableau tampon, pour les états Proposer-Code et Definir-Code
		
		self.set (initial)
		
	def afficher (self, quelquechose, t = 0):
		""" Une surcouche de iconsole.afficher 
			qui met automatiquement l'état courant 
			en « acteur »
			
			@quelquechose : str = un truc à afficher 
			@t : int = nombre de tabulations [opts]
			
			@return : None
		"""
		iconsole.afficher (self.get (), quelquechose, t)
	
	def afficher_liste (self, quelquechose, generateur, t = 0):
		""" Encore une surcouche qui englobe iconsole.afficher_liste
			
			@quelquechose : str = texte
			@generateur : generator = générateur de liste
			@t : int = tabulations [opts]
			
			@return : None
		"""
		iconsole.afficher_liste (self.get (), quelquechose, generateur, t)
	
	def demander (self, quelquechose, t = 0):
		""" Une surcouche de iconsole.demander 
			qui met l'état actuel en « acteur »
			
			@quelquechose : str = un truc à afficher 
			@t : int = nombre de tabulations [opts]
			
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
		if state not in self.etats:
			raise EtatInvalide (state)
		
		self.etat = state 
		# petits trucs ici pour les transitions 
		# iconsole.separateur ()
		iconsole.clear ()
		self.afficher ("Vous êtes maintenant dans un nouveau mode")
		self.aide () # Affiche l'aide du nouvel état 
		
	def set_ecran (self, new, t = False):
		""" Change d'écran sur la fenêtre turtle 
			
			@new : str = le nouvel écran
			@t : int = temps de chargement [opts]
			
			@return : None
		"""
		if new == "plateau":
			if t != False:
				chargement.run (t, "arc")
			
			if moteur.est_en_partie () == True:
				moteur.reprendre_partie ()
			else:
				affichage.plateau ()
				
		elif new == "regles":
			if t != False:
				chargement.run (t, "cercle")
				
			regles.regles (moteur.get_next_mode ())
		elif new == "scores":
			if t != False:
				chargement.run (t, "ligne")
				
			affichage.high_score ()
		elif new == "fond":
			if t != False:
				chargement.run (t, "ligne") 
		else:
			raise EcranInvalide
		
		self.ecran = new
	
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
			
			yield "Commandes du mode " + self.get ()
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
			
			self.set_ecran ("regles", 2)
		elif rep == "clear":
			iconsole.clear ()
		elif rep == "scores": # Commande indépendante de l'état courant !
			self.afficher ("Affichage des scores sur la fenêtre graphique ...")
			
			self.set_ecran ("scores", 1)
			
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
				
		elif rep == "couleurs":
			nombre_couleurs = False
			try:
				nombre_couleurs = moteur.get_nombre_couleurs ()
			except moteur.PasEnCoursDePartie:
				self.afficher ("Vous n'êtes pas en cours de partie, on affiche les couleurs futurement disponibles")
				nombre_couleurs = moteur.get_nombre_couleurs_next ()
			
			def generateur_liste_couleurs (nbr):
				abvrs = couleurs.liste_abreviations ()
				for i in abvrs[0:nbr]:
					a = "({0}) {1}".format (i, couleurs.abrv_to_string (i))
					yield a
				
			self.afficher_liste ("Couleurs futurement disponibles",generateur_liste_couleurs (nombre_couleurs))
				
		elif self.get () == "Humain-Joue":
			self.humain_joue (rep)
		elif self.get () == "Menu":
			self.menu (rep)
		elif self.get () == "Theme":
			self.theme (rep)
		elif self.get () == "Niveau":
			self.niveau (rep)
		elif self.get () == "Proposer-Code":
			self.proposer_code (rep)
		elif self.get () == "Definir-Code":
			self.definir_code (rep)
		else:
			raise ErreurFatale
		
		return self.get ()
	
	def humain_joue (self,rep):
		""" Une fonction qui permet de faire jouer 
			l'humain quand on est dans l'état 
			« Humain-Joue »
			
			@rep : str = l'évènement à gérer
			
			@return : None
		"""
		if self.get () != "Humain-Joue":
			raise LeProgrammeurEstCon
		
		if rep == "abandon": # Abandon de la partie -> retour au menu
			self.afficher ("Vous avez abandonné la partie ...")
			self.set ("Menu")
		elif rep == "score":
			self.afficher (moteur.calcul_score ())
		elif rep == "plateau":
			self.afficher ("Le plateau est affiché, vous pouvez proposer des solutions")
			moteur.reprendre_partie ()
			self.set_ecran ("plateau")
		elif rep == "historique":
			h = moteur.get_historique ()
			def generateur_historique (hist):
				for i in hist:
					# i = [[a,b,c,d], (e,f)]
					coup = i[0]
					resultat = i[1]
					
					sa = ""
					if resultat[0] > 1:
						sa = "s"
					
					sb = ""
					if resultat[1] > 1:
						sb = "s"
					
					string = "{0} rouge{1}, {2} blanche{3}".format (resultat[0],sa,resultat[1],sb)
					
					yield (coup,string) 
					
			self.afficher_liste ("Historique", generateur_historique (h))
		elif rep == "valider":
			self.afficher ("Valide le nouveau code ...")
			self.set_ecran ("plateau")
			try:
				r = moteur.verification_solution ( self.tableau_tampon )
			except moteur.TableauInvalide as exception:
				self.afficher ("Le tableau est invalide : {0}".format (exception.message))
			else:
				
				if r == "gagne":
					self.afficher ("Vous avez gagné !!!")
					
					nom = self.demander ("Nom du joueur")
					
					moteur.enregistre_score (nom)
					
					self.set ("Menu")
				elif r == "perdu":
					self.afficher ("Vous avez perdu !!!")
					
					self.set ("Menu")
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

					self.tableau_tampon = []
					
					iconsole.separateur ()
					self.afficher(messaga)
					self.afficher(messagb)
					
		elif rep == "annuler":
			try:
				self.tableau_tampon = self.tableau_tampon[:-1] # Retire la dernière valeur ...
				self.afficher (self.tableau_tampon)
			except:
				self.afficher ("Plus rien à annuler ...")
		else:
			self.tableau_tampon.append (rep)
			self.afficher (self.tableau_tampon)
	
	def theme (self,rep):
		""" Fonction qui premet de faire réagir le menu Theme
			
			@rep : str = l'évènement
			
			@reutrn : None
		"""
		if self.get () != "Theme":
			raise LeProgrammeurEstCon
		
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
				self.set_ecran ("fond")
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
			raise LeProgrammeurEstCon
		
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
				self.set_ecran ("regles", 3)
			else:
				self.afficher ("Ce niveau est invalide ...")
			
	def definir_code (self, rep):
		""" Fait réagir la définition de code 
		
			@rep : str = l'évènement
			
			@return : None
		"""
		if self.get () != "Definir-Code":
			raise LeProgrammeurEstCon
		
		if rep == "abandon":
			self.afficher ("Annule la propositon de code ... ")
			self.tableau_tampon = [] 
			self.set ("Menu")
		elif rep == "fin":
			self.afficher ("Valide le nouveau code ...")
			moteur.nouvelle_partie ()
			try:
				r = moteur.definir_code ( self.tableau_tampon )
			except moteur.TableauInvalide as exception:
				self.afficher ("Le tableau est invalide : {0}".format (exception.message))
			else:
				self.tableau_tampon = []
				self.set ("Menu")
		elif rep == "annuler":
			try:
				self.tableau_tampon = self.tableau_tampon[:-1] # Retire la dernière valeur ...
			except:
				self.afficher ("Plus rien à annuler ...")
			else:
				self.afficher (self.tableau_tampon)
		else:
			self.tableau_tampon.append (rep)
			self.afficher (self.tableau_tampon)
	
	def menu (self, rep):
		""" Fonction qui permet de faire réagir le menu 
			à des actions 
			
			@rep : str = l'évènement
			
			@return : None
		"""
		if self.get () != "Menu":
			raise LeProgrammeurEstCon
		
		if rep == "ia-code":
			moteur.nouvelle_partie ()
			self.afficher ( "L'IA va choisir un code, on commence une nouvelle partie")
			self.set_ecran ("plateau", 5)
			ia.choisir_code ()
			self.afficher ( "L'IA a déterminé un code")
		elif rep == "humain-code":
			self.set ("Definir-Code")
			self.afficher_liste ("Les couleurs disponibles sont : ", couleurs.liste_couleurs ()[0:moteur.get_nombre_couleurs_next ()])
		elif rep == "humain-joue":
			try:
				self.afficher ("Le niveau actuel est : " + moteur.get_mode ())
			except moteur.PasEnCoursDePartie:
				self.afficher ("Mmmh ... vous n'êtes pas en cours de partie ... il faut définir un code !")
			else:
				self.set_ecran ("plateau", 5)
				
				self.set ("Humain-Joue") # Change d'état
				self.afficher_liste ("Les couleurs disponibles sont : ", couleurs.liste_couleurs ()[0:moteur.get_nombre_couleurs ()])
		elif rep == "ia-joue":
			self.afficher ("L'IA va jouer une partie")
			try:
				self.afficher ("Le niveau actuel est : " + moteur.get_mode ())
			except moteur.PasEnCoursDePartie:
				self.afficher ("Vous n'êtes pas en cours de partie ... il faut définir un code !")
			else:
				self.afficher_liste ("Les IAs sont", [("knuth", "Une IA très forte"), ("aleatoire", "Une ia ... mauvaise !"), ("matrice","Une IA moyenne")])
				
				ia_mode = ""
				demander_ia = True
				while demander_ia == True:
					ia_mode = self.demander ("Quelle IA")
					if ia_mode in ["matrice", "aleatoire", "knuth"]:
						demander_ia = False
					else:
						self.afficher ("Ce mode d'IA est invalide !")
				self.afficher_liste ("Les couleurs disponibles sont : ", couleurs.liste_couleurs ()[0:moteur.get_nombre_couleurs ()])
				
				self.set_ecran ("plateau", 3)
				
				for i in ia.jouer (ia_mode):
					primitives.aller_a (200,-200)
					chargement.animation (3,"cercle",20)
				
				moteur.enregistre_score (ia_mode)
				
		elif rep == "theme":
			self.set ("Theme")
		elif rep == "niveau":
			self.set ("Niveau")
		else:
			self.afficher ("Cette requête est invalide dans le menu ...")