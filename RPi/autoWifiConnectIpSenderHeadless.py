#!/usr/bin/env/python3
# File name   : autoWifiConnectIpSender.py
# Description : auto Wifi Connect Ip Sender
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import requests
import socket
import time
import json
import serial
import subprocess
import logging
import datetime
import re

ser = serial.Serial("/dev/ttyS0", 115200)
dataCMD = json.dumps({'var': "", 'val': 0, 'ip': ""})
ten_minutes_timedelta = datetime.timedelta(minutes=20)
service_name = 'selfIpSender.service'


def stop_service(service_name):
    try:
        subprocess.run(['sudo', 'systemctl', 'stop', service_name], check=True)
        print(f"Service {service_name} has been stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop service {service_name}. Error: {e}")


def switch_wifi(ssid, password=None):
    try:
        # 尝试断开当前的WiFi连接
        subprocess.run(["nmcli", "device", "disconnect", "wlan0"], check=True)
    except subprocess.CalledProcessError as e:
        # 如果设备未激活，将捕获异常
        logging.error("Warning: " + str(e))
        logging.info("Device might not be active. Proceeding to connect...")

    # 连接到新的WiFi网络
    if password:
        # 需要密码的网络
        try:
            subprocess.run(["nmcli", "device", "wifi", "connect", ssid, "password", password], check=True)
        except subprocess.CalledProcessError as e:
            logging.info("Failed to connect to " + str(ssid))
            logging.error("Warning: " + str(e))
    else:
        # 开放网络
        try:
            subprocess.run(["nmcli", "device", "wifi", "connect", ssid], check=True)
        except subprocess.CalledProcessError as e:
            logging.info("Failed to connect to " + str(ssid))
            logging.error("Warning: " + str(e))


def get_current_wifi():
    try:
        # Run iwgetid to get the current SSID, "-r" flag returns only the SSID name
        result = subprocess.run(["iwgetid", "-r"], capture_output=True, text=True, check=True)
        current_ssid = result.stdout.strip()
        return current_ssid
    except subprocess.CalledProcessError:
        # Handle errors if iwgetid fails to run or doesn't return an SSID
        return "Unable to get current WiFi network."


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


def test_connectivity():
    try:
        socket.create_connection(('google.com',80),timeout=10)
        return True
    except OSError as es:
        logging.error("not connect to google or internet")
        return False

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_datetime_format = datetime.timedelta(seconds=uptime_seconds)
        if uptime_datetime_format > ten_minutes_timedelta:
            return True
        else:
            return False


def buzzerCtrl(buzzerCtrl, cmdInput=0):
    dataCMD = json.dumps({'var': "buzzer", 'val': buzzerCtrl})
    ser.write(dataCMD.encode())


def selfIpSender(r4bIpAddr):
    dataCMD = json.dumps({'var': "r4bIp", 'ip': r4bIpAddr})
    ser.write(dataCMD.encode())


def selfSsidSender(r4bSsid):
    dataCMD = json.dumps({'var': "r4bSsid", 'ip': r4bSsid})
    ser.write(dataCMD.encode())


def check_for_keywords(url='http://example.com', keywords=['example', 'domain', 'illustrative']):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()
            counter = 0
            for keyword in keywords:
                if keyword in text:
                    counter += 1
            if counter == 3:
                logging.info("find 3 keywords, may connect to internet")
                return True
            else:
                return False
        else:
            logging.info("cannot connect to example.com")
            return False
    except Exception as e:
        logging.error("error in check_for_keywords " + str(e))
        return False


def normal_beep_notification(sleep_time):
    buzzerCtrl(1)
    time.sleep(sleep_time)
    buzzerCtrl(0)


if __name__ == '__main__':
    logging.basicConfig(filename='autoconnectwifiipsender.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    logging.info('The program starts and begins to configure the webdriver.')
    stop_service(service_name)
    last_ip_address = '0.0.0.0'
    pre_ssid = 'no wifi'
    selfIpSender(last_ip_address)
    logging.info('First selfIpSender send 0.0.0.0')
    while get_current_wifi() != 'Cornell-Visitor':
        logging.info("wrong wifi")
        time.sleep(10)
        current_ip_address = get_ip_address()
        ssid = get_wifi_ssid()
        logging.info("current wifi is " + str(ssid))
        logging.info("current ip is " + str(current_ip_address))
        selfSsidSender(ssid)
        logging.info("send ip and ssid")
        selfIpSender(current_ip_address)
    normal_beep_notification(1)
    logging.info('!!!!!connect Cornell-Visitor & start sleeping 40 secs')
    time.sleep(40)
    logging.info('Slept 40 secs')
    isConnectInternet = check_for_keywords()
    if not isConnectInternet:
        options = Options()
        options.add_argument("lang=en-US")
        options = Options()
        options.headless = True  # 设置为无头模式
        logging.info('set Options arguments')
        try:
            service = webdriver.ChromeService(executable_path = '/usr/bin/chromedriver')
            driver = webdriver.Chrome(service=service, options=options)
            driver.get("https://cornell-visitor-cp.net.cornell.edu/guest/Cornell-Visitor.php?_browser=1")
            logging.info('The page opened successfully.')
            normal_beep_notification(1)
            time.sleep(9)
        except Exception as e:
            logging.error('An error occurred while opening the web page: ' + str(e))
            normal_beep_notification(3)
            pass
        

        try:
            visitor_name_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'guest_register_visitor_name') and @type='text']"))
            )
            normal_beep_notification(1)
            visitor_name_input = driver.find_element(By.XPATH, "//input[contains(@id, 'guest_register_visitor_name') and @type='text']")
            print('find the vistor_name_input')
            visitor_name_input.send_keys("Shihming Lin")
            logging.info('The visitor_name_input is inputted.')
            time.sleep(2)
        except Exception as e:
            logging.error('An error occurred while inputting visitor_name_input: ' + str(e))
            normal_beep_notification(3)
            pass
        
        try:
            email_input = driver.find_element(By.XPATH, "//input[contains(@id, 'guest_register_email') and @type='email']")
            print('email_input')
            email_input.send_keys("sl2874@cornell.edu")
            logging.info('The email_input is inputted.')
            time.sleep(2)
        except Exception as e:
            logging.error('An error occurred while inputting email_input: ' + str(e))
            normal_beep_notification(3)
            pass
        
        try:
            terms_checkbox = driver.find_element(By.XPATH, "//input[contains(@id, 'guest_register_creator_accept_terms') and @type='checkbox']")
            print('terms_checkbox')
            terms_checkbox.click()
            logging.info('The terms_checkbox is inputted.')
            time.sleep(2)
        except Exception as e:
            logging.error('An error occurred while inputting terms_checkbox: ' + str(e))
            normal_beep_notification(3)
            pass
        
        try:
            submit_button = driver.find_element(By.XPATH, "//input[contains(@id, 'guest_register_submit') and @type='submit']")
            print('submit_button')
            submit_button.click()
            logging.info('The submit_button is inputted.')
            time.sleep(10)
            normal_beep_notification(1)
        except Exception as e:
            logging.error('An error occurred while inputting submit_button: ' + str(e))
            normal_beep_notification(3)
            pass
        
        
        try:
            submit_button_second_page = driver.find_element(By.XPATH, "//input[contains(@id, 'guest_register_receipt_submit') and @type='submit']")
            submit_button_second_page.click()
            logging.info('The submit_button_second_page is inputted.')
            time.sleep(30)
            normal_beep_notification(1)
        except Exception as e:
            logging.error('An error occurred while inputting submit_button_second_page: ' + str(e))
            normal_beep_notification(3)
            pass

        logging.info('End of program. Start sending IP AND SSID')
    else:
        logging.info('if else: connect to Cornell')

    while 1:
        current_ip_address = get_ip_address()
        ssid = get_wifi_ssid()
        logging.info("while " + str(ssid))
        logging.info("while " + str(current_ip_address))
        if ssid is not None and pre_ssid != ssid:
            selfSsidSender(ssid)
            logging.info("send ssid in while")
            pre_ssid = ssid
            normal_beep_notification(0.5)
        if current_ip_address is not None and last_ip_address != current_ip_address:
            selfIpSender(current_ip_address)
            logging.info("send ip in while")
            last_ip_address = current_ip_address
            normal_beep_notification(0.5)
        if get_uptime():
            logging.info(">10 min")
            time.sleep(60)
        else:
            time.sleep(10)
        pass

