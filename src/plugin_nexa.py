# -*- coding: utf-8 -*-

#---------------------------------------------------------------
# Plugin importable permettant à la centrale de gérer le 
# protocole Nexa. C'est un plugin de type protocol. D'une part, 
# elle comporte le driver et d'autre part les nouveaux 
# périphériques qu'elle apporte.
#---------------------------------------------------------------

from core_classes import * 

# Fonction accessible dès l'importation du module Python.
# Elle permet d'identifier le plugin qui va être chargé 
# et d'adapter ainsi son chargement en conséquence.
PLUGIN_TYPE = 'protocol'
PLUGIN_NAME = 'nexa'
PLUGIN_DESCRIPTION = 'Plugin de type protocol permettant au coeur de gérer des périphériques Nexa.'
PLUGIN_CLASS = Driver

def introduce_plugin():
	return {
		'type' : PLUGIN_TYPE, 
		'name' : PLUGIN_NAME, 
		'description' : PLUGIN_DESCRIPTION,
		'class' : PLUGIN_CLASS} 

# Classe instanciée une seule fois par le coeur et gérant 
# toutes les requêtes concernant le protocole Nexa
class Driver():

	#---------------------------------------------------------------
	# Interface avec le kernel 
	#---------------------------------------------------------------

	def __init__(self):
		# Jusqu'à ce qu'on l'ait configuré, le driver n'a pas encore de modem
		self.modem = None

		# On définit la structure de messages radio propre au protocole nexa 
		self.message_structure = {
								'baselength' : 250,
								'symbols' : {
										'start' : [1,10],
										'one' : [1,5,1,1],
										'zero' : [1,1,1,5],
										'end' : [1,30]
										},
								'structure' : ['start'] + [('one','zero') for i in range(32)] + ['end']
								}

		# Ce sont les nouveaux périphériques qu'on propose au core
		self.handled_device_types = (NexaSwitch, NexaVirtualRemote)

		# Liste des périphériques connectés gérés par ce driver
		self.devices = []
		
		# Paramètres à fournir pour configurer le driver
		self.settings = {'modem' : {'name' : 'modem', 
								'type' : '433_radio_modem',
								'description' : 'Modem radio à utiliser avec ce driver'}}
		
		# Liste des périphériques potentiellement gérables par ce driver
		self.handled_devices = [NexaSwitch, NexaVirtualRemote]
	
	def get_set_arguments(self):
		""" Returns the arguments needed to set the driver.	"""
		return self.settings
	
	def set(self, settings):
		""" Sets the driver. Returns True if the setting was a success. 
		Otherwise, it returns a tuple containing the setting which caused 
		the issue.
		
		Keyword arguments:
		settings -- the dictionary of settings used to set the driver. Its 
		format is determined by the function get_set_arguments.
		
		"""
		
		# On vérifie que les arguments donnés sont valides
		retour = True
		if settings['modem'].get_modem_infos() == 'radio_433': 
			self.modem = settings['modem']
			# On spécifie au modem la structure de message qu'on attend au modem 
			# pour qu'il nous transmette ce qui est nous est adressé
			self.modem.attach(self, self.message_structure)
		else:
			retour = ('modem', "Le modem specifié n'est pas du bon type"))
	
		return retour

	def get_handled_devices(self):
		""" Returns a list of dictionaries describing the device handled 
		by the present driver. It doesn't return a direct reference to 
		the device classes to ensure that the driver is the only one being 
		able to instantiate a device (through the add_device method).
		
		"""
		# On ne fournit pas directement la classe pour que le driver reste
		# le seul à pouvoir instancier des périphériques
		return map(Device.get_device_info, self.handled_devices)

	def add_device(self, device_id, arguments):
		""" Proxy method used to instantiate a new device. Returns True
		if the instantiation has succeeded, otherwise the arguments which
		caused an issue.
		 
		"""

		retour = True
		for Dev in self.handled_devices:
			if Dev.get_device_info()['device_id'] == device_id:
				# TODO Vérifier que les bons arguments sont fournis
				# avec une fonction générique (ce problème se pose 
				# souvent dans le programme)
				new_device = Dev(arguments)
				self.devices.append(new_device)
				
	def get_devices(self):
		return self.devices

	#---------------------------------------------------------------
	# Interface avec le modem 
	#---------------------------------------------------------------

	# Reçoit une trame identifiée comme destinée à ce driver et
	# transmise par la couche inférieure. Cela suppose que la couche la
	# plus basse a la capacité d'identifier le protocole du message et
	# s'adresse ainsi directement à la méthode process_message du
	# driver.
	# La méthode doit être spécialisée pour traiter et décoder une trame Nexa
	# Elle sera totalement rédigée quand on saura sous quelle forme le message est obtenu
	def process_message(self, message):
		# TODO Transformation de ce qui est reçu du modem en message de 32 bits
		house_code = message[0:26]
		group_code = message[26:27]
		command = message[27:28]
		unit_code = message[28:32]
		for device in self.devices:
			if device.house_code == house_code:
				# TODO Il faudrait vérifier qu'on a bien à faire à un sensor
				device.update(command)

	#---------------------------------------------------------------
	# Interface avec les devices 
	#---------------------------------------------------------------

	def sendCommand(self, device, command):
		if(self.modem != None):
			sequence = startSequence + device.house_code + device.group_code + command + device.unit_code + endSequence
			self.modem.send(sequence)
			result = True
		else:
			result = False
		return result

# Interrupteur Nexa classique on/off
class NexaSwitch(Sensor):

	def __init__(self, name, description, location, house_code, group_code, unit_code):
		Sensor.__init__(name, location)
		self.house_code = house_code
		self.group_code = group_code
		self.unit_code = unit_code
		self.informations.append(Information("Bouton 1 de la télécommande", "", "state", ("on", "off")))

# Permet de simuler une télécommande Nexa (id généré aléatoirement ou fourni par l'utilisateur)
class NexaVirtualRemote(Actuator):

	# Ce sont les attributs qui caractérisent le type de périphérique
	device_name = "Nexa Virtual Remote"
	device_brand = "Nexa"
	device_description = "Simulation d'une télécommande deux états Nexa"

	def __init__(self, name, description, location, house_code, group_code, unit_code):
		super(NexaVirtualRemote, self).__init__(name, description, location)
		self.house_code = house_code
		self.group_code = group_code
		self.unit_code = unit_code
		self.actions.append(Action("on", "appuyer sur le bouton on de la télécommande", self.switch_on, {}))
		self.actions.append(Action("off", "appuyer sur le bouton off de la télécommande", self.switch_off, {}))

	def switch_on(self):
		self.driver.sendCommand(self, 1)

	def switch_off(self):
		self.driver.sendCommand(self, 0)