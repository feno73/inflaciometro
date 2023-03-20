from models import Producto, Marca, Categoria

marca = Marca.create(nombre='Marolio')
categoria = Categoria.create(nombre='Yerba')
producto = Producto.create(
    nombre='Yerba Marolio 1kg',
    marca=marca,
    categoria=categoria,
    precio=150.98,
    supermercado='DIA',
    canasta_basica=True
)

