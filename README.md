smartboard-3m-digital_easel-driver
==================================

*version: 0.0.1*

*author: Goran Kapun*

Driver for 3M digital easel smartboard

*Reverse engineering of input protocol for 3M digital easel smartboard*

## How it works (running driver & gui)
1. Connect 3M digital easel smartboard to computer using USB
2. Start driver/gui by issuing following command:

    Starting from root or sudo interacitve:
    ./sb_gui2.py
    Starting from normal permissons user:
    sudo ./sb_gui2.py

*if it is not working check USB device file, default is /dev/usb/hiddev0; if its on other device, append to calling full path to correct device / file*    
    
3. Use smartboard (draw) :)
4. If you want to save current frame to PNG and clear screen press marker on designated area on smartboars

## Steps to contributing

... to be continued ...

## Runing driver (data dump on stdout)

1. Connect 3M digital easel smartboard to computer using USB
2. Start driver by issuing following command:

    Starting from root or sudo interacitve:
    ./smartboard_driver.py
    Starting from normal permissons user:
    sudo ./smartboard_driver.py

## How to test driver

... to be continued ...
