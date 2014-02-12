# -*- coding: utf-8 -*-

from logical_core import * 

class Driver(object):

	def __init__(self):
		self.name = "Driver"
		self.description = "Premier test de driver."
		self.actuator = Actuator("Test", "Test de test", self)
		self.informations = [Information("temp", "température", 0), Information("temp2", "température 2", 3)]

		self.actuator.add_action("Action cool", "Une action très cool", 1)

		self.actuator.add_action("Action normale", "Une action moins cool", 2)

	def execute(self, ID):
		if ID == 1:
			print u"Une action cool a été lancée !"
		elif ID == 2:
			print u"Une action moins cool a été lancée."
		else:
			print u"Ceci n'est pas une véritable action."

