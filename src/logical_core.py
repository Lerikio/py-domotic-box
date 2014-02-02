# -*- coding: utf-8 -*-

class LogicalBloc(object):
	# Bloc de base du noyau logiciel.
	# Défini par les informations reçues en entrées et le code qu'il execute lorsque ces informations sont modifiées.

	def __init__(self, name, description):
		self.name = name
		self.description = description
		self.code = None
		self.informations_observed = []

	def add_information(self, information):
		if information not in self.informations_observed:
			self.informations_observed.append(information)
			information.attach(self)

	def remove_information(self, information):
		if information in self.informations_observed:
			information.detach(self)
			self.informations_observed.remove(information)

	def trigger(self): 
		# Activé par la modification des informations observées.
		# 'code' est soit une string, soit un code object, définissant le bloc logique.
		# Il peut modifier des informations et/ou effectuer des actions.
		exec self.code


#---------------------------------------------------------------


		