"""
Script para poblar StyleStore con datos de ejemplo.
Útil para demostraciones y pruebas ante el profesor.
Ejecutar UNA sola vez: python seed_data.py
"""

from database.db_setup import crear_tablas
from models.categoria_model import registrar_categoria
from models.proveedor_model import registrar_proveedor
from models.producto_model import registrar_producto
from models.cliente_model import registrar_cliente
from models.promocion_model import registrar_promocion
from models.venta_model import registrar_venta
from datetime import datetime, timedelta

crear_tablas()

print("=== Insertando categorías ===")
categorias = ["Playeras", "Jeans", "Vestidos", "Chamarras", "Sudaderas"]
ids_categorias = {}
for nombre in categorias:
    ok, resultado = registrar_categoria(nombre, f"Categoría de {nombre.lower()}")
    if ok:
        ids_categorias[nombre] = resultado
        print(f"  ✓ {nombre}")
    else:
        print(f"  - {nombre} (ya existía)")

print("\n=== Insertando proveedores ===")
proveedores = [
    ("Textiles del Norte", "Juan Pérez", "3311112222", "contacto@textilesnorte.com", "Guadalajara, Jalisco"),
    ("Confecciones GDL", "María López", "3313334444", "ventas@confeccionesgdl.com", "Zapopan, Jalisco"),
    ("Moda Urbana MX", "Carlos Ruiz", "3315556666", "info@modaurbana.mx", "Tlaquepaque, Jalisco"),
]
ids_proveedores = {}
for nombre, contacto, telefono, correo, direccion in proveedores:
    ok, resultado = registrar_proveedor(nombre, contacto, telefono, correo, direccion)
    if ok:
        ids_proveedores[nombre] = resultado
        print(f"  ✓ {nombre}")
    else:
        print(f"  - {nombre} ({resultado})")

print("\n=== Insertando productos ===")
# (nombre, categoria, talla, color, precio_compra, precio_venta, stock, proveedor, descripcion)
productos = [
    ("Playera básica", "Playeras", "M", "Blanco", 90, 150, 40, "Textiles del Norte", "Playera de algodón 100%"),
    ("Playera básica", "Playeras", "L", "Negro", 90, 150, 3, "Textiles del Norte", "Playera de algodón 100%"),
    ("Playera estampada", "Playeras", "M", "Azul", 110, 190, 22, "Textiles del Norte", "Playera con estampado frontal"),
    ("Jeans slim fit", "Jeans", "30", "Azul", 250, 450, 15, "Confecciones GDL", "Corte entallado, mezclilla stretch"),
    ("Jeans recto", "Jeans", "32", "Negro", 240, 430, 2, "Confecciones GDL", "Corte recto clásico"),
    ("Vestido floral", "Vestidos", "S", "Rosa", 320, 590, 8, "Moda Urbana MX", "Vestido casual de verano"),
    ("Vestido de noche", "Vestidos", "M", "Negro", 480, 890, 5, "Moda Urbana MX", "Vestido elegante para eventos"),
    ("Chamarra bomber", "Chamarras", "M", "Verde olivo", 380, 690, 12, "Moda Urbana MX", "Chamarra estilo bomber"),
    ("Chamarra de mezclilla", "Chamarras", "L", "Azul", 350, 650, 1, "Confecciones GDL", "Chamarra de mezclilla clásica"),
    ("Sudadera con capucha", "Sudaderas", "L", "Gris", 220, 420, 30, "Textiles del Norte", "Sudadera unisex con capucha"),
    ("Sudadera oversize", "Sudaderas", "XL", "Negro", 240, 450, 4, "Textiles del Norte", "Corte oversize, algodón grueso"),
]

ids_productos = []
for nombre, cat, talla, color, p_compra, p_venta, stock, prov, desc in productos:
    ok, resultado = registrar_producto(
        nombre=nombre,
        id_categoria=ids_categorias.get(cat),
        talla=talla,
        color=color,
        precio_compra=p_compra,
        precio_venta=p_venta,
        cantidad_inicial=stock,
        id_proveedor=ids_proveedores.get(prov),
        descripcion=desc
    )
    if ok:
        ids_productos.append({"sku": resultado, "nombre": nombre, "precio": p_venta})
        print(f"  ✓ {nombre} ({talla}, {color}) - SKU: {resultado} - Stock: {stock}")
    else:
        print(f"  ✗ Error con {nombre}: {resultado}")

print("\n=== Insertando clientes ===")
clientes = [
    ("Ana", "González", "3310001111", "ana.gonzalez@correo.com"),
    ("Luis", "Martínez", "3310002222", "luis.martinez@correo.com"),
    ("María", "Pérez", "3310003333", "maria.perez@correo.com"),
    ("Carlos", "Ramos", "3310004444", "carlos.ramos@correo.com"),
    ("Sofía", "Hernández", "3310005555", "sofia.hernandez@correo.com"),
]
ids_clientes = []
for nombre, apellido, telefono, correo in clientes:
    ok, resultado = registrar_cliente(nombre, apellido, telefono, correo)
    if ok:
        ids_clientes.append(resultado)
        print(f"  ✓ {nombre} {apellido}")
    else:
        print(f"  - {nombre} {apellido} ({resultado})")

print("\n=== Insertando promoción vigente ===")
hoy = datetime.now().strftime("%Y-%m-%d")
en_una_semana = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
ok, resultado = registrar_promocion("Rebaja de temporada", "porcentaje", 15, hoy, en_una_semana)
if ok:
    print(f"  ✓ Rebaja de temporada (15%, vigente hasta {en_una_semana})")
else:
    print(f"  ✗ Error: {resultado}")

print("\n=== Insertando ventas de ejemplo ===")
from database.db_setup import crear_conexion

# Obtenemos productos reales con su id_producto (no solo sku) para armar el carrito
conexion = crear_conexion()
cursor = conexion.cursor()
cursor.execute("SELECT id_producto, nombre, precio_venta, stock FROM producto ORDER BY id_producto")
productos_reales = cursor.fetchall()
conexion.close()

if len(productos_reales) >= 3 and len(ids_clientes) >= 3:
    ventas_ejemplo = [
        # (indice_cliente, [(indice_producto, cantidad), ...], id_pago)
        (0, [(0, 2), (3, 1)], 1),
        (1, [(2, 1)], 2),
        (2, [(5, 1), (9, 2)], 1),
        (3, [(6, 1)], 3),
        (None, [(1, 1)], 1),  # venta sin cliente asociado
    ]

    for idx_cliente, items, id_pago in ventas_ejemplo:
        carrito = []
        for idx_producto, cantidad in items:
            id_producto, nombre, precio_venta, stock = productos_reales[idx_producto]
            if stock >= cantidad:
                carrito.append({
                    "id_producto": id_producto,
                    "sku": "",
                    "nombre": nombre,
                    "cantidad": cantidad,
                    "precio_unitario": precio_venta,
                    "subtotal": precio_venta * cantidad
                })

        if carrito:
            id_cliente = ids_clientes[idx_cliente] if idx_cliente is not None else None
            ok, resultado, total = registrar_venta(carrito, id_cliente, id_pago)
            if ok:
                print(f"  ✓ Venta #{resultado} registrada - Total: ${total:.2f}")
            else:
                print(f"  ✗ Error en venta: {resultado}")

print("\n✅ Datos de ejemplo insertados. El sistema ya está listo para la demostración.")