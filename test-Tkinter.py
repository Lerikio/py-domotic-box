from Tkinter import *
import time 

def newFile(text):
    win.destroy()
    print text

def openFile():
    print "open file !"

def closeFile():
    print "close file !"

def displayProperties(*args):
    print "coucou"
    pass

root = Tk()
root.option_add('*tearOff', FALSE)

win = Toplevel(root)

menubar = Menu(root)
root['menu'] = menubar

menu_file = Menu(menubar)
menu_edit = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='File')
menubar.add_separator()
menubar.add_cascade(menu=menu_edit, label='Edit')

menu_file.add_command(label='New', command=newFile)
menu_file.add_command(label='Open...', command=openFile)
menu_file.add_command(label='Close', command=closeFile)

myList = StringVar(value=("bleu", "blanc", "rouge"))

l = Listbox(root, listvariable=myList, height=10)
l.pack(side=LEFT)

l.bind('<<ListboxSelect>>', displayProperties)

root.mainloop()

#root.destroy() # optional; see description below