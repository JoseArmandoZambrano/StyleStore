from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton
)
from PyQt5.QtCore import Qt

from models.dashboard_model import obtener_estadisticas, obtener_ventas_recientes, contar_bajo_stock
from ui import estilos


class HomeView(QWidget):
    def __init__(self, ir_a_pantalla_callback=None):
        super().__init__()
        self.setStyleSheet(f"background-color: {estilos.FONDO};")
        self.ir_a_pantalla_callback = ir_a_pantalla_callback
        self.init_ui()
        self.cargar_datos()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 20)
        layout.setSpacing(10)

        meta = QLabel("OVERVIEW")
        meta.setStyleSheet(estilos.META_PAGINA)
        layout.addWidget(meta)

        titulo = QLabel("Dashboard")
        titulo.setStyleSheet(estilos.TITULO_PAGINA)
        layout.addWidget(titulo)

        subtitulo = QLabel("General summary of your store's activity.")
        subtitulo.setStyleSheet(estilos.SUBTITULO_PAGINA)
        layout.addWidget(subtitulo)

        layout.addSpacing(10)

        # ---- Tarjetas de estadísticas ----
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)

        self.card_productos = self._crear_stat_card("PRODUCTS")
        self.card_clientes = self._crear_stat_card("CLIENTS")
        self.card_ventas = self._crear_stat_card("SALES TODAY")
        self.card_ingresos = self._crear_stat_card("REVENUE TODAY")

        stats_layout.addWidget(self.card_productos["widget"])
        stats_layout.addWidget(self.card_clientes["widget"])
        stats_layout.addWidget(self.card_ventas["widget"])
        stats_layout.addWidget(self.card_ingresos["widget"])

        layout.addLayout(stats_layout)
        layout.addSpacing(10)

        # ---- Dos columnas: ventas recientes | accesos rápidos ----
        columnas_layout = QHBoxLayout()
        columnas_layout.setSpacing(16)

        # Ventas recientes
        panel_ventas = QWidget()
        panel_ventas.setStyleSheet(estilos.TARJETA)
        panel_ventas_layout = QVBoxLayout(panel_ventas)
        panel_ventas_layout.setContentsMargins(16, 16, 16, 16)

        label_ventas = QLabel("Recent sales")
        label_ventas.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {estilos.VERDE_OSCURO};")
        panel_ventas_layout.addWidget(label_ventas)

        self.tabla_ventas = QTableWidget()
        self.tabla_ventas.setColumnCount(4)
        self.tabla_ventas.setHorizontalHeaderLabels(["Client", "Items", "Total", "Payment"])
        self.tabla_ventas.setStyleSheet(estilos.TABLA)
        self.tabla_ventas.setShowGrid(False)
        self.tabla_ventas.verticalHeader().setVisible(False)
        self.tabla_ventas.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_ventas.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla_ventas.verticalHeader().setDefaultSectionSize(38)
        panel_ventas_layout.addWidget(self.tabla_ventas)

        columnas_layout.addWidget(panel_ventas, stretch=3)

        # Accesos rápidos
        panel_accesos = QWidget()
        panel_accesos.setStyleSheet(estilos.TARJETA)
        panel_accesos_layout = QVBoxLayout(panel_accesos)
        panel_accesos_layout.setContentsMargins(16, 16, 16, 16)
        panel_accesos_layout.setSpacing(4)

        label_accesos = QLabel("Quick access")
        label_accesos.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {estilos.VERDE_OSCURO};")
        panel_accesos_layout.addWidget(label_accesos)
        panel_accesos_layout.addSpacing(6)

        accesos = [
            ("+ New sale", 3),
            ("+ Add product", 1),
            ("+ Register client", 2),
            ("View low stock report", 6),
            ("Run backup", 7),
        ]
        for texto, indice in accesos:
            btn = QPushButton(texto)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left; border: none; background: transparent;
                    padding: 8px 4px; font-size: 13px; color: #333;
                }
                QPushButton:hover { color: %s; }
            """ % estilos.VERDE_OSCURO)
            if self.ir_a_pantalla_callback:
                btn.clicked.connect(lambda checked, i=indice: self.ir_a_pantalla_callback(i))
            panel_accesos_layout.addWidget(btn)

        panel_accesos_layout.addStretch()
        columnas_layout.addWidget(panel_accesos, stretch=2)

        layout.addLayout(columnas_layout)

    def _crear_stat_card(self, etiqueta):
        widget = QWidget()
        widget.setStyleSheet(estilos.TARJETA)
        card_layout = QVBoxLayout(widget)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(4)

        label = QLabel(etiqueta)
        label.setStyleSheet(f"font-size: 11px; color: {estilos.GRIS_TEXTO}; letter-spacing: 1px; font-weight: bold;")
        card_layout.addWidget(label)

        valor = QLabel("0")
        valor.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {estilos.VERDE_OSCURO};")
        card_layout.addWidget(valor)

        return {"widget": widget, "valor": valor}

    def cargar_datos(self):
        stats = obtener_estadisticas()
        self.card_productos["valor"].setText(str(stats["productos"]))
        self.card_clientes["valor"].setText(str(stats["clientes"]))
        self.card_ventas["valor"].setText(str(stats["ventas_hoy"]))
        self.card_ingresos["valor"].setText(f"${stats['ingresos_hoy']:.2f}")

        ventas = obtener_ventas_recientes(limite=6)
        self.tabla_ventas.setRowCount(0)
        for fila_idx, venta in enumerate(ventas):
            id_venta, cliente, items, total, metodo_pago = venta
            self.tabla_ventas.insertRow(fila_idx)
            self.tabla_ventas.setItem(fila_idx, 0, QTableWidgetItem(cliente))
            self.tabla_ventas.setItem(fila_idx, 1, QTableWidgetItem(str(items)))
            self.tabla_ventas.setItem(fila_idx, 2, QTableWidgetItem(f"${total:.2f}"))
            self.tabla_ventas.setItem(fila_idx, 3, QTableWidgetItem(metodo_pago or "-"))