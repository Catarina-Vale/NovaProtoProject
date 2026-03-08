
import time
import random
import asyncio
import aioconsole
from rpi_ws281x import Color, PixelStrip, ws


# LED strip configuration:
LED_CHANNEL = 0
LED_COUNT = 512              # How many LEDs to light.
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

MOUTH_POS = [0,1,2,15,14,13,16,17,18,31,30,29,32,33,34,47,46,45,48,49,50,63,62,61,64,65,66,79,78,80,81,95,94,96,97,111,110,112,113,114,127,126,125,128,129,130,143,142,141,144,145,146,159,158,157,160,161,162,175,174,173,176,177,178,191,190,189,192,193,194,207,206,205,208,209,210,223,222,221,224,225,226,239,238,237,240,241,242,255,254,253,]
FEATURES_POS = [119,124,123	,122,121,120,131,132	,133,134,135,140,139	,138,137,136,147,148	,149,150,151,156,155	,154,153,152,163,164	,165,166,167,172,171	,170,169,168,179,180	,181,182,183,188,187	,186,185,184,195,196	,197,198,199,204,203	,202,201,200,211,212	,213,214,215,220,219	,218,217,216,227,228	,229,230,231,236,235	,234,233,232,243,244	,245,246,247,252,251	,250,249,248,3	,4	,5	,6,7,12,11	,10,9,8,19,20	,21,22,23,28,27	,26,25,24,35,36	,37,38,39,44,43	,42,41,40,51,52	,53,54,55,34,29,18,17]
EYES_POS = [115,116,117,118,77,82,93,98,109,60,59,58,57,56,67,68,69,70,71,76,75,74,73,72,83,84,85,86,87,92,91,90,89,88,99,100,101,102,103,108,107,106,105,104,]

CALM_EYE_POS = [69,73,75,86,84,89,90,91,101]
BLINK_EYE_POS = [91,101,89]
BASIC_SMILE_POS = [31,30,32,33,47,46,48,49,63,62,64,65,79,78,80,81,95,94,96,97,111,110,112,113,127,126,128,129,143,142,144,145,159,158,160,161,175,174,176,177,191,190,192,193,207,206,208,209,223,222,224,225,239,238,240,241,255,254,]

FLUSTERED_SMILE_POS = [145,158,162,173,177,190,192,207,209,222,226,237,241,254]
FLUSTERED_EYE_POS = [69,73,75,86,84,89,85,91,101]
FLUSTERED_FEATURE_POS = [132,138,150,155,165,169,180,186,198]

VERY_FLUSTERED_EYE_POS = [90,100,106,105,103,88,87,73,74,75,76,82,93,98,109,115]
VERY_FLUSTERED_FEATURE_POS = [21,20,37,38]


NOSE_POS = [234,246]

WORRIED_MOUTH_POS = [160,161,175,174,176,177,191,190,192,193,207,206,208,209,223,222,224,225,239,238,240,241,255,254,]
WORRIED_EYES_POS = [90,75,74,73,87,88,103,105,106,107,99,92,83]

SMUG_EYES_POS = [73,86,85,90,89,101,102,106,105]
SMUG_SMILE_POS = [178,190,192,207,208,223,224,239,241,253]
current_mode = "blink"
last_mode = "blink"

def MirrorList(list):
    newlist = [511-x for x in list]
    list.extend(newlist)
    return list

# Define functions which animate LEDs in various ways.
def SetMouth(channel, positions):
    """Wipe color across display a pixel at a time."""
    positions = MirrorList(positions)
    for pos in positions:
        ws.ws2811_led_set(channel, pos, FACE_COLOR)
    
    resp = ws.ws2811_render(leds)
    if resp != ws.WS2811_SUCCESS:
        message = ws.ws2811_get_return_t_str(resp)
        raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))
    
def SetEyes(channel, positions):
    positions = MirrorList(positions)
    for pos in positions:
        ws.ws2811_led_set(channel, pos, FACE_COLOR)
    
    resp = ws.ws2811_render(leds)
    if resp != ws.WS2811_SUCCESS:
        message = ws.ws2811_get_return_t_str(resp)
        raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))

def SetEye(channel, positions):
    for pos in positions:
        ws.ws2811_led_set(channel, pos, FACE_COLOR)
    
    resp = ws.ws2811_render(leds)
    if resp != ws.WS2811_SUCCESS:
        message = ws.ws2811_get_return_t_str(resp)
        raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))

def SetFeatures(channel, positions):
    positions = MirrorList(positions)
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
    
async def Blink(channel,lastEyePos):
    ClearRegion(channel,EYES_POS)
    mirror = BLINK_EYE_POS
    mirror.extend(MirrorList(BLINK_EYE_POS))
    SetEyes(channel, mirror)
    await asyncio.sleep(0.5)
    ClearRegion(channel,EYES_POS)
    SetEyes(channel, lastEyePos)

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
    lastEyePos = CALM_EYE_POS
    while True:
        SetFeatures(channel,NOSE_POS)
            
        if current_mode == "blink":
            lastEyePos = CALM_EYE_POS
            ClearRegion(channel, FEATURES_POS)
            SetEyes(channel, CALM_EYE_POS)
            SetMouth(channel, BASIC_SMILE_POS)
        elif current_mode == "off":
            FullClear(channel)
        elif current_mode == "flustered":
            lastEyePos = CALM_EYE_POS
            SetEyes(channel, CALM_EYE_POS)
            SetFeatures(channel, FLUSTERED_FEATURE_POS)
            SetMouth(channel, FLUSTERED_SMILE_POS)
        elif current_mode == "veryflustered":
            lastEyePos = VERY_FLUSTERED_EYE_POS
            SetEyes(channel, VERY_FLUSTERED_EYE_POS)
            SetFeatures(channel, VERY_FLUSTERED_FEATURE_POS)
            SetFeatures(channel, FLUSTERED_FEATURE_POS)
            SetMouth(channel, FLUSTERED_SMILE_POS)
        elif current_mode == "smug":
            lastEyePos = SMUG_EYES_POS
            SetEyes(channel, SMUG_EYES_POS)
            SetFeatures(channel, FLUSTERED_FEATURE_POS)
            SetMouth(channel, SMUG_SMILE_POS)
        elif current_mode == "worried":
            lastEyePos = WORRIED_EYES_POS
            SetEyes(channel, WORRIED_EYES_POS)
            SetMouth(channel, WORRIED_MOUTH_POS)
            SetFeatures(channel,VERY_FLUSTERED_FEATURE_POS)
        else:
            await asyncio.sleep(1)
            
        last_mode = current_mode
        # Wait 5 seconds, but check every 0.1s if mode changed
        for _ in range(100):
            await asyncio.sleep(0.1)
            c = random.randint(1, 100)
            if(c == 1):
                await Blink(channel,lastEyePos)
            if current_mode != last_mode:
                ClearRegion(channel,EYES_POS)
                ClearRegion(channel,FEATURES_POS)
                ClearRegion(channel,MOUTH_POS)
                break

async def input_loop():
    while True:
        cmd = await aioconsole.ainput("Enter command: ")
        global current_mode
        global current_tongue
        if cmd in ["blink", "flustered", "smug", "veryflustered", "off", "worried"]:
            current_mode = cmd
            print(f"Switched to mode: {cmd}")
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

