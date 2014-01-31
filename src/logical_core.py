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

class Information(object):
	# Utilisées comme entrées des blocs logiques, les informations sont des "Observables".
	# Lorsqu'une information est modifiée, elle "notifie" tous ses "Observers" pour qu'ils effectuent certaines actions.

	def __init__(self, name, description, value):
		self._observers = []
		self.name = name
		self.description = description
		self.value = value

	def __setattr__(self, name, value):
		# Override de setattr pour que, lorsque la valeur de l'information est changée, elle notifie ses observers.
		object.__setattr__(self, name, value)
		if name == 'value':
			self.notify()

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

#---------------------------------------------------------------

class Actuator(object):
	# CLasse Abstraite : ne devrait jamais être instanciée directement

	# Définition générale d'un actionneur. Permet d'utiliser des actions sur celui-ci, qui sont des méthodes rajoutées par le driver.
	# La liste des actions possibles de l'actionneur est disponible dans son attribut "actions"

	def __init__(self, name, description, driver):
		self.name = name
		self.description = description
		self.driver = driver
		self.actions = []

	def add_action(self, name, description, driver_ID):
		new_action = Action(name, description, self, driver_ID)
		self.actions.append(new_action)

#---------------------------------------------------------------

class Action(object):
	# Action d'un actionneur

	def __init__(self, name, description, actuator, driver_ID):
		self.name = name
		self.description = description
		self.actuator = actuator
		self.driver = self.actuator.driver
		self.ID = driver_ID

	def execute(self):
		self.driver.execute(self.ID)