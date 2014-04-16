# -*- coding: utf-8 -*-

import kernel as ker

import threading
import json
import time

from kivy.uix.actionbar import ActionBar, ActionView, ActionButton, ActionOverflow, ActionPrevious, ActionGroup
from kivy.interactive import InteractiveLauncher
from kivy.uix.settings import SettingSpacer
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.settings import (Settings, SettingsWithSidebar, SettingBoolean, SettingItem, SettingString)
from kivy.config import ConfigParser
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, NumericProperty, DictProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

class Menu(BoxLayout):
	pass

class AppScreen(BoxLayout):
	
	def __init__(self, kernel, *args, **kwargs):
		super(AppScreen, self).__init__(*args, **kwargs)
		# On récupère le kernel
		self.kernel = kernel
		
		self.orientation = 'vertical'
		
		# Création du manager d'écrans
		self.add_widget(Menu(size_hint_y=0.08))

		self.manager = ScreenManager()
		
		self.manager.add_widget(DevicesView(self.kernel, name='manage_devices'))
		self.manager.add_widget(InformationsView(self.kernel, name='manage_infos'))
				
		# On ajoute le manager à la fenêtre
		self.add_widget(self.manager)	
	

class SettingExecute(SettingItem):
	
	values = ListProperty(['0', '1'])
	
	def on_release(self):
		# The value doesn't matter: we just want to know 
		# when the user has clicked on the button
		self.value = '1' if (self.value=='0') else '0'

class SettingDescription(SettingItem):
	
	popup = ObjectProperty(None, allownone=True)
	textinput = ObjectProperty(None)

	def on_panel(self, instance, value):
		if value is None:
			return
		self.bind(on_release=self._create_popup)

	def _dismiss(self, *largs):
		if self.textinput:
			self.textinput.focus = False
		if self.popup:
			self.popup.dismiss()
		self.popup = None

	def _validate(self, instance):
		self._dismiss()
		value = self.textinput.text.strip()
		self.value = value
	
	def _create_popup(self, instance):
		# create popup layout
		content = BoxLayout(orientation='vertical', spacing='5dp')
		self.popup = popup = Popup(
			title=self.title, content=content, size_hint=(None, None),
			size=('400dp', '500dp'))

		# create the textinput used for numeric input
		self.textinput = textinput = TextInput(
			text=self.value, font_size='24sp', multiline=True,
			size_hint_y=None, height='300sp')
		textinput.bind(on_text_validate=self._validate)
		self.textinput = textinput

		# construct the content, widget are used as a spacer
		content.add_widget(Widget())
		content.add_widget(textinput)
		content.add_widget(Widget())
		content.add_widget(SettingSpacer())

		# 2 buttons are created for accept or cancel the current value
		btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
		btn = Button(text='Ok')
		btn.bind(on_release=self._validate)
		btnlayout.add_widget(btn)
		btn = Button(text='Cancel')
		btn.bind(on_release=self._dismiss)
		btnlayout.add_widget(btn)
		content.add_widget(btnlayout)

		# all done, open the popup !
		popup.open()

class DevicesView(Settings, Screen):
	
	def __init__(self, kernel, *args, **kwargs):
		super(DevicesView, self).__init__(*args, **kwargs)
		
		self.kernel = kernel
		
		# On récupère les références vers les devices qu'on va afficher/utiliser
		self.devices = kernel.devices
		
		# On customise avec de nouveaux types de "boutons"
		self.register_type('execute', SettingExecute)
		self.register_type('description', SettingDescription)
		
		# On ajoute un configParser qui va en réalité
		# contenir toutes les variables dans l'interface
		self.config = ConfigParser()
		
		# Les valeurs "par défaut" sont celles des devices 
		# au moment de la création du panel.
		# Puis on ajoute un panel par device.
		for d in self.devices:
			self.config.setdefaults(str(d.id), d.properties)
			print json.dumps(d.get_properties_format())
			properties_format = d.get_properties_format()
			for i in d.informations:
				self.config.setdefaults(str(i.id), i.properties)
				properties_format += i.get_properties_format()
			for a in d.actions:
				self.config.setdefaults(str(a.id), a.properties)
				properties_format += a.get_properties_format()
			print properties_format
			self.add_json_panel(d.properties['name'], self.config, data=json.dumps(properties_format))
		
	def on_config_change(self, config, section, key, value):
		if key == 'execute':
			# TODO: récupérer les arguments de l'action avec un config.get_value
			self.kernel.get_by_id(int(section)).execute({})
		else:
			self.kernel.get_by_id(int(section)).set({key: value})
			print self.kernel.get_by_id(int(section)).properties
	
	def on_pre_enter(self):
		self.clear_widgets()
		self.__init__(self.kernel)
	
	def on_close(self):
		self.clear_widgets()
		self.__init__(self.kernel)

class InformationsView(Settings, Screen):
	
	def __init__(self, kernel, *args, **kwargs):
		super(InformationsView, self).__init__(*args, **kwargs)
		
		self.kernel = kernel
		
		# On récupère les références vers les devices qu'on va afficher/utiliser
		self.informations = kernel.infos
		
		# On customise avec de nouveaux types de "boutons"
		self.register_type('description', SettingDescription)
		
		# On ajoute un configParser qui va en réalité
		# contenir toutes les variables dans l'interface
		self.config = ConfigParser()
		
		# Les valeurs "par défaut" sont celles des devices 
		# au moment de la création du panel.
		# Puis on ajoute un panel par device.
		for i in self.informations:
			self.config.setdefaults(str(i.id), i.properties)
			self.add_json_panel(i.properties['name'], self.config, data=json.dumps(i.get_properties_format()))
		
		
	def on_config_change(self, config, section, key, value):
		if key == 'execute':
			# TODO: récupérer les arguments de l'action avec un config.get_value
			self.kernel.get_by_id(int(section)).execute({})
		else:
			self.kernel.get_by_id(int(section)).set({key: value})
			print self.kernel.get_by_id(int(section)).properties
	
	def on_pre_enter(self):
		self.clear_widgets()
		self.__init__(self.kernel)
		
	def on_close(self):
		self.clear_widgets()
		self.__init__(self.kernel)

class KivyApp(App):

	def init_basic_config_for_tests(self):
		
		modem = self.kernel.modems[0]
		print "set method with COM port 5"
		try:
		    modem.set({'COM_port': 4})
		except Exception, e:
		    print e
		else:
		    print "L'ouverture du port s'est bien pass�e"
		print "\n\n"
		
		protocol = self.kernel.protocols[0]
		protocol.set({ 'modem': modem})
		
		light = protocol.add_device(0, {'name': 'lampe', 'description': 'lampe de la chambre', 'location': 'chambre', 'house_code': 25635, 'group_code': 0, 'unit_code': 15})

	def build(self):
		
		# Chargement du noyau de l'application
		self.kernel = ker.Kernel()
		self.kernel.load_plugins()

		# On initialise la centrale avec une config de base		
		self.init_basic_config_for_tests()

		return AppScreen(self.kernel)

KivyApp().run()