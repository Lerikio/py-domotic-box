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
		if information in self.informations_observed
			information.detach(self)
			self.informations_observed.remove(information)

	def trigger(self):
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

class Action(object):


	def __init__(self, name, description):
		self.name = name
		self.description = description
