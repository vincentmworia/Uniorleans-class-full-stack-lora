from network import LoRa
import socket
import binascii
import time

DEV_EUI = binascii.unhexlify('70B3D549998385BA')
APP_EUI = binascii.unhexlify('535441434B494F54')
APP_KEY = binascii.unhexlify('9A46F8FF92DF784CA5C0B50E9048BB33')

# -------------------------------------------------
# LoRaWAN setup (EU868)
# -------------------------------------------------
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

print('Joining TTN...')
lora.join(activation=LoRa.OTAA, auth=(DEV_EUI, APP_EUI, APP_KEY), timeout=0)

while not lora.has_joined():
    print('Waiting for join...')
    time.sleep(2)

print('Joined TTN')

# Create LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)  # DR0 (SF12) reliable, small payload
s.setblocking(True)

# -------------------------------------------------
# Compact payload encoder
# Format: [code][value...]
# 0x01 event   : 1 byte ASCII (e.g. 'E' = 0x45)
# 0x02 temp    : uint16 little-endian, unit = 0.1°C
# 0x03 default : 1 byte
# Example for E, 33.0°C, default=0:
# 01 45 03 00 02 4A 01
# -------------------------------------------------
def encode_payload(event_char, temp_c, default_code):
    b = bytearray()

    # event
    b.append(0x01)
    b.append(ord(event_char) & 0xFF)

    # default
    b.append(0x03)
    b.append(default_code & 0xFF)

    # temp in 0.1°C
    t = int(round(temp_c * 10))  # 33.0 -> 330
    b.append(0x02)
    b.append(t & 0xFF)           # LSB
    b.append((t >> 8) & 0xFF)    # MSB

    return b

# Send every 50 seconds
while True:
    payload = encode_payload('E', 33.0, 0) 
    
    rc = s.send(binascii.unhexlify('01450300024a01'))
    print("Bytes sent:", rc)
    print("Sent bytes (hex):", binascii.hexlify(payload).decode())

    time.sleep(120)
