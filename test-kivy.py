'''
Application example using build() + return
==========================================

An application can be built if you return a widget on build(), or if you set
self.root.
'''

import kivy
kivy.require('1.0.7')

from kivy.uix.settings import (Settings, SettingsWithSidebar, SettingBoolean, SettingItem, SettingString)
from kivy.app import App
from kivy.uix.button import Button


class TestApp(App):

    def build(self):
        # return a Button() as a root widget
        return SettingBoolean()

if __name__ == '__main__':
    TestApp().run()
