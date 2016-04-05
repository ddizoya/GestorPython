#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

class BaseDatos:
    """Este módulo se centrará en las conexiones entre la base de datos y nuestra aplicación, empleando sqlite3."""
    def __init__(self):
        """Constructor sin parámetros que inicializa la conexión a la base de datos."""
        self.conec = sqlite3.connect("basedatos.bd")
        self.c = self.conec.cursor()

    def borrar_tabla_pacientes(self):
        """Método para borrar directamente la tabla pacientes"""
        self.c.execute("DROP TABLE pacientes")

    def crearTablaPaciente(self):
        """Método que crea la tabla pacientes con unos campos predeterminados."""
        self.c.execute("create table pacientes (id text primary key not null, nombre texto, apellido1 text, apellido2 text, telefono integer, estado text, comentario text)")
        self.conec.commit()

    def nuevo_paciente(self, array):
        """Agregar un nuevo paciente. Este método se usa desde el botón de agregar de la toolbar de la clase Gestor."""
        consulta = "INSERT INTO pacientes VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.c.execute(consulta, (array[3], array[0], array[1], array[2], array[4], array[5], array[6]))
        self.conec.commit()

    def borrar_paciente(self, id):
        """Borrar un paciente. Este método se usará desde el botón de borrar de la toolbar de la clase Gestor."""
        vid = "'"+ id + "'"
        consulta = "DELETE FROM pacientes WHERE id=" + vid
        self.c.execute(consulta)
        self.conec.commit()

    def modificar_paciente(self, id, array):
        """Modificar un paciente según su DNI desde el botón de modificar en la toolbar de la clase Gestor."""
        consulta = "UPDATE pacientes SET nombre=(?), apellido1=(?), apellido2=(?), telefono=(?), estado=(?), comentario=(?) where id=(?)"
        self.c.execute(consulta, (array[0], array[1], array[2], array[3], array[4], array[5], id))
        self.conec.commit()

    def buscar_paciente(self, id):
        """Buscar un sólo paciente según su DNI. Este método se usará desde el botón de modificar de la toolbar de la clase Gestor."""
        vid = "'"+ id + "'"
        consulta = "SELECT * FROM pacientes WHERE id =" + vid
        self.c.execute(consulta)
        return list(self.c)


    def ver_pacientes(self):
        """Ver todos los pacientes que tenemos en la tabla. Es el método que vuelca los datos al treeview de nuestra clase Gestor
        y con el que generamos la tabla con el objeto canvas (reportlab) en la clase Historial."""
        consulta = "SELECT * FROM pacientes"
        self.c.execute(consulta);
        return list(self.c)

    def aceptar_licencia(self, user):
        """Método para aceptar por primera vez la licencia de uso. Se usa en el botón de Licencia.py."""
        user = "'" + user + "'"
        consulta = "UPDATE license SET license = 1 WHERE user =" + user
        self.c.execute(consulta)
        self.conec.commit()

    def estado_licencia(self, user):
        """Verifica, en la clase Log.py, si el user ha aceptado previamente las cláusulas de licencia."""
        user = "'" + user + "'"
        consulta = "SELECT license FROM license WHERE user=" + user
        self.c.execute(consulta)
        for ele in self.c:
            if 0 in ele:
                return False
            else:
                return True

    def  verificar_user(self, user, passwd):
        """Verifica si el user es un usuario registrado en la base de datos."""
        user = "'" + user + "'"
        passwd = "'" + passwd + "'"
        consulta = "SELECT COUNT(*) FROM user WHERE user =" +user + "AND passwd=" + passwd
        self.c.execute(consulta)
        for ele in self.c:
            if 0 in ele:
                return False
            else:
                return True


