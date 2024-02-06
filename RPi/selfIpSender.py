#!/usr/bin/env/python3
# File name   : robot.py
# Description : Robot interfaces.
import time
import json
import serial
import socket
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
    time.sleep(5)
    buzzerCtrl(0)
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
        time.sleep(10)
        pass

