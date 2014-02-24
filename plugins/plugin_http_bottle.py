from bottle import route, run
import jsonpickle

PLUGIN_TYPE = 'interface'
""" Module variable allowing the Kernel to determine the type
of the plugin and to instantiate it accordingly. 

"""

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

class Interface():
	""" Allows HTTP communications
	"""

	def __init__(self, kernel, host='localhost', port=8080):
		"""
			When loading this plugin, the kernel must past itself to it, as well as the desired host and port.
		"""
		self.kernel = kernel
		self.host = host
		self.port = port

	@methodroute('/plugins')
	def index_plugins(self):
		return self.kernel.plugins

	@methodroute('/drivers')
	def index_drivers(self):
		return jsonpickle.encode(self.kernel.drivers)

	@methodroute('/modems')
	def index_modems(self):
		return self.kernel.modems

	@methodroute('/automatons')
	def index_automatons(self):
		return self.kernel.automatons

	@methodroute('/interfaces')
	def index_interfaces(self):
		return self.kernel.interfaces

	@methodroute('/devices')
	def index_devices(self):
		return self.kernel.devices	

	def run(self):
		routing(self)
		run(host=self.host, port=self.port)