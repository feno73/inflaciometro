from models import Producto, Marca, Categoria
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument('headless')

with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
    driver.get("https://www.carrefour.com.ar/Almacen/Aceites-y-vinagres")
    time.sleep(10)
    driver.execute_script("window.scrollTo(0,300);")
    time.sleep(10)
    body = driver.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    soup = BeautifulSoup(source, "lxml")
    productos = soup.select("div.lyracons-product-summary-status-0-x-container")

    lista_productos = []
    for item in productos:
        nombre = item.select_one(
            "span.vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName.t-body").text
        precio_entero = item.select_one("span.lyracons-carrefourarg-product-price-1-x-currencyInteger").text
        precio_decimal = item.select_one("span.lyracons-carrefourarg-product-price-1-x-currencyFraction").text
        ##Por ahora hardcodeo esta parte:
        marca, created = Marca.get_or_create(nombre="N/A")
        categoria, created = Categoria.get_or_create(nombre="Aceites y vinagres")
        producto = Producto(
            nombre=nombre,
            supermercado="Carrefour",
            marca=marca,
            categoria=categoria,
            precio=float(f"{precio_entero}.{precio_decimal}"),
            canasta_basica=True
        )
        lista_productos.append(producto)

    Producto.bulk_create(lista_productos)


##TO-DO: Iterar la paginacion mientras el boton ">" exista
##Podria armar aparte la funcion que recorre el html y saca los productos
##y dejar la logica de paginado