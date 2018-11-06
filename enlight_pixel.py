__version__ = '0.1'

import json
import sys
import array
# from ola.ClientWrapper import ClientWrapper


def get_artnet_params(x_coord, y_coord):
    # TODO handle "holes" at intersections of ledstrips --> pass

    # Calculate strip x and y coordinates
    if x_coord == 0:
        strip_x = 0
    else:
        strip_x = int(x_coord / 28) * 2 + 1

    if y_coord == 0:
        strip_y = 0
    else:
        strip_y = int(y_coord / 28) * 2 + 1

    # calculate led_offset
    if x_coord % 2 == 0:
        led_offset = y_coord
    else:
        led_offset = x_coord
    led_offset %= 28
    led_offset -= 1
    led_offset *= 3

    print(f'#################  x: {x_coord}, y: {y_coord}')
    with open('cube.json') as json_data:
        d = json.load(json_data)
    strip = d[str(strip_x)][str(strip_y)]
    universe = strip['universe']
    channel = strip['channel']
    print(f'universe: {universe}, channel: {channel}, led_offset: {led_offset}')
    start_led = channel + led_offset
    universe_add = int(start_led/511)
    if universe_add > 0:
        universe += universe_add
        print(f'CHANGE UNIVERSE! start_led: {start_led}, mod: {start_led%511}')
        start_led %= 511
        start_led += 1
    return universe, [start_led, start_led + 1, start_led + 2]


def change_pixel(intensity, *coord):
    universe, indices = get_artnet_params(coord[0], coord[1])
    data_array = [intensity if(i in indices) else 0 for i in range(0, 511)]
    print(f'Data: {data_array}')
    print(f'Universe: {universe}')
    return array.array('B', data_array), universe


def send_artnet_frame(intensity, *coord):
    universe, data = change_pixel(intensity, *coord)
    '''wrapper = ClientWrapper()
    client = wrapper.Client()
    client.SendDmx(universe, data, DmxSent)
    wrapper.Run()

def DmxSent(state):
    wrapper.Stop()
'''


def main(argv):
    print(argv)
    send_artnet_frame(int(argv[0]), int(argv[1]), int(argv[2]))


if __name__ == '__main__':
    # call example for pixel 0, 85 and intensity = 127:
    # 'python cube_case.py 127 0 85'
    main(sys.argv[1:])
    '''
    print(get_artnet_params(0, 85))
    print(get_artnet_params(0, 86))
    print(get_artnet_params(0, 85 + 26))
    print(get_artnet_params(0, 85 + 27))
    print(get_artnet_params(0, 113))
    print(get_artnet_params(0, 114))
    print(get_artnet_params(0, 113 + 26))
    send_artnet_frame(127, 0, 85)
    '''
