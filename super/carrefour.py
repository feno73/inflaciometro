from models import Producto, Marca, Categoria
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.get("https://www.carrefour.com.ar/Almacen/Aceites-y-vinagres")
time.sleep(10)
driver.execute_script("window.scrollTo(0,300);")
time.sleep(10)

body = driver.execute_script("return document.body")
source = body.get_attribute('innerHTML')

soup = BeautifulSoup(source, "lxml")
productos = soup.find_all("div", class_="lyracons-product-summary-status-0-x-container")


for item in productos:
    nombre = item.find("span", class_="vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body").text
    precio_entero = item.find("span", class_="lyracons-carrefourarg-product-price-1-x-currencyInteger").text
    precio_decimal = item.find("span", class_="lyracons-carrefourarg-product-price-1-x-currencyFraction").text
    marca, created = Marca.get_or_create(nombre="N/A")
    categoria, created = Categoria.get_or_create(nombre="Aceites y vinagres")
    #print(f"{nombre} | $ {precio_entero},{precio_decimal}")
    producto = Producto.create(
        nombre=nombre,
        supermercado="Carrefour",
        marca=marca,
        categoria=categoria,
        precio=float(f"{precio_entero}.{precio_decimal}"),
        canasta_basica=True
    )

##TO-DO: Iterar la paginacion mientras el boton ">" exista