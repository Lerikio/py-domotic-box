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
		# TODO: supprimer les blocks, ils n'ont rien à faire là ils appartiendront à un scénario en particulier
		self.plugins = []
		self.protocols = []	
		self.modems = []
		self.interfaces = []
		self.devices = []
		self.actions = []
		self.infos = []
		#self.blocks = []
		self.block_models = []
		self.scenarios = []
		
		self.next_id = 0
			
	def load_plugins(self):
		""" Loads all plugins available in the plugin package/subdirectory. 
		If a plugin has already been loaded, it is ignored.
		
		"""

		for plugin_file in os.listdir('plugins'):
			if plugin_file != '__init__.py' and plugin_file[-3:] == '.py' and plugin_file[0:6] == 'plugin':
				plugin = importlib.import_module('plugins.' + plugin_file[:-3], package='plugins')
				if plugin not in self.plugins:
					print plugin.name
					self.plugins.append(plugin)
					if plugin.plugin_type == 'protocol':
						self.add_to_kernel(plugin.protocol_class(self))
					elif plugin.plugin_type == 'modem':
						self.add_to_kernel(plugin.modem_class())
					elif plugin.plugin_type == 'interface':
						self.add_to_kernel(plugin.interface_class(self))
						
# 		for plugin_file in os.listdir('plugins'):
# 			if plugin_file != '__init__.py' and plugin_file[-3:] == '.py' and plugin_file[0:6] == 'plugin':
# 				module = importlib.import_module('plugins.' + plugin_file[:-3], package='plugins')
# 				if module not in self.plugins:
# 					self.plugins.append(module)
# 					if module.PLUGIN_TYPE == 'protocol':
# 						self.drivers.append(module.Protocol(self))
# 					elif module.PLUGIN_TYPE == 'modem':
# 						self.modems.append(module.Modem())
# 					elif module.PLUGIN_TYPE == 'interface':
# 						self.interfaces.append(module.Interface(self))

	def get_new_id(self):
		""" Returns a unique identifier of type int which can later be used
		to reference an object. It is particularly useful when it comes
		to user interfaces.
		"""
		# TODO: à protéger par un sémaphore
		new_id = self.next_id
		self.next_id += 1
		return new_id

	def add_to_kernel(self, element):
		""" Adds the element given as argument to the corresponding objects
		list of the kernel. It accepts objects whose type is any of the 
		followings:
		* a python module
		* Modem
		* Interface
		* Device
		* Action
		* Info
		* BlockModel
		* Scenario
		It auto-detects the type of the argument given and automatically 
		appends it to the relevant list.	
		 
		"""
		
		element_parents = element.__class__.__mro__
		try:
			if IDableObject not in element.__class__.__mro__:
				print element
				raise TypeError("Error while adding the element '" + element + "' to the kernel. It is not an IDableObject.")
		except Exception, e:
			raise e
		else:
			try:
				if element is types.ModuleType: target_list = self.plugins
				elif Protocol in element_parents: target_list = self.protocols
				elif Modem in element_parents: target_list = self.modems
				elif Interface in element_parents: target_list = self.interfaces
				elif Device in element_parents: target_list = self.devices
				elif Action in element_parents: target_list = self.actions
				elif Information in element_parents: target_list = self.infos
				#elif Block in element_parents: target_list = self.blocks
				elif BlockModel in element_parents: target_list = self.block_models
				elif Scenario in element_parents: target_list = self.scenarios
				else:
					raise TypeError("The element you are trying to add to the kernel is not one of the possible types.")
			except Exception, e:
				raise e
			else:
				if element not in target_list:
					element.id = self.get_new_id()
					target_list.append(element)
		
		return element.id
	
	def get_by_id(self, searched_id):
		""" If the element whose ID has been given is in one of the
		object lists of the kernel, it returns it. If this ID is not 
		found, it returns False.

		"""
		
		# self.plugins, 
		lists = (self.protocols, self.modems, self.interfaces, self.devices, self.actions, self.infos, self.block_models, self.scenarios)
		methodReturn = False
		for li in lists:
			for el in li:
				if el.id == searched_id:
					methodReturn = el
		return methodReturn
	
	def remove_by_id(self, searched_id):
		""" If the element whose ID has been given is in one of the
		object lists of the kernel, it removes it from it and 
		returns the removed element. If this ID is not found, 
		it returns False.

		"""
		
		lists = (self.plugins, self.protocols, self.modems, self.interfaces, self.devices, self.actions, self.infos, self.blocks, self.block_models, self.scenarios)
		methodReturn = False
		for li in lists:
			for el in li:
				if el.id == searched_id:
					methodReturn = el
					li.remove(el)
					
		return methodReturn
	

class IDableObject(object):
	""" Class of an object which is accessible through 
	a unique ID. The ID is obtained when the object is
	added to the kernel through the add_to_kernel method.
	
	"""
	
	def __init__(self):
		self.id = None
		
	def get_id(self):
		return self.id

class Protocol(IDableObject):
	""" Base class for any Protocol.
	
	"""
	
	pass

class Modem(IDableObject):
	""" Base class for any Modem.
	
	"""
	
	pass

class Interface(IDableObject):
	""" Base class for any Interface.
	
	"""
	
	pass

class BlockModel(IDableObject):
	""" Base class for any BlockModel.
	
	"""
	
	pass

class Scenario(IDableObject):
	""" Base class for any Scenario.
	A scenario has a list of blocks and a list of links. 
	Blocks and links each have an ID which is unique (a block and
	a link can't either have the same ID) within a scenario and
	makes easier the reference to them. This ID is gotten from
	the get_new_id method when the object is added to the 
	Scenario. 
	
	"""
	
	def __init(self):
		self.blocks
		self.links
	
	def get_new_id(self):
		""" Returns an unique identifier in order to reference
		blocks and links within a scenario.
		
		"""
		
		pass

	def add_block(self, new_block):
		""" Adds the block given as argument to the scenario 
		and returns its ID within the scenario.
		
		"""
		pass
	
	def remove_block(self, block_id):
		""" Removes the block whose ID has been specified from
		the list of blocks of this Scenario and returns the Block.
		If the ID is not found, the method returns False.
		
		"""
		pass
	
	def add_link(self, src_block_id, src_port_id, dst_block_id, dst_port_id):
		""" Adds a link from the source port of the source block 
		to the destination port of the destination block given 
		as arguments.
		The blocks and ports are referenced by their respective IDs. 
		Returns the id of the new link.
		
		"""		
		pass

	def remove_link(self, link_id):
		""" Removes the link whose ID has been specified from
		the list of links of this Scenario and returns the Link.
		If the ID is not found, the method returns False.
		
		"""
		pass
	
	def activate(self):
		""" Activates this scenario, i.e. the links between ports
		of blocks become active: they are translated into 
		observer-observed relationships.
		
		"""
		pass
	
	def deactivate(self):
		""" Deactivates this scenario, i. e. resets all the 
		observer-observed relationships previously set.
		
		"""
		pass
		
# Classe générique à un périphérique (device)
# Elle offre une interface suffisante pour utiliser le périphérique
class Device(IDableObject):
	""" Base class for any Device.
	
	"""
	
	
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
		self.informations = []

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

class Action(IDableObject):
	""" Class used to wrap an action made available by a device.
	
	"""

	# On fournit la liste des arguments comme une liste de couples (type, range) :
	# [(integer, (0,100)), (real, (35.5,48.3)), (state, (sitting, standing, lying))]
	# De cette manière, on peut savoir que demander à l'utilisateur
	def __init__(self, name, description, method, arguments_format):
		
		self.properties = {
						'name': name,
						'description': description,
						'execute': '0'
						}
		
		self.properties_format = [
								{ 'type': 'title',
								'title': 'Action' },
								{ 'type': 'string',
								'title': 'Name',
								'desc': 'Name of the action',
								'key': 'name' },
								{ 'type': 'description',
								'title': 'Description',
								'desc': 'Description of the action',
								'key': 'description' }
								]
		
		self.properties_format += arguments_format
		
		self.properties_format += [{ 'type': 'execute',
								'title': 'Execute',
								'desc': 'Click to trigger the action',
								'key': 'execute' }]
		
		self.method = method

	def get_properties_format(self):
		properties_format = list(self.properties_format)
		for p in properties_format:
			if p['type'] != 'title':
				p['section'] = str(self.id)
		return properties_format
	
	def set(self, args):
		""" Method enabling the user to change the name, the description and
		the location of the device. The args must follow the format given in
		device_infos['arguments'].
		
		"""
		
		print "set"
		python_type = {
					'string': types.StringType,
					'bool': types.BooleanType,
					'numeric': types.FloatType,
					'options': types.StringType,
					'description': types.StringType
					}
		
		try:
			for k, v in args.iteritems():
				if self.properties.has_key(k):
					value_type = [f['type'] for f in self.properties_format if f.has_key('key') and f['key'] == k][0]
					self.properties[k] = python_type[value_type](v)
			print "fin set"
		except Exception, e:
			raise e

	def execute(self, arguments):
		#print "execute"
		# TODO vérifier que la structure des arguments est respectée 
		self.method(arguments)

class Information(IDableObject):
	""" Class used to wrap an information made available by a device.
	
	"""
	
	# Utilisées comme entrées des blocs logiques, les informations sont des "Observables".
	# Lorsqu'une information est modifiée, elle "notifie" tous ses "Observers" pour qu'ils effectuent certaines actions.

	def __init__(self, name, description, info_range):
		
				
		self.properties = {
						'name': name,
						'description': description,
						'value': 0
						}
		
		self.properties_format = [
								{ 'type': 'title',
								'title': 'Information' },
								{ 'type': 'string',
								'title': 'Name',
								'desc': 'Name of the information',
								'key': 'name' },
								{ 'type': 'description',
								'title': 'Description',
								'desc': 'Description of the information',
								'key': 'description' },
								{ 'type': 'bool',
								'title': 'Value',
								'desc': 'Value of the information',
								'key': 'value',
								'disabled': True }
								]
		
		#self.type = info_type
		self.range = info_range
		self.values = []
		self._observers = []
	
	def get_properties_format(self):
		properties_format = list(self.properties_format)
		for p in properties_format:
			if p['type'] != 'title':
				p['section'] = str(self.id)
		return properties_format
	
	def set(self, args):
		""" Method enabling the user to change the name, the description and
		the location of the device. The args must follow the format given in
		device_infos['arguments'].
		
		"""
		
		print "set"
		python_type = {
					'string': types.StringType,
					'bool': types.BooleanType,
					'numeric': types.FloatType,
					'options': types.StringType,
					'description': types.StringType
					}
		
		try:
			for k, v in args.iteritems():
				if self.properties.has_key(k):
					value_type = [f['type'] for f in self.properties_format if f.has_key('key') and f['key'] == k][0]
					self.properties[k] = python_type[value_type](v)
			print "fin set"
		except Exception, e:
			raise e
	
	def update(self, new_value):
		retour = True
		if self.check_range(new_value):
			self.values.append((new_value, time.time()))
			print new_value
			self.set_value(new_value)
			self.notify()
		else:
			retour = "erreur de range"
		return retour
	
	def set_value(self, value):
		if value == 'on':
			self.properties['value'] = '1'
		else:
			self.properties['value'] = '0'
	
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

#---------------------------------------------------------------------
#
#	Plein de classes qui seront utiles pour la construction de 
#	scénarios. Pour l'instant on les laisse de côté.
#
#
#---------------------------------------------------------------------

class Observer(object):
	
	def notify(self, observable):
		# the content of the method is very specific 
		# to a given Observer
		pass
	
class Observable(object):

	def attach(self, observer):
		if not observer in self._observers:
			self._observers.append(observer)

	def detach(self, observer):
		try:
			self._observers.remove(observer)
		except ValueError:
			pass

	def notify_observers(self, modifier=None):
		for observer in self._observers:
			if modifier != observer:
				observer.notify(self)

class Node(object):
	
	def __init__(self, name, value_type):
		self.name = name
		self.type = value_type

class SimpleNode(Node, Observer, Observable):
	
	def __init__(self, name, value_type):
		super(SimpleNode, self).__init__(name, value_type)
		self.value = None
		
	def notify(self, observable):
		self.value = observable.value

class CompositeNode(Node):

	def __init__(self, name, value_type):
		super(CompositeNode, self).__init__(name, value_type)
		self.nodes = []
	
	def add_node(self):
		new_node = SimpleNode(self.name, self.value_type)
		self.nodes.append(new_node)
		return new_node

class Block(IDableObject):
	
	def __init__(self):
		self.inputs = {}
		self.outputs = {}

class SimpleBlock(Block, Observer):
	pass

class CompositeBlock(Block):
	
	def __init__(self):
		self.blocks = {}
		self.links = []

class Multiply(SimpleBlock):
	
	def __init__(self):
		super(Multiply, self).__init__()
		self.inputs['operands'] = CompositeNode("operands", types.FloatType)
		self.inputs['operands'].attach(self)
		self.outputs['result'] = SimpleNode("result", types.FloatType)
		
	def notify(self, observable):
		result = 1
		for op in self.inputs['operands']:
			result = result*op.value
		self.output['result'].value = result
			
			
class Not(SimpleBlock):
	# observer
	# notifier d'observers sans qu'ils se soient inscrits
	
	def __init__(self):
		super(Not, self).__init__()
		
		# Inputs
		self.inputs['in'] = SimpleNode("in", types.BooleanType)
		self.inputs['in'].attach(self)
		
		# Outputs
		self.outputs['out'] = SimpleNode("out", types.BooleanType)
	
	def notify(self, observable):
		self.outputs['out'].value = not self.inputs['in'].value

class Constant(SimpleBlock):
	# observer
	# notifier d'observers sans qu'ils se soient inscrits
	
	def __init__(self, value):
		super(Constant, self).__init__()
		
		self.outputs['out'] = SimpleNode("out", type(value))
		self.outputs['out'].value = value

class Or(Block):
	pass
	
class And(Block):
	pass
	
# class Settable(object):
# 	
# 	properties_format = {
# 						'name': (True, types.StringType, None),
# 						'id': (False, types.IntType, None),
# 						'description': (True, types.StringType, None),
# 						'location': (True, types.StringType, None),
# 						'protocol': (False, types.StringType, None), 
# 						}
# 	
# 	@classmethod
# 	def get_properties_format(cls):
# 		return cls.properties_format
# 	
# 	def set_properties(self, properties):
# 		# On parcourt l'ensemble du dictionnaire fourni
# 		for key in properties.iter:
# 			# On vérifie pour chaque clé qu'elle correspond à une propriété existante
# 			if key in self.__class__.properties_format.iter:
# 				# On vérifie que cette propriété est effectivement modifiable et que la nouvelle valeur est valide
# 				if self.check(properties[key], self.__class__.properties_format[key]): 
# 					# Si c'est le cas, on assigne la nouvelle valeur
# 					self.properties[key] = properties[key]
# 	
# 	def check_format(self, arg, arg_format):
# 		check = True
# 		(allow_user, arg_type, arg_range) = arg_format
# 		if allow_user:
# 			if type(arg) == arg_type:
# 				if arg_type == types.StringType:
# 					pass
# 				elif arg_type == types.IntType or arg_type == types.FloatType:
# 					if arg_range[0] <= arg <= arg_range[1]:
# 						pass
# 					else: # L'argument n'est pas dans les limites données
# 						check = False
# 			else: # Le type de donnée proposé n'est pas bon
# 				check = False
# 		else: # Cette propriété n'est pas modifiable par l'utilisateur
# 			check = False
# 		return check
