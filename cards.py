#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Différentes classes et algo."""

import constantes as cst


class Card(object):
    "Les cartes du jeu."
    def __init__(self, valeur):
        """Créé une carte de la valeur donnée"""
        self.image = cst.IMAGE[valeur]
        self.valeur = valeur

    def priority(self):
        """Renvoie le niveau de priorité de la carte.
        Si la carte n'a pas de niveau de priorité, renvoie une exception."""
        try:
            return cst.PRIORITY[self.valeur]
        except KeyError:
            raise Exception("Card '{}' as no priority".format(self.valeur))

    def is_letter(self):
        """"Indique si la carte est une lettre ou non."""
        return self.valeur in ["A", "B", "C", "D"]

    def is_operator(self):
        """Indique si la carte est un opérateur."""
        return self.valeur in ["AND", "OR", "THEN"]

    def is_open(self):
        """Indique si la carte est une parenthèse ouvrante."""
        return self.valeur == "("

    def is_close(self):
        """Indique si la carte est une parenthèse fermante."""
        return self.valeur == ")"

    def is_not(self):
        """Indique si la carte est un "NOT"."""
        return self.valeur == "NOT"

    def __repr__(self):
        return self.valeur


class CardList(list):
    """Liste de cartes."""
    def __init__(self, *args):
        """Initialisation de la liste."""
        super().__init__(*args)
        self.test_correction()

    def append(self, card):
        super().append(card)
        self.test_correction()

    def insert(self, index, card):
        super().insert(index, card)
        self.test_correction()

    def pop(self, index=-1):
        card = super().pop(index)
        self.test_correction()
        return card

    def is_syntactically_correct(self):
        """Indique si la liste de cartes est syntaxiquement correcte,
        sans s'occuper de la correspondance des parenthèses."""
        if self == []:
            return True
        if len(self) == 1:
            return self[0].is_letter()
        for i_card in range(len(self)-1):
            card1, card2 = self[i_card], self[i_card+1]
            if card1.is_letter() or card1.is_close():
                if card2.is_letter() or card2.is_not():
                    return False
            if card1.is_operator():
                if card2.is_operator() or card2.is_close():
                    return False
            if card1.is_not():
                if card2.is_operator() or card2.is_close() or card2.is_not():
                    return False
            if card1.is_open():
                if card2.is_operator():
                    return False
        return not card2.is_operator()

    def to_npi(self):
        """Prend en paramètre une liste de carte en notation d'infixe, et renvoie

         * None si le parenthésage de la liste n'est pas correct

         * une liste de carte correspondant à la notation polonaise inversée de
           la liste de départ sinon."""
        npi_card_lst = []
        stack = []
        for card in self:
            if card.is_letter():
                npi_card_lst.append(card)
            elif card.is_open():
                stack.append(card)
            elif card.is_close():
                while stack != [] and not stack[-1].is_open():
                    npi_card_lst.append(stack.pop())
                if stack == []:  # PARENTHESE
                    return None
                else:
                    stack.pop()
            else:
                while stack != [] and stack[-1].priority() >= card.priority():
                    npi_card_lst.append(stack.pop())
                stack.append(card)
        while stack != []:
            card = stack.pop()
            if card.is_open():
                return None
            npi_card_lst.append(card)
        return npi_card_lst

    def test_correction(self):
        """teste la correction de la liste, et met à jour les attributs npi
        et correct."""
        if self.is_syntactically_correct():
            self.npi = self.to_npi()
        else:
            self.npi = None
        self.correct = self.npi is not None


def tests():
    """Des tests..."""
    card_list = CardList([Card("NOT"), Card("NOT"), Card("("), Card("A"),
                          Card("AND"), Card("NOT"), Card("B"), Card(")"), Card("AND"),
                          Card("D")])
    print(card_list)
    print(card_list.correct)
    card_list.pop(0)
    print(card_list)
    print(card_list.correct)
    print(card_list.npi)
    card_list.append(Card("OR"))
    card_list.append(Card("A"))
    print(card_list)
    print(card_list.correct)
    print(card_list.npi)


if __name__ == '__main__':
    print("Bienvenue dans Ergo, le jeu où vous prouvez votre existence.")
    tests()
