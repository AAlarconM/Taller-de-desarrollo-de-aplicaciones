import mysql.connector 
import tkinter as tk
from tkinter import ttk, messagebox

class VentanaEditoriales(tk.Toplevel):
    def __init__(self, parent, db, id_usuario):
        super().__init__(parent)
        self.title("Gestión de Editoriales")
        self.geometry("800x400")
        self.db = db
        self.id_usuario = id_usuario
        self.frame_lista = None 

        self.crear_botones()
        self.listar_editoriales() 

    def crear_botones(self):
        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Crear editorial", command=self.mostrar_crear_editorial).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Eliminar editorial", command=self.eliminar_editorial).pack(side=tk.LEFT, padx=5)
        # tk.Button(frame_botones, text="Actualizar Lista", command=self.actualizar_lista).pack(side=tk.LEFT, padx=5)

    def crear_lista_editoriales(self):
        frame_lista = tk.Frame(self)
        frame_lista.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_editoriales = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, width=70)
        self.listbox_editoriales.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox_editoriales.yview)

        self.listbox_editoriales.insert(tk.END, "ID\t\tNombre")

        self.listar_editoriales()
           
    def listar_editoriales(self):
        if self.frame_lista is None:
            self.frame_lista = tk.Frame(self)
            self.frame_lista.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

            self.scrollbar = ttk.Scrollbar(self.frame_lista)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.listbox_editoriales = tk.Listbox(self.frame_lista, yscrollcommand=self.scrollbar.set, width=70)
            self.listbox_editoriales.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.scrollbar.config(command=self.listbox_editoriales.yview)

            self.listbox_editoriales.insert(tk.END, "ID\t│\tNombre\t│\tPaís")  
            
        self.listbox_editoriales.delete(1, tk.END)

        try:
            query = "SELECT ID_EDITORIAL, NOMBRE_EDITORIAL, PAIS_EDITORIAL FROM EDITORIALES"
            self.db.cursor.execute(query)
            editoriales = self.db.cursor.fetchall()

            for editorial in editoriales:
                self.listbox_editoriales.insert(tk.END, f"{editorial[0]}\t│\t{editorial[1]}\t│\t{editorial[2]}")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener editoriales: {err}")
          
    def mostrar_crear_editorial(self):
        for widget in self.winfo_children():
            if widget != self.frame_lista:
                widget.destroy()

        tk.Label(self, text="Crear Nueva Editorial").pack(pady=10)
        tk.Label(self, text="Nombre:").pack()
        self.entry_nombre_editorial = tk.Entry(self)
        self.entry_nombre_editorial.pack()
        tk.Label(self, text="País:").pack()
        self.entry_pais_editorial = tk.Entry(self)
        self.entry_pais_editorial.pack()

        tk.Button(self, text="Guardar Editorial", command=self.crear_editorial).pack(pady=10)
        # tk.Button(self, text="Volver", command=self.volver_a_lista_editoriales).pack(pady=5) 
                
    def volver_a_lista_editoriales(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.crear_botones()
        self.listar_editoriales()
    
    def crear_editorial(self):
        nombre_editorial = self.entry_nombre_editorial.get()
        pais_editorial = self.entry_pais_editorial.get()  # Obtener el país

        if not nombre_editorial:
            messagebox.showerror("Error", "El nombre de la editorial no puede estar vacío.")
            return

        try:
            query_verificar = "SELECT * FROM EDITORIALES WHERE NOMBRE_EDITORIAL = %s"
            self.db.cursor.execute(query_verificar, (nombre_editorial,))
            if self.db.cursor.fetchone():
                raise ValueError("El nombre de la editorial ya existe.")

            query = "INSERT INTO EDITORIALES (NOMBRE_EDITORIAL, PAIS_EDITORIAL) VALUES (%s, %s)"  # Insertar país
            self.db.cursor.execute(query, (nombre_editorial, pais_editorial))
            self.db.conn.commit()
            messagebox.showinfo("Éxito", "Editorial creada con éxito")
            self.listar_editoriales() 
            self.mostrar_crear_editorial()
        except (mysql.connector.Error, ValueError) as err:
            messagebox.showerror("Error", f"Error al crear editorial: {err}")

    def eliminar_editorial(self):
        try:
            seleccion = self.listbox_editoriales.curselection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Selecciona una editorial para eliminar.")
                return

            id_editorial = self.listbox_editoriales.get(seleccion[0]).split()[0] 

            confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar la editorial con ID {id_editorial}?")
            if not confirmar:
                return

            query = "DELETE FROM editoriales WHERE ID_editorial = %s"
            self.db.cursor.execute(query, (id_editorial,))
            self.db.conn.commit()

            self.listar_editoriales()

            messagebox.showinfo("Éxito", f"editorial con ID {id_editorial} eliminada con éxito.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al eliminar editorial: {err}")

    def actualizar_lista(self):
        self.listar_editoriales()