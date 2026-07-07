
<img width="798" height="773" alt="Screenshot 2025-12-03 at 3 19 21 PM" src="https://github.com/user-attachments/assets/13009740-ad1a-4c22-a96c-cb451b5dae75" />


CECNextionEmulator is a Nextion emualtor for the KD8CEC software that runs on the uBITX. Since it is pretends to be a Nextion (at least as far as the CEC software can tell), there is no software changes required. It also works with both the original 1.x KD8CEC software as well as my CEC 2.0 fork that targets Pico and Teensy MCU's.

Installation requires you to reroute the wires that went originally to the Nextion thru a USB to TTL Serial converter such as https://www.amazon.com/dp/B0BJKCSZZW. 

<img width="606" height="384" alt="Screenshot 2025-12-03 at 7 42 41 AM" src="https://github.com/user-attachments/assets/9ac17bbd-9300-4481-8913-949088214d43" />


Using the original Nextion harness colors:

Black - Ground
Red - Power ( I left the jumper off)
Blue -   TXD (Nextion) to  RX Pin (D8) (Raduino)
Yellow - RXD (Nextion) to  TX Pin (D9)  (Raduino) 

Given the code is in active development, I have not yet created any distribution packages. So you will need to download the code and start the python script CECNextionEmulator that is in the Code directory.  I am using the latest Python 3.13/3.14 and the application requires Pyserial, Pillow and Pygubu (https://github.com/alejandroautalan/pygubu) libraries. I probably require a few more packages that I will add when I find them :-).

Obviously this is still a pre-alpha piece of software so expect "surprises". Please feel free to add to the issues list any surprises you might find!

73
Mark
AJ6CU
