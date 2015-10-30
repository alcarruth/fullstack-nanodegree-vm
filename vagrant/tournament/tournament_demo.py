#!/usr/bin/python -i
# -*- coding: utf-8 -*-

# tournament_demo.py

# Demo program for the P2: Tournament project

from tournament import *

players = [
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

def step(t):
    t.simulateRound()

def show():
    t1.show('standings')
    t2.show('standings')
    t3.show('standings')


if __name__ == '__main__':
    t1 = Tournament('One')
    t2 = Tournament('Two')
    t3 = Tournament('Three')
    for p in players[0:6]:
        t1.registerPlayer(p)
        t2.registerPlayer(p)
        t3.registerPlayer(p)

