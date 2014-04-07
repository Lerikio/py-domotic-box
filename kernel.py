# -*- coding: utf-8 -*-

import os
import importlib
import time
import types

class AttributeNotSet(Exception):
	""" Raised when an object tries to use an object whose
	an attribute essential to its working has not yet been 
	set. E.g. when you try sending a message with a modem
	whose COM port has not been set.
	
	
	"""
	pass

class Kernel:
	""" Gathers every plugin installed. 
	It centralizes every driver, modem, automation and device 
	instantiated in the box to allow each other to communicate.
	A plugin is instantiated once when it is loaded, the Kernel 
	keeps a reference to it to avoid to load it again.
	Drivers, modems and interfaces are also instantiated 
	only once when the plugin it comes from is loaded.
	Devices are instantiated by the drivers and added to the
	Kernel's devices list to make them accessible to every 
	other module. 
	
	
	"""

	def __init__(self):
		self.plugins = []
		self.protocols = []	
		self.modems = []
		self.automations = []
		self.interfaces = []
		self.devices = []
			
	def load_plugins(self):
		""" Loads all plugins available in the plugin package/subdirectory. 
		If a plugin has already been loaded, it is ignored.
		
		"""

		for plugin_file in os.listdir('plugins'):
			if plugin_file != '__init__.py' and plugin_file[-3:] == '.py' and plugin_file[0:6] == 'plugin':
				module = importlib.import_module('plugins.' + plugin_file[:-3], package='plugins')
				if module not in self.plugins:
					self.plugins.append(module)
					if module.PLUGIN_TYPE == 'protocol':
						self.drivers.append(module.Protocol(self))
					elif module.PLUGIN_TYPE == 'modem':
						self.modems.append(module.Modem())
					elif module.PLUGIN_TYPE == 'automaton':
						self.automatons.append(module.Automation())
					elif module.PLUGIN_TYPE == 'interface':
						self.interfaces.append(module.Interface(self))


class Settable:
	
	properties_format = {
						'name': (True, types.StringType, None),
						'id': (False, types.IntType, None),
						'description': (True, types.StringType, None),
						'location': (True, types.StringType, None),
						'protocol': (False, types.StringType, None), 
						}
	
	@classmethod
	def get_properties_format(cls):
		return cls.properties_format
	
	def set_properties(self, properties):
		# On parcourt l'ensemble du dictionnaire fourni
		for key in properties.iter:
			# On vérifie pour chaque clé qu'elle correspond à une propriété existante
			if key in self.__class__.properties_format.iter:
				# On vérifie que cette propriété est effectivement modifiable et que la nouvelle valeur est valide
				if self.check(properties[key], self.__class__.properties_format[key]): 
					# Si c'est le cas, on assigne la nouvelle valeur
					self.properties[key] = properties[key]
	
	def check_format(self, arg, arg_format):
		check = True
		(allow_user, arg_type, arg_range) = arg_format
		if allow_user:
			if type(arg) == arg_type:
				if arg_type == types.StringType:
					pass
				elif arg_type == types.IntType or arg_type == types.FloatType:
					if arg_range[0] <= arg <= arg_range[1]:
						pass
					else: # L'argument n'est pas dans les limites données
						check = False
			else: # Le type de donnée proposé n'est pas bon
				check = False
		else: # Cette propriété n'est pas modifiable par l'utilisateur
			check = False
		return check

class Protocol(Settable):
	pass

class Modem:
	pass

class Automation:
	pass

class Interface:
	pass



#---------------------------------------------------------------
# Classes de base liées aux périphériques
# Device, Action, Information
#---------------------------------------------------------------

# Classe générique à un périphérique (device)
# Elle offre une interface suffisante pour utiliser le périphérique
class Device(Settable):
	
	#---------------------------------------------------------------
	# Attributs et méthodes de classe
	# Elles permettent d'avoir des informations sur le périphérique 
	# avant toute instantiation
	#---------------------------------------------------------------
	
	device_properties = {
						'name': "",
						'description' : "",
						'brand': ""
						}
	
	@classmethod
	def get_device_properties(cls):
		return cls.device_properties
	
	properties_format = {
						'name': (True, types.StringType, None),
						'id': (False, types.IntType, None),
						'description': (True, types.StringType, None),
						'location': (True, types.StringType, None),
						'protocol': (False, types.StringType, None), 
						}
		
	#---------------------------------------------------------------
	
	def __init__(self, protocol):
		self.protocol = protocol
		self.properties = {}
		self.properties['protocol'] = protocol.properties['id']
		self.actions = []
		self.data = []

	def add_action(self, new_action):
		return self.actions
		
	def add_data(self, new_info):
		return self.infos
	
	def get_actions(self):
		return self.actions
	
	def get_infos(self):
		return self.infos

	def is_a_sensor(self):
		return not not self.informations

	def is_an_actuator(self):
		return not not self.actions



class Action(object):
	""" Class used to wrap an action made available by a device.
	
	"""

	# On fournit la liste des arguments comme une liste de couples (type, range) :
	# [(integer, (0,100)), (real, (35.5,48.3)), (state, (sitting, standing, lying))]
	# De cette manière, on peut savoir que demander à l'utilisateur
	def __init__(self, name, description, method, arguments_structure):
		self.name = name
		self.description = description
		self.method = method
		self.arguments_structure = arguments_structure

	def execute(self, arguments):
		#print "execute"
		# TODO vérifier que la structure des arguments est respectée 
		self.method(arguments)

class Information(object):
	# Utilisées comme entrées des blocs logiques, les informations sont des "Observables".
	# Lorsqu'une information est modifiée, elle "notifie" tous ses "Observers" pour qu'ils effectuent certaines actions.

	def __init__(self, name, description, info_range):
		self.name = name
		self.description = description
		#self.type = info_type
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