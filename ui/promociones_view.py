from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QDialog, QFormLayout, QDoubleSpinBox, QDateEdit
)
from PyQt5.QtCore import Qt, QDate

from models.promocion_model import registrar_promocion, obtener_promociones, esta_vigente
from ui import estilos


class PromocionesView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {estilos.FONDO};")
        self.init_ui()
        self.cargar_promociones()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 20)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        titulo_box = QVBoxLayout()
        titulo_box.setSpacing(2)

        meta = QLabel("PROMOTIONS")
        meta.setStyleSheet(estilos.META_PAGINA)
        titulo_box.addWidget(meta)

        titulo = QLabel("Promotions")
        titulo.setStyleSheet(estilos.TITULO_PAGINA)
        titulo_box.addWidget(titulo)

        subtitulo = QLabel("Create temporary discounts and promotions.")
        subtitulo.setStyleSheet(estilos.SUBTITULO_PAGINA)
        titulo_box.addWidget(subtitulo)

        header_layout.addLayout(titulo_box)
        header_layout.addStretch()

        self.btn_nuevo = QPushButton("+  New promotion")
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
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["Nombre", "Tipo", "Valor", "Inicio", "Fin", "Estado"])
        self.tabla.setStyleSheet(estilos.TABLA)
        self.tabla.setShowGrid(False)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla.verticalHeader().setDefaultSectionSize(42)
        tarjeta_layout.addWidget(self.tabla)

        layout.addWidget(tarjeta)

        self.label_contador = QLabel("")
        self.label_contador.setStyleSheet(f"font-size: 12px; color: {estilos.GRIS_TEXTO};")
        layout.addWidget(self.label_contador)

    def cargar_promociones(self):
        promociones = obtener_promociones()
        self.tabla.setRowCount(0)
        for fila_idx, promo in enumerate(promociones):
            id_promo, nombre, tipo, valor, fecha_inicio, fecha_fin, estado = promo

            self.tabla.insertRow(fila_idx)
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(nombre))

            texto_tipo = "Porcentaje" if tipo == "porcentaje" else "Monto fijo"
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(texto_tipo))

            texto_valor = f"{valor:.0f}%" if tipo == "porcentaje" else f"${valor:.2f}"
            self.tabla.setItem(fila_idx, 2, QTableWidgetItem(texto_valor))

            self.tabla.setItem(fila_idx, 3, QTableWidgetItem(fecha_inicio))
            self.tabla.setItem(fila_idx, 4, QTableWidgetItem(fecha_fin))

            vigente = esta_vigente(fecha_inicio, fecha_fin)
            item_estado = QTableWidgetItem("Vigente" if vigente else "No vigente")
            item_estado.setForeground(Qt.darkGreen if vigente else Qt.gray)
            self.tabla.setItem(fila_idx, 5, item_estado)

        self.label_contador.setText(f"{len(promociones)} promociones registradas")

    def abrir_formulario_nuevo(self):
        dialogo = FormularioPromocion(self)
        if dialogo.exec_() == QDialog.Accepted:
            self.cargar_promociones()


class FormularioPromocion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nueva promoción")
        self.setMinimumWidth(380)
        self.setStyleSheet(f"background-color: {estilos.FONDO};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        titulo = QLabel("Crear nueva promoción")
        titulo.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {estilos.VERDE_OSCURO};")
        layout.addWidget(titulo)
        layout.addSpacing(10)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.input_nombre = QLineEdit()
        self.input_nombre.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Nombre*:", self.input_nombre)

        self.combo_tipo = QComboBox()
        self.combo_tipo.setStyleSheet(estilos.INPUT)
        self.combo_tipo.addItem("Porcentaje (%)", "porcentaje")
        self.combo_tipo.addItem("Monto fijo ($)", "monto_fijo")
        form_layout.addRow("Tipo de descuento:", self.combo_tipo)

        self.spin_valor = QDoubleSpinBox()
        self.spin_valor.setMaximum(999999)
        self.spin_valor.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Valor*:", self.spin_valor)

        self.fecha_inicio = QDateEdit(calendarPopup=True)
        self.fecha_inicio.setDate(QDate.currentDate())
        self.fecha_inicio.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Fecha inicio*:", self.fecha_inicio)

        self.fecha_fin = QDateEdit(calendarPopup=True)
        self.fecha_fin.setDate(QDate.currentDate().addDays(7))
        self.fecha_fin.setStyleSheet(estilos.INPUT)
        form_layout.addRow("Fecha fin*:", self.fecha_fin)

        layout.addLayout(form_layout)
        layout.addSpacing(14)

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
        tipo = self.combo_tipo.currentData()
        valor = self.spin_valor.value()
        fecha_inicio = self.fecha_inicio.date().toString("yyyy-MM-dd")
        fecha_fin = self.fecha_fin.date().toString("yyyy-MM-dd")

        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return

        ok, resultado = registrar_promocion(nombre, tipo, valor, fecha_inicio, fecha_fin)
        if ok:
            QMessageBox.information(self, "Éxito", "Promoción creada exitosamente")
            self.accept()
        else:
            QMessageBox.warning(self, "Error al crear promoción", resultado)