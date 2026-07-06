from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QSpinBox, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt

from models.producto_model import obtener_productos
from models.venta_model import obtener_metodos_pago, registrar_venta
from models.cliente_model import obtener_clientes
from ui import estilos


class VentasView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {estilos.FONDO};")
        self.carrito = []  # lista de dicts: id_producto, sku, nombre, cantidad, precio_unitario, subtotal
        self.init_ui()
        self.cargar_datos_iniciales()

    def init_ui(self):
        layout_general = QVBoxLayout(self)
        layout_general.setContentsMargins(28, 28, 28, 20)
        layout_general.setSpacing(10)

        # ---- Encabezado ----
        titulo_box = QVBoxLayout()
        titulo_box.setSpacing(2)
        meta = QLabel("SALES MANAGEMENT")
        meta.setStyleSheet(estilos.META_PAGINA)
        titulo_box.addWidget(meta)
        titulo = QLabel("New Sale")
        titulo.setStyleSheet(estilos.TITULO_PAGINA)
        titulo_box.addWidget(titulo)
        subtitulo = QLabel("Process a transaction and update inventory automatically.")
        subtitulo.setStyleSheet(estilos.SUBTITULO_PAGINA)
        titulo_box.addWidget(subtitulo)
        layout_general.addLayout(titulo_box)
        layout_general.addSpacing(6)

        # ---- Dos columnas: carrito | resumen ----
        columnas_layout = QHBoxLayout()
        columnas_layout.setSpacing(16)

        # ===== Columna izquierda: buscar producto + carrito =====
        col_izquierda = QVBoxLayout()

        buscador_layout = QHBoxLayout()
        self.combo_producto = QComboBox()
        self.combo_producto.setStyleSheet(estilos.INPUT)
        self.combo_producto.setMinimumHeight(38)
        buscador_layout.addWidget(self.combo_producto, stretch=3)

        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(1)
        self.spin_cantidad.setMaximum(999)
        self.spin_cantidad.setStyleSheet(estilos.INPUT)
        self.spin_cantidad.setMinimumHeight(38)
        self.spin_cantidad.setMaximumWidth(70)
        buscador_layout.addWidget(self.spin_cantidad)

        btn_agregar = QPushButton("+ Add")
        btn_agregar.setCursor(Qt.PointingHandCursor)
        btn_agregar.setStyleSheet(estilos.BOTON_PRIMARIO)
        btn_agregar.clicked.connect(self.agregar_al_carrito)
        buscador_layout.addWidget(btn_agregar)

        col_izquierda.addLayout(buscador_layout)

        tarjeta_carrito = QWidget()
        tarjeta_carrito.setStyleSheet(estilos.TARJETA)
        tarjeta_carrito_layout = QVBoxLayout(tarjeta_carrito)
        tarjeta_carrito_layout.setContentsMargins(0, 0, 0, 0)

        self.tabla_carrito = QTableWidget()
        self.tabla_carrito.setColumnCount(5)
        self.tabla_carrito.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio", "Subtotal", ""])
        self.tabla_carrito.setStyleSheet(estilos.TABLA)
        self.tabla_carrito.setShowGrid(False)
        self.tabla_carrito.verticalHeader().setVisible(False)
        self.tabla_carrito.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_carrito.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla_carrito.verticalHeader().setDefaultSectionSize(42)
        tarjeta_carrito_layout.addWidget(self.tabla_carrito)

        col_izquierda.addWidget(tarjeta_carrito)
        columnas_layout.addLayout(col_izquierda, stretch=3)

        # ===== Columna derecha: resumen de la orden =====
        tarjeta_resumen = QWidget()
        tarjeta_resumen.setStyleSheet(estilos.TARJETA)
        resumen_layout = QVBoxLayout(tarjeta_resumen)
        resumen_layout.setContentsMargins(16, 16, 16, 16)
        resumen_layout.setSpacing(8)

        label_resumen = QLabel("Order summary")
        label_resumen.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {estilos.VERDE_OSCURO};")
        resumen_layout.addWidget(label_resumen)

        self.label_subtotal = QLabel("Subtotal: $0.00")
        self.label_subtotal.setStyleSheet("font-size: 13px; color: #666;")
        resumen_layout.addWidget(self.label_subtotal)

        self.label_total = QLabel("Total: $0.00")
        self.label_total.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {estilos.VERDE_OSCURO}; padding-top: 6px; border-top: 1px solid {estilos.BORDE};")
        resumen_layout.addWidget(self.label_total)

        resumen_layout.addSpacing(10)
        label_cliente = QLabel("Cliente (opcional)")
        label_cliente.setStyleSheet("font-size: 12px; color: #aaa;")
        resumen_layout.addWidget(label_cliente)

        self.combo_cliente = QComboBox()
        self.combo_cliente.setStyleSheet(estilos.INPUT)
        self.combo_cliente.setMinimumHeight(36)
        resumen_layout.addWidget(self.combo_cliente)

        resumen_layout.addSpacing(6)
        label_pago = QLabel("Payment method")
        label_pago.setStyleSheet("font-size: 12px; color: #aaa;")
        resumen_layout.addWidget(label_pago)

        self.combo_pago = QComboBox()
        self.combo_pago.setStyleSheet(estilos.INPUT)
        self.combo_pago.setMinimumHeight(36)
        resumen_layout.addWidget(self.combo_pago)

        resumen_layout.addSpacing(10)
        btn_confirmar = QPushButton("Confirm sale")
        btn_confirmar.setCursor(Qt.PointingHandCursor)
        btn_confirmar.setStyleSheet(estilos.BOTON_PRIMARIO)
        btn_confirmar.clicked.connect(self.confirmar_venta)
        resumen_layout.addWidget(btn_confirmar)

        resumen_layout.addStretch()
        tarjeta_resumen.setMaximumWidth(300)
        columnas_layout.addWidget(tarjeta_resumen, stretch=2)

        layout_general.addLayout(columnas_layout)

    def cargar_datos_iniciales(self):
        # Productos disponibles
        self.combo_producto.clear()
        self.productos_disponibles = obtener_productos(solo_activos=True)
        for prod in self.productos_disponibles:
            id_producto, sku, nombre, categoria, talla, color, precio_venta, stock, *_ = prod
            texto = f"{nombre} ({talla}, {color}) - ${precio_venta:.2f} - Stock: {stock}"
            self.combo_producto.addItem(texto, id_producto)

        # Clientes
        self.combo_cliente.clear()
        self.combo_cliente.addItem("Sin cliente asociado", None)
        for id_cliente, nombre, apellido, *_ in obtener_clientes():
            self.combo_cliente.addItem(f"{nombre} {apellido or ''}".strip(), id_cliente)

        # Métodos de pago
        self.combo_pago.clear()
        for id_pago, tipo_pago in obtener_metodos_pago():
            self.combo_pago.addItem(tipo_pago, id_pago)

    def agregar_al_carrito(self):
        id_producto = self.combo_producto.currentData()
        if id_producto is None:
            return

        cantidad = self.spin_cantidad.value()

        # Buscar datos del producto seleccionado
        producto = next((p for p in self.productos_disponibles if p[0] == id_producto), None)
        if producto is None:
            return

        _, sku, nombre, categoria, talla, color, precio_venta, stock, *_ = producto

        # Revisar si ya está en el carrito, sumar cantidad
        for item in self.carrito:
            if item["id_producto"] == id_producto:
                item["cantidad"] += cantidad
                item["subtotal"] = item["cantidad"] * item["precio_unitario"]
                self.actualizar_tabla_carrito()
                return

        self.carrito.append({
            "id_producto": id_producto,
            "sku": sku,
            "nombre": f"{nombre} ({talla}, {color})",
            "cantidad": cantidad,
            "precio_unitario": precio_venta,
            "subtotal": precio_venta * cantidad
        })
        self.actualizar_tabla_carrito()

    def actualizar_tabla_carrito(self):
        self.tabla_carrito.setRowCount(0)
        for fila_idx, item in enumerate(self.carrito):
            self.tabla_carrito.insertRow(fila_idx)
            self.tabla_carrito.setItem(fila_idx, 0, QTableWidgetItem(item["nombre"]))
            self.tabla_carrito.setItem(fila_idx, 1, QTableWidgetItem(str(item["cantidad"])))
            self.tabla_carrito.setItem(fila_idx, 2, QTableWidgetItem(f"${item['precio_unitario']:.2f}"))
            self.tabla_carrito.setItem(fila_idx, 3, QTableWidgetItem(f"${item['subtotal']:.2f}"))

            btn_quitar = QPushButton("✕")
            btn_quitar.setCursor(Qt.PointingHandCursor)
            btn_quitar.setStyleSheet(estilos.BOTON_PELIGRO)
            btn_quitar.clicked.connect(lambda checked, idx=fila_idx: self.quitar_del_carrito(idx))
            self.tabla_carrito.setCellWidget(fila_idx, 4, btn_quitar)

        self.actualizar_totales()

    def quitar_del_carrito(self, indice):
        del self.carrito[indice]
        self.actualizar_tabla_carrito()

    def actualizar_totales(self):
        total = sum(item["subtotal"] for item in self.carrito)
        self.label_subtotal.setText(f"Subtotal: ${total:.2f}")
        self.label_total.setText(f"Total: ${total:.2f}")

    def confirmar_venta(self):
        if not self.carrito:
            QMessageBox.warning(self, "Carrito vacío", "Agrega al menos un producto antes de confirmar la venta.")
            return

        id_cliente = self.combo_cliente.currentData()
        id_pago = self.combo_pago.currentData()

        if id_pago is None:
            QMessageBox.warning(self, "Error", "Selecciona un método de pago.")
            return

        ok, resultado, total = registrar_venta(self.carrito, id_cliente, id_pago)

        if ok:
            QMessageBox.information(self, "Venta registrada", f"Venta #{resultado} registrada exitosamente.\nTotal: ${total:.2f}")
            self.carrito = []
            self.actualizar_tabla_carrito()
            self.cargar_datos_iniciales()  # refresca stock disponible
        else:
            QMessageBox.warning(self, "Error al procesar venta", resultado)