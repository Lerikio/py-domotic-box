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

def introduce_plugin():
	return {'type' : PLUGIN_TYPE, 'name': PLUGIN_NAME, 'description' : PLUGIN_DESCRIPTION} 


# Classe instanciée une seule fois par le coeur et gérant 
# toutes les requêtes concernant le protocole Nexa
class Driver():

	#---------------------------------------------------------------
	# Interface avec le core 
	#---------------------------------------------------------------

	def __init__(self):
		self.modem = None

		# TODO Définir la façon dont on définit la structure d'un message
		self.messageStructure = []

		# Ce sont les nouveaux périphériques qu'on propose au core
		self.handledDeviceTypes = (NexaSwitch, NexaVirtualRemote)

	def get_devices(self):
		return self.handledDeviceTypes

	def add_device(self, device_type, arguments):
		# TODO Vérifier que les bons arguments sont fournis
		new_device = device_type(arguments)
		this.devices.append(newDevice)
		return new_device
	
	def set_modem(self, modem):
		# TODO Ajouter une vérification de compatibilité du modem proposé

		# On va pouvoir envoyer des données par notre modem
		self.modem = modem 
		
		# On spécifie au modem la structure de message qu'on attend au modem 
		# pour qu'il nous transmette ce qui est nous est adressé
		self.modem.attach(self, messageStructure) 
		
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