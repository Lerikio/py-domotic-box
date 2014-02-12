# -*- coding: utf-8 -*-

import kernel

kernel = kernel.Kernel()
kernel.load_plugins()

print kernel.plugins
print kernel.drivers
print kernel.modems

radio433 = kernel.modems[0]
radio433.set({'COM_port' : 4})

nexa = kernel.drivers[0]
nexa.set({'modem' : radio433})
print nexa.get_instantiable_devices()

nexa.add_device(0,
                {'name' : "Ma premi�re t�l�commande !",
                 'description' : "t�l�commande de test",
                 'location' : 'cuisine',
                 'house_code' : 25693,
                 'group_code' : 0,
                 'unit_code' : 15}) 

nexa_remote =  nexa.get_devices()[0]
actions = nexa_remote.actions
print [act.name for act in actions]
while True:
    num = input()
    print actions[num].method
    actions[num].execute({})