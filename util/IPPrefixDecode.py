import socket
import struct


def decode_ip_prefix(str_prefix: str):
    prefix = str_prefix.split("/")
    if len(prefix) != 2:
        raise RuntimeError("Bad IP Prefix: %s" % str_prefix)
    hex_ip = decode_ip(prefix[0])
    prefix_len = int(prefix[1])
    mask = hex(eval('0b' + '1' * prefix_len + '0' * (32 - prefix_len)))
    return {'str_address': prefix[0], 'prefix_len': prefix_len, 'hex_address': hex_ip, 'hex_mask': mask}


def decode_ip(ip_str):
    packed_ip = socket.inet_aton(ip_str.strip())
    int_ip = struct.unpack("!L", packed_ip)[0]
    hex_ip = hex(int_ip)
    return hex_ip
