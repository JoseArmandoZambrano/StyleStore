import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from database.db_setup import crear_tablas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StyleStore - Retail Manager")
        self.resize(1100, 700)
        self.setStyleSheet("background-color: #f0ede6;")

        contenedor = QWidget()
        layout_principal = QVBoxLayout(contenedor)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # ---- Barra superior ----
        topbar = QFrame()
        topbar.setFixedHeight(52)
        topbar.setStyleSheet("background-color: #1e3a2f;")
        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(20, 0, 20, 0)

        titulo = QLabel("StyleStore")
        titulo.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        topbar_layout.addWidget(titulo)
        topbar_layout.addStretch()

        layout_principal.addWidget(topbar)

        # ---- Cuerpo: sidebar + contenido ----
        cuerpo = QWidget()
        cuerpo_layout = QHBoxLayout(cuerpo)
        cuerpo_layout.setContentsMargins(0, 0, 0, 0)
        cuerpo_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: white; border-right: 1px solid #ddd8d0;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 0)
        sidebar_layout.setSpacing(4)
        sidebar_layout.setAlignment(Qt.AlignTop)

        opciones = ["Home", "Products", "Clients", "Sales", "Suppliers", "Promotions", "Reports", "Backup"]
        for opcion in opciones:
            boton = QPushButton(opcion)
            boton.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 10px 16px;
                    border: none;
                    font-size: 13px;
                    color: #444;
                    background-color: transparent;
                }
                QPushButton:hover {
                    background-color: #f0ede6;
                    color: #1e3a2f;
                }
            """)
            sidebar_layout.addWidget(boton)

        cuerpo_layout.addWidget(sidebar)

        # Contenido principal
        contenido = QFrame()
        contenido_layout = QVBoxLayout(contenido)
        contenido_layout.setContentsMargins(28, 28, 28, 20)

        bienvenida = QLabel("Bienvenido a StyleStore")
        bienvenida.setStyleSheet("font-size: 26px; color: #1e3a2f; font-weight: bold;")
        contenido_layout.addWidget(bienvenida)

        subtitulo = QLabel("El sistema está funcionando correctamente. La base de datos ya está lista.")
        subtitulo.setStyleSheet("font-size: 13px; color: #888;")
        contenido_layout.addWidget(subtitulo)

        contenido_layout.addStretch()

        cuerpo_layout.addWidget(contenido)
        layout_principal.addWidget(cuerpo)

        self.setCentralWidget(contenedor)


if __name__ == "__main__":
    crear_tablas()  # asegura que la BD y tablas existan al iniciar
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())