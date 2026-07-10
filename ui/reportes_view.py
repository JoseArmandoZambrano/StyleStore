from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDateEdit,
    QSpinBox, QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
    QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from datetime import datetime

from models.reporte_model import (
    reporte_ventas_por_periodo, reporte_bajo_stock,
    exportar_ventas_a_csv, exportar_bajo_stock_a_csv
)
from ui import estilos


class ReportesView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {estilos.FONDO};")
        self.ventas_actuales = []
        self.stock_actual = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 20)
        layout.setSpacing(10)

        titulo_box = QVBoxLayout()
        titulo_box.setSpacing(2)
        meta = QLabel("REPORTS")
        meta.setStyleSheet(estilos.META_PAGINA)
        titulo_box.addWidget(meta)
        titulo = QLabel("Reports")
        titulo.setStyleSheet(estilos.TITULO_PAGINA)
        titulo_box.addWidget(titulo)
        subtitulo = QLabel("Generate operational reports to support decision making.")
        subtitulo.setStyleSheet(estilos.SUBTITULO_PAGINA)
        titulo_box.addWidget(subtitulo)
        layout.addLayout(titulo_box)
        layout.addSpacing(6)

        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{ border: none; }}
            QTabBar::tab {{
                background: white; border: 1px solid {estilos.BORDE};
                padding: 8px 18px; margin-right: 4px; border-radius: 8px 8px 0 0;
                font-size: 13px; color: #666;
            }}
            QTabBar::tab:selected {{ background: {estilos.VERDE_OSCURO}; color: white; }}
        """)

        tabs.addTab(self._crear_tab_ventas(), "Ventas por periodo")
        tabs.addTab(self._crear_tab_stock(), "Bajo stock")

        layout.addWidget(tabs)

    def _crear_tab_ventas(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 16, 0, 0)

        filtros_layout = QHBoxLayout()
        filtros_layout.setSpacing(10)

        self.fecha_inicio = QDateEdit(calendarPopup=True)
        self.fecha_inicio.setDate(QDate.currentDate().addMonths(-1))
        self.fecha_inicio.setStyleSheet(estilos.INPUT)
        self.fecha_inicio.setMinimumHeight(36)
        filtros_layout.addWidget(QLabel("Desde:"))
        filtros_layout.addWidget(self.fecha_inicio)

        self.fecha_fin = QDateEdit(calendarPopup=True)
        self.fecha_fin.setDate(QDate.currentDate())
        self.fecha_fin.setStyleSheet(estilos.INPUT)
        self.fecha_fin.setMinimumHeight(36)
        filtros_layout.addWidget(QLabel("Hasta:"))
        filtros_layout.addWidget(self.fecha_fin)

        btn_generar = QPushButton("Generar")
        btn_generar.setCursor(Qt.PointingHandCursor)
        btn_generar.setStyleSheet(estilos.BOTON_PRIMARIO)
        btn_generar.clicked.connect(self.generar_reporte_ventas)
        filtros_layout.addWidget(btn_generar)

        self.btn_exportar_ventas = QPushButton("⬇  Exportar a CSV")
        self.btn_exportar_ventas.setCursor(Qt.PointingHandCursor)
        self.btn_exportar_ventas.setStyleSheet(estilos.BOTON_SECUNDARIO)
        self.btn_exportar_ventas.clicked.connect(self.exportar_ventas)
        self.btn_exportar_ventas.setEnabled(False)
        filtros_layout.addWidget(self.btn_exportar_ventas)

        filtros_layout.addStretch()

        layout.addLayout(filtros_layout)

        tarjeta = QWidget()
        tarjeta.setStyleSheet(estilos.TARJETA)
        tarjeta_layout = QVBoxLayout(tarjeta)
        tarjeta_layout.setContentsMargins(0, 0, 0, 0)

        self.tabla_ventas = QTableWidget()
        self.tabla_ventas.setColumnCount(5)
        self.tabla_ventas.setHorizontalHeaderLabels(["ID Venta", "Fecha", "Cliente", "Total", "Método de pago"])
        self.tabla_ventas.setStyleSheet(estilos.TABLA)
        self.tabla_ventas.setShowGrid(False)
        self.tabla_ventas.verticalHeader().setVisible(False)
        self.tabla_ventas.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_ventas.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.tabla_ventas.verticalHeader().setDefaultSectionSize(40)
        tarjeta_layout.addWidget(self.tabla_ventas)

        layout.addWidget(tarjeta)

        self.label_total_periodo = QLabel("Total acumulado: $0.00")
        self.label_total_periodo.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {estilos.VERDE_OSCURO}; padding-top: 6px;")
        layout.addWidget(self.label_total_periodo)

        return widget

    def generar_reporte_ventas(self):
        fecha_inicio = self.fecha_inicio.date().toString("yyyy-MM-dd")
        fecha_fin = self.fecha_fin.date().toString("yyyy-MM-dd")

        self.ventas_actuales = reporte_ventas_por_periodo(fecha_inicio, fecha_fin)

        self.tabla_ventas.setRowCount(0)
        total_acumulado = 0
        for fila_idx, venta in enumerate(self.ventas_actuales):
            id_venta, fecha, cliente, total, metodo_pago = venta
            self.tabla_ventas.insertRow(fila_idx)
            self.tabla_ventas.setItem(fila_idx, 0, QTableWidgetItem(str(id_venta)))
            self.tabla_ventas.setItem(fila_idx, 1, QTableWidgetItem(str(fecha)))
            self.tabla_ventas.setItem(fila_idx, 2, QTableWidgetItem(cliente))
            self.tabla_ventas.setItem(fila_idx, 3, QTableWidgetItem(f"${total:.2f}"))
            self.tabla_ventas.setItem(fila_idx, 4, QTableWidgetItem(metodo_pago or "-"))
            total_acumulado += total

        self.label_total_periodo.setText(f"Total acumulado: ${total_acumulado:.2f} ({len(self.ventas_actuales)} ventas)")
        self.btn_exportar_ventas.setEnabled(len(self.ventas_actuales) > 0)

    def exportar_ventas(self):
        if not self.ventas_actuales:
            QMessageBox.information(self, "Sin datos", "Genera el reporte antes de exportarlo.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_sugerido = f"reporte_ventas_{timestamp}.csv"

        ruta_archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar reporte de ventas", nombre_sugerido, "Archivo CSV (*.csv)"
        )
        if not ruta_archivo:
            return

        ok, resultado = exportar_ventas_a_csv(self.ventas_actuales, ruta_archivo)
        if ok:
            QMessageBox.information(self, "Reporte exportado", f"El reporte se guardó exitosamente en:\n{resultado}")
        else:
            QMessageBox.warning(self, "Error al exportar", resultado)

    def _crear_tab_stock(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 16, 0, 0)

        filtros_layout = QHBoxLayout()
        filtros_layout.setSpacing(10)

        filtros_layout.addWidget(QLabel("Umbral mínimo:"))
        self.spin_umbral = QSpinBox()
        self.spin_umbral.setMinimum(1)
        self.spin_umbral.setMaximum(999)
        self.spin_umbral.setValue(5)
        self.spin_umbral.setStyleSheet(estilos.INPUT)
        self.spin_umbral.setMinimumHeight(36)
        self.spin_umbral.setMaximumWidth(80)
        filtros_layout.addWidget(self.spin_umbral)

        btn_generar = QPushButton("Generar")
        btn_generar.setCursor(Qt.PointingHandCursor)
        btn_generar.setStyleSheet(estilos.BOTON_PRIMARIO)
        btn_generar.clicked.connect(self.generar_reporte_stock)
        filtros_layout.addWidget(btn_generar)

        self.btn_exportar_stock = QPushButton("⬇  Exportar a CSV")
        self.btn_exportar_stock.setCursor(Qt.PointingHandCursor)
        self.btn_exportar_stock.setStyleSheet(estilos.BOTON_SECUNDARIO)
        self.btn_exportar_stock.clicked.connect(self.exportar_stock)
        self.btn_exportar_stock.setEnabled(False)
        filtros_layout.addWidget(self.btn_exportar_stock)

        filtros_layout.addStretch()

        layout.addLayout(filtros_layout)

        tarjeta = QWidget()
        tarjeta.setStyleSheet(estilos.TARJETA)
        tarjeta_layout = QVBoxLayout(tarjeta)
        tarjeta_layout.setContentsMargins(0, 0, 0, 0)

        self.tabla_stock = QTableWidget()
        self.tabla_stock.setColumnCount(7)
        self.tabla_stock.setHorizontalHeaderLabels(["SKU", "Nombre", "Categoría", "Talla", "Color", "Stock", "Proveedor"])
        self.tabla_stock.setStyleSheet(estilos.TABLA)
        self.tabla_stock.setShowGrid(False)
        self.tabla_stock.verticalHeader().setVisible(False)
        self.tabla_stock.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_stock.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla_stock.verticalHeader().setDefaultSectionSize(40)
        tarjeta_layout.addWidget(self.tabla_stock)

        layout.addWidget(tarjeta)
        return widget

    def generar_reporte_stock(self):
        umbral = self.spin_umbral.value()
        self.stock_actual = reporte_bajo_stock(umbral)

        self.tabla_stock.setRowCount(0)
        for fila_idx, prod in enumerate(self.stock_actual):
            sku, nombre, categoria, talla, color, stock, proveedor = prod
            self.tabla_stock.insertRow(fila_idx)
            self.tabla_stock.setItem(fila_idx, 0, QTableWidgetItem(sku))
            self.tabla_stock.setItem(fila_idx, 1, QTableWidgetItem(nombre))
            self.tabla_stock.setItem(fila_idx, 2, QTableWidgetItem(categoria or "-"))
            self.tabla_stock.setItem(fila_idx, 3, QTableWidgetItem(talla or "-"))
            self.tabla_stock.setItem(fila_idx, 4, QTableWidgetItem(color or "-"))

            item_stock = QTableWidgetItem(str(stock))
            item_stock.setForeground(Qt.red)
            self.tabla_stock.setItem(fila_idx, 5, item_stock)

            self.tabla_stock.setItem(fila_idx, 6, QTableWidgetItem(proveedor or "-"))

        self.btn_exportar_stock.setEnabled(len(self.stock_actual) > 0)

    def exportar_stock(self):
        if not self.stock_actual:
            QMessageBox.information(self, "Sin datos", "Genera el reporte antes de exportarlo.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_sugerido = f"reporte_bajo_stock_{timestamp}.csv"

        ruta_archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar reporte de bajo stock", nombre_sugerido, "Archivo CSV (*.csv)"
        )
        if not ruta_archivo:
            return

        ok, resultado = exportar_bajo_stock_a_csv(self.stock_actual, ruta_archivo)
        if ok:
            QMessageBox.information(self, "Reporte exportado", f"El reporte se guardó exitosamente en:\n{resultado}")
        else:
            QMessageBox.warning(self, "Error al exportar", resultado)