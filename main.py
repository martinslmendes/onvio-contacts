from selenium import webdriver
from selenium.common import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException,
    ElementNotInteractableException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import csv
import os
import re
import time


def clean_string(string):
    return re.sub(r'[^\u0000-\uFFFF]', '', string)


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://onvio.com.br/br-messenger/")
(
    WebDriverWait(driver, 60)
    .until(EC.element_to_be_clickable((By.ID, 'trauth-continue-signin-btn')))
    .click()
)
load_dotenv()
(
    WebDriverWait(driver, 60)
    .until(EC.presence_of_element_located((By.ID, 'username')))
    .send_keys(os.getenv("EMAIL"))
)
(
    WebDriverWait(driver, 60)
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-action-button-primary='true']")))
    .click()
)
(
    WebDriverWait(driver, 60)
    .until(EC.presence_of_element_located((By.ID, 'password')))
    .send_keys(os.getenv("PASSWORD"))
)
(
    WebDriverWait(driver, 60)
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-action-button-primary='true']")))
    .click()
)

with (open('contacts.csv', newline='', encoding='utf-8') as file):
    reader = csv.reader(file, delimiter=';')
    next(reader)
    max_tries = 1000
    for line in reader:
        tries = 0
        while tries < max_tries:
            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='gestta_menu-configuracoes']"))
            ).click()

            WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[title$='contatos']"))
            ).click()
            try:
                toasts = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='close']")
                for toast in toasts:
                    WebDriverWait(driver, 60).until(
                        EC.element_to_be_clickable(toast)
                    ).click()
                if not line:
                    continue
                if len(line) < 2:
                    continue

                time.sleep(1)
                WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Cadastrar')]"))
                ).click()

                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='name']"))
                ).send_keys(clean_string(line[0]))

                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='area_code']"))
                ).send_keys(line[1][2:4])

                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='phone_number']"))
                ).send_keys(line[1][4:])

                WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type=submit]"))
                ).click()

                time.sleep(1)
                WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Confirmar')]"))
                ).click()
                tries = max_tries
            except (
                    StaleElementReferenceException,
                    ElementClickInterceptedException,
                    TimeoutException,
                    ElementNotInteractableException
            ) as e:
                tries += 1
                continue
