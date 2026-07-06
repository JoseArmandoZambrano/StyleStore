import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from database.db_setup import crear_tablas
from ui.productos_view import ProductosView
from ui import estilos
from ui.clientes_view import ClientesView
from ui.ventas_view import VentasView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StyleStore - Retail Manager")
        self.resize(1200, 740)
        self.setStyleSheet(f"background-color: {estilos.FONDO};")

        self.botones_sidebar = {}

        contenedor = QWidget()
        layout_principal = QVBoxLayout(contenedor)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # ---- Barra superior ----
        topbar = QFrame()
        topbar.setFixedHeight(56)
        topbar.setStyleSheet(estilos.TOPBAR)
        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(24, 0, 24, 0)

        marca_layout = QVBoxLayout()
        marca_layout.setSpacing(0)
        sub = QLabel("RETAIL MANAGER")
        sub.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 10px; letter-spacing: 1px;")
        marca_layout.addWidget(sub)
        titulo = QLabel("StyleStore")
        titulo.setStyleSheet("color: white; font-size: 19px; font-weight: bold; font-family: Georgia, serif;")
        marca_layout.addWidget(titulo)
        topbar_layout.addLayout(marca_layout)
        topbar_layout.addStretch()

        avatar = QLabel("AM")
        avatar.setFixedSize(32, 32)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet("background-color: #4a7c5f; color: white; border-radius: 16px; font-size: 11px; font-weight: bold;")
        topbar_layout.addWidget(avatar)

        layout_principal.addWidget(topbar)

        # ---- Cuerpo: sidebar + contenido ----
        cuerpo = QWidget()
        cuerpo_layout = QHBoxLayout(cuerpo)
        cuerpo_layout.setContentsMargins(0, 0, 0, 0)
        cuerpo_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setFixedWidth(210)
        sidebar.setStyleSheet(estilos.SIDEBAR)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 0)
        sidebar_layout.setSpacing(2)
        sidebar_layout.setAlignment(Qt.AlignTop)

        label_menu = QLabel("MAIN MENU")
        label_menu.setStyleSheet(f"color: {estilos.GRIS_TEXTO}; font-size: 10px; letter-spacing: 1px; padding: 0 16px 8px 16px;")
        sidebar_layout.addWidget(label_menu)

        self.stack = QStackedWidget()

        self.pantalla_home = QLabel("Bienvenido a StyleStore\n\nLa base de datos y el sistema ya están funcionando.")
        self.pantalla_home.setStyleSheet(f"font-size: 20px; color: {estilos.VERDE_OSCURO}; padding: 28px;")
        self.pantalla_home.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.pantalla_productos = ProductosView()
        self.pantalla_clientes = ClientesView()
        self.pantalla_ventas = VentasView()

        self.stack.addWidget(self.pantalla_home)       # índice 0
        self.stack.addWidget(self.pantalla_productos)  # índice 1
        self.stack.addWidget(self.pantalla_clientes)   # índice 2
        self.stack.addWidget(self.pantalla_ventas)     # índice 3

        opciones = [
            ("Home", 0),
            ("Products", 1),
            ("Clients", 2),
            ("Sales", 3),
            ("Suppliers", None),
            ("Promotions", None),
            ("Reports", None),
            ("Backup", None),
        ]
        for nombre, indice in opciones:
            boton = QPushButton(nombre)
            boton.setCursor(Qt.PointingHandCursor)
            boton.setStyleSheet(estilos.BOTON_SIDEBAR)
            if indice is not None:
                boton.clicked.connect(lambda checked, i=indice, n=nombre: self.cambiar_pantalla(i, n))
                self.botones_sidebar[nombre] = boton
            else:
                boton.setEnabled(False)
                boton.setStyleSheet(estilos.BOTON_SIDEBAR + "QPushButton { color: #ccc; }")
            sidebar_layout.addWidget(boton)

        self.botones_sidebar["Home"].setStyleSheet(estilos.BOTON_SIDEBAR_ACTIVO)

        cuerpo_layout.addWidget(sidebar)
        cuerpo_layout.addWidget(self.stack)
        layout_principal.addWidget(cuerpo)

        self.setCentralWidget(contenedor)

    def cambiar_pantalla(self, indice, nombre):
        self.stack.setCurrentIndex(indice)
        for nombre_boton, boton in self.botones_sidebar.items():
            if nombre_boton == nombre:
                boton.setStyleSheet(estilos.BOTON_SIDEBAR_ACTIVO)
            else:
                boton.setStyleSheet(estilos.BOTON_SIDEBAR)


if __name__ == "__main__":
    crear_tablas()
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())