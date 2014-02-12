# -*- coding: utf-8 -*-

import os
import importlib

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
	
	def load_imports(self, path):
		files = os.listdir(path)
		print files
		imps = []
	
		for i in range(len(files)):
			name = files[i].split('.')
			if len(name) > 1:
				if name[1] == 'py' and name[0] != '__init__':
					name = name[0]
					imps.append(name)
	
		file = open(path+'__init__.py','w')
	
		toWrite = '__all__ = '+str(imps)
	
		file.write(toWrite)
		file.close()

	def load_plugins(self):
		""" Loads all plugins available in the plugin package/subdirectory. 
		If a plugin has already been loaded, it is ignored.
		
		"""

		available_plugins = []
		for file in os.listdir('plugins'):
			if file == '__init__.py' or file[-3:] != '.py' or file[0:6] != 'plugin':
				continue
			module = importlib.import_module('plugins.'+file[:-3], package='plugins')
			available_plugins += [module]

		for plugin in available_plugins:
			if plugin not in self.plugins:
				self.plugins.append(plugin)
				if plugin.PLUGIN_TYPE == 'protocol':
					self.drivers.append(plugin.Driver())
				elif plugin.PLUGIN_TYPE == 'modem':
					self.modems.append(plugin.Modem())
				elif plugin.PLUGIN_TYPE == 'automaton':
					self.automatons.append(plugin.Automaton())
				elif plugin.PLUGIN_TYPE == 'interface':
					self.interfaces.append(plugin.Interface())