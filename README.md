# Serial Device Emulator

## Environment Configuration
It may be necessary to use virtual ports if a physical loopback is not available. A simple way to accomplish this is by using `socat`:
```bash
socat -d -d pty,raw,echo=0 pty,raw,echo=0
```
This will create two virtual ports that are tied together, and can subsequently used for running the ImuEmulator and ImuParser. 

#### Example 
```bash
$ socat -d -d pty,raw,echo=0 pty,raw,echo=0
socat[5255] N PTY is /dev/pts/3
socat[5255] N PTY is /dev/pts/5
$ sudo python ImuEmulator.py --serial-port=/dev/pts/3
```

## Operating Instructions
### To start the `ImuEmulator`: 
1. Navigate root project directory.
2. Launch the Python script with `sudo` (using default values):
```bash
sudo python ImuEmulator.py
```
There are several run-time configurable parameters that can be set via command line. They are outlined below:
| Parameter | Description |
| --- | --- |
| --serial-port | Serial port to read from (default: `/dev/tty1`) |
| --baud-rate | Baud rate for the serial connection (default: `921600`) |             
| --udp-ip | UDP destination IP address (default: `127.0.0.1`) |
| --udp-port | UDP destination port (default: `5005`) |
| --little-endian | Sets little-endian format for outgoing data (default: `big-endian`) |

#### Example
```bash
sudo python ImuEmulator.py --serial-port=/dev/ttyS0 --little-endian
```