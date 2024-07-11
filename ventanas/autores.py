import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

class VentanaAutores(tk.Toplevel):
    def __init__(self, parent, db, id_usuario):
        super().__init__(parent)
        self.title("Gestión de Autores")
        self.geometry("800x400")
        self.db = db
        self.id_usuario = id_usuario
        self.frame_lista = None
        
        self.listar_autores()
        self.crear_botones()

    def crear_botones(self):
        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Crear autor", command=self.mostrar_crear_autor).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Eliminar autor", command=self.eliminar_autor).pack(side=tk.LEFT, padx=5)
        # tk.Button(frame_botones, text="Actualizar Lista", command=self.actualizar_lista).pack(side=tk.LEFT, padx=5)

    def crear_lista_autores(self):
        frame_lista = tk.Frame(self)
        frame_lista.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_autores = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, width=70)
        self.listbox_autores.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox_autores.yview)

        self.listbox_autores.insert(tk.END, "ID\t\tNombre")

        self.listar_autores()

    def listar_autores(self):
        if self.frame_lista is None:
            self.frame_lista = tk.Frame(self)
            self.frame_lista.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

            self.scrollbar = ttk.Scrollbar(self.frame_lista)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.listbox_autores = tk.Listbox(self.frame_lista, yscrollcommand=self.scrollbar.set, width=70)
            self.listbox_autores.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.scrollbar.config(command=self.listbox_autores.yview)

            self.listbox_autores.insert(tk.END, "ID\t│\tNombre\t│\tApellido\t│\tPaís")
        
        self.listbox_autores.delete(1, tk.END)

        try:
            query = "SELECT ID_AUTOR, NOMBRE_AUTOR, APELLIDO_AUTOR, PAIS_AUTOR FROM AUTORES"
            self.db.cursor.execute(query)
            autores = self.db.cursor.fetchall()

            for autor in autores:
                self.listbox_autores.insert(tk.END, f"{autor[0]}\t│\t{autor[1]}\t│\t{autor[2]}\t│\t{autor[3]}") 
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener autores: {err}")

    def mostrar_crear_autor(self): 
        for widget in self.winfo_children():
            if widget != self.frame_lista:
                widget.destroy()

        tk.Label(self, text="Crear Nuevo Autor").pack(pady=10)

        tk.Label(self, text="Nombre:").pack()
        self.entry_nombre_autor = tk.Entry(self)
        self.entry_nombre_autor.pack()

        tk.Label(self, text="Apellido:").pack()
        self.entry_apellido_autor = tk.Entry(self)
        self.entry_apellido_autor.pack()

        tk.Label(self, text="País:").pack()
        self.entry_pais_autor = tk.Entry(self)
        self.entry_pais_autor.pack()

        tk.Button(self, text="Guardar Autor", command=self.crear_autor).pack(pady=10)
        tk.Button(self, text="Volver", command=self.destroy).pack(pady=5) 

    def volver_a_lista_autores(self):
        for widget in self.winfo_children():
            if widget != self.frame_lista:
                widget.destroy()

        self.frame_lista.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        self.crear_botones()
        self.listar_autores()

    def crear_autor(self):
        nombre = self.entry_nombre_autor.get()
        apellido = self.entry_apellido_autor.get()
        pais = self.entry_pais_autor.get()

        if not nombre:
            messagebox.showerror("Error", "El nombre del autor no puede estar vacío.")
            return

        try:
            query = "INSERT INTO AUTORES (NOMBRE_AUTOR, APELLIDO_AUTOR, PAIS_AUTOR) VALUES (%s, %s, %s)"
            self.db.cursor.execute(query, (nombre, apellido, pais))
            self.db.conn.commit()
            messagebox.showinfo("Éxito", "Autor creado con éxito")
            self.listar_autores() 
            self.mostrar_crear_autor()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al crear autor: {err}")

    def eliminar_autor(self):
        try:
            seleccion = self.listbox_autores.curselection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Selecciona un autor para eliminar.")
                return

            id_autor = self.listbox_autores.get(seleccion[0]).split()[0]

            confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar el autor con ID {id_autor}?")
            if not confirmar:
                return

            query = "DELETE FROM AUTORES WHERE ID_AUTOR = %s"
            self.db.cursor.execute(query, (id_autor,))
            self.db.conn.commit()

            self.listar_autores()

            messagebox.showinfo("Éxito", f"Autor con ID {id_autor} eliminado con éxito.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al eliminar autor: {err}")

    def actualizar_lista(self):
        self.listar_autores()
