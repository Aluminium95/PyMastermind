#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Fichier d'utilitaires 
# qui permet de regrouper 
# des fonctions généralistes
# utiles au programme

def bi_map (f,a,b):
	""" 
		- f
		- (a b c d ...)
		- (e f g h ...)
		-> (f(a,e) f(b,f) f(c,g) f(d,h) ...)
	"""

	k = 0
	S = []

	while k < len (a) and k < len (b):
		S.append (f (a[k],b[k]))
		k += 1
                
	return S

def foldl (f,n,l):
	""" fonction, neutre, liste
		
		[a, b, c, d]
		f(d,f(c,f(b,f(a,n))))
	"""

	for i in l:
		n = f (n,i)
	
	return n

def egal (a,b):
	""" Un wrapper autour de l'égalité """
	return a == b
