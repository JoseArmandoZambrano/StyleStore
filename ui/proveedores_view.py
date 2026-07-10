from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog,
    QFormLayout
)
from PyQt5.QtCore import Qt

from models.proveedor_model import (
    registrar_proveedor, obtener_proveedores, modificar_proveedor,
    eliminar_proveedor, obtener_proveedor_por_id
)
from ui import estilos


class ProveedoresView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {estilos.FONDO};")
        self.init_ui()
        self.cargar_proveedores()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 20)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        titulo_box = QVBoxLayout()
        titulo_box.setSpacing(2)

        meta = QLabel("SUPPLIER MANAGEMENT")
        meta.setStyleSheet(estilos.META_PAGINA)
        titulo_box.addWidget(meta)

        titulo = QLabel("Suppliers")
        titulo.setStyleSheet(estilos.TITULO_PAGINA)
        titulo_box.addWidget(titulo)

        subtitulo = QLabel("Manage the suppliers that provide your inventory.")
        subtitulo.setStyleSheet(estilos.SUBTITULO_PAGINA)
        titulo_box.addWidget(subtitulo)

        header_layout.addLayout(titulo_box)
        header_layout.addStretch()

        self.btn_nuevo = QPushButton("+  New supplier")
        self.btn_nuevo.setCursor(Qt.PointingHandCursor)
        self.btn_nuevo.setStyleSheet(estilos.BOTON_PRIMARIO)
        self.btn_nuevo.clicked.connect(self.abrir_formulario_nuevo)
        header_layout.addWidget(self.btn_nuevo, alignment=Qt.AlignTop)

        layout.addLayout(header_layout)
        layout.addSpacing(6)

        tarjeta = QWidget()
        tarjeta.setStyleSheet(estilos.TARJETA)
        tarjeta_layout = QVBoxLayout(tarjeta)
        tarjeta_layout.setContentsMargins(0, 0, 0, 0)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels(
            ["Nombre", "Contacto", "Teléfono", "Correo", "Dirección", "Editar", "Eliminar"]
        )
        self.tabla.setStyleSheet(estilos.TABLA)
        self.tabla.setShowGrid(False)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.tabla.verticalHeader().setDefaultSectionSize(44)
        tarjeta_layout.addWidget(self.tabla)

        layout.addWidget(tarjeta)

        self.label_contador = QLabel("")
        self.label_contador.setStyleSheet(f"font-size: 12px; color: {estilos.GRIS_TEXTO};")
        layout.addWidget(self.label_contador)

    def cargar_proveedores(self):
        proveedores = obtener_proveedores()
        self.tabla.setRowCount(0)
        for fila_idx, prov in enumerate(proveedores):
            id_proveedor, nombre, contacto, telefono, correo, direccion = prov
            self.tabla.insertRow(fila_idx)
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(nombre))
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(contacto or "-"))
            self.tabla.setItem(fila_idx, 2, QTableWidgetItem(telefono or "-"))
            self.tabla.setItem(fila_idx, 3, QTableWidgetItem(correo or "-"))
            self.tabla.setItem(fila_idx, 4, QTableWidgetItem(direccion or "-"))

            btn_editar = QPushButton("Editar")
            btn_editar.setCursor(Qt.PointingHandCursor)
            btn_editar.setStyleSheet(estilos.BOTON_SECUNDARIO)
            btn_editar.clicked.connect(lambda checked, pid=id_proveedor: self.abrir_formulario_editar(pid))
            self.tabla.setCellWidget(fila_idx, 5, btn_editar)

            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.setCursor(Qt.PointingHandCursor)
            btn_eliminar.setStyleSheet(estilos.BOTON_PELIGRO)
            btn_eliminar.clicked.connect(lambda checked, pid=id_proveedor: self.confirmar_eliminar(pid))
            self.tabla.setCellWidget(fila_idx, 6, btn_eliminar)

        self.label_contador.setText(f"{len(proveedores)} proveedores registrados")

    def abrir_formulario_nuevo(self):
        dialogo = FormularioProveedor(self, id_proveedor=None)
        if dialogo.exec_() == QDialog.Accepted:
            self.cargar_proveedores()

    def abrir_formulario_editar(self, id_proveedor):
        dialogo = FormularioProveedor(self, id_proveedor=id_proveedor)
        if dialogo.exec_() == QDialog.Accepted:
            self.cargar_proveedores()

    def confirmar_eliminar(self, id_proveedor):
        respuesta = QMessageBox.question(
            self, "Confirmar eliminación",
            "¿Seguro que deseas eliminar este proveedor?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            ok, mensaje = eliminar_proveedor(id_proveedor)
            if ok:
                QMessageBox.information(self, "Éxito", mensaje)
                self.cargar_proveedores()
            else:
                QMessageBox.warning(self, "No se pudo eliminar", mensaje)


class FormularioProveedor(QDialog):
    """Ventana emergente para registrar o editar un proveedor."""
    def __init__(self, parent=None, id_proveedor=None):
        super().__init__(parent)
        self.id_proveedor = id_proveedor
        self.modo_edicion = id_proveedor is not None

        self.setWindowTitle("Editar proveedor" if self.modo_edicion else "Nuevo proveedor")
        self.setMinimumWidth(380)
        self.setStyleSheet(f"background-color: {estilos.FONDO};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        titulo = QLabel("Editar proveedor" if self.modo_edicion else "Registrar nuevo proveedor")
        titulo.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {estilos.VERDE_OSCURO};")
        layout.addWidget(titulo)
        layout.addSpacing(10)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.input_nombre = QLineEdit()
        self.input_nombre.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Nombre*:", self.input_nombre)

        self.input_contacto = QLineEdit()
        self.input_contacto.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Contacto:", self.input_contacto)

        self.input_telefono = QLineEdit()
        self.input_telefono.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Teléfono:", self.input_telefono)

        self.input_correo = QLineEdit()
        self.input_correo.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Correo:", self.input_correo)

        self.input_direccion = QLineEdit()
        self.input_direccion.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Dirección:", self.input_direccion)

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
            self.cargar_datos_proveedor()

    def cargar_datos_proveedor(self):
        datos = obtener_proveedor_por_id(self.id_proveedor)
        if datos is None:
            return
        id_proveedor, nombre, contacto, telefono, correo, direccion = datos
        self.input_nombre.setText(nombre or "")
        self.input_contacto.setText(contacto or "")
        self.input_telefono.setText(telefono or "")
        self.input_correo.setText(correo or "")
        self.input_direccion.setText(direccion or "")

    def guardar(self):
        nombre = self.input_nombre.text().strip()
        contacto = self.input_contacto.text().strip()
        telefono = self.input_telefono.text().strip()
        correo = self.input_correo.text().strip()
        direccion = self.input_direccion.text().strip()

        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return

        if self.modo_edicion:
            ok, resultado = modificar_proveedor(
                self.id_proveedor, nombre, contacto or None, telefono or None, correo or None, direccion or None
            )
            if ok:
                QMessageBox.information(self, "Éxito", resultado)
                self.accept()
            else:
                QMessageBox.warning(self, "Error al actualizar proveedor", resultado)
        else:
            ok, resultado = registrar_proveedor(nombre, contacto or None, telefono or None, correo or None, direccion or None)
            if ok:
                QMessageBox.information(self, "Éxito", "Proveedor registrado exitosamente")
                self.accept()
            else:
                QMessageBox.warning(self, "Error al registrar proveedor", resultado)