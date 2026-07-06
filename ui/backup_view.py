from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt

from models.backup_model import realizar_backup, restaurar_backup
from ui import estilos


class BackupView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {estilos.FONDO};")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 20)
        layout.setSpacing(10)

        titulo_box = QVBoxLayout()
        titulo_box.setSpacing(2)
        meta = QLabel("SYSTEM CONFIGURATION")
        meta.setStyleSheet(estilos.META_PAGINA)
        titulo_box.addWidget(meta)
        titulo = QLabel("Backup & Restore")
        titulo.setStyleSheet(estilos.TITULO_PAGINA)
        titulo_box.addWidget(titulo)
        subtitulo = QLabel("Protect your data with regular backups.")
        subtitulo.setStyleSheet(estilos.SUBTITULO_PAGINA)
        titulo_box.addWidget(subtitulo)
        layout.addLayout(titulo_box)
        layout.addSpacing(16)

        # ---- Tarjeta de Backup ----
        tarjeta_backup = QWidget()
        tarjeta_backup.setStyleSheet(estilos.TARJETA)
        tarjeta_backup.setMaximumWidth(500)
        backup_layout = QVBoxLayout(tarjeta_backup)
        backup_layout.setContentsMargins(20, 20, 20, 20)
        backup_layout.setSpacing(8)

        label_backup_titulo = QLabel("Realizar respaldo")
        label_backup_titulo.setStyleSheet(f"font-size: 15px; font-weight: bold; color: {estilos.VERDE_OSCURO};")
        backup_layout.addWidget(label_backup_titulo)

        label_backup_desc = QLabel("Genera una copia de seguridad del archivo de base de datos en una carpeta local.")
        label_backup_desc.setWordWrap(True)
        label_backup_desc.setStyleSheet(f"font-size: 12px; color: {estilos.GRIS_TEXTO};")
        backup_layout.addWidget(label_backup_desc)

        backup_layout.addSpacing(8)
        btn_backup = QPushButton("Realizar Backup")
        btn_backup.setCursor(Qt.PointingHandCursor)
        btn_backup.setStyleSheet(estilos.BOTON_PRIMARIO)
        btn_backup.clicked.connect(self.realizar_backup)
        backup_layout.addWidget(btn_backup)

        layout.addWidget(tarjeta_backup)
        layout.addSpacing(16)

        # ---- Tarjeta de Restaurar ----
        tarjeta_restaurar = QWidget()
        tarjeta_restaurar.setStyleSheet(estilos.TARJETA)
        tarjeta_restaurar.setMaximumWidth(500)
        restaurar_layout = QVBoxLayout(tarjeta_restaurar)
        restaurar_layout.setContentsMargins(20, 20, 20, 20)
        restaurar_layout.setSpacing(8)

        label_restaurar_titulo = QLabel("Restaurar base de datos")
        label_restaurar_titulo.setStyleSheet(f"font-size: 15px; font-weight: bold; color: {estilos.ROJO_TEXT};")
        restaurar_layout.addWidget(label_restaurar_titulo)

        label_restaurar_desc = QLabel("⚠ Esta operación sobreescribirá todos los datos actuales con los del archivo de backup seleccionado.")
        label_restaurar_desc.setWordWrap(True)
        label_restaurar_desc.setStyleSheet(f"font-size: 12px; color: {estilos.GRIS_TEXTO};")
        restaurar_layout.addWidget(label_restaurar_desc)

        restaurar_layout.addSpacing(8)
        btn_restaurar = QPushButton("Restaurar desde archivo")
        btn_restaurar.setCursor(Qt.PointingHandCursor)
        btn_restaurar.setStyleSheet(estilos.BOTON_SECUNDARIO)
        btn_restaurar.clicked.connect(self.restaurar_backup)
        restaurar_layout.addWidget(btn_restaurar)

        layout.addWidget(tarjeta_restaurar)
        layout.addStretch()

    def realizar_backup(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Selecciona la carpeta de destino para el backup")
        if not carpeta:
            return

        ok, resultado = realizar_backup(carpeta)
        if ok:
            QMessageBox.information(self, "Backup realizado", f"Backup realizado exitosamente en:\n{resultado}")
        else:
            QMessageBox.warning(self, "Error al realizar backup", resultado)

    def restaurar_backup(self):
        respuesta = QMessageBox.warning(
            self, "Confirmar restauración",
            "Esta operación sobreescribirá todos los datos actuales.\n¿Deseas continuar?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta != QMessageBox.Yes:
            return

        archivo, _ = QFileDialog.getOpenFileName(self, "Selecciona el archivo de backup", "", "Archivos de base de datos (*.db)")
        if not archivo:
            return

        ok, mensaje = restaurar_backup(archivo)
        if ok:
            QMessageBox.information(self, "Restauración exitosa", mensaje)
        else:
            QMessageBox.warning(self, "Error al restaurar", mensaje)