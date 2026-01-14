from network import LoRa
import socket
import binascii
import time
import ujson  # MicroPython JSON

DEV_EUI = binascii.unhexlify('70B3D549998385BA')
APP_EUI = binascii.unhexlify('535441434B494F54')
APP_KEY = binascii.unhexlify('9A46F8FF92DF784CA5C0B50E9048BB33')

# Initialize LoRaWAN (EU868)
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

print('Joining TTN...')
lora.join(activation=LoRa.OTAA, auth=(DEV_EUI, APP_EUI, APP_KEY), timeout=0)

while not lora.has_joined():
    print('Waiting for join...')
    time.sleep(2)

print('Joined TTN')

# Create LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)  # DR0 = SF12 (small payloads)
s.setblocking(True)

# Build JSON payload (dictionary -> JSON string -> bytes)
data = {
    "event": "E",
    "temp": 33,
    "default": 0
}

json_str = ujson.dumps(data)          # '{"event":"E","temp":33,"default":0}'
payload = json_str.encode('utf-8')    # bytes

rc = s.send(payload)

print("JSON string:", json_str)
print("Sent bytes:", payload)
print("Bytes sent:", rc)
