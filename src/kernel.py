# -*- coding: utf-8 -*-

class Kernel:
	""" Gathers every plugin installed. 
	It centralizes every driver, modem, automaton and devices 
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
		self.drivers = []
		self.modems = []
		self.automatons = []
		self.interfaces = []
		self.devices = []
		
	def load_plugins(self):
		""" Loads all plugins available in the plugin package/subdirectory. 
		If a plugin has already been loaded, it is ignored.
		
		"""
		available_plugins = __import__('plugins', fromlist=['o'])
		for plugin in available_plugins:
			if plugin not in self.plugins:
				self.plugins.append(plugin)
				if plugin.PLUGIN_TYPE == 'protocol':
					self.drivers.append(plugin.Driver())
				else if plugin.PLUGIN_TYPE == 'modem':
					self.modems.append(plugin.Modem())
				else if plugin.PLUGIN_TYPE == 'automaton':
					self.automatons.append(plugin.Automaton())
				else if plugin.PLUGIN_TYPE == 'interface':
					self.interfaces.append(plugin.Interface())