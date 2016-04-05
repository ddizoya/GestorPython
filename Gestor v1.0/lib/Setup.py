# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
 name="Admin My Surgeries",
 version="1.0",
 description="Gestor de pacientes.",
 author="David Diz",
 author_email="ddizoya@danielcastelao.org",
 license="GPL",
 scripts=["Log.py"],
 py_modules=["BaseDatos","Gestor","Licencia","Historial"]
)

#http://mundogeek.net/archivos/2008/09/23/distribuir-aplicaciones-python/

#Comandos usados.
#python Setup.py install
#python Setup.py sdist