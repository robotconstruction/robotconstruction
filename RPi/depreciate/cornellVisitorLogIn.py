#!/usr/bin/env/python3
# File name   : robot.py
# Description : Robot interfaces.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
import socket
import time

options = Options()
options.add_argument("lang=en-US")
service = webdriver.ChromeService(executable_path = '/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service)
driver.get("https://cornell-visitor-cp.net.cornell.edu/guest/Cornell-Visitor.php?_browser=1")
time.sleep(10)

visitor_name_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'guest_register_visitor_name') and @type='text']"))
)

visitor_name_input = driver.find_element(By.XPATH, "//input[contains(@id, 'guest_register_visitor_name') and @type='text']")
print('find the vistor_name_input')
visitor_name_input.send_keys("Shihming Lin")

time.sleep(2)
email_input = driver.find_element(By.XPATH, "//input[contains(@id, 'guest_register_email') and @type='email']")
print('email_input')
email_input.send_keys("sl2874@cornell.edu")

time.sleep(2)
terms_checkbox = driver.find_element(By.XPATH, "//input[contains(@id, 'guest_register_creator_accept_terms') and @type='checkbox']")
print('terms_checkbox')
terms_checkbox.click()

time.sleep(2)
submit_button = driver.find_element(By.XPATH, "//input[contains(@id, 'guest_register_submit') and @type='submit']")
print('submit_button') 
submit_button.click()


time.sleep(10)

submit_button_second_page = driver.find_element(By.XPATH, "//input[contains(@id, 'guest_register_receipt_submit') and @type='submit']")
submit_button_second_page.click()
time.sleep(30)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't need to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def check_internet():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        print("Connected to the internet")
        cur_ip = get_ip_address()
        print(cur_ip)
    except requests.ConnectionError:
        print("Not connected to the internet")
        
check_internet()