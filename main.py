import mysql.connector 
import tkinter as tk
from tkinter import messagebox

from ventanas import bodegas
from ventanas import productos
from ventanas import autores
from ventanas import editoriales
from ventanas import movimientos
from ventanas import informes

class BaseDatos:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="Tito2898@",
            database="EL_GRAN_POETA"
        )
        self.cursor = self.conn.cursor()

    def verificar_conexion(self):
        try:
            self.cursor.execute("SELECT 1")
            result = self.cursor.fetchone()
            if result:
                return True
            else:
                return False
        except mysql.connector.Error as err:
            print(f"Error de conexión: {err}")
            return False
db = BaseDatos() 

try:
    if db.verificar_conexion():
        print("Conexión exitosa a la base de datos")
    else:
        print("Error al conectar a la base de datos") 
except mysql.connector.Error as err:
    print(f"Error de conexión: {err}") 

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("El gran poeta")
        self.geometry("800x400")
        
        self.contenedor_modulos = tk.Frame(self)
        self.contenedor_modulos.pack(fill=tk.BOTH, expand=True)

        self.mostrar_iniciar_sesion()
        
        self.db = None
        self.db = BaseDatos()

    def mostrar_iniciar_sesion(self):
        for widget in self.contenedor_modulos.winfo_children():
            widget.destroy()
            
        mensaje = tk.Label(self.contenedor_modulos, text="¡Bienvenido a El Gran Poeta!", font=("Arial", 16))
        mensaje.grid(row=0, column=0, columnspan=2, pady=(20, 0)) 
            
        label_username = tk.Label(self.contenedor_modulos, text="Nombre de usuario:")
        label_username.grid(row=1, column=0, sticky="e", padx=(0, 10))  
        self.entry_username = tk.Entry(self.contenedor_modulos, width=30)
        self.entry_username.grid(row=1, column=1, sticky="w", padx=(10, 0))  

        label_password = tk.Label(self.contenedor_modulos, text="Contraseña:")
        label_password.grid(row=2, column=0, sticky="e", padx=(0, 10))  
        self.entry_password = tk.Entry(self.contenedor_modulos, show="*", width=30)
        self.entry_password.grid(row=2, column=1, sticky="w", padx=(10, 0))  
        
        button_iniciar_sesion = tk.Button(self.contenedor_modulos, text="Iniciar sesión", command=self.iniciar_sesion)
        button_iniciar_sesion.grid(row=3, column=1, pady=10, sticky="w")
        button_registrar = tk.Button(self.contenedor_modulos, text="Crear Usuario", command=self.mostrar_registro)
        button_registrar.grid(row=3, column=0, pady=10, sticky="e")
        
        for i in range(4):
            self.contenedor_modulos.grid_rowconfigure(i, weight=2)
            self.contenedor_modulos.grid_columnconfigure(0, weight=1)
            self.contenedor_modulos.grid_columnconfigure(1, weight=1)   
        
    def mostrar_registro(self):
        for widget in self.contenedor_modulos.winfo_children():
            widget.destroy()
            
        mensaje = tk.Label(self.contenedor_modulos, text="Registrar nuevo usuario", font=("Arial", 12))
        mensaje.grid(row=0, column=0, columnspan=2, pady=(20, 0)) 
            
        label_username = tk.Label(self.contenedor_modulos, text="Nombre del trabajador:")
        label_username.grid(row=1, column=0, sticky="e", padx=(0, 10))  
        self.entry_nombre_trabajador = tk.Entry(self.contenedor_modulos, width=30)
        self.entry_nombre_trabajador.grid(row=1, column=1, sticky="w", padx=(10, 0))  

        label_username = tk.Label(self.contenedor_modulos, text="Nombre de usuario:")
        label_username.grid(row=2, column=0, sticky="e", padx=(0, 10))  
        self.entry_username = tk.Entry(self.contenedor_modulos, width=30)
        self.entry_username.grid(row=2, column=1, sticky="w", padx=(10, 0))  
        
        label_password = tk.Label(self.contenedor_modulos, text="Crear contraseña:")
        label_password.grid(row=3, column=0, sticky="e", padx=(0, 10))  
        self.entry_password = tk.Entry(self.contenedor_modulos, show="*", width=30)
        self.entry_password.grid(row=3, column=1, sticky="w", padx=(10, 0))  

        label_perfil = tk.Label(self.contenedor_modulos, text="Perfil:")
        label_perfil.grid(row=4, column=0, pady=10, sticky="e")
        self.var_perfil = tk.StringVar(self.contenedor_modulos)
        self.var_perfil.set("JEFE DE BODEGAS")
        perfil_options = ["JEFE DE BODEGAS", "BODEGUERO"]
        perfil_menu = tk.OptionMenu(self.contenedor_modulos, self.var_perfil, *perfil_options)
        perfil_menu.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        button_registrar = tk.Button(self.contenedor_modulos, text="Atrás", command=self.mostrar_iniciar_sesion)
        button_registrar.grid(row=5, column=0, pady=10, sticky="e")
        button_iniciar_sesion = tk.Button(self.contenedor_modulos, text="Registrar", command=self.registrar)
        button_iniciar_sesion.grid(row=5, column=1, pady=10, sticky="w")
            
        for i in range(4):
            self.contenedor_modulos.grid_rowconfigure(i, weight=2)
            self.contenedor_modulos.grid_columnconfigure(0, weight=1)
            self.contenedor_modulos.grid_columnconfigure(1, weight=1)   
                
    def registrar(self):
        nombre_trabajador = self.entry_nombre_trabajador.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        tipo_perfil = self.var_perfil.get()

        try:
            query_verificar_trabajador = "SELECT * FROM PERFILES WHERE NOMBRE_TRABAJADOR = %s"
            self.db.cursor.execute(query_verificar_trabajador, (nombre_trabajador,))
            trabajador_existente = self.db.cursor.fetchone()

            if trabajador_existente:
                messagebox.showerror("Error", "El nombre del trabajador ya está registrado.")
                return

            query_insertar_trabajador = "INSERT INTO PERFILES (NOMBRE_TRABAJADOR, TIPO_PERFIL) VALUES (%s, %s)"
            self.db.cursor.execute(query_insertar_trabajador, (nombre_trabajador, tipo_perfil))
            self.db.conn.commit()

            id_perfil = self.db.cursor.lastrowid

            query_verificar_usuario = "SELECT * FROM USUARIOS WHERE NOMBRE_USUARIO = %s"
            self.db.cursor.execute(query_verificar_usuario, (username,))
            usuario_existente = self.db.cursor.fetchone()

            if usuario_existente:
                messagebox.showerror("Error", "El nombre de usuario ya está en uso.")
                return

            query_insertar_usuario = "INSERT INTO USUARIOS (NOMBRE_USUARIO, CONTRASEÑA, ID_PERFIL) VALUES (%s, %s, %s)"
            self.db.cursor.execute(query_insertar_usuario, (username, password, id_perfil))
            self.db.conn.commit()

            messagebox.showinfo("Registro Exitoso", "Usuario registrado con éxito!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de base de datos", f"Error al registrar usuario: {err}")

    def iniciar_sesion(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        try:
            query = "SELECT * FROM USUARIOS WHERE NOMBRE_USUARIO = %s AND CONTRASEÑA = %s"
            self.db.cursor.execute(query, (username, password))
            usuario = self.db.cursor.fetchone()
            
            if usuario:
                messagebox.showinfo("Inicio de Sesión Exitoso", f"Bienvenido, {username}!")
                self.id_usuario = usuario[0]
                self.tipo_perfil = usuario[3]
                self.nombre_usuario = username  
                self.mostrar_perfil()
            else:
                messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de base de datos", f"Error al iniciar sesión: {err}")

    def mostrar_perfil(self):
        for widget in self.contenedor_modulos.winfo_children():
            widget.destroy()

        try:
            query_trabajador = "SELECT NOMBRE_TRABAJADOR, TIPO_PERFIL FROM PERFILES WHERE ID_PERFIL = %s" 
            self.db.cursor.execute(query_trabajador, (self.tipo_perfil,))
            nombre_trabajador, tipo_perfil = self.db.cursor.fetchone()

            label_nombre = tk.Label(self.contenedor_modulos, text=f"Bienvenido, {nombre_trabajador}!")
            label_nombre.pack(pady=10)

            label_perfil = tk.Label(self.contenedor_modulos, text=f"Perfil: {tipo_perfil}")
            label_perfil.pack(pady=10)

            if tipo_perfil == "JEFE DE BODEGAS":
                self.mostrar_jefebodega()
            elif tipo_perfil == "BODEGUERO":
                self.mostrar_bodeguero()
            else:
                messagebox.showerror("Error", "Tipo de perfil desconocido.")
            
        except (mysql.connector.Error, ValueError) as err:
            messagebox.showerror("Error", f"Error al cargar el perfil: {err}")

        boton_salir = tk.Button(self.contenedor_modulos, text="Salir", command=self.confirmar_cerrar_sesion)
        boton_salir.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)
                
    def confirmar_cerrar_sesion(self):
        confirmacion = messagebox.askyesno("Confirmar cierre de sesión", "¿Confirmar cierre de sesión?")
        if confirmacion:
            self.mostrar_iniciar_sesion()

    def mostrar_jefebodega(self):
        mensaje = tk.Label(self.contenedor_modulos, text="¡Bienvenido, Jefe de Bodega! ¿Qué deseas hacer hoy?", font=("Arial", 12))
        mensaje.pack(pady=10)
        tk.Button(self.contenedor_modulos, text="Gestionar Bodegas", command=self.abrir_ventana_bodegas).pack(pady=5)
        tk.Button(self.contenedor_modulos, text="Gestionar Autores", command=self.abrir_ventana_autores).pack(pady=5)
        tk.Button(self.contenedor_modulos, text="Gestionar Editoriales", command=self.abrir_ventana_editoriales).pack(pady=5)
        tk.Button(self.contenedor_modulos, text="Gestionar Productos", command=self.abrir_ventana_productos).pack(pady=5)
        tk.Button(self.contenedor_modulos, text="Informes", command=self.abrir_ventana_informes).pack(pady=5)

    def abrir_ventana_bodegas(self):
        ventana_bodegas = bodegas.VentanaBodegas(self, self.db, self.id_usuario)
        ventana_bodegas.grab_set()
        
    def abrir_ventana_autores(self):
        ventana_autores = autores.VentanaAutores(self.master, self.db, self.id_usuario)  
        ventana_autores.grab_set()
        
    def abrir_ventana_editoriales(self):
        ventana_editoriales = editoriales.VentanaEditoriales(self, self.db, self.id_usuario)
        ventana_editoriales.grab_set()
        
    def abrir_ventana_productos(self):
        ventana_productos = productos.VentanaProductos(self, self.db, self.id_usuario)
        ventana_productos.grab_set()
    
    def abrir_ventana_informes(self):
        ventana_informes = informes.VentanaInformes(self, self.db, self.id_usuario)
        ventana_informes.grab_set()
        
    def mostrar_bodeguero(self):
        mensaje = tk.Label(self.contenedor_modulos, text="¡Hola, Bodeguero! ¿Qué movimientos necesitas realizar?", font=("Arial", 12))
        mensaje.pack(pady=10)
        tk.Button(self.contenedor_modulos, text="Realizar movimientos", command=self.abrir_ventana_movimientos).pack(pady=5)
      
    def abrir_ventana_movimientos(self):
        ventana_movimientos = movimientos.VentanaMovimientos(self, self.db, self.id_usuario)
        ventana_movimientos.grab_set()
                
ventana_principal = VentanaPrincipal()
ventana_principal.mainloop()