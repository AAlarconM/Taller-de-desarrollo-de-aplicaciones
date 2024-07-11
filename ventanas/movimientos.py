import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import pytz

class VentanaMovimientos(tk.Toplevel):
    def __init__(self, parent, db, id_usuario):
        super().__init__(parent)
        self.title("Gestión de Movimientos")
        self.geometry("1000x500")
        self.db = db
        self.id_usuario = id_usuario
        self.frame_lista = None

        self.crear_widgets()

    def crear_widgets(self):
        tk.Button(self, text="Nuevo Movimiento", command=self.mostrar_formulario_movimiento).pack(pady=10)

        self.frame_lista = tk.Frame(self)
        self.frame_lista.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_movimientos = tk.Listbox(self.frame_lista, yscrollcommand=scrollbar.set, width=100)
        self.listbox_movimientos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox_movimientos.yview)

        self.listbox_movimientos.insert(tk.END, "ID Mov.\t│\tFecha\t│\tID Trab.\t│\tNombre Trab.\t│\tTipo\t│\tBodega Origen\t│\tBodega Destino\t│\tCantidad")

        self.listar_movimientos()

    def listar_movimientos(self):
        self.listbox_movimientos.delete(1, tk.END)
        try:
            query = """
                SELECT m.ID_MOVIMIENTO, m.FECHA, m.ID_PERFIL, p.NOMBRE_TRABAJADOR, 
                       bo.NOMBRE_BODEGA AS ORIGEN, bd.NOMBRE_BODEGA AS DESTINO, m.CANTIDAD_EN_MOVIMIENTO
                FROM MOVIMIENTOS m
                JOIN PERFILES p ON m.ID_PERFIL = p.ID_PERFIL
                JOIN BODEGAS bo ON m.ID_BODEGA_ORIGEN = bo.ID_BODEGA
                JOIN BODEGAS bd ON m.ID_BODEGA_DESTINO = bd.ID_BODEGA
            """
            self.db.cursor.execute(query)
            for movimiento in self.db.cursor.fetchall():
                self.listbox_movimientos.insert(tk.END, "\t│\t".join(map(str, movimiento)))
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener movimientos: {err}")

    def mostrar_formulario_movimiento(self):
        ventana_nuevo_movimiento = tk.Toplevel(self)
        ventana_nuevo_movimiento.title("Crear Nuevo Movimiento")

        tk.Label(ventana_nuevo_movimiento, text="Bodega Origen:").grid(row=1, column=0, sticky="w")
        self.combobox_bodega_origen = ttk.Combobox(ventana_nuevo_movimiento)
        self.cargar_bodegas(self.combobox_bodega_origen)
        self.combobox_bodega_origen.grid(row=1, column=1, sticky="ew", padx=5)

        tk.Label(ventana_nuevo_movimiento, text="Producto:").grid(row=2, column=0, sticky="w")
        self.combobox_producto = ttk.Combobox(ventana_nuevo_movimiento)
        self.cargar_productos()
        self.combobox_producto.grid(row=2, column=1, sticky="ew", padx=5)
              
        tk.Label(ventana_nuevo_movimiento, text="Bodega Destino:").grid(row=3, column=0, sticky="w")
        self.combobox_bodega_destino = ttk.Combobox(ventana_nuevo_movimiento)
        self.cargar_bodegas(self.combobox_bodega_destino)
        self.combobox_bodega_destino.grid(row=3, column=1, sticky="ew", padx=5)

        tk.Label(ventana_nuevo_movimiento, text="Cantidad:").grid(row=4, column=0, sticky="w")
        self.entry_cantidad = tk.Entry(ventana_nuevo_movimiento)
        self.entry_cantidad.grid(row=4, column=1, sticky="ew", padx=5)

        tk.Button(ventana_nuevo_movimiento, text="Guardar Movimiento", command=self.crear_movimiento).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(ventana_nuevo_movimiento, text="Volver", command=ventana_nuevo_movimiento.destroy).grid(row=6, column=0, columnspan=2, pady=5)
        
        self.combobox_bodega_origen.bind("<<ComboboxSelected>>", lambda event: self.cargar_productos())
             
    def cargar_bodegas(self, combobox):
        try:
            query = "SELECT ID_BODEGA, NOMBRE_BODEGA FROM BODEGAS"
            self.db.cursor.execute(query)
            bodegas = self.db.cursor.fetchall()
            combobox['values'] = [f"{bodega[0]} - {bodega[1]}" for bodega in bodegas]
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar bodegas: {err}")

    def cargar_productos(self):
        try:
            # Obtener el ID de la bodega de origen seleccionada
            selected_bodega_origen = self.combobox_bodega_origen.get()
            if selected_bodega_origen:
                id_bodega_origen = int(selected_bodega_origen.split(" - ")[0])
                # Consulta SQL para obtener productos de la bodega seleccionada
                query = """
                    SELECT p.ID_PRODUCTO, p.NOMBRE_PRODUCTO 
                    FROM PRODUCTOS p
                    JOIN INVENTARIO i ON p.ID_PRODUCTO = i.ID_PRODUCTO
                    WHERE i.ID_BODEGA = %s AND i.CANTIDAD > 0 
                """
                self.db.cursor.execute(query, (id_bodega_origen,))
                productos = self.db.cursor.fetchall()
                self.combobox_producto['values'] = [f"{producto[0]} - {producto[1]}" for producto in productos]
            else:
                # Si no se ha seleccionado una bodega, limpiar el combobox de productos
                self.combobox_producto['values'] = []
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar productos: {err}")
        
    def crear_movimiento(self):
        tz_chile = pytz.timezone('America/Santiago')
        fecha_hora = datetime.now(tz_chile)
        fecha = fecha_hora.date() 
        
        id_perfil = self.id_usuario
        id_bodega_origen = self.combobox_bodega_origen.get().split(" - ")[0]
        id_bodega_destino = self.combobox_bodega_destino.get().split(" - ")[0]
        id_producto = self.combobox_producto.get().split(" - ")[0]
        cantidad = self.entry_cantidad.get()
        id_inventario = self.obtener_id_inventario(id_producto, id_bodega_origen) 

        try:
            id_inventario_origen = self.obtener_id_inventario(id_producto, id_bodega_origen)

            query_update_origen = """
                UPDATE INVENTARIO
                SET CANTIDAD = CANTIDAD - %s
                WHERE ID_INVENTARIO = %s
            """
            self.db.cursor.execute(query_update_origen, (cantidad, id_inventario_origen))

            id_inventario_destino = self.obtener_id_inventario(id_producto, id_bodega_destino)
            if id_inventario_destino:
                query_update_destino = """
                    UPDATE INVENTARIO
                    SET CANTIDAD = CANTIDAD + %s
                    WHERE ID_INVENTARIO = %s
                """
                self.db.cursor.execute(query_update_destino, (cantidad, id_inventario_destino))
            else:
                query_insert_destino = """
                    INSERT INTO INVENTARIO (CANTIDAD, ID_PRODUCTO, ID_BODEGA)
                    VALUES (%s, %s, %s)
                """
                self.db.cursor.execute(query_insert_destino, (cantidad, id_producto, id_bodega_destino))

            query = """
                INSERT INTO MOVIMIENTOS (FECHA, ID_PERFIL, ID_BODEGA_ORIGEN, ID_BODEGA_DESTINO, ID_PRODUCTO, ID_INVENTARIO, CANTIDAD_EN_MOVIMIENTO)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.db.cursor.execute(query, (fecha_hora, id_perfil, id_bodega_origen, id_bodega_destino, id_producto, id_inventario_origen, cantidad))

            self.db.conn.commit()
            messagebox.showinfo("Éxito", "Movimiento creado con éxito")
            self.listar_movimientos()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al crear movimiento: {err}")
    
    def obtener_id_inventario(self, id_producto, id_bodega):
        try:
            query = """
                SELECT ID_INVENTARIO
                FROM INVENTARIO
                WHERE ID_PRODUCTO = %s AND ID_BODEGA = %s
            """
            self.db.cursor.execute(query, (id_producto, id_bodega))
            resultado = self.db.cursor.fetchone()
            return resultado[0] if resultado else None
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener ID de inventario: {err}")
            return None