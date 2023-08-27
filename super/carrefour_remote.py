import time

from selenium.webdriver.common.by import By

from models import Producto, Marca, Categoria, Seccion
from utils.log import log_debug
from utils.selenium_conf import get_driver


def obtener_productos(driver, url):
    driver.get(url)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0,300);")
    time.sleep(10)
    productos = driver.find_elements(By.CLASS_NAME, 'lyracons-product-summary-status-0-x-container')
    try:
        no_encontrado = driver.find_element(By.CLASS_NAME, "lyracons-search-result-1-x-searchNotFoundWhatDoIDo")
        prox_btn = False if no_encontrado else True
    except:
        prox_btn = True
    return productos, prox_btn


def crear_producto(item, seccion):
    nombre = item.find_element(By.CLASS_NAME,
                               "vtex-product-summary-2-x-productBrand.vtex-product-summary-2-x-brandName.t-body").text
    precio_venta = item.find_element(By.CLASS_NAME, "lyracons-carrefourarg-product-price-1-x-sellingPriceValue")
    precios_enteros = precio_venta.find_elements(By.CLASS_NAME,
                                                 "lyracons-carrefourarg-product-price-1-x-currencyInteger")
    precio_entero = ''.join([p.text for p in precios_enteros])
    precio_decimal = precio_venta.find_element(By.CLASS_NAME,
                                               "lyracons-carrefourarg-product-price-1-x-currencyFraction").text
    marca, created = Marca.get_or_create(nombre="N/A")
    categoria, created = Categoria.get_or_create(nombre=seccion.url.replace("-", " "))
    producto = Producto(
        nombre=nombre,
        supermercado="Carrefour",
        marca=marca,
        categoria=categoria,
        precio=float(f"{precio_entero}.{precio_decimal}"),
        canasta_basica=True
    )
    return producto


def carrefourscrapp():
    secciones = Seccion.select().where(Seccion.supermercado == "Carrefour")

    with get_driver() as driver:
        for seccion in secciones:
            log_debug(f"Accediendo a la seccion {seccion.nombre}")
            url = f"https://www.carrefour.com.ar/Almacen/{seccion.url}?page="
            pagina = 1
            log_debug(f"Accediendo a {url}{str(pagina)}")
            while True:
                productos, sigue = obtener_productos(driver, f"{url}{str(pagina)}")
                lista_productos = [crear_producto(item, seccion) for item in productos]
                log_debug(f"{len(lista_productos)} productos a guardar")
                Producto.bulk_create(lista_productos)
                pagina += 1
                if not sigue:
                    break


if __name__ == '__main__':
    carrefourscrapp()
