# -*- coding: utf-8 -*-
from BaseDatos import BaseDatos
from gi.repository import Gtk, Gdk
from Historial import Historial

class Gestor:
    """Clase Gestor en la que almacenaremos y registraremos pacientes y sus estados a lo largo de las consultas."""
    def __init__(self):
        """Constructor sin parámetros que inicializa atributos, y la interfaz del Gestor."""
        #Inicializamos atributos que serán imprescindibles para el gestor, como el objeto de base de datos, treeview,formulario, etc
        self.bdcon = BaseDatos() #Objeto con los métodos sqlite
        self.treeview = Gtk.TreeView()  #Tabla donde veremos los resultados de nuestra base
        self.campos_texto = [] #Array para labels de ficheros .glade
        self.formulario_agregar = Gtk #Empleado para agregar un nuevo paciente
        self.formulario_modificar = Gtk #Empleado para modificar un paciente
        self.formulario_buscar = Gtk #Empleado para buscar un paciente
        self.dni = Gtk #Atributo dni, necesario para pasarlo en algunos métodos al objeto bdcon
        self.ventana = Gtk #Atributo ventana para cuando pulsas el botón de ayuda en la toolbar
        self.hijo = None
        self.aux = []
        self.todo_ok = bool
        self.builderAgregarPaciente = None


        #Creamos la ventana principal y otros componentes
        self.ventana = Gtk.Window()
        self.ventana.connect("delete-event", Gtk.main_quit)
        self.ventana.set_resizable(False)
        self.ventana.set_title("AdminMySurgeries v0.1")
        self.ventana.set_icon_from_file("../img/default-icon.jpg")


        #Creamos una caja para crear un layout general de todo el contenido d la imagen.
        self.layout =  Gtk.VBox()
        self.ventana.add(self.layout)

        #Imagen decorativa en forma de banner.
        self.banner = Gtk.Image()
        self.banner.set_from_file("../img/top.jpg")
        self.layout.pack_start(self.banner, True, True, 0)

        #añadimos un panel como segundo elemento de la caja vertical. Me interesa que sea un panel, al tener dos unidades (derecha e izquierda) independientes.
        #En el panel, añadiremos, a la derecha, el treeview, y a la izquierda, un toolbar con los botones de edición del treeview.
        self.panel = Gtk.Paned()
        self.layout.add(self.panel)


        #Creamos un label al modo de footer y lo alineamos a la derecha.
        self.label = Gtk.Label("AdminMySurgeries v0.1 by David Diz Oya")
        self.label.set_alignment(Gtk.Align.END, 0)
        self.layout.add(self.label)

        #Añadimos una imagen final.
        self.bot_banner = Gtk.Image()
        self.bot_banner.set_from_file("../img/bot.jpg")
        self.bot_banner.set_from_file("../img/bot.jpg")
        self.layout.pack_end(self.bot_banner, True, True, 0)

        #Creamos un segundo layout de tipo caja y lo añadimos al lado iqzuierdo del panel. Necesito al menos 2 columnas en esa parte del panel, y por eso añado esta caja.
        #La primera columna sería para el toolbar, y la segunda para los formularios que saldrán y se esconderán cargados desde ficheros .glade
        self.layout2 = Gtk.Box()
        self.panel.pack1(self.layout2)

        #Creamos el toolbar, vertical, y lo añadimos
        self.toolbar = Gtk.Toolbar()
        self.toolbar.set_orientation(Gtk.Orientation.VERTICAL)
        self.layout2.pack_start(self.toolbar, True, True, 0)

        #Agregamos una serie de botones, con imágenes predeterminadas, y los añadimos al toolbar.
        self.agregar = Gtk.ToolButton(Gtk.STOCK_ADD, label="Añadir")
        self.toolbar.insert(self.agregar, 0)

        self.borrar = Gtk.ToolButton(Gtk.STOCK_DELETE, label="Borrar")
        self.toolbar.insert(self.borrar, 1)

        self.buscar = Gtk.ToolButton(Gtk.STOCK_FIND, label="Buscar")
        self.toolbar.insert(self.buscar, 2)

        self.modificar = Gtk.ToolButton(Gtk.STOCK_EDIT, label="Modificar")
        self.toolbar.insert(self.modificar, 3)

        self.help = Gtk.ToolButton(Gtk.STOCK_HELP, label="Ayuda")
        self.toolbar.insert(self.help, 4)

        self.historial = Gtk.ToolButton(Gtk.STOCK_SAVE, label="Historial")
        self.toolbar.insert(self.historial, 5)

        #Creamos dos scrollwindows.

        #El primer ScrolledWindow será para la segunda columna de la caja contenida en la parte izquierda del panel (Sí, complicado, leelo a despacio)
        self.scroll1 = Gtk.ScrolledWindow()
        self.scroll1.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.layout2.pack_end(self.scroll1, True, True, 0)

        #Este segundo scroll irá en el lado derecho del panel, conteniendo el treeview.
        self.scroll2 = Gtk.ScrolledWindow()
        self.scroll2.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.panel.add2(self.scroll2)
        self.scroll2.add(self.treeview)

        #Cargamos el treeview ya desde el inicio de ejecución del programa.
        self.cargar_treeview()

        #Asignamos los eventos correspondientes a los botones del Toolbar de la izquierda
        self.agregar.connect("clicked", self.nuevo_paciente)
        self.borrar.connect("clicked", self.borrar_paciente)
        self.modificar.connect("clicked", self.modificar_paciente)
        self.buscar.connect("clicked", self.buscar_paciente)
        self.help.connect("clicked", self.ayuda)
        self.historial.connect("clicked", self.generar_pdf)


        self.ventana.show_all()

    #Cargamos desde un fichero glade un modelo para buscar, identificamos sus objetos, le asignamos el panel en el que se muestra, y le conectamos los eventos correspondientes.
    def nuevo_paciente(self, widget):
	"""Carga el fichero .glade (XML) en el gestor. Agrega todos los Gtk.Entry en un array para ir usando los datos en la inserción en la base de datos."""
        if self.hijo:
            self.hijo.destroy()
            self.hijo = None
            del self.campos_texto[:]
            del self.aux[:]
            self.recargar_pacientes()

        builder = Gtk.Builder()
        builder.add_from_file("../glade/agregar_paciente.glade")
        self.formulario_agregar = builder.get_object("vp1")
        self.hijo = self.formulario_agregar
        aplicar_cambios = builder.get_object("apply")

        for i in range(7): #Añadimos los 7 labels que tiene el fichero glade en un array de objetos para su posterior uso a la hora de pasarle los textos por parámetro al objeto de la base de datos.
            label = builder.get_object(str(i))
            self.campos_texto.append(label)

        self.scroll1.add(self.formulario_agregar)
        signal ={"on_apply_clicked":self.on_apply_clicked}
        builder.connect_signals(signal)


    def on_apply_clicked(self, widget):
	"""Evento para el botón del formulario de nuevo paciente. Verifica que los datos están bien. Si es así, hace la inserción. En caso de clave repetida, lo notifica."""
        self.verificar_datos_introducidos()
        if self.todo_ok:
            try:
                for obj in self.campos_texto:
                    self.aux.append(obj.get_text())
                self.bdcon.nuevo_paciente(self.aux)
                self.recargar_pacientes()
                self.formulario_agregar.destroy()
                del self.campos_texto [:]
                del self.aux [:]
            except self.bdcon.conec.IntegrityError:
                self.emergente("La clave ya existe en la base de datos.")
                del self.aux[:]
                self.todo_ok = False
                pass

    def borrar_paciente(self, widget):
	"""Borra un paciente de la base de datos haciendo clic previamente sobre él. Se eliminará en la base por su clave primaria (campo DNI)."""
        selection = self.treeview.get_selection() #Obtenemos el objeto seleccionador que analiza las selecciones
        model, treeiter = selection.get_selected() #Mediante el objeto seleccionador, obtenemos la fila seleccionada
        if treeiter != None: #Si hay una fila seleccionada, cogemos su DNI(clave primaria) que ocupa la posición 0, y lo borramos de la BD.
            self.dni = model[treeiter][0]
            self.bdcon.borrar_paciente(self.dni)
            self.recargar_pacientes() #Refresh del contenido del treeview

				
				
    #Cargamos desde un fichero glade un modelo para buscar, identificamos sus objetos, le asignamos el panel en el que se muestra, y le conectamos los eventos correspondientes.
    #Debemos seleccionar antes la fila a modificar, y se despliega el panel de edición.
    def modificar_paciente(self, widget):
	"""Permite modificar un paciente al que previamente hemos seleccionado. Obteniendo, dentro del TreeView la fila seleccionada, modificaremos por su clave primaria (campoDNI)."""
        if self.hijo:
            self.hijo.destroy()
            self.hijo = None
            del self.campos_texto[:]
            del self.aux[:]

        selection = self.treeview.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter != None:
            self.dni = model[treeiter][0]
            builder = Gtk.Builder()
            builder.add_from_file("../glade/modificar_paciente.glade")
            self.formulario_modificar = builder.get_object("vp1")
            self.hijo = self.formulario_modificar
            modificar = builder.get_object("modify")

            for i in range(6): #Añadimos los 6 labels que tiene (No tiene el label DNI)
                label = builder.get_object(str(i))
                self.campos_texto.append(label)
            print (self.campos_texto)

            self.scroll1.add(self.formulario_modificar)
            signal ={"on_modify_clicked":self.on_modify_clicked}
            builder.connect_signals(signal)

    #Evento del botón del formulario de edición del paciente. Cuando se ejecuta la edición, acaba eliminándose a sí mismo, dejando el panel donde estaba libre de nuevo.
    def on_modify_clicked(self, widget):
	"""Evento de botón llamado una vez se aplica el botón de aplicar cambios en la modificación. Se registran los nuevos cambios en un array auxiliar que emplearemos para actualizar los datos."""
        for texto in self.campos_texto:
            self.aux.append(texto.get_text())

        self.bdcon.modificar_paciente(self.dni, self.aux)
        self.recargar_pacientes()
        self.formulario_modificar.destroy()
       # del self.campos_texto[:]
        del self.aux[:]

    #Cargamos desde un fichero glade un modelo para buscar, identificamos sus objetos, le asignamos el panel en el que se muestra, y le conectamos los eventos correspondientes.
    def buscar_paciente(self, widget):
	"""Buscamos un paciente por su clave primaria. Simplemente obtendremos una fila concreta. El formulario se carga desde un .glade (formato XML)"""
        if self.hijo:
            self.hijo.destroy()
            self.hijo = None

        builder = Gtk.Builder()
        builder.add_from_file("../glade/buscar_paciente.glade")
        self.formulario_buscar = builder.get_object("vp1")
        self.hijo = self.formulario_buscar
        find = builder.get_object("find")
        back = builder.get_object("back")

        label = builder.get_object("0")
        self.campos_texto.append(label)
        print (self.campos_texto)

        self.scroll1.add(self.formulario_buscar)
        signal ={"on_find_clicked": self.on_find_clicked,
                 "on_back_clicked": self.on_back_clicked}
        builder.connect_signals(signal)

    
    def on_find_clicked(self, widget):
	"""Evento del botón del formulario de búsqueda del paciente por su clave primaria."""
        self.model.clear() #Limpiamos la lista para meterle nuevos datos a posteriori.
        for i in self.campos_texto: #Recorremos el array en busca del dni, aunque en este caso solo tenemos un label guardado en el array
            self.dni = i.get_text()
        datos = self.bdcon.buscar_paciente(self.dni) #Hacemos la consulta con el dni obtenido
        for fila in datos: #Le metemos los datos en la lista modelo
            self.model.append(fila)

        self.treeview.set_model(self.model) #Volvemos a cargar la lista.
        del self.campos_texto [:] #Vaciamos el array que contiene labels del .glade por si necesitamos usar el array en otro sitio

    #Evento del botón del formulario de búsqueda del paciente. Cuando se ejecuta, vuelve a recargar a todos los pacientes y acaba eliminándose a sí mismo, dejando el panel donde estaba libre de nuevo.
    def on_back_clicked(self, widget):
	"""Vuelve a atrás, a la vista general."""
        self.recargar_pacientes()
        self.formulario_buscar.destroy()

    def ayuda(self, widget):
	"""Cargamos desde un fichero .glade una ventana emergente que explica sobre el funcionamiento de los botones de la toolbar."""
        builder = Gtk.Builder()
        builder.add_from_file("../glade/ayuda.glade")
        ventana = builder.get_object("dialog1")
        ventana.show()

    def generar_pdf(self, widget):
	"""Genera un PDF a modo de historial de los pacientes que tenemos registrados en nuestra base de datos."""
        Historial().generar_pdf()
        self.emergente("PDF generado.")

    #Cargamos el treeview por primera vez, y le asignamos un panel en el que se muestra, y el modelo predeterminado.
    def cargar_treeview(self):
	"""Cargamos todos los pacientes en un Gtk.TreeView para poder ver claramente el contenido de nuestra base de datos."""
        datos = self.bdcon.ver_pacientes() #Datos de la base
        self.model = Gtk.ListStore(str, str, str, str, int, str, str) #Modelo de lista, según el tipo de columnas
        for fila in datos: #Añadimos datos a la lista.
            self.model.append(fila)

        self.treeview.set_model(self.model) #Le asignamos el modelo al treeview

        for i, column_title in enumerate(["DNI", "Nombre", "Primer apellido", "Segundo apellido", "Teléfono", "Estado", "Comentario"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i) #Renderizamos cada columna con los datos, para que se muestren correctamente con su correspondiente título y texto
            self.treeview.append_column(column)

   
    def recargar_pacientes(self):
	"""Método que para recarga los datos que veremos en el Treeview constantemente. Se aplica automáticamente en cada botón del toolbar al final de su ejecución para refrescar el contenido."""
        self.model.clear() #Tenemos que usar clear para vaciar el contenido del modelo y volver a llenarlo de datos de la base de datos.
        datos = self.bdcon.ver_pacientes() #Consultamos todo lo que hay en la base de datos.
        for fila in datos: #Lo añadimos al modelo.
            self.model.append(fila)

        self.treeview.set_model(self.model) #Lo agregamos al treeview.


    def verificar_datos_introducidos(self): #Verificamos los datos introducidos en la plantilla de nuevo cliente.
	"""Método que se llama automáticamente cuando se pulsa el botón de agregar un nuevo usuario a la base de datos. Se verifica campo a campo los datos introducidos, y se comprueba que todo está en orden."""
        for contador, obj in enumerate(self.campos_texto): #En el array campos_texto tengo almacenados todos los labels GTK que el user ha rellenado
            self.verificar_campos(obj, contador)


   
    def verificar_campos(self, campo = Gtk.Entry, pos=int):
	"""Método llamado por verificar_datos_introducidos. Campo a campo revisa los datos introducidos. Comprueba la longitud del teléfono y el contenido del teléfono, y la longitud del DNI."""
        texto = campo.get_text() #Cogemos el texto
        if pos == 3:
            if len(texto) == 9:
                self.todo_ok = True
            else:
                self.emergente("DNI inválido. No tiene una longitud de 9 caracteres.")
                self.todo_ok = False
        elif pos == 4:
            if texto.isdigit():
                if len(texto) == 9:
                    self.todo_ok = True
                else:
                    self.todo_ok = False
                    self.emergente("Número de teléfono no válido. Debe tener 9 caracteres. ")
            else:
                self.todo_ok = False
                self.emergente("Número de teléfono no válido. No es numérico. ")


    def emergente(self, mensaje): #Ventana emergente de error.
	"""Ventana emergente que se usa de forma recursiva a medida que se necesite interactuar con el usuario."""
        vent_emergente = Gtk.Window(title = "Error")
        vent_emergente.set_size_request(500,100)
        vent_emergente.set_resizable(False)

        img = Gtk.Image()
        img.set_from_file("../img/error.jpg")

        caja = Gtk.Box()
        label = Gtk.Label() #Mensaje de error a mostrar
        label.set_text("    " + mensaje)

        vent_emergente.add(caja)

        caja.add(img)
        caja.add(label)

        vent_emergente.connect("delete-event", self.eliminarWidget)
        vent_emergente.show_all()

    #Para eliminar diferentes widgets desde eventos
    def eliminarWidget(self, widget):
	"""Método recursivo para autodestruir ventanas enteras."""
        widget.destroy()



