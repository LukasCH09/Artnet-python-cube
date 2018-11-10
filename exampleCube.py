from lib.primitives import CubeAPI
from lib.StupidArtnet import StupidArtnet
import time

target_ip = '127.0.0.1'	 # typically in 2.x or 10.x range
universe = 0 					# see docs
packet_size = 512				# it is not necessary to send whole universe

# CREATING A STUPID ARTNET OBJECT
# SETUP NEEDS A FEW ELEMENTS
# TARGET_IP   = DEFAULT 127.0.0.1
# UNIVERSE    = DEFAULT 0
# PACKET_SIZE = DEFAULT 512
# FRAME_RATE  = DEFAULT 30
a = StupidArtnet(target_ip, universe, packet_size)

a.set_simplified(False)
# MORE ADVANCED CAN BE SET WITH SETTERS IF NEEDED
# NET         = DEFAULT 0
# SUBNET      = DEFAULT 0

# CHECK INIT
print(a)

a.start()       # start continuous sending, else error pops when cleaning

packet = bytearray(packet_size)		# create packet for Artnet
brightness = 255

cubeAPI = CubeAPI()
vertical = cubeAPI.get_vertical(0)  # set the indice of vertical bar (0 to 8)
for key in vertical:
    print(f'Universe: {key} => channels: {vertical[key]}')
    for i in range(packet_size):  # fill packet with sequential values
        packet[i] = brightness if i+1 in vertical[key] else 0
    subnet = int(key / 16)
    universe = key % 16
    print(f'subnet: {subnet}, universe: {universe}, packet: {packet}')
    a.set_subnet(subnet)
    a.set_universe(universe)
    a.set(packet)           # set the packet to stupid Artnet
    print(a)
    a.show()                # send the data

time.sleep(2)

# SOME DEVICES WOULD HOLD LAST DATA, TURN ALL OFF WHEN DONE
for key in vertical:
    subnet = int(key / 16)
    universe = key % 16
    print(f'blackout subnet {subnet} universe {universe}')
    a.set_subnet(subnet)
    a.set_universe(universe)
    a.blackout()

# ... REMEMBER TO CLOSE THE THREAD ONCE YOU ARE DONE
a.stop()

# CLEANUP IN THE END
del a
