import time
import configparser
import pyautogui

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class AluraBot:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def run(self):
        self.login()
        self.loop_watch_classes()

    def login(self):
        config = configparser.ConfigParser()
        config.read("config.ini")

        logger.opt(colors=True).debug("Realizando login..")
        driver = self.driver
        driver.get(
            "https://cursos.alura.com.br/loginForm?urlAfterLogin=https://cursos.alura.com.br/dashboard"
        )
        username = driver.find_element_by_xpath("//input[@name='username']")
        username.clear()
        username.send_keys(config["dados"]["username"])
        password = driver.find_element_by_xpath("//input[@name='password']")
        password.send_keys(config["dados"]["password"])
        password.send_keys(Keys.RETURN)

        logger.opt(colors=True).info("Login realizado\n")
        time.sleep(2)

    def watch_classes(self):
        driver = self.driver
        time.sleep(2)
        pyautogui.keyDown('space')
        try:
            a = driver.find_elements_by_xpath("//span[contains(@class, 'vjs-duration-display')]")[0].get_attribute("innerHTML")
            to_sleep=7
        except IndexError:
            to_sleep=0

        time.sleep(to_sleep)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")        

        try:
            continuar_lendo = driver.find_elements_by_xpath("//span[contains(@class, 'video-transcription-button-text')]")
            continuar_lendo[0].click()
        except Exception:
            ...

        try:
            questao = driver.find_elements_by_xpath("//li[contains(@data-correct, 'true')]")
            for q in questao:
                q.click()
        except Exception:
            ...
        
        proxima_atividade = driver.find_elements_by_xpath("//a[contains(@class, 'task-actions-button task-body-actions-button task-actions-button-next bootcamp-next-button bootcamp-primary-button-theme')]")
        
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        driver.get(proxima_atividade[0].get_attribute('href'))
        
        time.sleep(3)
        

    def loop_watch_classes(self):       
        driver = self.driver
        course = driver.find_elements_by_xpath("//a[contains(@class,'big-card__button')]")
        # course = driver.find_element_by_class_name("big-card__button")
        course[0].click()
        while True:
            self.watch_classes()
        

if __name__ == "__main__":
    AluraBot().run()