# CamoverPy, a CAM Table's Worst Nightmare
### A Python port of [stuenkels/camover](https://github.com/stuenkels/camover)
CamoverPy is a cross-platform command-line tool written in Python meant to generate broadcast ethernet frames with random source MAC addresses. Frames generated with this tool can be used to overflow a network switch's CAM Table, forcing the switch to operate like a hub and exposing all network traffic to all devices on the network.

## Requirements
- Python 3.2 or newer
- [Scapy](https://pypi.org/project/scapy/), [PSUtil](https://pypi.org/project/psutil/) (`pip install -r requirements.txt`)

## Usage 
```
usage: camover.py [-h] [-?] [-i INTERFACE] [-n NUMBER] [-d DELAY] [-p PACKET]
```

## Options:
```
  -h, --help            show this help message and exit
  -?                    show this help message and exit
  -i INTERFACE, --interface INTERFACE
                        Interface to send packets on (if a valid interface isn't specified, a list of interfaces will be shown)
  -n NUMBER, --number NUMBER
                        Number of packets to send (0 = unlimited)
  -d DELAY, --delay DELAY
                        Delay between packets in seconds (defaults to 1ms)
  -p PACKET, --packet PACKET
                        Specify custom .bin file to use for packet
```
Example:
```
camover.py -i eno0 -n 6500 -p exploit_packet.bin 
```
Sends 6500 packets over the interface **eno0** using the packet file **exploit_packet.bin**

## Disclaimer
This program was designed for cybersecurity research purposes. Do not use this tool on any network unless you have the explicit permission from the network owner. This program serves as a demonstration for how specific exploits can operate and as a learning tool for cybersecurity, and is not intended for any malicious purpose.
