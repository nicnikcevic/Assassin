# Assassin Game Manager

## Game Description

A Python CLI to automate the tracking of big games of assaassin. At my highschool it was a big tradition to play "Senior Assassin" during your final semester. This is when everyone in the grade is randomly paired up with another person, and those two people are given targets. The objective of the game is to eliminate your target and avoid being eliminated. Each week new targets are assigned. If by the end of the week you have not eliminted your targets or you have been eliminated, you're team is out. The game continues until one team is left standing.

## Inspiration

Because almost everyone in the senior class participates, students usually need to find one person in a grade below to orchestrate the game. In the past that includes sending out emails every week to every player with updates. Keeping track of who is targeting who, and sending out reminders. It is sometimes hard to find a non-participating student who is willing to spend time doing this. My junior year I was selected for this task and found it annoyingly tedious. So I decided to make this pretty simple CLI to automate some of the annoying stuff for me. 

### Impact

The hope was that by making the administrative role easier, more students would be willing to take it on, and thus the fun tradition could stay alive. I think the tradition is value because it bring the senior class together.

## Design

The implementation is very simple and uses a CLI in order to prompt the game manager about key functions of the game. The program reads in a list of names from a text file and assigns random partners and targets, and it can also save the state of a game to a .json file and reload it which is important because a whole game of assassin takes several weeks. 
