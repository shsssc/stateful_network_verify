import socket
import struct


def decode_ip_prefix(str_prefix: str):
    prefix = str_prefix.split("/")
    if len(prefix) != 2:
        raise RuntimeError("Bad IP Prefix: %s" % str_prefix)
    packed_ip = socket.inet_aton(prefix[0].strip())
    hex_ip = hex(struct.unpack("!L", packed_ip)[0])
    return{'str_address': prefix[0], 'prefix_len': int(prefix[1]), 'hex_address': hex_ip}
