# -*- coding: utf-8 -*-

from core_classes import * 

# Plugin importable permettant à la centrale de communiquer en radio
class Modem():

	# def __init__(self):
		# TODO Initialiser aussi l'interface matérielle, mais ça 
		# dépendra de ce que l'on utilisera. Dans tous les cas, 
		# il faut faire un interrupt sur cette classe pour appeler
		# on_input 

	# Fonction déclenchée lors de la réception d'un message 
	# def on_input(self):
		# TODO En fonction de ce que l'on reçoit, appeler la
		# fonction process_sequence du protocole considéré

	# Méthode appelée par un protocole pour envoyer une 
	# séquence radio
	# def sendSequence(self, sequence):

	# Fonction appelée pour ajouter un protocole en tant 
	# qu'observer de ce modem. 
	def attach(self, observer):
		if not observer in self._observers:
			self._observers.append(observer)

		# TODO aller chercher l'attribut message_structure
		# de l'observer ajouté et l'envoyer au module de 
		# réception radio
