from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog,
    QFormLayout, QDialogButtonBox
)
from PyQt5.QtCore import Qt

from models.cliente_model import registrar_cliente, obtener_clientes, obtener_historial_compras
from ui import estilos


class ClientesView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {estilos.FONDO};")
        self.init_ui()
        self.cargar_clientes()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 20)
        layout.setSpacing(10)

        # ---- Encabezado ----
        header_layout = QHBoxLayout()
        titulo_box = QVBoxLayout()
        titulo_box.setSpacing(2)

        meta = QLabel("CLIENT MANAGEMENT")
        meta.setStyleSheet(estilos.META_PAGINA)
        titulo_box.addWidget(meta)

        titulo = QLabel("Clients")
        titulo.setStyleSheet(estilos.TITULO_PAGINA)
        titulo_box.addWidget(titulo)

        subtitulo = QLabel("Manage your customer base and purchase history.")
        subtitulo.setStyleSheet(estilos.SUBTITULO_PAGINA)
        titulo_box.addWidget(subtitulo)

        header_layout.addLayout(titulo_box)
        header_layout.addStretch()

        self.btn_nuevo = QPushButton("+  New client")
        self.btn_nuevo.setCursor(Qt.PointingHandCursor)
        self.btn_nuevo.setStyleSheet(estilos.BOTON_PRIMARIO)
        self.btn_nuevo.clicked.connect(self.abrir_formulario_nuevo)
        header_layout.addWidget(self.btn_nuevo, alignment=Qt.AlignTop)

        layout.addLayout(header_layout)
        layout.addSpacing(6)

        # ---- Buscador ----
        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Search clients...")
        self.input_busqueda.setStyleSheet(estilos.INPUT)
        self.input_busqueda.setMinimumHeight(38)
        self.input_busqueda.setMaximumWidth(340)
        self.input_busqueda.textChanged.connect(self.cargar_clientes)
        layout.addWidget(self.input_busqueda)

        # ---- Tarjeta con tabla ----
        tarjeta = QWidget()
        tarjeta.setStyleSheet(estilos.TARJETA)
        tarjeta_layout = QVBoxLayout(tarjeta)
        tarjeta_layout.setContentsMargins(0, 0, 0, 0)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Nombre", "Teléfono", "Correo", "Compras", "Acciones"])
        self.tabla.setStyleSheet(estilos.TABLA)
        self.tabla.setShowGrid(False)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.tabla.verticalHeader().setDefaultSectionSize(44)
        tarjeta_layout.addWidget(self.tabla)

        layout.addWidget(tarjeta)

        self.label_contador = QLabel("")
        self.label_contador.setStyleSheet(f"font-size: 12px; color: {estilos.GRIS_TEXTO};")
        layout.addWidget(self.label_contador)

    def cargar_clientes(self):
        texto = self.input_busqueda.text().strip()
        clientes = obtener_clientes(texto_busqueda=texto if texto else None)

        self.tabla.setRowCount(0)
        for fila_idx, cli in enumerate(clientes):
            id_cliente, nombre, apellido, telefono, correo, compras = cli
            nombre_completo = f"{nombre} {apellido or ''}".strip()

            self.tabla.insertRow(fila_idx)
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(nombre_completo))
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(telefono or "-"))
            self.tabla.setItem(fila_idx, 2, QTableWidgetItem(correo or "-"))
            self.tabla.setItem(fila_idx, 3, QTableWidgetItem(str(compras)))

            btn_historial = QPushButton("History")
            btn_historial.setCursor(Qt.PointingHandCursor)
            btn_historial.setStyleSheet(estilos.BOTON_SECUNDARIO)
            btn_historial.clicked.connect(lambda checked, cid=id_cliente, cnombre=nombre_completo: self.ver_historial(cid, cnombre))
            self.tabla.setCellWidget(fila_idx, 4, btn_historial)

        self.label_contador.setText(f"{len(clientes)} clientes mostrados")

    def abrir_formulario_nuevo(self):
        dialogo = FormularioCliente(self)
        if dialogo.exec_() == QDialog.Accepted:
            self.cargar_clientes()

    def ver_historial(self, id_cliente, nombre_cliente):
        compras = obtener_historial_compras(id_cliente)
        if not compras:
            QMessageBox.information(self, "Historial de compras", f"{nombre_cliente} no tiene compras registradas todavía.")
            return

        texto = f"Historial de compras de {nombre_cliente}:\n\n"
        for id_venta, fecha, total, metodo_pago in compras:
            texto += f"Venta #{id_venta} — {fecha} — ${total:.2f} — {metodo_pago}\n"

        QMessageBox.information(self, "Historial de compras", texto)


class FormularioCliente(QDialog):
    """Ventana emergente para registrar un nuevo cliente."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo cliente")
        self.setMinimumWidth(360)
        self.setStyleSheet(f"background-color: {estilos.FONDO};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        titulo = QLabel("Registrar nuevo cliente")
        titulo.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {estilos.VERDE_OSCURO};")
        layout.addWidget(titulo)
        layout.addSpacing(10)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.input_nombre = QLineEdit()
        self.input_nombre.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Nombre*:", self.input_nombre)

        self.input_apellido = QLineEdit()
        self.input_apellido.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Apellido:", self.input_apellido)

        self.input_telefono = QLineEdit()
        self.input_telefono.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Teléfono:", self.input_telefono)

        self.input_correo = QLineEdit()
        self.input_correo.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Correo:", self.input_correo)

        layout.addLayout(form_layout)
        layout.addSpacing(14)

        botones = QDialogButtonBox()
        btn_guardar = QPushButton("Guardar")
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

    def guardar(self):
        nombre = self.input_nombre.text().strip()
        apellido = self.input_apellido.text().strip()
        telefono = self.input_telefono.text().strip()
        correo = self.input_correo.text().strip()

        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return

        ok, resultado = registrar_cliente(nombre, apellido, telefono or None, correo or None)
        if ok:
            QMessageBox.information(self, "Éxito", "Cliente registrado exitosamente")
            self.accept()
        else:
            QMessageBox.warning(self, "Error al registrar cliente", resultado)