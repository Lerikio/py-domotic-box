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
print "\r"
print "Interface(s) chargée(s) :"
print kernel.interfaces

http = kernel.interfaces[0]
http.run()