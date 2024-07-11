import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

class VentanaInformes(tk.Toplevel):
    def __init__(self, parent, db, id_usuario):
        super().__init__(parent)
        self.title("Informes")
        self.geometry("800x400")
        self.db = db
        self.id_usuario = id_usuario

        tk.Label(self, text="Informes", font=("Arial", 14)).pack(pady=20)

        tk.Button(self, text="Informe de Inventario").pack(pady=5)
        tk.Button(self, text="Informe de Movimientos").pack(pady=5)