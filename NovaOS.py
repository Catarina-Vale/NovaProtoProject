
import time
import random
import asyncio
import aioconsole
from rpi_ws281x import Color, PixelStrip, ws


# LED strip configuration:
LED_CHANNEL = 0
LED_COUNT = 256              # How many LEDs to light.
LED_FREQ_HZ = 800000        # Frequency of the LED signal.  Should be 800khz or 400khz.
LED_DMA_NUM = 10            # DMA channel to use, can be 0-14.
LED_GPIO = 18               # GPIO connected to the LED signal line.  Must support PWM!
LED_BRIGHTNESS = 255        # Set to 0 for darkest and 255 for brightest
LED_INVERT = 0   

FACE_COLOR = 0x000020
BLEP_COLOR = 0x002020
CLEAR_COLOR = 0x000000
# LED_STRIP = ws.SK6812W_STRIP
leds = ws.new_ws2811_t()

blinkchoice = [True, False]

MOUTH_POS = [78,82,126,129,173,177,15,16,31,32,47,48,63,64,79,80,95,96,111,112,143,144,159,160,175,176,191,192,207,208,223,224,239,240,255,254,241,1,14]
FEATURES_POS = [225,237,243,206,210,220,30,18,12,49,45,35]
EYES_POS = [42,213,214,42,41,77,66,61,178,189,194,51,52,53,54,55,60,59,58,57,56,67,68,69,70,71,76,75,74,73,72,83,84,85,86,87,171,170,172,169,168,167,179,180,181,182,183,188,187,186,185,184,195,196,197,198,199,204,203,202,201,200]

CALM_EYE_POS = [187,186,185,196,197,198,201,213,68,69,70,59,58,57,54,42]
BLINK_EYE_POS = [57,69,59,196,198,186]
BASIC_SMILE_POS = [1,14,241,254,15,16,31,32,47,48,63,64,79,80,95,96,111,112,143,144,159,160,175,176,191,192,207,208,223,224,239,240]

FLUSTERED_EYE_POS = [69,68,59,52,53,54,56,71,72,86,85,84,83,77,66,61,194,189,178,171,170,172,169,183,184,199,201,202,203,196,187,186]
FLUSTERED_FEATURE_POS = [225,237,243,206,210,220,30,18,12,49,45,35]

BLEP_TONGUE_POS = [127,128]

WORRIED_EYES_POS = [69,186,70,57,58,185,197,198]

SMUG_EYES_POS = [186,185,197,198,202,201,213,214,42,41,53,54,58,57,69,70]
SMUG_SMILE_POS = [82,78,80,95,96,111,112,126,129,143,144,159,160,175,177,173]
SMALL_SMILE_POS = [80,95,96,111,112,143,144,159,160,175]
current_mode = "blink"
current_tongue = False
last_tongue = False
last_mode = "blink"

def SetTongue(channel):
    for pos in BLEP_TONGUE_POS:
        ws.ws2811_led_set(channel, pos, BLEP_COLOR)
    
    resp = ws.ws2811_render(leds)
    if resp != ws.WS2811_SUCCESS:
        message = ws.ws2811_get_return_t_str(resp)
        raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))

# Define functions which animate LEDs in various ways.
def SetMouth(channel, positions):
    """Wipe color across display a pixel at a time."""
    for pos in positions:
        ws.ws2811_led_set(channel, pos, FACE_COLOR)
    
    resp = ws.ws2811_render(leds)
    if resp != ws.WS2811_SUCCESS:
        message = ws.ws2811_get_return_t_str(resp)
        raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))
    
def SetEyes(channel, positions):
    """Wipe color across display a pixel at a time."""
    for pos in positions:
        ws.ws2811_led_set(channel, pos, FACE_COLOR)
    
    resp = ws.ws2811_render(leds)
    if resp != ws.WS2811_SUCCESS:
        message = ws.ws2811_get_return_t_str(resp)
        raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))

def SetFeatures(channel, positions):
    """Wipe color across display a pixel at a time."""
    for pos in positions:
        ws.ws2811_led_set(channel, pos, FACE_COLOR)
    
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

def ClearRegion(channel, position):
    for pos in position:
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

async def led_loop():
    global last_mode
    global blinkchoice
    while True:
        blink = random.choice(blinkchoice)
        if(blink):
            ClearRegion(channel,EYES_POS)
            SetEyes(channel, BLINK_EYE_POS)
            await asyncio.sleep(0.5)
            ClearRegion(channel,EYES_POS)
            
        if(current_tongue):
            SetTongue(channel)
        else:
            ClearRegion(channel,BLEP_TONGUE_POS)
            
        if current_mode == "blink":
            ClearRegion(channel, FEATURES_POS)
            SetEyes(channel, CALM_EYE_POS)
            SetMouth(channel, BASIC_SMILE_POS)
        elif current_mode == "off":
            FullClear(channel)
        elif current_mode == "flustered":
            SetEyes(channel, CALM_EYE_POS)
            SetFeatures(channel, FLUSTERED_FEATURE_POS)
            SetMouth(channel, SMALL_SMILE_POS)
        elif current_mode == "veryflustered":
            SetEyes(channel, FLUSTERED_EYE_POS)
            SetFeatures(channel, FLUSTERED_FEATURE_POS)
            SetMouth(channel, SMALL_SMILE_POS)
        elif current_mode == "smug":
            SetEyes(channel, SMUG_EYES_POS)
            SetFeatures(channel, FLUSTERED_FEATURE_POS)
            SetMouth(channel, SMUG_SMILE_POS)
        elif current_mode == "worried":
            SetEyes(channel, WORRIED_EYES_POS)
            SetMouth(channel, SMALL_SMILE_POS)
        else:
            await asyncio.sleep(1)
        last_mode = current_mode
        last_tongue = current_tongue
        # Wait 5 seconds, but check every 0.1s if mode changed
        for _ in range(70):
            await asyncio.sleep(0.1)
            if current_tongue != last_tongue:
                FullClear(channel)
                break
            if current_mode != last_mode:
                FullClear(channel)
                break

async def input_loop():
    while True:
        cmd = await aioconsole.ainput("Enter command: ")
        global current_mode
        global current_tongue
        if cmd in ["blink", "flustered", "smug", "veryflustered", "off", "worried"]:
            current_mode = cmd
            print(f"Switched to mode: {cmd}")
        elif cmd == "blep":
            print("Blep! :3")
            if(current_tongue == False):
                current_tongue = True
            else:
                current_tongue = False
        else:
            print(f"Unknown command: {cmd}")

# Wrap following code in a try/finally to ensure cleanup functions are called
# after library is initialized.
async def main():
    try:
        print("INITIALIZING NOVA")
        led_task = asyncio.create_task(led_loop())
        input_task = asyncio.create_task(input_loop())
        await asyncio.gather(led_task, input_task)
    finally:
        print("STOPPING NOVA")
        FullClear(channel)
        # Ensure ws2811_fini is called before the program quits.
        ws.ws2811_fini(leds)
        # Example of calling delete function to clean up structure memory.  Isn't
        # strictly necessary at the end of the program execution here, but is good practice.
        ws.delete_ws2811_t(leds)

asyncio.run(main())

