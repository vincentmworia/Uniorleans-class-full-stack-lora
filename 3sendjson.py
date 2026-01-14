from network import LoRa
import socket, binascii, time, machine

DEV_EUI = binascii.unhexlify('70B3D549998385BA')
APP_EUI = binascii.unhexlify('535441434B494F54')
APP_KEY = binascii.unhexlify('9A46F8FF92DF784CA5C0B50E9048BB33')

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
print("Joining TTN...")
lora.join(activation=LoRa.OTAA, auth=(DEV_EUI, APP_EUI, APP_KEY), timeout=0)
while not lora.has_joined():
    time.sleep(2)
print("Joined TTN")

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
s.setblocking(True)

def encode_payload(event_char, temp_c, default_code):
    t = int(round(temp_c * 10))
    return bytes([
        0x01, ord(event_char) & 0xFF,
        0x03, default_code & 0xFF,
        0x02, t & 0xFF, (t >> 8) & 0xFF
    ])

while True:
    temp = 25 + (machine.rng() & 0xFF) / 255 * 10
    default = 1 if temp > 32.5 else 0
    payload = encode_payload('E', temp,default)

    rc = s.send(payload)
    print("Temp:", round(temp, 1), "°C | sent:", rc, "| hex:", binascii.hexlify(payload).decode())

    time.sleep(120)
