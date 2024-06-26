#Builtin LED Controller for status indication
#    """
#    Driver for WS2812 RGB LEDs. May be used for controlling single LED or chain
#    of LEDs.
#    """
    
class WS2812_RGB_LED():
    
    def __init__(self, Parent):
        self.buf_bytes = (0x88, 0x8e, 0xe8, 0xee)
        self.Parent = Parent
        self.pyb = Parent.Machine
        self.loop_counter = 0
    
        # -*- coding: utf-8 -*-
        """
        Params:
        * spi_bus = SPI bus ID (1 or 2)
        * led_count = count of LEDs
        * intensity = light intensity (float up to 1)
        """
        self.spi_bus = self.Parent.spi_bus
        self.intensity = self.Parent.intensity
        self.led_count = self.Parent.led_count

        # prepare SPI data buffer (4 bytes for each color)
        self.buf_length = self.led_count * 3 * 4
        self.buf = bytearray(self.buf_length)

        # SPI init
        # machine.SPI(id,baudrate=1000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=None, mosi=None, miso=None)
        self.spi = self.pyb.SPI(self.spi_bus,baudrate=32000000)

        # turn LEDs off
        self.show([])

    def show(self, data):
        """
        Show RGB data on LEDs. Expected data = [(R, G, B), ...] where R, G and B
        are intensities of colors in range from 0 to 255. One RGB tuple for each
        LED. Count of tuples may be less than count of connected LEDs.
        """
        self.fill_buf(data)
        self.send_buf()

    def send_buf(self):
        """
        Send buffer over SPI.
        """
        self.spi.write(self.buf)
        #self.Parent.Machine.gc.collect()

    def update_buf(self, data, start=0):
        """
        Fill a part of the buffer with RGB data.

        Order of colors in buffer is changed from RGB to GRB because WS2812 LED
        has GRB order of colors. Each color is represented by 4 bytes in buffer
        (1 byte for each 2 bits).

        Returns the index of the first unfilled LED

        Note: If you find this function ugly, it's because speed optimisations
        beated purity of code.
        """

        buf = self.buf
        buf_bytes = self.buf_bytes
        intensity = self.intensity

        mask = 0x03
        index = start * 12
        for red, green, blue in data:
            red = int(red * intensity)
            green = int(green * intensity)
            blue = int(blue * intensity)

            buf[index] = buf_bytes[green >> 6 & mask]
            buf[index+1] = buf_bytes[green >> 4 & mask]
            buf[index+2] = buf_bytes[green >> 2 & mask]
            buf[index+3] = buf_bytes[green & mask]

            buf[index+4] = buf_bytes[red >> 6 & mask]
            buf[index+5] = buf_bytes[red >> 4 & mask]
            buf[index+6] = buf_bytes[red >> 2 & mask]
            buf[index+7] = buf_bytes[red & mask]

            buf[index+8] = buf_bytes[blue >> 6 & mask]
            buf[index+9] = buf_bytes[blue >> 4 & mask]
            buf[index+10] = buf_bytes[blue >> 2 & mask]
            buf[index+11] = buf_bytes[blue & mask]

            index += 12

        return index // 12

    def fill_buf(self, data):
        """
        Fill buffer with RGB data.

        All LEDs after the data are turned off.
        """
        end = self.update_buf(data)

        # turn off the rest of the LEDs
        buf = self.buf
        off = self.buf_bytes[0]
        for index in range(end * 12, self.buf_length):
            buf[index] = off
            index += 1
            
    def self_test(self, test_loops):
        data = [
            (255, 0, 0),    # red
            (0, 255, 0),    # green
            (0, 0, 255),    # blue
            (85, 85, 85),   # white
        ]
        self.show(data)
        """
        Driver for WS2812 RGB LEDs. May be used for controlling single LED or chain
        of LEDs.

        Example of use:

            chain = WS2812(spi_bus=1, led_count=4)
            data = [
                (255, 0, 0),    # red
                (0, 255, 0),    # green
                (0, 0, 255),    # blue
                (85, 85, 85),   # white
            ]
            chain.show(data)

        Version: 1.0
        """
        
