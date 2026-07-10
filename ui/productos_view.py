from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFrame,
    QDialog, QFormLayout, QDoubleSpinBox, QSpinBox, QTextEdit
)
from PyQt5.QtCore import Qt

from models.producto_model import (
    obtener_productos, eliminar_producto, registrar_producto,
    modificar_producto, obtener_producto_por_id
)
from models.categoria_model import obtener_categorias
from models.proveedor_model import obtener_proveedores
from ui import estilos


class ProductosView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {estilos.FONDO};")
        self.init_ui()
        self.cargar_categorias()
        self.cargar_productos()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 20)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        titulo_box = QVBoxLayout()
        titulo_box.setSpacing(2)

        meta = QLabel("PRODUCT MANAGEMENT")
        meta.setStyleSheet(estilos.META_PAGINA)
        titulo_box.addWidget(meta)

        titulo = QLabel("Products")
        titulo.setStyleSheet(estilos.TITULO_PAGINA)
        titulo_box.addWidget(titulo)

        subtitulo = QLabel("Browse, search and manage your full catalog.")
        subtitulo.setStyleSheet(estilos.SUBTITULO_PAGINA)
        titulo_box.addWidget(subtitulo)

        header_layout.addLayout(titulo_box)
        header_layout.addStretch()

        self.btn_nuevo = QPushButton("+  New product")
        self.btn_nuevo.setCursor(Qt.PointingHandCursor)
        self.btn_nuevo.setStyleSheet(estilos.BOTON_PRIMARIO)
        self.btn_nuevo.clicked.connect(self.abrir_formulario_nuevo)
        header_layout.addWidget(self.btn_nuevo, alignment=Qt.AlignTop)

        layout.addLayout(header_layout)
        layout.addSpacing(6)

        filtros_layout = QHBoxLayout()
        filtros_layout.setSpacing(10)

        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Search by name or SKU...")
        self.input_busqueda.setStyleSheet(estilos.INPUT)
        self.input_busqueda.setMinimumHeight(38)
        self.input_busqueda.textChanged.connect(self.cargar_productos)
        filtros_layout.addWidget(self.input_busqueda, stretch=3)

        self.combo_categoria = QComboBox()
        self.combo_categoria.setStyleSheet(estilos.INPUT)
        self.combo_categoria.setMinimumHeight(38)
        self.combo_categoria.currentIndexChanged.connect(self.cargar_productos)
        filtros_layout.addWidget(self.combo_categoria, stretch=1)

        layout.addLayout(filtros_layout)

        tarjeta = QWidget()
        tarjeta.setStyleSheet(estilos.TARJETA)
        tarjeta_layout = QVBoxLayout(tarjeta)
        tarjeta_layout.setContentsMargins(0, 0, 0, 0)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(9)
        self.tabla.setHorizontalHeaderLabels(
            ["SKU", "Nombre", "Categoría", "Talla", "Color", "Precio", "Stock", "Editar", "Eliminar"]
        )
        self.tabla.setStyleSheet(estilos.TABLA)
        self.tabla.setShowGrid(False)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla.verticalHeader().setDefaultSectionSize(44)
        tarjeta_layout.addWidget(self.tabla)

        layout.addWidget(tarjeta)

        self.label_contador = QLabel("")
        self.label_contador.setStyleSheet(f"font-size: 12px; color: {estilos.GRIS_TEXTO};")
        layout.addWidget(self.label_contador)

    def cargar_categorias(self):
        self.combo_categoria.blockSignals(True)
        self.combo_categoria.clear()
        self.combo_categoria.addItem("Todas las categorías", None)
        for id_cat, nombre, _ in obtener_categorias():
            self.combo_categoria.addItem(nombre, id_cat)
        self.combo_categoria.blockSignals(False)

    def cargar_productos(self):
        texto = self.input_busqueda.text().strip()
        id_categoria = self.combo_categoria.currentData()

        productos = obtener_productos(
            solo_activos=True,
            id_categoria=id_categoria,
            texto_busqueda=texto if texto else None
        )

        self.tabla.setRowCount(0)
        for fila_idx, prod in enumerate(productos):
            (id_producto, sku, nombre, categoria, talla, color,
             precio_venta, stock, status, _, _, _, _) = prod

            self.tabla.insertRow(fila_idx)
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(sku))
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(nombre))
            self.tabla.setItem(fila_idx, 2, QTableWidgetItem(categoria or "-"))
            self.tabla.setItem(fila_idx, 3, QTableWidgetItem(talla or "-"))
            self.tabla.setItem(fila_idx, 4, QTableWidgetItem(color or "-"))
            self.tabla.setItem(fila_idx, 5, QTableWidgetItem(f"${precio_venta:.2f}"))

            item_stock = QTableWidgetItem(str(stock))
            if stock <= 5:
                item_stock.setForeground(Qt.red)
            self.tabla.setItem(fila_idx, 6, item_stock)

            btn_editar = QPushButton("Editar")
            btn_editar.setCursor(Qt.PointingHandCursor)
            btn_editar.setStyleSheet(estilos.BOTON_SECUNDARIO)
            btn_editar.clicked.connect(lambda checked, pid=id_producto: self.abrir_formulario_editar(pid))
            self.tabla.setCellWidget(fila_idx, 7, btn_editar)

            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.setCursor(Qt.PointingHandCursor)
            btn_eliminar.setStyleSheet(estilos.BOTON_PELIGRO)
            btn_eliminar.clicked.connect(lambda checked, pid=id_producto: self.confirmar_eliminar(pid))
            self.tabla.setCellWidget(fila_idx, 8, btn_eliminar)

        self.label_contador.setText(f"{len(productos)} productos mostrados")

    def confirmar_eliminar(self, id_producto):
        respuesta = QMessageBox.question(
            self, "Confirmar baja",
            "¿Seguro que deseas dar de baja este producto?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            ok, mensaje = eliminar_producto(id_producto)
            if ok:
                QMessageBox.information(self, "Éxito", mensaje)
                self.cargar_productos()
            else:
                QMessageBox.warning(self, "Error", mensaje)

    def abrir_formulario_nuevo(self):
        dialogo = FormularioProducto(self, id_producto=None)
        if dialogo.exec_() == QDialog.Accepted:
            self.cargar_categorias()
            self.cargar_productos()

    def abrir_formulario_editar(self, id_producto):
        dialogo = FormularioProducto(self, id_producto=id_producto)
        if dialogo.exec_() == QDialog.Accepted:
            self.cargar_categorias()
            self.cargar_productos()


class FormularioProducto(QDialog):
    """Ventana emergente para registrar (RF01) o editar (RF02) un producto."""
    def __init__(self, parent=None, id_producto=None):
        super().__init__(parent)
        self.id_producto = id_producto
        self.modo_edicion = id_producto is not None

        self.setWindowTitle("Editar producto" if self.modo_edicion else "Nuevo producto")
        self.setMinimumWidth(420)
        self.setStyleSheet(f"background-color: {estilos.FONDO};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        titulo = QLabel("Editar producto" if self.modo_edicion else "Registrar nuevo producto")
        titulo.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {estilos.VERDE_OSCURO};")
        layout.addWidget(titulo)
        layout.addSpacing(10)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.input_nombre = QLineEdit()
        self.input_nombre.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Nombre*:", self.input_nombre)

        self.combo_categoria = QComboBox()
        self.combo_categoria.setStyleSheet(estilos.INPUT)
        for id_cat, nombre, _ in obtener_categorias():
            self.combo_categoria.addItem(nombre, id_cat)
        form_layout.addRow("Categoría:", self.combo_categoria)

        self.combo_proveedor = QComboBox()
        self.combo_proveedor.setStyleSheet(estilos.INPUT)
        for id_prov, nombre, *_ in obtener_proveedores():
            self.combo_proveedor.addItem(nombre, id_prov)
        form_layout.addRow("Proveedor:", self.combo_proveedor)

        self.input_talla = QLineEdit()
        self.input_talla.setStyleSheet(estilos.INPUT)
        self.input_talla.setPlaceholderText("Ej: M, 30, Única")
        form_layout.addRow("Talla:", self.input_talla)

        self.input_color = QLineEdit()
        self.input_color.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Color:", self.input_color)

        self.spin_precio_compra = QDoubleSpinBox()
        self.spin_precio_compra.setMaximum(999999)
        self.spin_precio_compra.setPrefix("$ ")
        self.spin_precio_compra.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Precio de compra:", self.spin_precio_compra)

        self.spin_precio_venta = QDoubleSpinBox()
        self.spin_precio_venta.setMaximum(999999)
        self.spin_precio_venta.setPrefix("$ ")
        self.spin_precio_venta.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Precio de venta*:", self.spin_precio_venta)

        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMaximum(99999)
        self.spin_cantidad.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Cantidad inicial*:", self.spin_cantidad)

        if self.modo_edicion:
            # En edición, el stock se maneja por ventas, no se debería reeditar libremente
            self.spin_cantidad.setEnabled(False)
            self.spin_cantidad.setToolTip("El stock se actualiza automáticamente mediante ventas")

        self.input_descripcion = QTextEdit()
        self.input_descripcion.setStyleSheet(estilos.INPUT)
        self.input_descripcion.setMaximumHeight(70)
        form_layout.addRow("Descripción:", self.input_descripcion)

        layout.addLayout(form_layout)
        layout.addSpacing(14)

        btn_guardar = QPushButton("Guardar cambios" if self.modo_edicion else "Guardar")
        btn_guardar.setStyleSheet(estilos.BOTON_PRIMARIO)
        btn_guardar.setCursor(Qt.PointingHandCursor)
        btn_guardar.clicked.connect(self.guardar)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet(estilos.BOTON_SECUNDARIO)
        btn_cancelar.setCursor(Qt.PointingHandCursor)
        btn_cancelar.clicked.connect(self.reject)

        botones_layout = QHBoxLayout()
        botones_layout.addStretch()
        botones_layout.addWidget(btn_cancelar)
        botones_layout.addWidget(btn_guardar)
        layout.addLayout(botones_layout)

        if self.modo_edicion:
            self.cargar_datos_producto()

    def cargar_datos_producto(self):
        """Precarga los campos del formulario con los datos actuales del producto."""
        datos = obtener_producto_por_id(self.id_producto)
        if datos is None:
            return

        (id_producto, sku, nombre, id_categoria, talla, color,
         precio_compra, precio_venta, stock, id_proveedor, descripcion, status) = datos

        self.input_nombre.setText(nombre or "")

        indice_cat = self.combo_categoria.findData(id_categoria)
        if indice_cat >= 0:
            self.combo_categoria.setCurrentIndex(indice_cat)

        indice_prov = self.combo_proveedor.findData(id_proveedor)
        if indice_prov >= 0:
            self.combo_proveedor.setCurrentIndex(indice_prov)

        self.input_talla.setText(talla or "")
        self.input_color.setText(color or "")
        self.spin_precio_compra.setValue(precio_compra or 0)
        self.spin_precio_venta.setValue(precio_venta or 0)
        self.spin_cantidad.setValue(stock or 0)
        self.input_descripcion.setPlainText(descripcion or "")

    def guardar(self):
        nombre = self.input_nombre.text().strip()
        precio_venta = self.spin_precio_venta.value()

        if not nombre or precio_venta <= 0:
            QMessageBox.warning(self, "Error", "El nombre y el precio de venta son obligatorios")
            return

        if self.modo_edicion:
            ok, resultado = modificar_producto(
                id_producto=self.id_producto,
                nombre=nombre,
                id_categoria=self.combo_categoria.currentData(),
                talla=self.input_talla.text().strip() or None,
                color=self.input_color.text().strip() or None,
                precio_compra=self.spin_precio_compra.value(),
                precio_venta=precio_venta,
                id_proveedor=self.combo_proveedor.currentData(),
                descripcion=self.input_descripcion.toPlainText().strip()
            )
            if ok:
                QMessageBox.information(self, "Éxito", resultado)
                self.accept()
            else:
                QMessageBox.warning(self, "Error al actualizar producto", resultado)
        else:
            cantidad = self.spin_cantidad.value()
            ok, resultado = registrar_producto(
                nombre=nombre,
                id_categoria=self.combo_categoria.currentData(),
                talla=self.input_talla.text().strip() or None,
                color=self.input_color.text().strip() or None,
                precio_compra=self.spin_precio_compra.value(),
                precio_venta=precio_venta,
                cantidad_inicial=cantidad,
                id_proveedor=self.combo_proveedor.currentData(),
                descripcion=self.input_descripcion.toPlainText().strip()
            )
            if ok:
                QMessageBox.information(self, "Éxito", f"Producto registrado exitosamente con SKU: {resultado}")
                self.accept()
            else:
                QMessageBox.warning(self, "Error al registrar producto", resultado)