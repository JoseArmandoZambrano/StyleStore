# Paleta de colores basada en los mockups de StyleStore
VERDE_OSCURO = "#1e3a2f"
VERDE_HOVER = "#2a4d3e"
FONDO = "#f0ede6"
BLANCO = "#ffffff"
BORDE = "#ddd8d0"
GRIS_TEXTO = "#888888"
GRIS_OSCURO = "#333333"
TEAL_BG = "#e1f5ee"
TEAL_TEXT = "#0f6e56"
AMBER_BG = "#faeeda"
AMBER_TEXT = "#854f0b"
ROJO_BG = "#fcebeb"
ROJO_TEXT = "#a32d2d"
AZUL_BG = "#e6f1fb"
AZUL_TEXT = "#185fa5"
ROSA_BG = "#fbeaf0"
ROSA_TEXT = "#993556"


TOPBAR = f"background-color: {VERDE_OSCURO};"

SIDEBAR = f"background-color: {BLANCO}; border-right: 1px solid {BORDE};"

BOTON_SIDEBAR = f"""
    QPushButton {{
        text-align: left;
        padding: 10px 16px;
        border: none;
        font-size: 13px;
        color: #444;
        background-color: transparent;
        border-radius: 0px;
    }}
    QPushButton:hover {{
        background-color: {FONDO};
        color: {VERDE_OSCURO};
    }}
"""

BOTON_SIDEBAR_ACTIVO = f"""
    QPushButton {{
        text-align: left;
        padding: 10px 16px;
        border: none;
        border-left: 3px solid {VERDE_OSCURO};
        font-size: 13px;
        font-weight: bold;
        color: {VERDE_OSCURO};
        background-color: {FONDO};
    }}
"""

BOTON_PRIMARIO = f"""
    QPushButton {{
        background-color: {VERDE_OSCURO};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 18px;
        font-size: 13px;
        font-weight: 500;
    }}
    QPushButton:hover {{ background-color: {VERDE_HOVER}; }}
"""

BOTON_SECUNDARIO = f"""
    QPushButton {{
        background-color: white;
        color: #444;
        border: 1px solid {BORDE};
        border-radius: 8px;
        padding: 9px 16px;
        font-size: 13px;
    }}
    QPushButton:hover {{ background-color: {FONDO}; }}
"""

BOTON_PELIGRO = f"""
    QPushButton {{
        background-color: white;
        border: 1px solid {BORDE};
        border-radius: 6px;
        padding: 5px 12px;
        font-size: 12px;
        color: {ROJO_TEXT};
    }}
    QPushButton:hover {{ background-color: {ROJO_BG}; }}
"""

INPUT = f"""
    QLineEdit, QComboBox {{
        background-color: white;
        border: 1px solid {BORDE};
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 13px;
        color: #333;
    }}
    QLineEdit:focus, QComboBox:focus {{
        border: 1px solid {VERDE_OSCURO};
    }}
"""

TARJETA = f"""
    background-color: white;
    border: 1px solid {BORDE};
    border-radius: 12px;
"""

TABLA = f"""
    QTableWidget {{
        background-color: white;
        border: 1px solid {BORDE};
        border-radius: 8px;
        gridline-color: {FONDO};
        font-size: 13px;
    }}
    QHeaderView::section {{
        background-color: white;
        color: {GRIS_TEXTO};
        font-size: 11px;
        font-weight: bold;
        border: none;
        border-bottom: 1px solid #eee;
        padding: 10px 8px;
    }}
    QTableWidget::item {{
        padding: 6px;
        border-bottom: 1px solid {FONDO};
    }}
"""

TITULO_PAGINA = f"font-size: 26px; color: {VERDE_OSCURO}; font-weight: bold; font-family: Georgia, serif;"
SUBTITULO_PAGINA = f"font-size: 13px; color: {GRIS_TEXTO};"
META_PAGINA = f"font-size: 11px; color: {GRIS_TEXTO}; letter-spacing: 1px; font-weight: bold;"


def badge(texto, tipo="teal"):
    """Retorna un QLabel con estilo de 'badge' redondeado, tipo: teal, amber, red."""
    colores = {
        "teal": (TEAL_BG, TEAL_TEXT),
        "amber": (AMBER_BG, AMBER_TEXT),
        "red": (ROJO_BG, ROJO_TEXT),
        "blue": (AZUL_BG, AZUL_TEXT),
        "pink": (ROSA_BG, ROSA_TEXT),
    }
    bg, color = colores.get(tipo, colores["teal"])
    return f"background-color: {bg}; color: {color}; border-radius: 10px; padding: 3px 10px; font-size: 11px; font-weight: 500;"