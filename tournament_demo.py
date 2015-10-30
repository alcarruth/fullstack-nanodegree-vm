#!/usr/bin/python -i
# -*- coding: utf-8 -*-

# tournament_demo.py

# Demo program for the P2: Tournament project

from tournament import *

names = [
    "Markov Chaney",
    "Joe Malik",
    "Mao Tsu-hsi",
    "Atlanta Hope",
    "Twilight Sparkle",
    "Fluttershy",
    "Applejack",
    "Pinkie Pie",
    "Bruno Walton",
    "Boots O'Neal",
    "Cathy Burton",
    "Diane Grant",
    "Chandra Nalaar",
    "Melpomene Murray",
    "Randy Schwartz",
    "Udacious Ulysses"
]
    
def run(players):
    tournament.simulateTournament(players)

if __name__ == '__main__':
    run(names)
