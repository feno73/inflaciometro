import time

from selenium.webdriver.common.by import By

from models import Keyword
from utils.log import log_debug
from utils.selenium_conf import get_driver


def obtener_resultados(driver, url):
    driver.get(url)
    time.sleep(5)
    resultados = driver.find_element(By.ID, 'rso')
    divs = resultados.find_elements(By.TAG_NAME, 'div')
    for div in divs:
        #print(div.text)
        log_debug(f"Aca va una etiqueta a ------------------------------------------------OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        a = div.find_element(By.XPATH, '//div/div/div[1]/div/div/a')
        url = a.get_attribute("href")
        print(a)
    #for resultado in resultados:
    #print(resultados.get_attribute("outerHTML"))

    return resultados


def googlescrapp():
    keywords = Keyword.select()

    with get_driver() as driver:
        for keyword in keywords:
            log_debug(f"Buscando la palabra: {keyword.nombre}")

            ## Ejemplo "https://www.google.com/search?q=selenium+grid+LiveView+(VNC)+Password"
            url = f"https://www.google.com/search?q={keyword.nombre}"
            log_debug(f"Accediendo a {url}")
            resultados = obtener_resultados(driver, url)
            #print(resultados)


if __name__ == '__main__':
    googlescrapp()





























