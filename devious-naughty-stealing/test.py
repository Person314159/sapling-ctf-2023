import base64
import re

from scapy.all import *

pcap = sniff(offline="logs.pcap", filter="udp", quiet=True)
b = b""

for i in pcap:
    if i.payload.payload.payload.qr and i.payload.payload.payload.qd.qname.endswith(b".evil-elpam-encroachers.org."):
        b += i.payload.payload.payload.qd.qname[:48]

print(re.search(r"maple\{[a-zA-Z0-9_!\-\?]+\}", base64.b64decode(b, altchars="-_").decode())[0])
