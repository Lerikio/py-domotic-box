# -*- coding: utf-8 -*-

import kernel as ker

kernel = ker.Kernel()
kernel.load_plugins()

modem = kernel.modems[0]

print "set method with COM port 5"
try:
    modem.set({'COM_port': 4})
except Exception, e:
    print e
else:
    print "L'ouverture du port s'est bien pass�e"
print "\n\n"

protocol = kernel.protocols[0]
protocol.set({ 'modem': modem})

light = protocol.add_device(0, {'name': 'lampe', 'description': 'lampe de la chambre', 'location': 'chambre', 'house_code': 25635, 'group_code': 0, 'unit_code': 15})

print light.__class__.__mro__