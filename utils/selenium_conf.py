from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
CHROME = os.getenv('CHROME_HOST')


def get_driver():
    options = webdriver.ChromeOptions()
    return webdriver.Remote(f"http://{CHROME}:4444/wd/hub", options=options)
