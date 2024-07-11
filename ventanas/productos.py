import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

class VentanaProductos(tk.Toplevel):
    def __init__(self, parent, db, id_usuario):
        super().__init__(parent)
        self.title("Gestión de Productos")
        self.geometry("1100x400") 
        self.db = db
        self.id_usuario = id_usuario
        self.frame_lista = None

        self.crear_widgets()

    def crear_widgets(self):
        self.frame_lista = tk.Frame(self)
        self.frame_lista.grid(row=0, column=0, pady=(20, 0), padx=20, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.frame_lista)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.listbox_productos = tk.Listbox(self.frame_lista, yscrollcommand=scrollbar.set, width=100)
        self.listbox_productos.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=self.listbox_productos.yview)

        self.listbox_productos.insert(tk.END, "ID\t│\tNombre\t│\tDescripción\t│\tTipo\t│\tBodega\t│\tEditorial\t│\tAutor\t│\tCantidad")

        self.gestor_productos()

        frame_botones = tk.Frame(self)
        frame_botones.grid(row=1, column=0, pady=(0, 20), padx=20, sticky="w")
        tk.Button(frame_botones, text="Eliminar Producto", command=self.eliminar_producto).pack(side=tk.LEFT, padx=5)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def gestor_productos(self):
        self.listbox_productos.delete(1, tk.END)
        
        try:
            query = """
                SELECT p.ID_PRODUCTO, p.NOMBRE_PRODUCTO, p.DESCRIPCION, p.TIPO_PRODUCTO, 
                    b.NOMBRE_BODEGA, e.NOMBRE_EDITORIAL, 
                    CONCAT(a.NOMBRE_AUTOR, ' ', a.APELLIDO_AUTOR) AS NOMBRE_COMPLETO_AUTOR, 
                    i.CANTIDAD
                FROM PRODUCTOS p
                JOIN BODEGAS b ON p.ID_BODEGA = b.ID_BODEGA
                LEFT JOIN EDITORIALES e ON p.ID_EDITORIAL = e.ID_EDITORIAL
                LEFT JOIN AUTORES a ON p.ID_AUTOR = a.ID_AUTOR
                JOIN INVENTARIO i ON p.ID_PRODUCTO = i.ID_PRODUCTO
            """
            self.db.cursor.execute(query)

            productos_vistos = set()          
            
            for producto in self.db.cursor.fetchall():
                if producto[0] not in productos_vistos:
                    self.listbox_productos.insert(tk.END, "\t│\t".join(map(str, producto)))
                    productos_vistos.add(producto[0]) 
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener productos: {err}")

    # ----------------------------------------------------------------------------------------------------------

        frame_formulario = tk.Frame(self)
        frame_formulario.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        tk.Label(frame_formulario, text="Crear Nuevo Producto", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="w")
        
        tk.Label(self, text="Nombre:").grid(row=1, column=0, sticky="e", padx=(0, 10))
        self.entry_nombre = tk.Entry(self, width=30)
        self.entry_nombre.grid(row=1, column=1, sticky="w", padx=(10, 0))

        tk.Label(self, text="Descripción:").grid(row=2, column=0, sticky="e", padx=(0, 10))
        self.entry_descripcion = tk.Entry(self, width=30)
        self.entry_descripcion.grid(row=2, column=1, sticky="w", padx=(10, 0))

        tk.Label(self, text="Tipo:").grid(row=3, column=0, sticky="e", padx=(0, 10))
        self.tipo_producto_var = tk.StringVar(value="LIBRO")
        opciones_tipo = ["LIBRO", "REVISTA", "ENCICLOPEDIA"]
        ttk.Combobox(self, textvariable=self.tipo_producto_var, values=opciones_tipo).grid(row=3, column=1, sticky="w", padx=(10, 0))

        tk.Label(self, text="Bodega:").grid(row=4, column=0, sticky="e", padx=(0, 10))
        self.combobox_bodega = ttk.Combobox(self, width=25)
        self.cargar_bodegas()
        self.combobox_bodega.grid(row=4, column=1, sticky="w", padx=(10, 0))

        tk.Label(self, text="Editorial:").grid(row=5, column=0, sticky="e", padx=(0, 10))
        self.combobox_editorial = ttk.Combobox(self, width=25)
        self.cargar_editoriales()
        self.combobox_editorial.grid(row=5, column=1, sticky="w", padx=(10, 0))

        tk.Label(self, text="Autor:").grid(row=6, column=0, sticky="e", padx=(0, 10))
        self.combobox_autor = ttk.Combobox(self, width=25)
        self.cargar_autores()
        self.combobox_autor.grid(row=6, column=1, sticky="w", padx=(10, 0))

        tk.Label(self, text="Cantidad:").grid(row=7, column=0, sticky="e", padx=(0, 10))
        self.entry_cantidad = tk.Entry(self, width=30)
        self.entry_cantidad.grid(row=7, column=1, sticky="w", padx=(10, 0))

        tk.Button(frame_formulario, text="Guardar Producto", command=self.crear_producto).grid(row=8, column=0, columnspan=2, pady=(0, 10), sticky="ew")        
        
        for i in range(10):
            self.rowconfigure(i, weight=1)
        frame_formulario.rowconfigure(8, weight=0)
        for i in range(2): 
            self.columnconfigure(i, weight=1)
    
    def cargar_bodegas(self):
        try:
            query = "SELECT ID_BODEGA, NOMBRE_BODEGA FROM BODEGAS"
            self.db.cursor.execute(query)
            bodegas = self.db.cursor.fetchall()
            self.combobox_bodega['values'] = [f"{bodega[0]} - {bodega[1]}" for bodega in bodegas]
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar bodegas: {err}")

    def cargar_editoriales(self):
        try:
            query = "SELECT ID_EDITORIAL, NOMBRE_EDITORIAL FROM EDITORIALES"
            self.db.cursor.execute(query)
            editoriales = self.db.cursor.fetchall()
            self.combobox_editorial['values'] = [f"{editorial[0]} - {editorial[1]}" for editorial in editoriales]
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar editoriales: {err}")

    def cargar_autores(self):
        try:
            query = "SELECT ID_AUTOR, NOMBRE_AUTOR FROM AUTORES"
            self.db.cursor.execute(query)
            autores = self.db.cursor.fetchall()
            self.combobox_autor['values'] = [f"{autor[0]} - {autor[1]}" for autor in autores]
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar autores: {err}")

    def crear_producto(self):
        nombre = self.entry_nombre.get()
        descripcion = self.entry_descripcion.get()
        tipo_producto = self.tipo_producto_var.get()
        id_bodega = self.combobox_bodega.get()

        if not id_bodega:
            messagebox.showerror("Error", "Debes seleccionar una bodega.")
            return

        id_bodega = int(id_bodega.split(" - ")[0])  

        id_editorial = self.combobox_editorial.get().split(" - ")[0] if self.combobox_editorial.get() else None
        id_autor = self.combobox_autor.get().split(" - ")[0] if self.combobox_autor.get() else None
        cantidad = self.entry_cantidad.get()

        if not nombre or not cantidad:
            messagebox.showerror("Error", "El nombre y la cantidad son obligatorios.")
            return

        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser un número positivo.")
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
            return

        try:
            query_producto = """
                INSERT INTO PRODUCTOS (NOMBRE_PRODUCTO, DESCRIPCION, TIPO_PRODUCTO, ID_EDITORIAL, ID_AUTOR, ID_BODEGA) 
                VALUES (%s, %s, %s, %s, %s, %s)  
            """
            self.db.cursor.execute(query_producto, (nombre, descripcion, tipo_producto, id_editorial, id_autor, id_bodega))     
            id_producto = self.db.cursor.lastrowid 
            
            self.insertar_autor_producto(id_producto, id_autor)

            query_inventario = """
                INSERT INTO INVENTARIO (CANTIDAD, ID_PRODUCTO, ID_BODEGA)
                VALUES (%s, %s, %s)
            """
            self.db.cursor.execute(query_inventario, (cantidad, id_producto, id_bodega))

            self.db.conn.commit()
            messagebox.showinfo("Éxito", "Producto creado con éxito")
            self.gestor_productos() 
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al crear producto: {err}")


    def eliminar_producto(self):
        try:
            seleccion = self.listbox_productos.curselection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Selecciona un producto para eliminar.")
                return

            id_producto = self.listbox_productos.get(seleccion[0]).split()[0]

            confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar el producto con ID {id_producto}?")
            if not confirmar:
                return

            query = "DELETE FROM PRODUCTOS WHERE ID_PRODUCTO = %s"
            self.db.cursor.execute(query, (id_producto,))
            self.db.conn.commit()

            self.listar_productos()
            
            messagebox.showinfo("Éxito", f"Producto con ID {id_producto} eliminado con éxito.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al eliminar producto: {err}")

    def insertar_autor_producto(self, id_producto, id_autor):
        if id_autor:
            try:
                query = """
                    INSERT INTO AUTORES_PRODUCTOS (ID_AUTOR, ID_PRODUCTO)
                    VALUES (%s, %s)
                """
                self.db.cursor.execute(query, (id_autor, id_producto))
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al relacionar autor con producto: {err}")