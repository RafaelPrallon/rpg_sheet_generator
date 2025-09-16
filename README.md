# README

This is a program made in python to generate a RPG character sheet to practice the language

It seeks to be system agnostic and to generate a final file for the generated sheet

To add a RPG system to the program, it's necessary to add it to a systems folder inside this project folder and, for now, need to contain the following:
- a file with the characteristics the caracter may have(strength, dexterity, etc) and the rule to calculate it
  - the possible rules will be:
    - random-number: a random number inside range
    - list of values: it will list valid values and how many times those values may be used
- a folder containing classes(if applicable). inside this folder there will be a file for each class(or equivalent).
- a folder containing races(if applicable). inside this folder there will be a file for each available race.
- a folder containing advantages/feats. inside this folder will also have a file describing how many may be picked
- a folder containing disadvantages or equivalent