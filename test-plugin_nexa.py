# -*- coding: utf-8 -*-

import plugins.plugin_433radio as radio
import plugins.plugin_nexa as nexa

modem = radio.Modem()

print "set method with COM port 5"
try:
    modem.set({'COM_port': 4})
except Exception, e:
    print e
else:
    print "L'ouverture du port s'est bien pass�e"
print "\n\n"

protocol = nexa.Protocol()
protocol.set({ 'modem': modem})

light = protocol.add_device(0, {
                                'name' : 'lampe',
                                'description' : 'lampe de la chambre', 
                                'location' : 'chambre',  
                                'house_code' : 25635, 
                                'group_code' : 0, 
                                'unit_code' : 15})

print nexa.NexaDevice
print light.__class__.__mro__
print nexa.NexaDevice not in light.__class__.__mro__

while True:
    print "\n"
    input = raw_input("a = on | z = off | e = sync | r = unsync - ")
    if input == 'a':
        light.actions[0].execute({})
    elif input == 'z':
        light.actions[1].execute({})
    elif input == 'e':
        light.actions[2].execute({})
    elif input == 'r':
        light.actions[3].execute({})