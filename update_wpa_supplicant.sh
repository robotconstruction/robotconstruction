#!/bin/bash

WPA_SUPPLICANT_CONF="/etc/wpa_supplicant/wpa_supplicant.conf"

cat > $WPA_SUPPLICANT_CONF << EOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=CN

network={
	ssid="JSBPI"
	scan_ssid=1
	psk="waveshare0755"
	disabled=1
}

network={
	ssid="napp-lab-printers"
	psk="rh353@voron.24"
	key_mgmt=WPA-PSK
}

network={
	ssid="Cornell-Visitor"
	key_mgmt=NONE
	disabled=1
}
EOF
wpa_cli -i wlan0 reconfigure
