# -*- coding: utf-8 -*-

import time # Pour pouvoir ajouter un timestamp à la réception d'une information 

#---------------------------------------------------------------
# Package core_classes
# Il contient toutes les classes de base de la centrale
# utilisées par le core et les plugins
#---------------------------------------------------------------





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

