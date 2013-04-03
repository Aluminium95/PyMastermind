#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
# Lopez Aliaume
# 
# 30 mars 2013
# 15:18
#
#
# Ce module sert à créer des 
# FSM de manière simple et efficace,
# en permettant une programmation 
# plus facile de tout ce qui requiert
# par définition des machines à état 

## Constructeur 
def new ():
	""" Crée une nouvelle machine à état 
		
		@return : fsm
	"""
	m = {}
	
	m["state"] = None
	
	m["states"] = {}
	m["states"][None] = {}
	
	m["transitions"] = {}
	m["proprietes"] = {}
	
	return m

## Gestion des transitions 
def get_state (machine):
	""" Retourne l'état courant de la machine
		
		@machine : fsm = machine à examiner
		
		@return : string = état courant 
	"""
	return machine["state"]

def add_state (machine,name):
	""" Ajoute un état possible à la liste 
		Le crée s'il n'existe pas, sinon,
		ne fait rien 
		
		@machine : fsm = machine à modifier
		@name : string = nom de l'état 
		
		@return : None
	"""
	if name not in machine["states"]:
		machine["states"][name] = {} # crée l'état
		machine["transitions"][name] = {} # crée les transitions 
		
def set_transition (machine,depart,arrivee,func):
	""" Ajoute une transition 
		
		@depart : string = état de départ
		@arrivee : string = état d'arrivée
		@func : fonction = fonction de transition
			de la forme : « f (fsm) -> None »
			
		@return : None
	"""
	add_state (machine, depart)
	add_state (machine, arrivee)
	
	machine["transitions"][depart][arrivee] = func
	
def transition (machine,arrivee):
	""" Lance la transititon vers l'état d'arrivée
		
		@arrivee : string = état d'arrivée
		
		@return : bool = si cela s'est bien passé 
	"""
	if get_state (machine) == None:
		machine["state"] = arrivee
	else:
		try:
			prec = get_state (machine)
			machine["transitions"][prec][arrivee] (machine) # on prend la machine en argument
			machine["state"] = arrivee
			machine["states"][prec] = {} # supprime les variables d'état
		except:
			return False
			
	return True

## Accesseurs des propriétés 
def set_special_property (machine,prop,value):
	""" Définit une propriété globale, accessible
		plus tard, de n'importe quel état 
		
		@machine : fsm = la machine à modifier
		@prop : string = le nom de la propriété 
		@value : ? = la valeur à mettre
	
		@return : None
	"""
	machine["proprietes"][prop] = value
	
def get_special_property (machine,prop):
	""" Récupère une propriété globale 
		
		@machine : fsm = la machine
		@prop : string = le nom de la propriété 
		
		@return : ? = la valeur de la propriété 
	"""
	return machine["proprietes"][prop]

def get_state_property (machine, prop):
	""" Récupère une propriété spécifique à l'état
		actuel de la machine ... 
		
		@machine : fsm = la machine
		@prop : string = le nom de la propriété
		
		@return : ? = la valeur de la propriété 
	"""
	return machine["states"][get_state (machine)][prop]

def set_state_property (machine, prop, value):
	""" Définit une propriété spécifique à l'état courant
		qui sera supprimée à la prochaine transition
		
		@machine : fsm = la machine
		@prop : string = le nom de la propriété
		@value : ? = la valeur 
		
		@return : None
	"""
		
	machine["states"][get_state (machine)][prop] = value
	
### EXAMPLE :

if __name__ == '__main__':
	def hello_world (m):
		print "hello"
	
	def world_hello (m):
		print "world"

	turtlemachine = new ()
	set_transition (turtlemachine, "hello", "world", hello_world)
	set_transition (turtlemachine, "world", "hello", world_hello)

	while True:
		r = raw_input ()
		if get_state (turtlemachine) == "hello":
			transition (turtlemachine,"world")
		else:
			transition (turtlemachine,"hello")
	
