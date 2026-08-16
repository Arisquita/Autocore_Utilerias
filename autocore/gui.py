import tkinter as tk
from tkinter import messagebox, ttk

from database.connection import crear_tabla_clientes
from modules.clientes import consultar_clientes, editar_cliente, registrar_cliente
from modules.ordenes_servicio import (
    ESTADOS_PERMITIDOS,
    actualizar_estado_orden,
    actualizar_observaciones_orden,
    consultar_ordenes_servicio,
    crear_tabla_ordenes_servicio,
    registrar_orden_servicio,
)
from modules.vehiculos import (
    consultar_vehiculos,
    crear_tabla_vehiculos,
    registrar_vehiculo,
)


class AutoCoreGUI:
    """Interfaz Tkinter que presenta las operaciones existentes de AutoCore."""

    def __init__(self, root):
        self.root = root
        self.root.title("AutoCore - Sistema de Gestión para Taller Mecánico")
        self.root.geometry("1120x720")
        self.root.minsize(960, 620)

        self._configurar_estilos()
        self._inicializar_base_datos()
        self._crear_encabezado()
        self._crear_pestanas()

        self.consultar_clientes_gui()
        self.consultar_vehiculos_gui()
        self.consultar_ordenes_gui()

    def _configurar_estilos(self):
        estilo = ttk.Style(self.root)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")

        estilo.configure("TNotebook", background="#eef2f5", borderwidth=0)
        estilo.configure(
            "TNotebook.Tab", padding=(18, 10), font=("Segoe UI", 10, "bold")
        )
        estilo.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        estilo.configure("Subtitle.TLabel", font=("Segoe UI", 10))
        estilo.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"))
        estilo.configure("Treeview", rowheight=26, font=("Segoe UI", 9))
        estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    @staticmethod
    def _inicializar_base_datos():
        crear_tabla_clientes()
        crear_tabla_vehiculos()
        crear_tabla_ordenes_servicio()

    def _crear_encabezado(self):
        encabezado = ttk.Frame(self.root, padding=(24, 18, 24, 10))
        encabezado.pack(fill="x")
        ttk.Label(encabezado, text="AutoCore", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            encabezado,
            text="Sistema de Gestión para Taller Mecánico",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(2, 0))

    def _crear_pestanas(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tab_clientes = ttk.Frame(self.notebook, padding=16)
        self.tab_vehiculos = ttk.Frame(self.notebook, padding=16)
        self.tab_ordenes = ttk.Frame(self.notebook, padding=16)

        self.notebook.add(self.tab_clientes, text="CLIENTES")
        self.notebook.add(self.tab_vehiculos, text="VEHÍCULOS")
        self.notebook.add(self.tab_ordenes, text="ÓRDENES DE SERVICIO")

        self._crear_seccion_clientes()
        self._crear_seccion_vehiculos()
        self._crear_seccion_ordenes()

    @staticmethod
    def _agregar_campo(contenedor, fila, texto, variable, ancho=28):
        ttk.Label(contenedor, text=texto).grid(
            row=fila, column=0, sticky="w", padx=(0, 8), pady=4
        )
        entrada = ttk.Entry(contenedor, textvariable=variable, width=ancho)
        entrada.grid(row=fila, column=1, sticky="ew", pady=4)
        return entrada

    @staticmethod
    def _crear_treeview(contenedor, columnas, encabezados, anchos):
        marco = ttk.Frame(contenedor)
        marco.pack(fill="both", expand=True)

        tabla = ttk.Treeview(marco, columns=columnas, show="headings")
        barra_y = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
        barra_x = ttk.Scrollbar(marco, orient="horizontal", command=tabla.xview)
        tabla.configure(yscrollcommand=barra_y.set, xscrollcommand=barra_x.set)

        for columna, encabezado, ancho in zip(columnas, encabezados, anchos):
            tabla.heading(columna, text=encabezado)
            tabla.column(columna, width=ancho, minwidth=60, anchor="w")

        tabla.grid(row=0, column=0, sticky="nsew")
        barra_y.grid(row=0, column=1, sticky="ns")
        barra_x.grid(row=1, column=0, sticky="ew")
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)
        return tabla

    @staticmethod
    def _reemplazar_filas(tabla, filas):
        tabla.delete(*tabla.get_children())
        for fila in filas:
            tabla.insert("", "end", values=tuple("" if v is None else v for v in fila))

    @staticmethod
    def _limpiar_variables(*variables):
        for variable in variables:
            variable.set("")

    @staticmethod
    def _mostrar_resultado(resultado, al_completar=None):
        exito, mensaje = resultado
        if exito:
            messagebox.showinfo("AutoCore", mensaje)
            if al_completar:
                al_completar()
        else:
            messagebox.showerror("AutoCore", mensaje)
        return exito

    @staticmethod
    def _mostrar_excepcion(error):
        messagebox.showerror("AutoCore", f"No fue posible completar la operación: {error}")

    def _crear_seccion_clientes(self):
        panel = ttk.Frame(self.tab_clientes)
        panel.pack(fill="x", pady=(0, 14))
        panel.columnconfigure(0, weight=1)
        panel.columnconfigure(1, weight=1)

        registro = ttk.LabelFrame(panel, text="Registrar cliente", padding=12)
        registro.grid(row=0, column=0, sticky="nsew", padx=(0, 7))
        registro.columnconfigure(1, weight=1)

        self.cliente_nombre = tk.StringVar()
        self.cliente_telefono = tk.StringVar()
        self.cliente_correo = tk.StringVar()
        self.cliente_direccion = tk.StringVar()
        self._agregar_campo(registro, 0, "Nombre *", self.cliente_nombre)
        self._agregar_campo(registro, 1, "Teléfono *", self.cliente_telefono)
        self._agregar_campo(registro, 2, "Correo", self.cliente_correo)
        self._agregar_campo(registro, 3, "Dirección", self.cliente_direccion)
        ttk.Button(registro, text="Registrar", command=self.registrar_cliente_gui).grid(
            row=4, column=1, sticky="e", pady=(10, 0)
        )

        edicion = ttk.LabelFrame(panel, text="Editar cliente", padding=12)
        edicion.grid(row=0, column=1, sticky="nsew", padx=(7, 0))
        edicion.columnconfigure(1, weight=1)

        self.editar_cliente_id = tk.StringVar()
        self.editar_cliente_nombre = tk.StringVar()
        self.editar_cliente_telefono = tk.StringVar()
        self.editar_cliente_correo = tk.StringVar()
        self.editar_cliente_direccion = tk.StringVar()
        self._agregar_campo(edicion, 0, "ID del cliente *", self.editar_cliente_id)
        self._agregar_campo(edicion, 1, "Nombre *", self.editar_cliente_nombre)
        self._agregar_campo(edicion, 2, "Teléfono *", self.editar_cliente_telefono)
        self._agregar_campo(edicion, 3, "Correo", self.editar_cliente_correo)
        self._agregar_campo(edicion, 4, "Dirección", self.editar_cliente_direccion)
        ttk.Button(edicion, text="Guardar cambios", command=self.editar_cliente_gui).grid(
            row=5, column=1, sticky="e", pady=(10, 0)
        )

        consulta = ttk.LabelFrame(
            self.tab_clientes, text="Clientes registrados", padding=10
        )
        consulta.pack(fill="both", expand=True)
        ttk.Button(
            consulta, text="Actualizar consulta", command=self.consultar_clientes_gui
        ).pack(anchor="e", pady=(0, 8))
        self.tabla_clientes = self._crear_treeview(
            consulta,
            ("id", "nombre", "telefono", "correo", "direccion"),
            ("ID", "Nombre", "Teléfono", "Correo", "Dirección"),
            (60, 190, 120, 190, 240),
        )
        self.tabla_clientes.bind("<<TreeviewSelect>>", self._cargar_cliente_seleccionado)

    def registrar_cliente_gui(self):
        try:
            resultado = registrar_cliente(
                self.cliente_nombre.get(),
                self.cliente_telefono.get(),
                self.cliente_correo.get(),
                self.cliente_direccion.get(),
            )
            if self._mostrar_resultado(resultado):
                self._limpiar_variables(
                    self.cliente_nombre,
                    self.cliente_telefono,
                    self.cliente_correo,
                    self.cliente_direccion,
                )
                self.consultar_clientes_gui()
        except Exception as error:
            self._mostrar_excepcion(error)

    def consultar_clientes_gui(self):
        try:
            self._reemplazar_filas(self.tabla_clientes, consultar_clientes())
        except Exception as error:
            self._mostrar_excepcion(error)

    def _cargar_cliente_seleccionado(self, _evento=None):
        seleccion = self.tabla_clientes.selection()
        if not seleccion:
            return
        valores = self.tabla_clientes.item(seleccion[0], "values")
        variables = (
            self.editar_cliente_id,
            self.editar_cliente_nombre,
            self.editar_cliente_telefono,
            self.editar_cliente_correo,
            self.editar_cliente_direccion,
        )
        for variable, valor in zip(variables, valores):
            variable.set(valor)

    def editar_cliente_gui(self):
        try:
            resultado = editar_cliente(
                self.editar_cliente_id.get(),
                self.editar_cliente_nombre.get(),
                self.editar_cliente_telefono.get(),
                self.editar_cliente_correo.get(),
                self.editar_cliente_direccion.get(),
            )
            if self._mostrar_resultado(resultado):
                self._limpiar_variables(
                    self.editar_cliente_id,
                    self.editar_cliente_nombre,
                    self.editar_cliente_telefono,
                    self.editar_cliente_correo,
                    self.editar_cliente_direccion,
                )
                self.consultar_clientes_gui()
        except Exception as error:
            self._mostrar_excepcion(error)

    def _crear_seccion_vehiculos(self):
        registro = ttk.LabelFrame(
            self.tab_vehiculos, text="Registrar y asociar vehículo", padding=12
        )
        registro.pack(fill="x", pady=(0, 14))
        for columna in (1, 3, 5):
            registro.columnconfigure(columna, weight=1)

        self.vehiculo_cliente_id = tk.StringVar()
        self.vehiculo_marca = tk.StringVar()
        self.vehiculo_modelo = tk.StringVar()
        self.vehiculo_anio = tk.StringVar()
        self.vehiculo_placas = tk.StringVar()
        self.vehiculo_color = tk.StringVar()
        campos = (
            ("ID cliente *", self.vehiculo_cliente_id),
            ("Marca *", self.vehiculo_marca),
            ("Modelo *", self.vehiculo_modelo),
            ("Año", self.vehiculo_anio),
            ("Placas *", self.vehiculo_placas),
            ("Color", self.vehiculo_color),
        )
        for indice, (texto, variable) in enumerate(campos):
            fila, bloque = divmod(indice, 3)
            columna = bloque * 2
            ttk.Label(registro, text=texto).grid(
                row=fila, column=columna, sticky="w", padx=(0, 8), pady=5
            )
            ttk.Entry(registro, textvariable=variable).grid(
                row=fila, column=columna + 1, sticky="ew", padx=(0, 18), pady=5
            )
        ttk.Button(registro, text="Registrar vehículo", command=self.registrar_vehiculo_gui).grid(
            row=2, column=5, sticky="e", pady=(10, 0)
        )

        consulta = ttk.LabelFrame(
            self.tab_vehiculos, text="Vehículos registrados", padding=10
        )
        consulta.pack(fill="both", expand=True)
        ttk.Button(
            consulta, text="Actualizar consulta", command=self.consultar_vehiculos_gui
        ).pack(anchor="e", pady=(0, 8))
        self.tabla_vehiculos = self._crear_treeview(
            consulta,
            ("id", "cliente", "marca", "modelo", "anio", "placas", "color"),
            ("ID", "ID cliente", "Marca", "Modelo", "Año", "Placas", "Color"),
            (55, 85, 130, 140, 70, 120, 120),
        )

    def registrar_vehiculo_gui(self):
        try:
            resultado = registrar_vehiculo(
                self.vehiculo_cliente_id.get(),
                self.vehiculo_marca.get(),
                self.vehiculo_modelo.get(),
                self.vehiculo_anio.get(),
                self.vehiculo_placas.get(),
                self.vehiculo_color.get(),
            )
            if self._mostrar_resultado(resultado):
                self._limpiar_variables(
                    self.vehiculo_cliente_id,
                    self.vehiculo_marca,
                    self.vehiculo_modelo,
                    self.vehiculo_anio,
                    self.vehiculo_placas,
                    self.vehiculo_color,
                )
                self.consultar_vehiculos_gui()
        except Exception as error:
            self._mostrar_excepcion(error)

    def consultar_vehiculos_gui(self):
        try:
            self._reemplazar_filas(self.tabla_vehiculos, consultar_vehiculos())
        except Exception as error:
            self._mostrar_excepcion(error)

    def _crear_seccion_ordenes(self):
        panel = ttk.Frame(self.tab_ordenes)
        panel.pack(fill="x", pady=(0, 14))
        panel.columnconfigure(0, weight=2)
        panel.columnconfigure(1, weight=1)

        registro = ttk.LabelFrame(panel, text="Crear orden de servicio", padding=12)
        registro.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 7))
        registro.columnconfigure(1, weight=1)

        self.orden_vehiculo_id = tk.StringVar()
        self.orden_descripcion = tk.StringVar()
        self.orden_fecha = tk.StringVar()
        self.orden_estado = tk.StringVar(value=ESTADOS_PERMITIDOS[0])
        self.orden_observaciones = tk.StringVar()
        self._agregar_campo(registro, 0, "ID del vehículo *", self.orden_vehiculo_id)
        self._agregar_campo(registro, 1, "Descripción *", self.orden_descripcion)
        self._agregar_campo(registro, 2, "Fecha *", self.orden_fecha)
        ttk.Label(registro, text="Estado *").grid(
            row=3, column=0, sticky="w", padx=(0, 8), pady=4
        )
        ttk.Combobox(
            registro,
            textvariable=self.orden_estado,
            values=ESTADOS_PERMITIDOS,
            state="readonly",
        ).grid(row=3, column=1, sticky="ew", pady=4)
        self._agregar_campo(registro, 4, "Observaciones", self.orden_observaciones)
        ttk.Button(registro, text="Crear orden", command=self.registrar_orden_gui).grid(
            row=5, column=1, sticky="e", pady=(10, 0)
        )

        estado = ttk.LabelFrame(panel, text="Actualizar estado", padding=12)
        estado.grid(row=0, column=1, sticky="nsew", padx=(7, 0), pady=(0, 7))
        estado.columnconfigure(1, weight=1)
        self.actualizar_estado_id = tk.StringVar()
        self.actualizar_estado_valor = tk.StringVar(value=ESTADOS_PERMITIDOS[0])
        self._agregar_campo(estado, 0, "ID orden *", self.actualizar_estado_id)
        ttk.Label(estado, text="Nuevo estado *").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=4
        )
        ttk.Combobox(
            estado,
            textvariable=self.actualizar_estado_valor,
            values=ESTADOS_PERMITIDOS,
            state="readonly",
        ).grid(row=1, column=1, sticky="ew", pady=4)
        ttk.Button(estado, text="Actualizar", command=self.actualizar_estado_gui).grid(
            row=2, column=1, sticky="e", pady=(8, 0)
        )

        observaciones = ttk.LabelFrame(
            panel, text="Actualizar observaciones", padding=12
        )
        observaciones.grid(row=1, column=1, sticky="nsew", padx=(7, 0), pady=(7, 0))
        observaciones.columnconfigure(1, weight=1)
        self.actualizar_observaciones_id = tk.StringVar()
        self.actualizar_observaciones_valor = tk.StringVar()
        self._agregar_campo(
            observaciones, 0, "ID orden *", self.actualizar_observaciones_id
        )
        self._agregar_campo(
            observaciones, 1, "Observaciones *", self.actualizar_observaciones_valor
        )
        ttk.Button(
            observaciones,
            text="Actualizar",
            command=self.actualizar_observaciones_gui,
        ).grid(row=2, column=1, sticky="e", pady=(8, 0))

        consulta = ttk.LabelFrame(
            self.tab_ordenes, text="Órdenes registradas", padding=10
        )
        consulta.pack(fill="both", expand=True)
        ttk.Button(
            consulta, text="Actualizar consulta", command=self.consultar_ordenes_gui
        ).pack(anchor="e", pady=(0, 8))
        self.tabla_ordenes = self._crear_treeview(
            consulta,
            ("id", "vehiculo", "descripcion", "fecha", "estado", "observaciones"),
            ("ID", "ID vehículo", "Descripción", "Fecha", "Estado", "Observaciones"),
            (55, 85, 230, 100, 110, 280),
        )

    def registrar_orden_gui(self):
        try:
            resultado = registrar_orden_servicio(
                self.orden_vehiculo_id.get(),
                self.orden_descripcion.get(),
                self.orden_fecha.get(),
                self.orden_estado.get(),
                self.orden_observaciones.get(),
            )
            if self._mostrar_resultado(resultado):
                self._limpiar_variables(
                    self.orden_vehiculo_id,
                    self.orden_descripcion,
                    self.orden_fecha,
                    self.orden_observaciones,
                )
                self.orden_estado.set(ESTADOS_PERMITIDOS[0])
                self.consultar_ordenes_gui()
        except Exception as error:
            self._mostrar_excepcion(error)

    def consultar_ordenes_gui(self):
        try:
            self._reemplazar_filas(self.tabla_ordenes, consultar_ordenes_servicio())
        except Exception as error:
            self._mostrar_excepcion(error)

    def actualizar_estado_gui(self):
        try:
            resultado = actualizar_estado_orden(
                self.actualizar_estado_id.get(), self.actualizar_estado_valor.get()
            )
            if self._mostrar_resultado(resultado):
                self.actualizar_estado_id.set("")
                self.actualizar_estado_valor.set(ESTADOS_PERMITIDOS[0])
                self.consultar_ordenes_gui()
        except Exception as error:
            self._mostrar_excepcion(error)

    def actualizar_observaciones_gui(self):
        try:
            resultado = actualizar_observaciones_orden(
                self.actualizar_observaciones_id.get(),
                self.actualizar_observaciones_valor.get(),
            )
            if self._mostrar_resultado(resultado):
                self._limpiar_variables(
                    self.actualizar_observaciones_id,
                    self.actualizar_observaciones_valor,
                )
                self.consultar_ordenes_gui()
        except Exception as error:
            self._mostrar_excepcion(error)


def main():
    root = tk.Tk()
    AutoCoreGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
