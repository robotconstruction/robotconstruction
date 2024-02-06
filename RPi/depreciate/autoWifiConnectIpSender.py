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
import json
import serial
import subprocess
import re

ser = serial.Serial("/dev/ttyS0", 115200)
dataCMD = json.dumps({'var': "", 'val': 0, 'ip': ""})
  
  
def get_wifi_ssid():
    try:
        ssid = subprocess.check_output(['iwgetid', '-r']).decode('utf-8').strip()
        return ssid
    except subprocess.CalledProcessError:
        return "No WiFi"
        
        
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


def buzzerCtrl(buzzerCtrl, cmdInput=0):
    dataCMD = json.dumps({'var': "buzzer", 'val': buzzerCtrl})
    ser.write(dataCMD.encode())


def selfIpSender(r4bIpAddr):
    dataCMD = json.dumps({'var': "r4bIp", 'ip': r4bIpAddr})
    ser.write(dataCMD.encode())


def selfSsidSender(r4bSsid):
    dataCMD = json.dumps({'var': "r4bSsid", 'ip': r4bSsid})
    ser.write(dataCMD.encode())


if __name__ == '__main__':
    last_ip_address = '0.0.0.0'
    pre_ssid = 'no wifi'
    selfIpSender(last_ip_address)
    buzzerCtrl(1)
    time.sleep(1)
    buzzerCtrl(0)
    time.sleep(50)
    options = Options()
    options.add_argument("lang=en-US")
    try:
        service = webdriver.ChromeService(executable_path = '/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service)
        driver.get("https://cornell-visitor-cp.net.cornell.edu/guest/Cornell-Visitor.php?_browser=1")
        buzzerCtrl(1)
        time.sleep(1)
        buzzerCtrl(0)
        time.sleep(9)
    except Exception as e:
        buzzerCtrl(1)
        time.sleep(3)
        buzzerCtrl(0)
        pass
    

    try:
        visitor_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'guest_register_visitor_name') and @type='text']"))
        )
        buzzerCtrl(1)
        time.sleep(1)
        buzzerCtrl(0)
        visitor_name_input = driver.find_element(By.XPATH, "//input[contains(@id, 'guest_register_visitor_name') and @type='text']")
        print('find the vistor_name_input')
        visitor_name_input.send_keys("Shihming Lin")
        time.sleep(2)
    except Exception as e:
        buzzerCtrl(1)
        time.sleep(3)
        buzzerCtrl(0)
        pass
    
    try:
        email_input = driver.find_element(By.XPATH, "//input[contains(@id, 'guest_register_email') and @type='email']")
        print('email_input')
        email_input.send_keys("sl2874@cornell.edu")
        time.sleep(2)
    except Exception as e:
        buzzerCtrl(1)
        time.sleep(3)
        buzzerCtrl(0)
        pass
    
    try:
        terms_checkbox = driver.find_element(By.XPATH, "//input[contains(@id, 'guest_register_creator_accept_terms') and @type='checkbox']")
        print('terms_checkbox')
        terms_checkbox.click()
        time.sleep(2)
    except Exception as e:
        buzzerCtrl(1)
        time.sleep(3)
        buzzerCtrl(0)
        pass
    
    try:
        submit_button = driver.find_element(By.XPATH, "//input[contains(@id, 'guest_register_submit') and @type='submit']")
        print('submit_button')
        submit_button.click()
        time.sleep(10)
        buzzerCtrl(1)
        time.sleep(1)
        buzzerCtrl(0)
    except Exception as e:
        buzzerCtrl(1)
        time.sleep(3)
        buzzerCtrl(0)
        pass
    
    
    try:
        submit_button_second_page = driver.find_element(By.XPATH, "//input[contains(@id, 'guest_register_receipt_submit') and @type='submit']")
        submit_button_second_page.click()
        time.sleep(30)
        buzzerCtrl(1)
        time.sleep(1)
        buzzerCtrl(0)
    except Exception as e:
        buzzerCtrl(1)
        time.sleep(3)
        buzzerCtrl(0)
        pass
    
    while 1:
        current_ip_address = get_ip_address()
        ssid = get_wifi_ssid()
        print(ssid)
        print(current_ip_address)
        if ssid is not None and pre_ssid != ssid:
            selfSsidSender(ssid)
            print("send ssid")
            pre_ssid = ssid
            buzzerCtrl(1)
            time.sleep(0.5)
            buzzerCtrl(0)
        if current_ip_address is not None and last_ip_address != current_ip_address:
            selfIpSender(current_ip_address)
            print("send ip")
            last_ip_address = current_ip_address
            buzzerCtrl(1)
            time.sleep(0.5)
            buzzerCtrl(0)
        time.sleep(30)
        pass

