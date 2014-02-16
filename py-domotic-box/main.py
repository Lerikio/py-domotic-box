# -*- coding: utf-8 -*-

import kernel

kernel = kernel.Kernel()
kernel.load_plugins()

print "--- Initialisation de la centrale ---"
print "\r"
print "Chargement des plugins..."
print "\r"
print "Driver(s) chargé(s) : "
print kernel.drivers
print "\r"
print "Modem(s) chargé(s) : "
print kernel.modems

radio433 = kernel.modems[0]
radio433.set({'COM_port' : 4})
print "\r"

nexa = kernel.drivers[0]
nexa.set({'modem' : radio433})

print "Ajout automatique d'une télécommande virtuelle Nexa"
print "Identifiant HC 25693 / GP 0 / UC 15" 
nexa.add_device(0,
                {'name' : "Ma première télécommande !",
                 'description' : "t�l�commande de test",
                 'location' : 'cuisine',
                 'house_code' : 25693,
                 'group_code' : 0,
                 'unit_code' : 15}) 

while True:
    print "\n--- Menu principal ---"
    print "1) afficher les périphériques connectés"
    print "2) ajouter une télécommande virtuelle Nexa"
    print "3) utiliser un périphérique"
    num = raw_input("Votre choix ? ")
    if num == '1':
        print "\rListe des périphériques connectés"
        for i, device in enumerate(kernel.devices):
            print str(i+1) + ") " + device.name + " / " + str(device.house_code) + " / " + str(device.unit_code)
    elif num == '2':
        args = {'name' : raw_input("Quel nom ? "),
                'description' : raw_input("Description ? "),
                'location' : raw_input("Emplacement ? "),
                'house_code' : raw_input("House Code ? "),
                'group_code' : 0,
                'unit_code' : 15}
        new_device = kernel.drivers[0].add_device(0, args)
        pass
    elif num == '3':
        id = int(raw_input("Lequel ? "))
        print "\rInformations disponibles :"
        for i, info in enumerate(kernel.devices[id-1].informations):
            print str(i+1) + ") " + info.name
        print "Actions disponibles :"
        for i, action in enumerate(kernel.devices[id-1].actions):
            print str(i+1) + ") " + action.name + " / " + action.description
        choice = raw_input("\rInformation ou action (i/a) ? ")
        num = int(raw_input("\rNuméro ? "))
        if choice == 'i':
            print kernel.devices[id-1].informations[num-1].values
        elif choice == 'a':
            kernel.devices[id-1].actions[num-1].execute({})
        