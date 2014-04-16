# -*- coding: utf-8 -*-

#---------------------------------------------------------------
# Plugin importable permettant a la centrale de gerer Oregon.
# C'est un plugin de type protocol. D'une part, 
# elle comporte le driver et d'autre part les nouveaux 
# peripheriques qu'elle apporte.
#---------------------------------------------------------------

# TODO: reflechir a cette histoire de core_classes

import kernel

class Oregon(kernel.Protocol):
    """ Main class of a protocol plugin.
    
    """

    #---------------------------------------------------------------
    # Interface avec le kernel 
    #---------------------------------------------------------------

    def __init__(self, kernel):
        self.kernel = kernel

        # Jusqu'a ce qu'on l'ait configure, le driver n'a pas encore de modem
        self.modem = None

        # On definit la structure de messages radio propre au protocole OregonTHGR122NX 
        self.message_structure = {
                                'baselength' : 1,
                                'symbols' : {
                                        'start' : [] ,
                                        'one' : [1,5,1,1],
                                        'zero' : [1,1,1,5],
                                        'end' : [1,30]
                                        },
                                'structure' : ['start'] + 32*[('one','zero')] + ['end']
                                }

        # Liste des peripheriques connectes geres par ce driver
        self.devices = []

        # Parametres a fournir pour configurer le driver
        self.settings = {'modem' : ('Modem', None)}

        # Liste des peripheriques potentiellement gerables par ce driver
        self.handled_devices = [OregonTHGR122NX]

        # Le driver ne propose a l'exterieur d'instantier un peripherique
        # seulement si cela a un sens. Ici, une sonde Oregon ne sera instantie
        # que si on en detecte un, automatiquement.
        self.instantiable_devices = [OregonTHGR122NX]

    def get_set_arguments(self):
        """ Returns the arguments needed to set the driver.    """
        return self.settings

    def set(self, args):
        """ Sets the driver. Returns True if the setting was a success. 
        Otherwise, it returns a tuple containing the setting which caused 
        the issue.
        
        Keyword arguments:
        settings -- the dictionary of settings used to set the driver. Its 
        format is determined by the function get_set_arguments.
        
        """

        # On verifie que les arguments donnes sont valides
        retour = True
        if args['modem'].get_modem_type() == 'radio_433': 
            self.modem = args['modem']
            # On specifie au modem la structure de message qu'on attend au modem 
            # pour qu'il nous transmette ce qui est nous est adresse
            self.modem.attach(self, self.message_structure)
        else:
            retour = ('modem', "Le modem specifie n'est pas du bon type")
        return retour

    def get_instantiable_devices(self):
        """ Returns a list of the devices instantiable by the user
        of the driver. 
        The list of user-instantiable devices is included in the 
        list of the driver-handled devices but not necessarily 
        equal.  
        
        """
        # On ne fournit pas directement la classe pour que le driver reste
        # le seul a pouvoir instancier des peripheriques
        return [i.device_infos for i in self.instantiable_devices]

    def add_device(self, device_id, args):
        """ Proxy method used to instantiate a new device. Returns True
        if the instantiation has succeeded, otherwise the arguments which
        caused an issue.
          
        """
        retour = True
        if device_id == 0:
            new_device = OregonTHGR122NX()
            # TODO: Verifier que les bons arguments sont fournis
            # avec une fonction generique (ce probleme se pose 
            # souvent dans le programme)
            new_device.set(self, args)
            self.devices.append(new_device)
        else:
            retour = ('device_id', "device_id out of range")

        return retour

    def get_devices(self):
        return self.devices

    #---------------------------------------------------------------
    # Interface avec le modem 
    #---------------------------------------------------------------

    # Recoit une trame identifiee comme destinee a ce driver et
    # transmise par la couche inferieure. Cela suppose que la couche la
    # plus basse a la capacite d'identifier le protocole du message et
    # s'adresse ainsi directement a la methode process_message du
    # driver.
    # La methode doit etre specialisee pour traiter et decoder une trame Nexa
    # Elle sera totalement redigee quand on saura sous quelle forme le message est obtenu
    def process_message(self, message):
        # TODO: Transformation de ce qui est recu du modem en message de 32 bits
        # Transformation d'un tableau de bits en entiers
        def from_bitfield_to_int(bitfield):
            return sum([i*2**(len(bitfield)-1-idi) for idi, i in enumerate(bitfield)])

        house_code = from_bitfield_to_int(message[0:26])
        group_code = message[26]
        command = message[27]
        unit_code = from_bitfield_to_int(message[28:32])

        device_found = False
        for device in self.devices:
            if device.house_code == house_code:
                device_found = True
                # TODO: Il faudrait verifier qu'on a bien a faire a un sensor
                device.update(command)
        if not device_found:
            new_device = OregonTHGR122NX()
            new_device.set(self, {
                                'name' : "New OregonTHGR122NX",
                                'description' : "A new Oregon Scientific has been detected and added to your devices.",
                                'location' : "Specify a location.",
                                'house_code' : house_code,
                                'group_code' : group_code,
                                'unit_code' : unit_code})
            self.devices.append(new_device)
    #---------------------------------------------------------------
    # Interface avec les devices 
    #---------------------------------------------------------------

    def send_command(self, device, command):

        def from_int_to_bitfield(n):
            return [1 if digit=='1' else 0 for digit in bin(n)[2:]]

        sequence = from_int_to_bitfield(device.house_code)
        sequence.append(device.group_code)
        sequence.append(command)
        sequence.append(from_int_to_bitfield(device.unit_code))

        # TODO: transformer le bitfield sequence en une reelle 
        # sequence radio de type (pulse, duree du pulse) a 
        # envoyer au modem radio
        # Pour cela, utiliser les conventions donnees dans 
        # self.message_structure
        radio_sequence = []

        result = True
        if(self.modem != None):
            self.modem.send(radio_sequence)
        else:
            result = ("Il faut definir un modem radio 433 pour ce driver !")
        return result



#--------------------------------------------------------------------


#Fonction pour creer des intervalles 

def arithmetic_progression(start, step, length):
    for i in xrange(length):
        yield start + i * step



# Sonde Oregon THGR122NX, code 1D20
class OregonTHGR122NX():

        # Ce sont les attributs qui caracterisent ce type de peripherique
        device_infos = {
                                'device_name' : "Oregon Scientific" , 
                                'device_brand' : "Oregon" , 
                                'device_description' : "Sonde OregonTHGR122NX" ,
                                'arguments' :       {
                                                    'name' : ('string', 50),
                                                    'description' : ('string', 1000),
                                                    'location' : ('string', 100),
                                                    'house_code' : ('integer', (0,131071)),
                                                    'group_code' : ('integer', (0,1)),
                                                    'unit_code' : ('integer', (0,15))
                                                    }
                        }
        
        
        
        def __init__(self, name, description, location, house_code, group_code, unit_code):
                self.name = None 
                self.description = None 
                self.location = None 
                self.driver = None

                self.house_code = None
                self.group_code = None
                self.unit_code = None

                self.informations = []
                self.informations.append(kernel.Information(
                                            "Temperature", "Donne la temperature relevee", ("Temperature", arithmetic_progression(-50, 50, 0.1)),
                                            "Humidity", "Donne l'humidite relevee", ("Humidity, range[0;100] ")
                                                    )
                                         )


        def set(self, driver, args):
        # TODO: verifier la coherence des arguments fournis avec ce qui a ete demande
                self.name = args['name']
                self.description = args['description']
                self.location = args['location']
                self.driver = driver

                self.house_code = args['house_code']
                self.group_code = args['group_code']
                self.unit_code = args['unit_code']

""" Set of attributes which describe the plugin, in order 
to add it to the kernel and then be able to describe it
to the user.  

"""
plugin_type = "protocol"
name = "Oregon"
description = "A protocol plugin which enables the use of Oregon-powered devices. A compatible 433 MHz modem is needed for the protocol to function."
plugin_id = "4"
protocol_class = Oregon