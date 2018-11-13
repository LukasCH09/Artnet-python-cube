from lib.StupidArtnet import StupidArtnet
import sys
import time


target_ip = '127.0.0.1'
#target_ip = '192.168.0.50'	 # typically in 2.x or 10.x range
# universe = 0 					# see docs
packet_size = 512				# it is not necessary to send whole universe


def main(universe):
    a = StupidArtnet(target_ip, universe, packet_size)
    a.start()
    # a.flash_all()
    packet = bytearray(packet_size)
    for i in range(packet_size):  # fill packet with sequential values
        packet[i] = 255
    a.set(packet)
    a.show()
    time.sleep(5)
    a.blackout()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        universe = sys.argv[1]
        print(f"Flashing universe: {universe}")
        main(int(universe))
    else:
        print("Wrong argument")