#!/usr/bin/python -i
# -*- coding: utf-8 -*-

# tournament_demo.py

# Author: Al Carruth
# Submitted for the Udacity Fullstack Developer Nanodegree
# Project 2: Tournament Results

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

if __name__ == '__main__':
    t1 = Tournament('City Tournament')
    t2 = Tournament('State Tournament')
    t1.simulateTournament(players[0:13])
    #t2.simulateTournament(players[0:10])


