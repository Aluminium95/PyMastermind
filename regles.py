# -*- coding: utf-8 -*-
#règles du jeu (mode facile au mode difficile)
#05/04/2013
#regles_du_jeu1 : niveau facile.
#regles_du_jeu2 : niveau normal.
#regles_du_jeu3 : niveau difficile.
# Bien appeler la fonction ainsi : regles_du_jeu1("black") ==> avec "black" ainsi histoire de pourvoir lire les caractères.

from turtle import*

def regles_du_jeu1(couleur):
        """Affiche les règles ainsi que les aides du jeu. En mode facil.
(un fond y est inséré)"""
        screensize(600,600,"white")
        bgpic("ff.gif")
        up()
        goto(30,220)
        color(couleur)
        text="Voici les règles du mastermind mode facil:"
        write(text, False, "center", ("calibri",16,"underline"))
        goto(50,150)
        text2="- Vous devez deviner le code couleur du jeu."
        write(text2, False, "center", ("calibri",16,"normal"))
        goto(-132,120)
        dot(10,"red")
        goto(80,110)
        text3=" : Signifie que la couleur est juste et bien placée."
        write(text3, False, "center", ("calibri",16,"normal"))
        goto(-132,90)
        dot(10,"black")
        goto(90,80)
        text4=" : Signifie que la couleur est juste mais mal placée."
        write(text4, False, "center", ("calibri",16,"normal"))
        goto(9,50)
        text5="- Il y a 8 couleurs sélectionnables."
        write(text5, False, "center", ("calibri",16,"normal"))
        goto(64,20)
        text6="- Le code à trouver est composé de 4 couleurs."
        write(text6, False, "center", ("calibri",16,"normal"))
        goto(69,-10)
        text7="- Vous avez 10 essais maximum pour le deviner."
        write(text7, False, "center", ("calibri",16,"normal"))
        goto(50,-40)
        color("red")
        begin_fill()
        text8="Attention,"
        write(text8, False, "center", ("calibri",16,"normal"))
        end_fill()
        color("black")
        goto(80,-60)
        text9="si rien n'est indiqué, alors votre réponse est fausse."
        write(text9, False, "center", ("calibri",16,"normal"))


def regles_du_jeu2(couleur):
        """Affiche les règles ainsi que les aides du jeu. En mode normal.
(un fond y est inséré)"""
        screensize(600,600,"white")
        bgpic("fn.gif")
        up()
        goto(30,220)
        color(couleur)
        text="Voici les règles du mastermind mode normal:"
        write(text, False, "center", ("calibri",16,"underline"))
        goto(50,150)
        text2="- Vous devez deviner le code couleur du jeu."
        write(text2, False, "center", ("calibri",16,"normal"))
        goto(-132,120)
        dot(10,"red")
        goto(80,110)
        text3=" : Signifie que la couleur est juste et bien placée."
        write(text3, False, "center", ("calibri",16,"normal"))
        goto(-132,90)
        dot(10,"black")
        goto(90,80)
        text4=" : Signifie que la couleur est juste mais mal placée."
        write(text4, False, "center", ("calibri",16,"normal"))
        goto(14,50)
        text5="- Il y a 12 couleurs sélectionnables."
        write(text5, False, "center", ("calibri",16,"normal"))
        goto(63,20)
        text6="- Le code à trouver est composé de 4 couleurs."
        write(text6, False, "center", ("calibri",16,"normal"))
        goto(69,-10)
        text7="- Vous avez 10 essais maximum pour le deviner."
        write(text7, False, "center", ("calibri",16,"normal"))
        goto(50,-40)
        color("red")
        begin_fill()
        text8="Attention,"
        write(text8, False, "center", ("calibri",16,"normal"))
        end_fill()
        color("black")
        goto(80,-60)
        text9="si rien n'est indiqué, alors votre réponse est fausse."
        write(text9, False, "center", ("calibri",16,"normal"))

def regles_du_jeu3(couleur):
        """Affiche les règles ainsi que les aides du jeu. En mode difficile.
(un fond y est inséré)"""
        screensize(600,600,"white")
        bgpic("fd.gif")
        up()
        goto(30,220)
        color(couleur)
        text="Voici les règles du mastermind mode difficile:"
        write(text, False, "center", ("calibri",16,"underline"))
        goto(50,150)
        text2="- Vous devez deviner le code couleur du jeu."
        write(text2, False, "center", ("calibri",16,"normal"))
        goto(-132,120)
        dot(10,"red")
        goto(80,110)
        text3=" : Signifie que la couleur est juste et bien placée."
        write(text3, False, "center", ("calibri",16,"normal"))
        goto(-132,90)
        dot(10,"black")
        goto(90,80)
        text4=" : Signifie que la couleur est juste mais mal placée."
        write(text4, False, "center", ("calibri",16,"normal"))
        goto(14,50)
        text5="- Il y a 16 couleurs sélectionnables."
        write(text5, False, "center", ("calibri",16,"normal"))
        goto(63,20)
        text6="- Le code à trouver est composé de 4 couleurs."
        write(text6, False, "center", ("calibri",16,"normal"))
        goto(69,-10)
        text7="- Vous avez 10 essais maximum pour le deviner."
        write(text7, False, "center", ("calibri",16,"normal"))
        goto(50,-40)
        color("red")
        begin_fill()
        text8="Attention,"
        write(text8, False, "center", ("calibri",16,"normal"))
        end_fill()
        color("black")
        goto(80,-60)
        text9="si rien n'est indiqué, alors votre réponse est fausse."
        write(text9, False, "center", ("calibri",16,"normal"))


