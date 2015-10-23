#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

if __name__ == '__main__':
    resetDB()
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

    initPlayers(names)
    initMatches()

    report(standings())