#!/usr/bin/python3

import sharedGUI as sg
import gui as gi

sg.objs.start()
menu = gi.Menu()
menu.show()
print(menu.choice)
sg.objs.end()
