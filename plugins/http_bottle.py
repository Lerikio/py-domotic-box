from bottle import Bottle, run

class Interface(object):
	""" Allows HTTP communications
	"""

	def __init__(self, kernel, host='localhost', port=8080):
		"""
			When loading this plugin, the kernel must past itself to it, as well as the desired host and port.
		"""

		self.bottle = Bottle()
		self.kernel = kernel
		self.host = host
		self.port = port

	@self.bottle.route('/plugins')
	def index_plugins():
		return self.kernel.plugins

	@self.bottle.route('/drivers')
	def index_drivers():
		return self.kernel.drivers

	@self.bottle.route('/modems')
	def index_modems():
		return self.kernel.modems

	@self.bottle.route('/automatons')
	def index_automatons():
		return self.kernel.automatons

	@self.bottle.route('/interfaces')
	def index_interfaces():
		return self.kernel.interfaces

	@self.bottle.route('/devices')
	def index_devices():
		return self.kernel.devices	

	def run():
		run(self.bottle, host, port)