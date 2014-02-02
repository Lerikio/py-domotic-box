# -*- coding: utf-8 -*-

from core_classes import *

# Classe gérant l'ensemble des plugins, des périphériques, des informations et des actions
# Elle permet de charger de nouveaux plugins, de configurer de nouveaux périphériques,
# de gérer la détection d'un nouveau périphérique que l'utilisateur devra configurer
class Core:

	def __init__(self):
		self.plugins = []
		self.drivers = []
		self.devices = []
		
	# Charge un plugin, c'est-à-dire détecte le type de plugin (modem ou protocole dans un premier temps)
	# puis charge ce qu'apporte ce plugin (nouveaux périphériques...)
	def load_plugin(self, plugin_path):
		plugin = __import__(plugin_path, fromlist=['o'])
		if plugin not in self.plugins:
			print plugin.introduce_plugin()
			if(plugin.introduce_plugin()['type'] == 'protocol'):
				print "Chargement d'un plugin de protocole"
				self.drivers.append(plugin.Driver())
				print "Le driver suivant vient d'être chargé : "
				print self.drivers[len(self.drivers)-1]
				newDevices = self.drivers[len(self.drivers)-1].get_devices()
				print "Les nouvelles classes de périphériques suivantes sont disponibles : "
				print newDevices
			else:
				print "Ce n'est pas un plugin de protocole"
		else:
			print "Ce plugin a déjà été chargé."

	# def add_device():
                
