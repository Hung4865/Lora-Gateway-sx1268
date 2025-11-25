
Please leave a star if you find me useful!

---

In this repo I have uploaded the 3 folder that came from the waveshare demo from their website https://www.waveshare.com/wiki/SX1268_433M_LoRa_HAT and 1 additional demo made by me that built upon their original code. For the waveshare tutorial, you can go to their website. I will only be explaining the setup for mine below

---
![Diagram](./Image/Diagram.jpg?v=1)
This is the diagram for my gateway setup. There are 2 raspberry pi 4b, one is the end node that sent LoRa signal to the gateway. 

The 2nd pi will be the gateway node that receives the signal from the end node and then send it to the internet using MQTT protocol. MQTT, which stands for Message Queuing Telemetry Transport, is a lightweight messaging protocol based on the publish-subscribe model that is ideal for connecting devices with limited bandwidth and low power.

---
Make sure you download these app to run this project:

Raspberry Pi Imager - Help to install the Rasbian OS to your SDcard

Putty - Help connect the Rasbian OS terminal to your laptop screen

VNC - Help connect Rasbian OS GUI (sometimes you don't need Putty, VNC is enough, but if there is connection issues, you would need both)

RF_Setting - Help config our LoRa module  (you could config the moudule using code in rasbian OS, but I'm having trouble doing it. In addition, there is a line in my code that prevent the code from overwriting the RF_setting config)

Watch this video for the step by step setup: https://www.youtube.com/watch?v=F5OYpPUJiOw&t=239s 

---
![Mapping](./Image/Mapping.png?v=1)
![Mapping](./Image/Mapping2.png?v=1)
We can change the mode that of our sx1268. Notice that there are 2 coloums and 6 rows. The first 3 row is for the UART Selection, conbine 2 rows will let you enter each A,B,C mode. The 3 rows below is for LoRa mode selection. The jumper will always be put vertically connecting 2 rows together.

--
This is the interface of RF_Setting. Make sure each device address is different from each other.
![Mapping](./Image/RF.png?v=1)

Everytime you that you change the a parameter in RF_Setting, you need to adjust the jumpers to mode A (the first 2 rows) and short M0, open M1.
![Mapping](./Image/Config.png?v=1)

Make sure you press Set Para button and it said that you succeed. If if it said you failed, Pull out all the cables, restart RF_Setting and try again.
--

To enter transmisson mode, you need to adjust the jumpers to mode A (the first 2 rows) and short M0, short M1 (because my code will work with both M0,M1). 
![Mapping](./Image/Transmission.png?v=1)
