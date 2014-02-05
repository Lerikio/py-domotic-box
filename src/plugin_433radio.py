# -*- coding: utf-8 -*-

PLUGIN_TYPE = 'modem'
""" Module variable allowing the Kernel to determine the type
of the plugin and to instantiate it accordingly. 

"""

# Plugin importable permettant à la centrale de communiquer en radio
class Modem():
	
	def __init__(self):
		
		self.tx_pin = None
		self.rx_pin = None
		self.observers = []
		# TODO: spécifier comment on dialogue avec 
		# la partie hardware
		self.settings = {'hardware_pin' : ('IOPin', None)}
		self.modem_type = 'radio_433' 
	
	def get_set_arguments(self):
		return self.settings
	
	def get_modem_type(self):
		return self.modem_type
	
	def set(self, args):
		retour = True
		# TODO: vérifier la cohérence des arguments
		self.tx_pin = args['tx_pin']
		self.rx_pin = args['rx_pin']
		return retour
	
	def attach(self, observer, message_structure):
		if not observer in self.observers:
			self.observers.append(observer, message_structure)
		self.register_new_message_structure(message_structure)
		
	def register_new_message_structure(self):
		""" Signal to the hardware part that a new set of
		symbols must be recognized and sent to this class.
		
		"""
		# TODO: signaler au module hardware qu'un nouvel
		# ensemble de symboles est à surveiller
		pass
	
	def process_radio_sequence(self):
		""" Once the hardware module has detected a set of 
		known symbols, it is sent to this method. This method 
		aims at identifying if the recognized sequence is 
		actually adressed to one of the handled protocols and  
		if it is the case, to which protocol, by comapring it 
		the message_structure table.
		Once the protocol has been recognized, it calls the
		observer.process_sequence() method.
		
		"""
		# TODO: Ecrire la méthode
		pass