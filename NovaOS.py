# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

from rpi_ws281x import Color, PixelStrip, ws


# LED strip configuration:
LED_CHANNEL = 0
LED_COUNT = 256              # How many LEDs to light.
LED_FREQ_HZ = 800000        # Frequency of the LED signal.  Should be 800khz or 400khz.
LED_DMA_NUM = 10            # DMA channel to use, can be 0-14.
LED_GPIO = 18               # GPIO connected to the LED signal line.  Must support PWM!
LED_BRIGHTNESS = 255        # Set to 0 for darkest and 255 for brightest
LED_INVERT = 0   

DOT_COLORS = 0x000020
CLEAR_COLOR = 0x000000
# LED_STRIP = ws.SK6812W_STRIP
leds = ws.new_ws2811_t()

EYE_REGION = [53,	54,
58,	57, 41, 186,185,
197,198 ,201, 202, 42]
CALM_EYE_POS = [53,	54,
58,	57, 41, 186,185,
197,198 ,201]
BLINK_EYE_POS = [53,58, 186,197,42,202]
BASIC_SMILE_POS = [1,
14,
241,
254,
15,
16,
31,
32,
47,
48,
63,
64,
79,
80,
95,
96,
111,
112,
127,
128,
143,
144,
159,
160,
175,
176,
191,
192,
207,
208,
223,
224,
239,
240]

# Define functions which animate LEDs in various ways.
def SetMouth(channel, positions):
    """Wipe color across display a pixel at a time."""
    for pos in positions:
        ws.ws2811_led_set(channel, pos, DOT_COLORS)
    
    resp = ws.ws2811_render(leds)
    if resp != ws.WS2811_SUCCESS:
        message = ws.ws2811_get_return_t_str(resp)
        raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))
    
def SetEyes(channel, positions):
    for clear in EYE_REGION:
        ws.ws2811_led_set(channel, clear, CLEAR_COLOR)
    """Wipe color across display a pixel at a time."""
    for pos in positions:
        ws.ws2811_led_set(channel, pos, DOT_COLORS)
    
    resp = ws.ws2811_render(leds)
    if resp != ws.WS2811_SUCCESS:
        message = ws.ws2811_get_return_t_str(resp)
        raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))
    
def FullClear(channel):
    for pos in range(LED_COUNT):
        ws.ws2811_led_set(channel, pos, CLEAR_COLOR)
    resp = ws.ws2811_render(leds)
    if resp != ws.WS2811_SUCCESS:
        message = ws.ws2811_get_return_t_str(resp)
        raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))

for channum in range(2):
    channel = ws.ws2811_channel_get(leds, channum)
    ws.ws2811_channel_t_count_set(channel, 0)
    ws.ws2811_channel_t_gpionum_set(channel, 0)
    ws.ws2811_channel_t_invert_set(channel, 0)
    ws.ws2811_channel_t_brightness_set(channel, 0)

channel = ws.ws2811_channel_get(leds, LED_CHANNEL)

ws.ws2811_channel_t_count_set(channel, LED_COUNT)
ws.ws2811_channel_t_gpionum_set(channel, LED_GPIO)
ws.ws2811_channel_t_invert_set(channel, LED_INVERT)
ws.ws2811_channel_t_brightness_set(channel, LED_BRIGHTNESS)

ws.ws2811_t_freq_set(leds, LED_FREQ_HZ)
ws.ws2811_t_dmanum_set(leds, LED_DMA_NUM)

# Initialize library with LED configuration.
resp = ws.ws2811_init(leds)
if resp != ws.WS2811_SUCCESS:
    message = ws.ws2811_get_return_t_str(resp)
    raise RuntimeError('ws2811_init failed with code {0} ({1})'.format(resp, message))

# Wrap following code in a try/finally to ensure cleanup functions are called
# after library is initialized.
try:
    
    print("INITIALIZING NOVA")
    while True:
        # Update each LED color in the buffer.
        SetEyes(channel,BLINK_EYE_POS)
        time.sleep(0.25)
        SetEyes(channel,CALM_EYE_POS)
        SetMouth(channel,BASIC_SMILE_POS)
        time.sleep(5)

finally:
    print("STOPPING NOVA")
    FullClear(channel)
    # Ensure ws2811_fini is called before the program quits.
    ws.ws2811_fini(leds)
    # Example of calling delete function to clean up structure memory.  Isn't
    # strictly necessary at the end of the program execution here, but is good practice.
    ws.delete_ws2811_t(leds)

