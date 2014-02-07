# -*- coding: utf-8 -*-

import time # Pour pouvoir ajouter un timestamp à la réception d'une information 

#---------------------------------------------------------------
# Package core_classes
# Il contient toutes les classes de base de la centrale
# utilisées par le core et les plugins
#---------------------------------------------------------------

#---------------------------------------------------------------
# Classes de base liées aux périphériques
#---------------------------------------------------------------

# Classe générique pour un sensor ou un actuator
# Elle permet d'offrir une interface minimaliste commune à tous les périphériques
class Device(object):
	
	device_name = ""
	device_brand = ""
	
	def __init__(self, name, location, driver):
		self.name = name
		self.location = location
		self.driver = driver

	@classmethod
	def get_device_info(cls):
		return {
			'name' : cls.device_name,
			'brand' : cls.device_brand}

# TODO: les classes Actuator et Sensor n'ont en fait pas de raison
# d'être, à vérifier et les virer

# Un périphérique concret de type actionneur implémente cette classe.
# Les actions sont des attributs de classe, rendant leur accès possible
# indépendamment d'une instanciation du périphérique
# class Actuator(Device):
# 	# CLasse Abstraite : ne devrait jamais être instanciée directement
# 
# 	def __init__(self, name, description, location, driver):
# 		super(Actuator, self).__init__(name, description, location, driver)
# 		self.actions = []
# 
# 	# Permet d'accéder aux actions
# 	# Les actions sont propres à une instanciation du périphérique puisqu'elles
# 	# contiennent un pointeur vers une méthode d'un objet
# 	def get_actions(self):
# 		return actions
# 
# # Classe spécialisant un périphérique en sensor, stockant des informations
# class Sensor(Device):
# 	# CLasse Abstraite : ne devrait jamais être instanciée directement
# 
# 	def __init__(self, name, description, location, driver):
# 		super(Actuator, self).__init__(name, description, location, driver)
# 		self.informations = []

		
			

	# Gère la réception d'une nouvelle information, l'ajoute à la liste des informations disponibles


	# Permet de présenter le type d'informations mises à disposition par le capteur au core
	# def introduce_informations(self):

#---------------------------------------------------------------
# Classes de base liées aux actions et informations
#---------------------------------------------------------------

class Action(object):
	# Action d'un actionneur

	# On fournit la liste des arguments comme une liste de couples (type, range) :
	# [(integer, (0,100)), (real, (35.5,48.3)), (state, (sitting, standing, lying))]
	# De cette manière, on peut savoir que demander à l'utilisateur
	def __init__(self, name, description, method, arguments_structure):
		self.name = name
		self.description = description
		self.method = method
		self.arguments_structure = arguments_structure

	def execute(self, arguments):
		# TODO vérifier que la structure des arguments est respectée 
		self.method(arguments)

class Information(object):
	# Utilisées comme entrées des blocs logiques, les informations sont des "Observables".
	# Lorsqu'une information est modifiée, elle "notifie" tous ses "Observers" pour qu'ils effectuent certaines actions.

	def __init__(self, name, description, info_type, info_range):
		self.name = name
		self.description = description
		self.type = info_type
		self.range = info_range
		self.values = []
		self._observers = []
	
	def update(self, new_value):
		retour = True
		if self.check_range(new_value):
			self.values.append((new_value, time.time()))
			self.notify()
		else:
			retour = "erreur de range"
		return retour
	
	def check_range(self, new_value):
		# TODO: vérifier que la nouvelle valeur donnée est bien dans 
		# le range de cette information donnée par info_range 
		return True

	def attach(self, observer):
		if not observer in self._observers:
			self._observers.append(observer)

	def detach(self, observer):
		try:
			self._observers.remove(observer)
		except ValueError:
			pass

	def notify(self, modifier=None):
		for observer in self._observers:
			if modifier != observer:
				observer.trigger()
