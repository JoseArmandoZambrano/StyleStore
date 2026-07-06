from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt

from models.producto_model import obtener_productos, eliminar_producto
from models.categoria_model import obtener_categorias
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
        self.tabla.setColumnCount(8)
        self.tabla.setHorizontalHeaderLabels(
            ["SKU", "Nombre", "Categoría", "Talla", "Color", "Precio", "Stock", "Acciones"]
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

            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.setCursor(Qt.PointingHandCursor)
            btn_eliminar.setStyleSheet(estilos.BOTON_PELIGRO)
            btn_eliminar.clicked.connect(lambda checked, pid=id_producto: self.confirmar_eliminar(pid))
            self.tabla.setCellWidget(fila_idx, 7, btn_eliminar)

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