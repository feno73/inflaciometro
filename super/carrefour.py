from models import Producto, Marca, Categoria
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


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
    categoria, created = Categoria.get_or_create(nombre=seccion.replace("-", " "))
    producto = Producto(
        nombre=nombre,
        supermercado="Carrefour",
        marca=marca,
        categoria=categoria,
        precio=float(f"{precio_entero}.{precio_decimal}"),
        canasta_basica=True
    )
    return producto


def main():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # revisar porque no carga bien los productos en modo headless

    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
        for seccion in secciones:
            url = f"https://www.carrefour.com.ar/Almacen/{seccion}?page="
            pagina = 1
            while True:
                productos, sigue = obtener_productos(driver, f"{url}{str(pagina)}")
                lista_productos = [crear_producto(item, seccion) for item in productos]
                Producto.bulk_create(lista_productos)
                pagina += 1
                if not sigue:
                    break


secciones = [
    "Pastas-secas",
    "Arroz-y-legumbres",
    "Harinas",
    "Enlatados-y-Conservas",
    "Sal-aderezos-y-saborizadores",
    "Caldos-sopas-y-pure",
    "Reposteria-y-postres",
    "Snacks",
    "Aceites-y-vinagres"
]

if __name__ == '__main__':
    main()
