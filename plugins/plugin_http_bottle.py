# -*- coding: utf-8 -*-

from bottle import route, run
from json import dumps
import kernel

def routing(obj):
	""" Set the routes for the app
	"""
	for kw in dir(obj):
		attr = getattr(obj, kw)
		if hasattr(attr, 'route'):
			route(attr.route)(attr)

def methodroute(route):
	""" Decorator to set route to methods
	"""
	def decorator(f):
		f.route = route
		return f
	return decorator

class HTTPInterface(kernel.Interface):
	""" Allows HTTP communications
	"""

	def __init__(self, kernel, host='localhost', port=8080):
		"""
			When loading this plugin, the kernel must past itself to it, as well as the desired host and port.
		"""
		self.kernel = kernel
		self.host = host
		self.port = port

		# Nécessaire pour l'interface
		self.name = "Module HTTP"

	# Indexes
	@methodroute('/plugins')
	def index_plugins(self):
		message = []
		for plugin in self.kernel.plugins:
			message.append(plugin.name)
		return dumps(message)

	@methodroute('/drivers')
	def index_drivers(self):
		message = []
		for driver in self.kernel.drivers:
			message.append(driver.name)
		return dumps(message)

	@methodroute('/modems')
	def index_modems(self):
		message = []
		for modem in self.kernel.modems:
			message.append(modem.name)
		return dumps(message)

	@methodroute('/automatons')
	def index_automatons(self):
		message = []
		for automatons in self.kernel.automatons:
			message.append(automatons.name)
		return dumps(message)

	@methodroute('/interfaces')
	def index_interfaces(self):
		message = []
		for interface in self.kernel.interfaces:
			message.append(interface.name)
		return dumps(message)

	@methodroute('/devices')
	def index_devices(self):
		message = []
		for device in self.kernel.devices:
			message.append(device.name)
		return dumps(message)

	# Shows
	
	def run(self):
		routing(self)
		run(host=self.host, port=self.port)
		
""" Set of attributes which describe the plugin, in order 
to add it to the kernel and then be able to describe it
to the user.  

"""
plugin_type = "interface"
name = "HTTP Interface"
description = "An interface plugin which enables the use of the HTTP protocol to communicate with the box."
plugin_id = "5"
interface_class = HTTPInterface 