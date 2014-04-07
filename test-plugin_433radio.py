# -*- coding: utf-8 -*-

import plugins.plugin_433radio as plg

modem = plg.Modem()

print "get_set_arguments method"
print modem.get_set_arguments()
print "\n\n"

print "get_modem_type method"
print modem.get_modem_type()
print "\n\n"

print "get_modem_name method"
print modem.get_modem_name()
print "\n\n"

print "set method with COM port 5"
try:
    modem.set({'COM_port': 4})
except Exception, e:
    print e
else:
    print "L'ouverture du port s'est bien passée"
print "\n\n"

