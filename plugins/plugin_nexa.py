# -*- coding: utf-8 -*-

import kernel, types, time

#---------------------------------------------------------------
# Plugin importable permettant à la centrale de gérer le 
# protocole Nexa. C'est un plugin de type protocol. D'une part, 
# elle comporte le driver et d'autre part les nouveaux 
# périphériques qu'elle apporte.
#---------------------------------------------------------------


PLUGIN_TYPE = 'protocol'
""" Module variable allowing the Kernel to determine the type
of the plugin and to instantiate it accordingly. 

"""

class Protocol():
	""" Main class of a protocol plugin.
	
	"""

	#---------------------------------------------------------------
	# Interface avec le kernel 
	#---------------------------------------------------------------

	def __init__(self):
		# TODO: rajouter le kernel comme argument et la ligne
		# suivante quand le kernel marchera
		# self.kernel = kernel
		
		# Jusqu'à ce qu'on l'ait configuré, le driver n'a pas encore de modem
		self.modem = None

# 		# On définit la structure de messages radio propre au protocole nexa 
# 		self.message_structure = 4*32*[((200,300),(2000,2500))]
# 		
# 		{
# 								'baselength' : 250,
# 								'symbols' : {
# 										'start' : [1,10],
# 										'one' : [1,5,1,1],
# 										'zero' : [1,1,1,5],
# 										'end' : [1,30]
# 										},
# 								'structure' : ['start'] + 32*[('one','zero')] + ['end']
# 								}

		# Liste des périphériques connectés gérés par ce driver
		self.devices = []
		
		# Paramètres à fournir pour configurer le driver
		self.settings = {'modem' : ('Modem', None)}
		
		# Liste des périphériques potentiellement gérables par ce driver
		self.handled_devices = [NexaRemote, NexaDevice]
		
		# Le driver ne propose à l'extérieur d'instantier un périphérique
		# seulement si cela a un sens. Ici, un NexaSwitch ne sera instantié
		# que si on en détecte un, automatiquement.
		self.instantiable_devices = [NexaDevice]

		# Nécessaire pour l'interface
		self.name = "Nexa"
			
	def get_set_arguments(self):
		""" Returns the arguments needed to set the driver.	"""
		return self.settings
	
	def set(self, args):
		""" Sets the driver. It raises a TypeError if the given modem doesn't
		match the awaited modem type.
		
		Keyword arguments:
		settings -- the dictionary of settings used to set the driver. Its 
		format is determined by the function get_set_arguments.
		
		"""
		
		try:
			# On vérifie que les arguments donnés sont valides
			if args['modem'].get_modem_type() == 'radio_433': 
				self.modem = args['modem']
				self.modem.attach(self)
			else:
				# Si ce n'est pas le cas, on lève une TypeError
				raise TypeError("A modem whose type is 'radio_433' is awaited. Received instead a modem whose type is '"+args['modem'].get_modem_type()+"'.");
		except Exception, e:
			raise e
		
# 			{
# 				'structure' : 4*32*[[(150,350),(1000,1500)]],
# 				'i' : 0,
# 				'length' : 4*32,
# 				'method' : self.decode_sequence}

	def get_instantiable_devices(self):
		""" Returns a list of the devices instantiable by the user
		of the driver. 
		The list of user-instantiable devices is included in the 
		list of the driver-handled devices but not necessarily 
		equal.  
		
		"""
		# On ne fournit pas directement la classe pour que le driver reste
		# le seul à pouvoir instancier des périphériques
		return [i.device_infos for i in self.instantiable_devices]

	def add_device(self, device_id, args):
		""" Proxy method used to instantiate a new device. It raises a 
		ValueError if the device_id given is out of range. It may raise 
		a TypeError if the args given to set the new device don't match 
		the settings format.
 		
		"""
		
		try:
			if device_id == 0:
				new_device = NexaDevice()
				# TODO: Vérifier que les bons arguments sont fournis
				# avec une fonction générique (ce problème se pose 
				# souvent dans le programme)
				new_device.set(self, args)
				self.devices.append(new_device)
				# TODO: rajouter cette ligne quand le kernel fonctionnera
				# self.kernel.devices.append(new_device)
			else:
				raise ValueError("The device id given is out of range.")
		except Exception, e:
			raise e
		
	def get_devices(self):
		""" Returns the list of the devices that are currently handled 
		by this protocol. 
		 
		"""
		return self.devices

	#---------------------------------------------------------------
	# Interface avec le modem 
	#---------------------------------------------------------------

	# Reçoit une trame identifiée comme destinée à ce driver et
	# transmise par la couche inférieure. Cela suppose que la couche la
	# plus basse a la capacité d'identifier le protocole du message et
	# s'adresse ainsi directement à la méthode decode_sequence du
	# driver.
	# La méthode doit être spécialisée pour traiter et décoder une trame Nexa
	# Elle sera totalement rédigée quand on saura sous quelle forme le message est obtenu
	def decode_sequence(self, sequence):
		""" Processes a radio sequence received by the radio modem 
		into a message understable by the protocol.
		The implementation of the sequence processing is , for the
		moment, a hard-coded finite-state machine.		
		
		"""
		# TODO: Transformation de ce qui est reçu du modem en message de 32 bits
		# Transformation d'un tableau de bits en entiers
		#print len(sequence)
		#print sequence
		
		state = 'unknown'
		
		def is_start(duration):
			return True if (1800 < duration*32 < 3000) else False
		
		def is_short(duration):
			return True if (0 < duration*32 < 800) else False
		
		def is_long(duration):
			return True if (800 < duration*32 < 2000) else False
		
		def is_end(duration):
			return True if (2000 < duration*32) else False
		
		for i in sequence:
			if state == 'unknown':
				nexa_sequence = []
				if is_short(i):	state = 'start1'
			elif state == 'start1':
				if is_start(i): state = 'start2'
				else: state = 'unknown'				
			elif state == 'start2':
				if is_short(i): state = 'short'
				else: state = 'unknown'	
			elif state == 'short':
				if is_short(i): state = 'zero1'
				elif is_long(i): state = 'one1'
				elif is_end(i): state = 'end'
				else: state = 'unknown'	
			elif state == 'one1':
				if is_short(i): state = 'one2'
				else: state = 'unknown'	
			elif state == 'one2':
				if is_short(i): state = 'one_ok'
				else: state = 'unknown'	
			elif state == 'one_ok':
				nexa_sequence.append(1)
				if is_short(i): state = 'short'
				else: state = 'unknown'	
			elif state == 'zero1':
				if is_short(i): state = 'zero2'
				else: state = 'unknown'	
			elif state == 'zero2':
				if is_long(i): state = 'zero_ok'
				else: state = 'unknown'	
			elif state == 'zero_ok':
				nexa_sequence.append(0)
				if is_short(i): state = 'short'
				else: state = 'unknown'	
			elif state == 'end':
				break
		
		if len(nexa_sequence) == 32: # On s'assure qu'on a une séquence cohérente
			
			# Converts a list of binary values to integer
			def from_bitfield_to_int(bitfield):
				return sum([i*2**(len(bitfield)-1-idi) for idi, i in enumerate(bitfield)])
			
			house_code = from_bitfield_to_int(nexa_sequence[0:26])
			group_code = nexa_sequence[26]
			command = nexa_sequence[27]
			unit_code = from_bitfield_to_int(nexa_sequence[28:32])
			
			device_found = False
			
			for device in self.devices:
				# Si la device est déjà dans la liste ET que ce n'est pas une NexaDevice, c'est que c'est une NexaRemote qu'on connait et on la met à jour
				if device.house_code == house_code and device.unit_code == unit_code and NexaDevice not in device.__class__.__bases__:
					device_found = True
					if command == 1 : device.switch_on()
					else: device.switch_off()
			
			if not device_found:
				new_device = NexaRemote(self, house_code, group_code, unit_code)
				new_device.set({
							'name' : "New Nexa Switch",
							'description' : "A new Nexa Switch has been detected and added to your devices.",
							'location' : "Specify a location."})
				self.devices.append(new_device)
				# TODO: rajouter cette ligne quand le kernel marchera
				# self.kernel.devices.append(new_device)	
				
				print "nouvelle télécommande"
				print house_code
				print group_code
				print unit_code
				print "\n\n"

				
			
			
		
# 		for index in range(len(sequence)):
# 			if is_short(sequence[index]):
# 				sequence[index] = 'short'
# 			else:
# 				sequence[index] = 'long'
# 		#print sequence
# 		
# 		abort = False
# 		temp_list = [0,0,0,0]
# 		nexa_sequence = []
# 		for j in range(len(sequence)/4):
# 			for i in range(4):
# 				temp_list[i] = sequence.pop(0)
# 			
# 			#print temp_list
# 			if temp_list == ['short', 'long', 'short', 'short']:
# 				nexa_sequence += [1]
# 			elif temp_list == ['short', 'short', 'short', 'long']:
# 				nexa_sequence += [0]
# 			else:
# 				abort = True
# 		
# 		if not abort:
			
	#---------------------------------------------------------------
	# Interface avec les devices 
	#---------------------------------------------------------------

	def send_command(self, device, command):
		""" Method called when a device intends to send a message.
		It builds up the Nexa message according to the command 
		to be sent and the identity of the sending device. 
		
		"""
		# error_code = True
		
		symbols = ['1' + 10*'0',
				'10000010',
				'10100000',
				'1' + 40*'0']

		bin_house_code = (26-len(bin(device.house_code)[2:]))*'0' + bin(device.house_code)[2:]
		bin_group_code = bin(device.group_code)[2:]
		bin_command = bin(command)[2:]
		bin_unit_code = (4-len(bin(device.unit_code)[2:]))*'0' + bin(device.unit_code)[2:]
	
		nexa_sequence = bin_house_code + bin_group_code + bin_command + bin_unit_code
		
		coded_sequence = [0]
		for char in nexa_sequence:
			if char == '1':
				coded_sequence += [1]
			else:
				coded_sequence += [2]
		coded_sequence += [3]
		
		call_arg = [16,250] + symbols + [coded_sequence]
		
		try:
			self.modem.send_sequence(call_arg)
		except Exception, e:
			raise e
		
# 		try:
# 			self.modem.send_sequence([16,250].extend(symbols) + coded_sequence)
# 		except:
# 			print "problème dans send_sequence"
# 			error_code = False
			
		# return error_code

#---------------------------------------------------------------

# Interrupteur Nexa classique on/off
class NexaDevice(kernel.Device):
	""" This is the class used to implement any Nexa-controlled device.
	 
	"""

	# Ce sont les attributs qui caractérisent ce type de périphérique
	device_infos = {
				'device_name' : "Nexa Device",
				'device_brand' : "Nexa",
				'device_description' : "Any Nexa-compatible device.",
				'arguments' : {
							'name' : ('string', 50),
							'description' : ('string', 1000),
							'location' : ('string', 100),
							'house_code' : ('integer', (0,67108863)),
							'group_code' : ('integer', (0,1)),
							'unit_code' : ('integer', (0,15))}}

	def __init__(self, protocol):
		""" The constructor only takes the protocol to which
		the device is linked as argument.
		
		
		"""
		
		self.protocol = protocol
		
		self.name = None
		self.description = None
		self.location = None
		self.house_code = None
		self.group_code = None
		self.unit_code = None
		
		self.informations = []
		self.informations. append(kernel.Information("Etat de l'interrupteur", 
													"Décrit l'état de l'interrupteur", 
													("state", ("on", "off"))))
		self.actions = []
		self.actions.append(kernel.Action(
								"on", 
								"allumer le périphérique", 
								self.switch_on, 
								{}))
		self.actions.append(kernel.Action(
								"off", 
								"éteindre le périphérique", 
								self.switch_off, 
								{}))
		self.actions.append(kernel.Action(
								"sync", 
								"synchroniser le périphérique avec la centrale", 
								self.sync, 
								{}))
		self.actions.append(kernel.Action(
								"unsync", 
								"désynchroniser le périphérique de la centrale", 
								self.unsync, 
								{}))
		
	def set(self, args):
		""" The Nexa Device can be set according to the settings 
		dictionary given in device_infos['arguments'] 
		
		
		"""
		
		try:
			if(type(args['name']) == types.StringType): self.name = args['name']
			else: raise TypeError("The name given is not a string !")
			
			if(type(args['description']) == types.StringType): self.description = args['description']
			else: raise TypeError("The description given is not a string !")
			
			if(type(args['location']) == types.StringType): self.location = args['location']
			else: raise TypeError("The location given is not a string !")
						
			if(type(args['house_code']) == types.IntType): self.house_code = args['house_code']
			else: raise TypeError("The house_code given is not an integer !")
			
			if(type(args['group_code']) == types.IntType): self.group_code = args['group_code']
			else: raise TypeError("The group_code given is not an integer !")
			
			if(type(args['unit_code']) == types.IntType): self.unit_code = args['unit_code']
			else: raise TypeError("The unit_code given is not an integer !")
		except Exception, e:
			raise e

	def switch_on(self):
		""" Method called when the "on" action is triggered. 
		On the one side, it sends the radio command accordingly.
		On the other side, it updates the Information which 
		reflects the state of the device.
		
		"""
		
		self.protocol.send_command(self, 1)
		self.update(1)

	def switch_off(self):
		""" Method called when the "off" action is triggered. 
		On the one side, it sends the radio command accordingly.
		On the other side, it updates the Information which 
		reflects the state of the device.
		
		"""
		
		self.protocol.send_command(self, 0)
		self.update(0)
	
	def sync(self):
		""" Method called when the "sync" action is triggered. 
		It sends a series of "on" commands.
		
		"""
		
		for i in range(5):
			self.switch_on({})
			time.sleep(0.1)
	
	def unsync(self):
		""" Method called when the "unsync" action is triggered. 
		It sends a series of "off" commands.
		
		"""
		
		for i in range(5):
			self.switch_off({})
			time.sleep(0.1)
	
	def update(self, new_command):
		""" Method called to update the state of the device. 
		It updates the linked Information accordingly.		
		
		"""
		
		try:
			if new_command == 1:
				self.informations[0].update("on")
			elif new_command == 0:
				self.informations[0].update("off")
			else:
				raise ValueError("The new state was neither 0 nor 1.")
		except Exception, e:
			raise e

#---------------------------------------------------------------

class NexaRemote(kernel.Device):

	# Ce sont les attributs qui caractérisent ce type de périphérique
	device_infos = {
				'device_name' : "Nexa Remote",
				'device_brand' : "Nexa",
				'device_description' : "Auto-detected Nexa remote.",
				'arguments' : {
							'name' : ('string', 50),
							'description' : ('string', 1000),
							'location' : ('string', 100),}}

	def __init__(self, protocol, house_code, group_code, unit_code):
		""" The constructor does not only take the protocol but also 
		the house_code, the group_code and the unit_code of the newly
		discovered remote as arguments since they will always remain
		the same.
		
		"""
		
		self.name = None
		self.description = None
		self.location = None
		
		self.protocol = protocol
		self.house_code = house_code
		self.group_code = group_code
		self.unit_code = unit_code
		
		self.informations = []
		self.informations. append(kernel.Information("Etat de la télécommande", 
													"Décrit l'état de la télécommande", 
													("state", ("on", "off"))))
		
	def set(self, args):
		""" Method enabling the user to change the name, the description and
		the location of the device. The args must follow the format given in
		device_infos['arguments'].
		
		"""
		
		try:
			if(type(args['name']) == types.StringType): self.name = args['name']
			else: raise TypeError("The name given is not a string !")
			
			if(type(args['description']) == types.StringType): self.description = args['description']
			else: raise TypeError("The description given is not a string !")
			
			if(type(args['location']) == types.StringType): self.location = args['location']
			else: raise TypeError("The location given is not a string !")
		except Exception, e:
			raise e
		
	def switch_on(self):
		""" Method called by the protocol when an "on" radio
		message for this specific device has been received.
		
		"""
		
		self.update(1)

	def switch_off(self):
		""" Method called by the protocol when an "off" radio
		message for this specific device has been received.
		
		"""
		
		self.update(0)
	
	def update(self, new_command):
		""" Method called to update the state of the device. 
		It updates the linked Information accordingly.		
		
		"""
		
		try:
			if new_command == 1:
				self.informations[0].update("on")
			elif new_command == 0:
				self.informations[0].update("off")
			else:
				raise ValueError("The new state was neither 0 nor 1.")
		except Exception, e:
			raise e