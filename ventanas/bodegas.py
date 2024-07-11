import mysql.connector 
import tkinter as tk
from tkinter import ttk, messagebox

class VentanaBodegas(tk.Toplevel):
    def __init__(self, parent, db, id_usuario):
        super().__init__(parent)
        self.title("Gestión de Bodegas")
        self.geometry("800x400")
        self.db = db
        self.id_usuario = id_usuario
        self.frame_lista = None 

        self.crear_botones()
        self.listar_bodegas() 

    def crear_botones(self):
        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Crear Bodega", command=self.mostrar_crear_bodega).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Eliminar Bodega", command=self.eliminar_bodega).pack(side=tk.LEFT, padx=5)
        # tk.Button(frame_botones, text="Actualizar Lista", command=self.actualizar_lista).pack(side=tk.LEFT, padx=5)

    def crear_lista_bodegas(self):
        frame_lista = tk.Frame(self)
        frame_lista.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_bodegas = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, width=70)
        self.listbox_bodegas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox_bodegas.yview)

        self.listbox_bodegas.insert(tk.END, "ID\t\tNombre")

        self.listar_bodegas()
           
    def listar_bodegas(self):
        if self.frame_lista is None:
            self.frame_lista = tk.Frame(self)
            self.frame_lista.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

            self.scrollbar = ttk.Scrollbar(self.frame_lista)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.listbox_bodegas = tk.Listbox(self.frame_lista, yscrollcommand=self.scrollbar.set, width=70)
            self.listbox_bodegas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.scrollbar.config(command=self.listbox_bodegas.yview)

            self.listbox_bodegas.insert(tk.END, "ID\t│\tNombre\t│\tID Perfil\t│\tNombre Trabajador")
            
        self.listbox_bodegas.delete(1, tk.END)

        try:
            query = "SELECT b.ID_BODEGA, b.NOMBRE_BODEGA, b.ID_PERFIL, p.NOMBRE_TRABAJADOR FROM BODEGAS b JOIN PERFILES p ON b.ID_PERFIL = p.ID_PERFIL"
            self.db.cursor.execute(query)
            bodegas = self.db.cursor.fetchall()

            for bodega in bodegas:
                self.listbox_bodegas.insert(tk.END, f"{bodega[0]}\t│\t{bodega[1]}\t│\t{bodega[2]}\t│\t{bodega[3]}")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener bodegas: {err}")
          
    def mostrar_crear_bodega(self):
        for widget in self.winfo_children():
            if widget not in (self.frame_lista,):
                widget.destroy()

        tk.Label(self, text="Crear Nueva Bodega").pack(pady=10)

        tk.Label(self, text="Nombre Bodega:").pack()
        self.entry_nombre_bodega = tk.Entry(self)
        self.entry_nombre_bodega.pack()

        query_trabajador = "SELECT NOMBRE_TRABAJADOR FROM PERFILES WHERE ID_PERFIL = %s"
        self.db.cursor.execute(query_trabajador, (self.id_usuario,))
        nombre_trabajador = self.db.cursor.fetchone()[0]

        tk.Label(self, text=f"Creador: {nombre_trabajador}").pack()
        
        tk.Button(self, text="Guardar Bodega", command=self.crear_bodega).pack(pady=10)
                
    def volver_a_lista_bodegas(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.crear_botones()
        self.listar_bodegas()
    
    def crear_bodega(self):
        nombre_bodega = self.entry_nombre_bodega.get()

        if not nombre_bodega:
            messagebox.showerror("Error", "El nombre de la bodega no puede estar vacío.")
            return

        try:
            query_verificar = "SELECT * FROM BODEGAS WHERE NOMBRE_BODEGA = %s"
            self.db.cursor.execute(query_verificar, (nombre_bodega,))
            if self.db.cursor.fetchone():
                raise ValueError("El nombre de la bodega ya existe.")

            query = "INSERT INTO BODEGAS (NOMBRE_BODEGA, ID_PERFIL) VALUES (%s, %s)"
            self.db.cursor.execute(query, (nombre_bodega, self.id_usuario))
            self.db.conn.commit()
            messagebox.showinfo("Éxito", "Bodega creada con éxito")
            self.listar_bodegas()
        except (mysql.connector.Error, ValueError) as err:
            messagebox.showerror("Error", f"Error al crear bodega: {err}")

    def eliminar_bodega(self):
        try:
            seleccion = self.listbox_bodegas.curselection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Selecciona una bodega para eliminar.")
                return

            id_bodega = self.listbox_bodegas.get(seleccion[0]).split()[0] 

            confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar la bodega con ID {id_bodega}?")
            if not confirmar:
                return

            query = "DELETE FROM BODEGAS WHERE ID_BODEGA = %s"
            self.db.cursor.execute(query, (id_bodega,))
            self.db.conn.commit()

            self.listar_bodegas()

            messagebox.showinfo("Éxito", f"Bodega con ID {id_bodega} eliminada con éxito.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al eliminar bodega: {err}")

    def actualizar_lista(self):
        self.listar_bodegas()
