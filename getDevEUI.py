from network import LoRa
import binascii

lora = LoRa(mode=LoRa.LORAWAN)
print(binascii.hexlify(lora.mac()).decode())