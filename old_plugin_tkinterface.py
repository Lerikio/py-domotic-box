# -*- coding: utf-8 -*-

from Tkinter import *
import kernel as ker
import threading

class View(Frame):
	def __init__(self, parent, kernel):
		Frame.__init__(self, parent, width=300)
		self.kernel = kernel   
		self.parent = parent
		#self.display()
		#self.grid(sticky=NW)
	
	def forget_all_children(self, parent):
		for child in parent.winfo_children():
			self.forget_all_children(child)
		parent.grid_forget()
	
	def show(self):
		self.parent.title("Manage devices")
		self.forget_all_children(self)
		self.display()
# 		self.parent.update()
# 		self.parent.deiconify()
		self.grid(sticky=NW, padx=(5,5), pady=(5,5))
	
	def hide(self):
# 		self.parent.withdraw()
		self.forget_all_children(self)
	
	def display(self):
		pass
	
class ManageDevicesView(View):
	
	def display(self):
		
		def onDeviceSelect(*args):
			if len(self.devices_list) > 0:
				if self.device_view != None: self.device_view.grid_forget()
				self.device_view = self.new_device_view(self.devices_list[int(self.devices_menu.curselection()[0])])
				self.device_view.grid(row = 0, column=1, sticky=NW, padx=(10,10), pady=(10,10))
		
		self.device_view = None
		self.devices_list = list(self.kernel.devices)
		self.display_devices_list = StringVar(value=tuple([d.name for d in self.devices_list]))
		self.devices_menu = Listbox(self, listvariable=self.display_devices_list, height=20)
		self.devices_menu.grid(row=0, column=0)
		self.devices_menu.bind('<<ListboxSelect>>', onDeviceSelect)
	
	def new_device_view(self, device):
		
		def apply_change_name(device, name, name_button):
			device.set({'name': name.get(), 'description': device.description, 'location': device.location})
			
			name.grid_remove()
			name = Label(view, text="Name : "+device.name+"\n", wraplength=300, anchor=NW, justify=LEFT)
			name.grid(row = 0, column=0, sticky=NW)
			
			name_button.grid_remove()
			name_button = Button(view, text="change", command=lambda: change_name(device, name, name_button), anchor=NW)
			name_button.grid(row = 0, column=1, sticky=E)
		
		def change_name(device, name, name_button):
			name.grid_remove()
			name = Entry(view)
			name.grid(row = 0, column=0, sticky=NW)
			
			name_button.grid_remove()
			name_button = Button(view, text="apply", command=lambda: apply_change_name(device, name, name_button), anchor=NW)
			name_button.grid(row = 0, column=1, sticky=E)
					
		def change_description():
			pass
		
		def change_location():
			pass
		
		view = Frame(self, width=300)
		
		name = Label(view, text="Name : "+device.name+"\n", wraplength=300, anchor=NW, justify=LEFT)
		name.grid(row = 0, column=0, sticky=NW)
		name_button = Button(view, text="change", command=lambda: change_name(device, name, name_button), anchor=NW)
		name_button.grid(row = 0, column=1, sticky=E)
		
		description = Label(view, text="Description : "+device.description+"\n", wraplength=300, anchor=NW, justify=LEFT)
		description.grid(row = 1, column=0, sticky=NW)
		description_button = Button(view, text="change", command=change_description, anchor=NW)
		description_button.grid(row = 1, column=1, sticky=E)
		
		location = Label(view, text="Location : "+device.location+"\n", wraplength=300, anchor=NW, justify=LEFT)
		location.grid(row = 2, column=0, sticky=NW)
		location_button = Button(view, text="change", command=change_location, anchor=NW)
		location_button.grid(row = 2, column=1, sticky=E)
		
		if not not device.informations:
			infos_view = self.new_infos_view(device, view)
			infos_view.grid(row = 3, column=0, sticky=NW, pady=(0,10))
		
		if not not device.actions:
			actions_view = self.new_actions_view(device, view)
			actions_view.grid(row = 4, column=0, sticky=NW)
			
		return view
	
	def new_infos_view(self, device, device_view):
		
			def onInfoSelect(*args):
				info_value = infos_list[int(tk_info_list.curselection()[0])].values[-1:]
				if info_value:
					tk_info_value = Label(infos_view, text=info_value[0][0], width = 20, anchor=NW, justify=LEFT)
					tk_info_value.grid(row = 0, column=1, sticky=NW, padx=(5,5), pady=(5,5))
				
			infos_view = Frame(device_view)
				
			infos_list = list(device.informations)
			display_infos_list = StringVar(value=tuple([i.name for i in infos_list]))
			
			tk_info_list = Listbox(infos_view, listvariable=display_infos_list, height=5)
			tk_info_list.grid(row = 0, column=0, sticky=NW)
			
			tk_info_list.bind('<<ListboxSelect>>', onInfoSelect)
			
			return infos_view
			
	def new_actions_view(self, device, device_view):
			
			def onActionSelect(*args):
				action = actions_list[int(tk_info_list.curselection()[0])]
				if action:
					tk_action = Button(actions_view, text="execute", command=lambda: action.execute({}))
					#Label(actions_view, text=action.name, width = 20, anchor=NW, justify=LEFT)
					tk_action.grid(row = 0, column=1, sticky=NW, padx=(5,5), pady=(5,5))
				
			actions_view = Frame(device_view)
				
			actions_list = list(device.actions)
			display_infos_list = StringVar(value=tuple([a.name for a in actions_list]))
			
			tk_info_list = Listbox(actions_view, listvariable=display_infos_list, height=5)
			tk_info_list.grid(row = 0, column=0, sticky=NW)
			
			tk_info_list.bind('<<ListboxSelect>>', onActionSelect)
			
			return actions_view
	
class TkInterface(ker.Interface):

	def display_view(self, new_view):
		self.current_view.hide()
		self.current_view = new_view
		self.current_view.show()
		
	def __init__(self, kernel):

		self.kernel = kernel
		
		# Fenêtre principale root
		self.root = Tk()
		self.root.option_add('*tearOff', FALSE) # Pour ne pas pouvoir tearoff les menus
		#win = Toplevel(root)
		
		self.frame = Frame(self.root)
		self.frame.grid()
		
		manage_devices_view = ManageDevicesView(self.root, self.kernel)
		self.current_view = manage_devices_view
		self.display_view(manage_devices_view)

		# Fonction qui crée le menu de l'interface
		
		def setup_menu():
			menubar = Menu(self.root)
			self.root['menu'] = menubar			
			
			# Trois menus principaux
			menu_addnew = Menu(menubar)
			menubar.add_cascade(menu=menu_addnew, label='Add new...')
			menu_manage = Menu(menubar)
			menubar.add_cascade(menu=menu_manage, label='Manage...')
			menu_settings = Menu(menubar)
			menubar.add_cascade(menu=menu_settings, label='Settings')
			
			# Sous-menus du menu "Add new..."
			menu_addnew.add_command(label='Scenario', command=new_scenario_view)
			menu_addnew.add_command(label='Block model', command=new_blockmodel_view)
			menu_addnew.add_separator()
			menu_addnew.add_command(label='Device', command=new_device_view)
			
			# Sous-menus du menu "Manage.."
			menu_manage.add_command(label='Scenarios', command=manage_scenarios_view)
			menu_manage.add_command(label='Block models', command=manage_blockmodels_view)
			menu_manage.add_separator()
			menu_manage.add_command(label='Actions', command=manage_actions_view)
			menu_manage.add_command(label='Informations', command=manage_informations_view)
			menu_manage.add_separator()
			menu_manage.add_command(label='Devices', command= lambda: self.display_view(manage_devices_view))
			menu_manage.add_command(label='Protocols', command=manage_protocols_view)
			menu_manage.add_command(label='Modems', command=manage_modems_view)
			
			# Sous-menus du menu "Settings"
			menu_settings.add_command(label='Plugins', command=settings_plugins_view)
			menu_settings.add_command(label='Interface', command=settings_interface_view)
		
		# We start with teh definition of all the possible views
		
		# "New..." views
		
		def new_scenario_view():
			print "coucou"
			pass
		
		def new_blockmodel_view():
			pass
		
		def new_device_view():
			pass
		
		# "Manage" views
		
		def manage_scenarios_view():
			pass
		
		def manage_blockmodels_view():
			pass
		
		def manage_actions_view():
			pass
		
		def manage_informations_view():
			pass
		
		def manage_protocols_view():
			pass
		
		def manage_modems_view():
			pass
		
		# "Settings" views
		
		def settings_plugins_view():
			pass
		
		def settings_interface_view():
			pass
		
		# Création du menu principal
		setup_menu()

		# Then we launch the main Tkinter view in a new thread
		
		class InterfaceWindowThread(threading.Thread):
				
			def __init__(self, root):
				threading.Thread.__init__(self)
				self.root = root
			
			def run(self):
				# On lance la boucle de la fenêtre principale de l'interface Tkinter
				self.root.mainloop()	
								
		interfaceWindowThread = InterfaceWindowThread(self.root)
		interfaceWindowThread.start()


""" Set of attributes which describe the plugin, in order 
to add it to the kernel and then be able to describe it
to the user.  

"""
plugin_type = "interface"
name = "TkInterface"
description = "A local user interface using Tkinter allowing the user to have an overview of the box."
plugin_id = "3"
interface_class = TkInterface	