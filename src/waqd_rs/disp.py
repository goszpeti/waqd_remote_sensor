from epaper import EPD
import time
import adafruit_framebuf

BLACK = 0
WHITE = 1

class WaveShare2in9Disp():

    def __init__(self):
        self.epd = EPD()
        print("Initializing display...")
        self.epd.init()
        print("Clear display...")
        self.epd.clear_frame_memory(0xff)
        self.epd.display_frame()
        self.buf = bytearray(128 * 296 // 8)
        self.fb = adafruit_framebuf.FrameBuffer(self.buf, self.epd.width, self.epd.height, adafruit_framebuf.MHMSB)
        self.fb.rotation = 2 # 180 deg
        self._text_line_pix = 0

    def format_date(self, time):
        return "{:4}-{:02}-{:02d}".format( \
            time[0], time[1], time[2])

    def format_time(self, time):
        return "{:02}:{:02d}:{:02d}".format( \
            time[3], time[4], time[5])

    def _write_text(self, text, size=2, margin=1):
        self.fb.text(text, margin, self._text_line_pix,color=BLACK,size=2)
        self._text_line_pix += (7 * size) + 2

    def _reset_text_lines(self):
        self._text_line_pix = 3

    def draw_header(self):
        # max 10 characters in line with size 2
        self._write_text("WAQD", margin=3)
        self._write_text("Remote", margin=3)
        self._write_text("Sensor", margin=3)
        self.fb.rect(1,1,self.epd.width, self._text_line_pix + 3, BLACK)
        self._text_line_pix += 5

    def draw_footer(self):
        self.fb.text("(c)2022 WAQD Project", 5, 280, color=BLACK, size=1)
        self.fb.text("Peter Gosztolya", 5, 288, color=BLACK, size=1)

    def draw_hline(self):
        self.fb.hline(0,self._text_line_pix + 3,self.epd.width, BLACK)
        self._text_line_pix += 5

    def draw_main(self, temp: float, hum: float, mode: int):
        self.fb.fill(WHITE) # size 6? -> +7
        self._reset_text_lines()
        self.draw_header()
        self._write_text("Temperature")
        self._write_text("{:3.1f} deg C\n".format(temp))
        self.draw_hline()
        self._write_text("Humidity")
        self._write_text("{:3.1f}%\n".format(hum))
        self.draw_hline()
        self._write_text("Mode")
        self._write_text("Exterior")
        self.draw_hline()
        now = time.localtime()
        self._write_text("Last Update")
        self._write_text(self.format_date(now))
        self._write_text(self.format_time(now))
        self.draw_footer()
        self.epd.display_frame_buf(self.buf, True)
