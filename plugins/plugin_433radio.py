# -*- coding: utf-8 -*-

import bitarray
import serial
import math
import time 
import threading

PLUGIN_TYPE = 'modem'
""" Module variable allowing the Kernel to determine the type
of the plugin and to instantiate it accordingly. 

"""

# Plugin importable permettant à la centrale de communiquer en radio
class Modem():
	""" Class implementing the interface between the computer
	running the domotic box and the Arduino, which is used as 
	a 433MHz radio modem. 
	
	"""
	
	def __init__(self):
		""" Method called at the instantiation of the class. 
		The initialization of variables is made later through
		the "set" function.
		 
		"""
		
		self.COM_port = None
		self.serial = None
		self.observers = []
		# TODO: spécifier comment on dialogue avec 
		# la partie hardware
		self.settings = {'COM_port' : ('integer', None)}
		self.modem_type = 'radio_433' 
		# Nécessaire pour l'interface
		self.name = "Radio 433MHz"

	def get_set_arguments(self):
		""" Returns the dictionary of arguments that
		have to be used in order to set this module.
		 
		"""
		
		return self.settings
	
	def get_modem_type(self):
		""" Returns the  
		"""
		return self.modem_type
			
	def set(self, args):
		""" Sets the serial communication used by the domotic 
		box to communicate with the Arduino. If the given COM
		port number is not valid (i.e. it raises a SerialException
		when we try to open the connection, the method returns
		False. If everything went smoothly, it returns True.
		 
		"""
		
		methodResult = True
		new_serial = serial.Serial()
		new_serial.port = args['COM_port']
		new_serial.baudrate = 9600
		new_serial.timeout = 1
		new_serial.setDTR(False)
		try:
			new_serial.open()
		except serial.SerialException:
			print "Le port COM spécifié est déjà utilisé !"
			methodResult = False
		else:
			self.COM_port = args['COM_port']
			self.serial = new_serial
			print "Port " + self.serial.name + " ouvert et fonctionnel !"
		
		class radioSequenceReception(threading.Thread):
			def __init__(self, processing_method, serial):
				threading.Thread.__init__(self)
				self.processing_method = processing_method
				self.serial = serial
			def run(self):
				while True:
					sequence = []
					if self.serial.inWaiting() > 0:
						byte = self.serial.read()
						if len(byte) > 0:
							while ord(byte) != 255:
								byte = self.serial.read()
								sequence.append(ord(byte))
							self.processing_method(sequence)
							
		radio_sequence_reception = radioSequenceReception(self.identify_sequence, self.serial)
		radio_sequence_reception.start()
				
		return methodResult
	
	def format_arg(self, binary):
		""" Formats a binary sequence so that it fits the format 
		of the parameters of a command sent to the Arduino. This
		method is called by the send_sequence method.

		"""
		
		formatedArg = (7-len(binary)%7)*'0' + binary
		loop_range = reversed(range(len(formatedArg)/7-1))
		for i in loop_range:
			formatedArg = formatedArg[0:7*(i+1)] + '0' + formatedArg[7*(i+1):]
		formatedArg = '11111' + (3-len(bin((7-len(binary)%7))[2:]))*'0' + bin((7-len(binary)%7))[2:] + '0' + formatedArg
		return formatedArg

	
	def send_sequence(self, sequence):
		""" Sends the radio sequence given as an argument.
		The sequence must be the following format :
		sequence = [(int) number_of_repetitions,
					(int) base_radio_pulse_length_in_microseconds,
            		(binary_string) symbol_1,
            		(binary_string) symbol_2,
            		...
            		(binary_string) symbol_n,
            		(symbols_list) symbol_coded_message]
		
		"""
	
		args = [bin(sequence[0])[2:], bin(sequence[1])[2:]]
		args += sequence[2:len(sequence)-1]
		
		bin_coded_message = ''
		for sym in sequence[len(sequence)-1]:
			bin_coded_message += (int(math.ceil(math.log((len(sequence)-3),2))) - len(bin(sym)[2:]))*'0' + bin(sym)[2:]
		
		args += [bin_coded_message]
		
		serial_message = '10000010'
		for arg in args:
			serial_message += self.format_arg(arg)
		serial_message += '11111111'
		byte_sequence = bitarray.bitarray(serial_message).tobytes()
		
		for i in range(5):
			for byte in byte_sequence:
				self.serial.write(byte)
			time.sleep(0.1)
				#print bin(ord(byte))

	def identify_sequence(self, sequence):
		start_position = 0
		for i, duration in enumerate(sequence):
			for obs in self.observers:
				bitOkay = False
				for pos in obs['structure'][obs['i']]:
					if pos[0] < duration*32 < pos[1]:
						bitOkay = True
				#print bitOkay
				if bitOkay:
					obs['i'] += 1
				else:
					obs['i'] = 0
					start_position = i
				if obs['i'] == obs['length']:
					obs['method'](sequence[start_position+1:start_position+1+obs['length']])
					obs['i'] = 0

	def attach(self, observer_dictionary):
		if not observer_dictionary in self.observers:
			self.observers.append(observer_dictionary)
		#self.register_new_message_structure(message_structure)
			
	def register_new_message_structure(self, message_structure):
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