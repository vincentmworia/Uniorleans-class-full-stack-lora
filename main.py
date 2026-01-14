from network import LoRa
import socket
import binascii
import time

# =================================================
# TTN credentials (YOUR DEVICE)
# =================================================
DEV_EUI = binascii.unhexlify('70B3D54997173C54')
APP_EUI = binascii.unhexlify('A26C05587F96CC6A')
APP_KEY = binascii.unhexlify('F6E8856539C52EC43753E9FBB7CF9F24')

# =================================================
# Initialize LoRaWAN (EU868)
# =================================================
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

print('Joining TTN...')

lora.join(
    activation=LoRa.OTAA,
    auth=(DEV_EUI, APP_EUI, APP_KEY),
    timeout=0
)

while not lora.has_joined():
    print('Waiting for join...')
    time.sleep(2)

print('Joined TTN')

# =================================================
# Create LoRa socket
# =================================================
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)  # DR0 (SF12) reliable
s.setblocking(True)

# =================================================
# Send payload
# =================================================
payload = bytearray(b'Hello Vincent')
rc = s.send(payload)

print('Sent payload:', payload)
print('Bytes sent:', rc)
