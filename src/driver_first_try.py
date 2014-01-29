from logical_core import * 

class Driver(object):

	def __init__(self):
		self.name = "Driver"
		self.description = "Premier test de driver."
		self.actuator = Actuator("Test", "Test de test", self)
		self.informations = [Information("temp", "température", 0), Information("temp2", "température 2", 3)]

		self.actuator.new_action("Action cool", "Une action très cool", 1)

		self.actuator.new_action("Action normale", "Une action moins cool", 2)

	def execute(ID):
		if ID == 1:
			print "Une action cool a été lancée !"
		elif ID == 2:
			print "Une action moins cool a été lancée."
		else:
			print "Ceci n'est pas une véritable action."

