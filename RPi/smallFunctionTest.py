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
ten_minutes_timedelta = datetime.timedelta(minutes=10)


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


def get_current_wifi():
    try:
        # Run iwgetid to get the current SSID, "-r" flag returns only the SSID name
        result = subprocess.run(["iwgetid", "-r"], capture_output=True, text=True, check=True)
        current_ssid = result.stdout.strip()
        return current_ssid
    except subprocess.CalledProcessError:
        # Handle errors if iwgetid fails to run or doesn't return an SSID
        return "Unable to get current WiFi network."
    
    
def check_captive_portal(test_url='http://httpbin.org/get'):
    try:
        response = requests.get(test_url, allow_redirects=False)
        if response.status_code == 302: # 302 Found (HTTP重定向状态码)
            redirect_location = response.headers.get('Location', None)
            if redirect_location:
                print(f"可能存在捕获门户，被重定向到: {redirect_location}")
                return True
            else:
                print("没有检测到重定向。")
                return False
        else:
            print("正常连接，没有检测到捕获门户。")
            return False
    except Exception as e:
        print(f"检测时发生错误: {e}")
        return False

# 检测是否存在捕获门户

def check_for_keywords(url='http://example.com', keywords=['example', 'domain', 'illustrative']):
    try:
        response = requests.get(url)
        if response.status_code == 200: # 检查是否成功获取内容
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower() # 获取所有文本并转换为小写
            counter = 0
            for keyword in keywords:
                if keyword in text:
                    print(f"检测到关键字‘{keyword}’，may connect to internet")
                    counter += 1
            if counter == 3:
                print("find 3 keywords, may connect to internet")
                return True
            else:
                return False
        else:
            print("cannot connect to example.com")
            return False
    except Exception as e:
        print(f"检测时发生错误: {e}")
        return False

# 检测是否存在网络认证门户
check_for_keywords('http://www.example.com', ['example', 'domain', 'illustrative'])


if __name__ == '__main__':
    print(check_for_keywords())

