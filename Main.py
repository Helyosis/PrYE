#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interface graphique."""

import tkinter as tk
from tkinter import messagebox
from ErgoIntro import ErgoIntro
from Deck import Deck
from ErgoCanvas import ErgoCanvas
from Proof import Proof
from ForceBrute import ForceBrute
from DPLL import DPLL
from OrdiRandom import OrdiRandom


class Main(tk.Tk):
    """Interface graphique."""
    def __init__(self):
        """Constructeur de la classe

        :return: Objet ErgoGui
        :rtype: ErgoGui
        """
        tk.Tk.__init__(self)
        ErgoIntro()
        self.title("Ergo")
#        self.geometry("1500x500")  # dimension fenetre jeu
        self.resizable(width=False, height=False)
        # initialisation du menu et canvas
        self.nb_player = 1
        self.__init_menu__()
        self.scores = [0]*4
        self.player_names = ["Joueur "+chr(ord('A')+i) for i in range(4)]
        self.can = ErgoCanvas(self)
        self.can.grid(row=0, column=1, rowspan=7)
        for i in range(4):
            tk.Label(text="Prémisse "+str(i+1)).grid(row=i, column=2)
        tk.Label(text="Ergo le jeu", font="Arial 16 italic").grid(row=0,
                                                                  column=0)
        tk.Label(text="Prouve que tu existes ...",
                 font="Arial 28 italic").grid(row=7, column=1)
        tk.Button(text="jouer", command=self.play).grid(row=5, column=0)

    def init_round(self):
        """Inialise un début de tour."""
        self.deck = Deck()
        self.can.reset()
        self.proof = Proof()
        self.demoDPLL = DPLL(self.proof)
        self.demoFB = ForceBrute(self.proof)
        self.num_player = 0
        self.can.display_current_player(self.num_player)
        self.ordi_player = [False]*self.nb_player + [True]*(4-self.nb_player)
        self.hands = [self.deck.draw(5) for _ in range(4)]
        self.hands[self.num_player].extend(self.deck.draw(2))
        self.cards_played = 0
        self.can.affiche_cards("hand", self.hands[self.num_player])

    def __init_menu__(self):
        """creation de la barre de menu qui permet d'afficher l'aide,
        les règles, la version et de pouvoir quitter le jeu."""
        self.barre_menu = tk.Menu(self)
        # creation du menu "Aide"
        self.aide = tk.Menu(self.barre_menu, tearoff=0)
        self.barre_menu.add_cascade(label="Aide", underline=0, menu=self.aide)
        self.aide.add_command(label="Règles", underline=0, command=self.rules)
        self.aide.add_command(label="A propos", underline=0,
                              command=self.version)
        self.aide.add_command(label="Quitter", underline=0,
                              command=self.quitter)
        # afficher le menu
        self.config(menu=self.barre_menu)

    def play(self):
        """Valide un coup si possible, et passe au joueur suivant."""
        if len(self.hands[self.num_player]) != 5:
            messagebox.showwarning("Ergo",
                                   "Il faut garder 5 cartes pour valider.")
            return
        if not self.proof.is_all_correct():
            messagebox.showwarning("Ergo", "Jeu invalide")
            return
        # passe au joueur suivant.
        if self.deck.is_finished():
            self.fin_manche()
        self.proof.reset_added()
        self.cards_played = 0
        self.can.delete("pile")
        self.num_player = (self.num_player + 1) % 4
        self.hands[self.num_player].extend(self.deck.draw(2))
        self.can.affiche_cards("hand", self.hands[self.num_player])
        self.can.display_current_player(self.num_player)
        if self.ordi_player[self.num_player]:
            self.ordi_plays()

    def ordi_plays(self):
        """Fait jouer l'ordinateur."""
        hand = self.hands[self.num_player]
        name = "Joueur " + chr(ord('A') + self.num_player)
        play = "Joue {} sur la ligne {} en position {}"
        drop = "Jette le {}"
        ordi = OrdiRandom(self.proof, hand)
        coup = ordi.joue()
        for (i_hand, num_premise, index_premise) in coup:
            card = hand.pop(i_hand)
            if index_premise == -1:
                messagebox.showinfo(name, drop.format(card))
            else:
                self.proof.insert(num_premise, index_premise, card)
                self.can.affiche_cards("premise",
                                       self.proof.premises[num_premise],
                                       num_premise)
                messagebox.showinfo(name,
                                    play.format(card,
                                                num_premise,
                                                index_premise))
        self.can.affiche_cards("hand", self.hands[self.num_player])
        self.play()

    def fin_manche(self):
        """Fin de la manche, affichage des gagnants et du score."""
        # TODO faire plus propre
        prouve = self.demoFB.conclusion()
        if prouve is None:
            msg = "La preuve contient une contradiction,\
                    personne ne marque de point"
        else:
            score = self.proof.score()
            msg = "Le(s) gagnant(s) est(sont) : "
            for index, val in enumerate(prouve):
                if val:
                    msg += chr(ord('A')+index) + " "
                    self.scores[index] += score
                msg += "\n"
            msg += "\nChacun marque {} points".format(score)
        messagebox.showinfo("Fin de la manche", msg)
        self.init_round()

    def version(self):
        """Affiche la version du jeu"""
        messagebox.showinfo("Ergo", "Version Beta 17/03/19")

    def rules(self):
        """Affiche les règles du jeu à partir du fichier regles_ergo.txt"""
        texte = ""
        with open("regles_ergo.txt", encoding="utf-8") as fic:
            for ligne in fic:
                texte += ligne
        messagebox.showinfo("Ergo", texte)

    def quitter(self):
        """Quitte"""
        self.quit()
        self.destroy()


if __name__ == '__main__':
    Main().mainloop()
