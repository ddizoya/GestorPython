#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gi.repository import Gtk
from Gestor import Gestor
from BaseDatos import BaseDatos

class Licencia:
    """Licencia predeterminada de uso. Se llama la primera vez que el usuario usa la aplicación."""
    def __init__(self, user, bd):
        """Constructor con parámetros usuario y objeto BaseDatos. Cuando el usuario no ha aceptado la licencia,
        usamos su nombre de usuario para, en el caso de aceptar los términos, actualizar el estado de su licencia en la base de datos."""
        self.bd = bd
        self.user = user
        #Desde el fichero .glade, cargamos la ventana.
        self.builder = Gtk.Builder()
        self.builder.add_from_file("../glade/licencia.glade")

        #Obtenemos los objetos que nos interesan; botón, caja y ventana.
        self.aceptar = self.builder.get_object("acept")
        self.box = self.builder.get_object("box2")
        self.ventana = self.builder.get_object("window1")
        self.ventana.set_icon_from_file("../img/default-icon.jpg")
        self.ventana.connect("delete-event", Gtk.main_quit) #Cierre default
        signal = {"on_acept_clicked":self.on_acept_clicked} #Diccionario de eventos
        self.builder.connect_signals(signal) #Le asignamos el evento al boton desdee el builder

        imagen = Gtk.Image()
        imagen.set_from_file("../img/license.jpg")
        self.box.pack_end(imagen, False, True, 0)
        self.ventana.show_all()

    def on_acept_clicked(self, widget):
        """Evento que llama al Gestor, y que autoelimina la ventana de licencia."""
        self.bd.aceptar_licencia(self.user)
        gestor = Gestor()
        self.ventana.destroy()

