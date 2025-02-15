import serial
import socket
import struct
import random
import re
import argparse

# IMU packet header
HEADER = b'\x7F\xF0\x1C\xAF'

# generates a random value with a positive/negative 'drift'
def rand_gen(start=0.0, drift_range=(-0.5, 1.0)):
    value = start
    while True:
        value += random.uniform(*drift_range)
        yield value

# compares two values with a tolerance
def comp(a, b, tol=0.01):
    return True if abs(a) - abs(b) < tol else False
    
# program entry-point
def main(args):
    
    # open serial port
    ser = serial.Serial(args.serial_port, args.baud_rate, timeout=1)
    if ser.is_open:
        print(f"Serial port opened successfully. (Serial: {args.serial_port}, Baud: {args.baud_rate})")

    # open UDP socket for receiving responses
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.udp_ip, args.udp_port))
    sock.settimeout(1)
    if sock:
        print(f"UDP socket opened successfully. (IP: {args.udp_ip}, Port: {args.udp_port})")

    # generators for simulated X, Y, Z values
    genx = rand_gen(start=random.uniform(-10, 10), drift_range=(-0.2, 0.2))
    geny = rand_gen(start=random.uniform(-10, 10), drift_range=(-0.2, 0.2))
    genz = rand_gen(start=random.uniform(-10, 10), drift_range=(-0.2, 0.2))
    packet_count = 0

    # determine the structure packing based on whether the little-endian flag is set
    pack_fmt = '<Ifff' if args.little_endian else '!Ifff'

    while True:
        packet_count += 1
        rate_x = next(genx)
        rate_y = next(geny)
        rate_z = next(genz)

        # build the outgoing packet with count, and xyz values
        packet = HEADER + struct.pack(pack_fmt, packet_count, rate_x, rate_y, rate_z)

        # send the packet over serial
        ser.write(packet)
        print(f"Sent: Packet {packet_count} | ", end='')
        for byte in packet:
            print(f'{hex(byte)} ', end='')
        print(flush=True)
        
        # attempt to read a response
        try:
            data, _ = sock.recvfrom(1024)
            print(f"Recv: {data.decode()}",end='')

            # regex to extract the IMU values
            match = re.search(r'X=(-?\d+\.\d+), Y=(-?\d+\.\d+), Z=(-?\d+\.\d+)', data.decode())
            if match:
                x, y, z = map(float, match.groups())
                # do a comparison on the values sent vs. values received with a 0.01 tolerance
                if comp(x, rate_x) and comp(y, rate_y) and comp(z, rate_z):
                    print("\tValidated received packet!\n",flush=True)
                else:
                    print(f"\tCould not validate packet\n",flush=True)
            else:
                continue
        except socket.timeout:
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Read from a serial port and send data over UDP.")
    parser.add_argument("--serial-port", help="Serial port to read from (e.g., /dev/tty1 or /dev/pts/3)", default='/dev/tty1')
    parser.add_argument("--baud-rate", type=int, help="Baud rate for the serial connection", default=921600)
    parser.add_argument("--udp-ip", help="UDP destination IP address", default="127.0.0.1")
    parser.add_argument("--udp-port", type=int, help="UDP destination port", default=5005)
    parser.add_argument("--little-endian", action="store_true", help="Sets little-endian format for outgoing data (default: big-endian)")

    args = parser.parse_args()
    main(args)