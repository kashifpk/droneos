Tools:
PyCK (Python Code Karigar)

Harware:
Raspberry Pi, GPS receiver, Snake Camera, Quad copter, LEDs, Lithium Batteries (3.5 V)

Operating System:
Linux Mint 

System:
Intel(R) Core™ i5 CPU, Processor 2.40 GHz

Once You have got Raspberry Pi, you have to install a Raspbian Image to an SD Card..
For Complete Guide, Follow the link given..
http://www.engadget.com/2012/09/04/raspberry-pi-getting-started-guide-how-to/
                OR
http://lifehacker.com/5976912/a-beginners-guide-to-diying-with-the-raspberry-pi

After installing Raspbian image, and connect the Raspberry Pi with an output screen to get an interface.
Connecting Raspberry Pi with your computer system, steps are:
1- Connect Tp-link to one of the USB port.
2- Run the commnads from the Terminal
   ping (IP address of RPi) #ip address can be taken from the wifi devices connected to your internet
   When the data packets are received,
   ssh pi@(IP address)
3- Enter the RPi password.

Now you are in your Raspberry Pi system.

Install Pyck, GPSD, GPIO modules.
PyCK Installation : https://pythonhosted.org/PyCK/installation.html
GPSD Installation : http://www.pridopia.co.uk/rs-pi-set-usb-gps.html    OR
                    http://www.raspberrypi.org/forums/viewtopic.php?f=29&t=66427
GPIO Installation : http://www.raspberrypi-spy.co.uk/2012/07/install-rpi-gpio-library-in-raspbian/

For running the project, you need to activate a virtual environment. 
Virtual Environment : http://docs.python-guide.org/en/latest/dev/virtualenvs/

Basic Requirements for running the project are given, other details are mentioned in the Documentation.