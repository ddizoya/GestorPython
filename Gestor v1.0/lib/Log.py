#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gi.repository import Gtk
from Gestor import Gestor
from BaseDatos import BaseDatos
from Licencia import Licencia

class Log:
    def __init__(self):
        """Constructor por defecto que creará directamente la ventana de log in para el user"""
        self.ventana = Gtk.Window(title="Log in.")
        self.ventana.set_icon_from_file("../img/default-icon.jpg")
        self.vbox= Gtk.VBox()
        self.ventana.add(self.vbox)

        self.fila = Gtk.Box()
        self.vbox.add(self.fila)
        self.fila.set_homogeneous(True)

        self.label = Gtk.Label("ID")
        self.id = Gtk.Entry()
        self.fila.add(self.label)
        self.fila.add(self.id)

        self.fila2 = Gtk.Box()
        self.vbox.add(self.fila2)
        self.fila2.set_homogeneous(True)

        self.label = Gtk.Label("Passwd")
        self.passwd = Gtk.Entry()
        self.passwd.set_visibility(False)
        self.fila2.add(self.label)
        self.fila2.add(self.passwd)

        self.ventana.show_all()
        self.ventana.connect("delete-event", Gtk.main_quit)
        self.passwd.connect("activate", self.validar)

    def validar (self, widget):
        """Valida que el usuario introducido existe. Si existe, valida si ha aceptado o no los términos de licencia. Si se han aceptado
        previamente, directamente se ejecuta el gestor. Sino tendrá que aceptarlos."""
        user = str(self.id.get_text())
        passwd = str(self.passwd.get_text())

        bd = BaseDatos()
        user_valido = bd.verificar_user(user, passwd)
        if user_valido:
            licencia_aceptada = bd.estado_licencia(user)
            if licencia_aceptada:
                Gestor()
                self.ventana.destroy()
            else:
                Licencia(user, bd)
                self.ventana.destroy()
        else:
            pass


Log()
Gtk.main()