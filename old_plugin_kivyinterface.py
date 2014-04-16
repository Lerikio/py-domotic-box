# -*- coding: utf-8 -*-

import kernel

import threading
import json
import time

from kivy.uix.settings import SettingSpacer
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.settings import (Settings, SettingsWithSidebar, SettingBoolean, SettingItem)
from kivy.config import ConfigParser
#from kivy.properties import OptionProperty, ObjectProperty

from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, NumericProperty, DictProperty

a, b, c = 3, 4, 5

device1_defaults = {
				'device_name': u'télécommande 1',
				'device_location': 'salon',
				'device_code': 18976,
				'execute': '0',
				'device_description': u'bonjour je suis un appareil domotiqu esuper bien qui prend des lignes et des lignes pour être décrit'
				}

device1_data = [
		{ 'type': 'title',
		'title': 'Device configuration' },
		{ 'type': 'string',
		'title': 'Name',
		'desc': 'Name of the device',
		'key': 'device_name',
		'section': 'device1'},
		{ 'type': 'description',
		'title': 'Description',
		'desc': 'Description of the device',
		'key': 'device_description',
		'section': 'device1'},
		{ 'type': 'string',
		'title': 'Location',
		'desc': 'The place where the device is located',
		'key': 'device_location',
		'section': 'device1'},
		{ 'type': 'numeric',
		'title': 'Device code',
		'desc': 'The code which uniquely refers to the device.',
		'key': 'device_code',
		'section': 'device1',
		'disabled': True
		},
		{ 'type': 'button',
		'title': 'Launch action',
		'desc': 'Toggle this to launch the action.',
		'key': 'execute',
		'section': 'device1'
		}]

device2_defaults = {
				'device_name': u'télécommande 2',
				'device_location': 'cuisine',
				'device_code': 76543
				}

device2_data = [
		{ 'type': 'title',
		'title': 'Device configuration' },
		{ 'type': 'string',
		'title': 'Name',
		'desc': 'Name of the device',
		'key': 'device_name',
		'section': 'device2'},
		{ 'type': 'string',
		'title': 'Location',
		'desc': 'The place where the device is located',
		'key': 'device_location',
		'section': 'device2'},
		{ 'type': 'numeric',
		'title': 'Device code',
		'desc': 'The code which uniquely refers to the device.',
		'key': 'device_code',
		'section': 'device2'
		}]

# class KivyInterface(kernel.Interface):
# 	
# 	def __init__(self):
# 		KivyApp().run()

class MySetting(SettingItem):
	
	values = ListProperty(['0', '1'])
	
	def on_release(self):
		print 'avant ' + self.value
	 	if self.value == '1':
	 		self.value = '0'
	 	else:
	 		self.value = '1'
	 	print 'après ' + self.value


class MyDescriptionSetting(SettingItem):
	
	values = StringProperty()
	
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

class KivyApp(App):

	testProperty = NumericProperty()

	def on_testProperty(self, instance, value):
		print self.testProperty

	def build(self):
		
		self.testProperty = a
		
		devices = Settings()
		devices.interface_cls = SettingsWithSidebar
		config = ConfigParser()
		
		devices.register_type('button', MySetting)
		devices.register_type('description', MyDescriptionSetting)
		
		config.setdefaults('device1', device1_defaults)
		devices.add_json_panel('Device 1', config, data=json.dumps(device1_data))
		
		
		
		config.setdefaults('device2', device2_defaults)
		self.mypanel = devices.add_json_panel('Device 2', config, data=json.dumps(device2_data))
		
		def fonction(config, section, key, value):
			print config, section, key, value
			
			if section == 'device1' and key == 'execute':
# 				self.mypanel.set_value('device1', 'execute', '1')
# 				config.set('device1', 'execute', '1')
				print 'coucou'
				a = 7
				
		
		devices.on_config_change = fonction
		return devices


# """ Set of attributes which describe the plugin, in order 
# to add it to the kernel and then be able to describe it
# to the user.  
# 
# """
# plugin_type = "interface"
# name = "KivyInterface"
# description = "A local user interface using Kivy."
# plugin_id = "5"
# interface_class = KivyInterface	

class MyThread(threading.Thread):
	
	def run(self):
		KivyApp().run()

class KivyInterface(kernel.Interface):
	
	def __init__(self, kernel):
		myThread = MyThread()
		myThread.start()

""" Set of attributes which describe the plugin, in order 
to add it to the kernel and then be able to describe it
to the user.  

"""
plugin_type = "interface"
name = "KivyInterface"
description = "A local user interface using Kivy."
plugin_id = "5"
interface_class = KivyInterface	