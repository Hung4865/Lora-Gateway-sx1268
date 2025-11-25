
Please leave a star if you find me useful!

---
In this repo I have uploaded the 3 folder that came from the waveshare demo from their website https://www.waveshare.com/wiki/SX1268_433M_LoRa_HAT and a additional demo made by me that built upon their original code. For the waveshare tutorial, you can go to their website. I will only be explaining the setup for mine below
---

This is the diagram for my gateway setup. There are 2 raspberry pi 4b, one is the end node that sent LoRa signal to the gateway. 

The 2nd pi will be the gateway node that receives the signal from the end node and then sen it to the internet using MQTT protocol. MQTT, which stands for Message Queuing Telemetry Transport, is a lightweight messaging protocol based on the publish-subscribe model that is ideal for connecting devices with limited bandwidth and low power.

---
Make sure you download these app to run this project:

Raspberry Pi Imager - Help to install the Rasbian OS to your SDCard

Putty - Help connect the Rasbian OS terminal to your laptop screen

VNC - Help connect Rasbian OS GUI (sometimes you don't need Putty, VNC is enough, but if there is connection issues, you would need both)

RF_Setting - Help config our LoRa module (you could config the moudule using code in rasbian OS, but I'm having trouble doing it. In addition, there is a line in my code that prevent the code from overwriting the RF_setting config)

Watch this video for the step by step setup: https://www.youtube.com/watch?v=F5OYpPUJiOw&t=239s 

---
This is the mode that our module have. Notice that there are 2 coloums and 6 rows. The first 3 row is for the UART Selection, conbine 2 rows will let you enter each A,B,C mode. The 3 rows below is for LoRa mode selection. The jumper will always be put vertically connecting 2 rows together.

UART selection jumpers

A: control the LoRa module through USB TO UART

B: control the LoRa module through Raspberry Pi

C: access Raspberry Pi through USB TO UART

LoRa mode selection jumpers

short M0, short M1: transmission mode

short M0, open M1: configuration mode

open M0, short M1: WOR mode

open M0, open M1: deep sleep mode

【Note】

Combine M1 and M0 with high and low levels to determine the working mode. M1 and M0 are high when they are not connected to the jumper cap. After switching the working mode, if the module is idle, it will enter the new working mode. Otherwise, the current transmission will be processed and enter the new working mode after receiving.

Mode 0: Transmission mode, Module transmits data when users send data to the UART interface. Wireless receiving is enabled to receive data and send it to the UART interface when idle.

Mode 1: When it is defined to Transmit, the user needs to add wakeup codes before transmitting, receiving is the same as Mode 0.

Mode 2: Wireless transmit and wireless receive are disabled, users can configure configuration according to #Registers Configuration

Mode 3: Wireless transmit and wireless receive are disabled, and the module enters deep sleep mode. The module will configure when switching to other modes.

--
