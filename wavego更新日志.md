# 更新日志

## 2024/2/2

### Shihming Lin: 

### Rpi 上位机

1. 上位机增加 selfIpSender.py : 
	a. 通过窗口(pyserial)从raspberrypi4b(上位机, upper computer, r4b)向esp32(下位机, lower computer)发送上位机ssid和ip。
	b. 增加串口发送信息指令 r4bIp, r4bSsid
```
	备注, 复制robot.py as selfIpSender.py 前, 使用指令 sudo chmod -R 777 /path/to/folder
```
2. 上位机将 selfIpSender.py 添加至开机自启服务
```
	开机自启服务添加流程
	sudo nano /etc/systemd/system/selfIpSender.service

	in /etc/systemd/system/selfIpSender.service add:
	由于是GNU nano 编辑器, 编辑结束 使用 ctrl+O 保存后再ctrl+X退出
	[Unit]
	Description=My Python Script Service
	After=multi-user.target

	[Service]
	Type=simple
	ExecStart=/usr/bin/python3 /home/pi/WAVEGO/Arduino/selfIpSender.py

	[Install]
	WantedBy=multi-user.target


	commandline:
	sudo systemctl daemon-reload
	sudo systemctl enable selfIpSender.service
	sudo systemctl start selfIpSender.service

	检查服务的状态
	sudo systemctl status selfIpSender.service

	修改.service后, 或修改selfIpSender.py后需要使用一下指令:
	sudo systemctl daemon-reload
	sudo systemctl restart service3.service
	sudo systemctl status selfIpSender.service

```

### ESP32 下位机
1. 下位机修改 WAVEGO.ino : 增加串口接受信息指令 r4bIp, r4bSsid, 接受来自上位机ip, ssid等信息
2. 下位机修改 InitConfig.h : 修改oled显示界面(1. 页面3显示上位机wifi ssid&ip; 2. 页面4显示下位机wifi ip&status)
