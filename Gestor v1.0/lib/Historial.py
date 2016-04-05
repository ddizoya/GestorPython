# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, Image, BaseDocTemplate, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors
import os
import time
import datetime
from BaseDatos import BaseDatos

class Historial:
    """Módulo para la impresión de un PDF de los pacientes de basedatos.bd"""
    def __init__(self):
        """Base sin parámetros usada para inicializar atributos predeterminados"""
        self.bd = BaseDatos()
        self.pacientes = self.bd.ver_pacientes()
        self.elements = []
        self.docName = "Historial pacientes_" + str(datetime.date.today()) +".pdf"
        self.doc = BaseDocTemplate(self.docName, pagesize=A4) #landscape(A4) para Horizontal
        self.canvas = canvas.Canvas(self.docName, pagesize=A4)


    def generar_pdf(self):
        """Genera un PDF automáticamente con la tabla de pacientes, y con una imagen y texto predeterminada, usando Canvas (reportlab)."""
        self.logo = "../img/top.jpg"
        hora = str(time.ctime())
        dia = str(datetime.date.today())
        nombreApp = "Admin My Surgeries V0.1"

        #Agregamos imagen de cabecera
        self.canvas.drawImage(self.logo, 1*cm, 26*cm, 19*cm, 3*cm)

        #Agregamos texto
        self.canvas.setFont('Helvetica', 7)
        text = 'PDF autogenerado a %s, a fecha de %s:' % (hora, dia)
        self.canvas.drawString(2*cm, 25*cm,text)

        text = 'Actualmente estos son los usuarios que se encuentran en la base de datos de %s.' % nombreApp
        self.canvas.drawString(2*cm,24.5*cm,text)

        #Agregamos la tabla al final del documento
        tabla = self.generar_tabla_pacientes()
        tabla.wrapOn(self.canvas, 50, 50)
        tabla.drawOn(self.canvas, 2*cm, 18*cm)
        self.canvas.save()

        os.system(self.docName)


    def generar_tabla_pacientes(self):
        """Retorna un objeto de tipo Tabla (reportlab) con los usuarios de la base de datos BaseDatos."""

        titulos = [["DNI", "NOMBRE","PRIMER APELLIDO", "SEGUNDO APELLIDO", "TElEFONO", "ESTADO", "COMENTARIO"]]

        self.pacientes = titulos + self.pacientes
        tabla = Table(self.pacientes)

        tabla.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 2, colors.white),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('LEFTPADDING', (0, 0), (-1, -1), 3),
                                   ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                                   ('FONTSIZE', (0, 1), (-1, -1), 10),
                                   ('BACKGROUND', (0,1),(-1,-1), colors.lightblue),
                                   ('BACKGROUND', (0, 0), (-1, 0), colors.aliceblue)]))

        return tabla

