from network import LoRa
from machine import I2C
import socket, binascii, time

# ---------- TTN credentials ----------
DEV_EUI = binascii.unhexlify('70B3D549998385BA')
APP_EUI = binascii.unhexlify('535441434B494F54')
APP_KEY = binascii.unhexlify('9A46F8FF92DF784CA5C0B50E9048BB33')

# ---------- I2C (TC74) ----------
TC74_ADDR = 0x48
i2c = I2C(0, I2C.MASTER, pins=('P9', 'P10'))

def read_tc74_temp_c(): 
    return i2c.readfrom(TC74_ADDR, 1)[0]

# ---------- LoRaWAN setup (EU868) ----------
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
print("Joining TTN...")
lora.join(activation=LoRa.OTAA, auth=(DEV_EUI, APP_EUI, APP_KEY), timeout=0)

while not lora.has_joined():
    print("Waiting for join...")
    time.sleep(2)

print("Joined TTN")

# ---------- LoRa socket ----------
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
s.setblocking(True)

# ---------- Payload encoder ----------
def encode_payload(event_char, temp_c, default_code):
    # temp is sent as 0.1°C units in uint16 little-endian
    t = int(round(temp_c * 10))
    return bytes([
        0x01, ord(event_char) & 0xFF,        # event
        0x03, default_code & 0xFF,           # default flag
        0x02, t & 0xFF, (t >> 8) & 0xFF      # temp (LE)
    ])

# ---------- Main loop ----------
while True:
    temp = float(read_tc74_temp_c())          # TC74 gives integer °C; make it float for your logic
    default = 1 if temp > 32.5 else 0         # your rule
    payload = encode_payload('E', temp, default)

    rc = s.send(payload)

    print("Temp:", temp, "°C | default:", default,
          "| sent:", rc, "| hex:", binascii.hexlify(payload).decode())

    time.sleep(120)
