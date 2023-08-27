import time
from selenium.webdriver.common.by import By
from models import Keyword
from utils.log import log_debug
from utils.selenium_conf import get_driver
from bs4 import BeautifulSoup


def obtener_resultados(driver, url, links):
    driver.get(url)
    time.sleep(5)
    resultados = BeautifulSoup(driver.page_source, 'html.parser')
    search = resultados.find_all('div', class_="yuRUbf")
    for h in search:
        links.append(h.a.get('href'))


def googlescrapp():
    keywords = Keyword.select()
    links = []

    with get_driver() as driver:
        for keyword in keywords:
            log_debug(f"Buscando la palabra: {keyword.nombre}")
            n_pages = 2
            for page in range(1, n_pages):
                ## Ejemplo "https://www.google.com/search?q=selenium+grid+LiveView+(VNC)+Password"
                url = f"https://www.google.com/search?q={keyword.nombre}&start={(page - 1) * 10}"
                log_debug(f"Accediendo a {url}")
                resultados = obtener_resultados(driver, url, links)

    print(links)


if __name__ == '__main__':
    googlescrapp()






    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # soup = BeautifulSoup(r.text, 'html.parser')

    search = soup.find_all('div', class_="yuRUbf")
    for h in search:
        links.append(h.a.get('href'))























