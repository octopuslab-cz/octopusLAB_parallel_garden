#octopuslab-timelapsephoto

2019/01 - RaspberryPi and webcam

Hydropony Rpi prepare
---------------------

1) dd raspbian stretch
2) mount boot partition
3) touch ssh
4) create wpa_supplicant.conf

```ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
network={
    ssid="YOUR_NETWORK_NAME"
    psk="YOUR_PASSWORD"
    key_mgmt=WPA-PSK
}```

5) insert SD to Rpi, boot



Hydropony Rpi system install
----------------------------

1) apt-get install fswebcam
2) apt-get install fontconfig
3) useradd -d /opt/octopuslab -s /bin/false -r octopus
4) usermod -a -G video octopus
5) copy timelapsephoto.conf.sample to /etc/octopuslab/timelapsephoto.conf and change parameters

