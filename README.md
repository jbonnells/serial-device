```text
____ ____ ____ _ ____ _       ___  ____ _  _ _ ____ ____ 
[__  |___ |__/ | |__| |       |  \ |___ |  | | |    |___ 
___] |___ |  \ | |  | |___    |__/ |___  \/  | |___ |___   
____ _  _ _  _ _    ____ ___ ____ ____ 
|___ |\/| |  | |    |__|  |  |  | |__/ 
|___ |  | |__| |___ |  |  |  |__| |  \ 
```
#  

## Environment Configuration
It may be necessary to use virtual ports if a physical loopback is not available. A simple way to accomplish this is by using `socat`:
```bash
socat -d -d pty,raw,echo=0 pty,raw,echo=0
```
This will create two virtual ports that are tied together, which can be subsequently used for running the ImuEmulator with another device. 

#### Example 
```bash
$ socat -d -d pty,raw,echo=0 pty,raw,echo=0
socat[5255] N PTY is /dev/pts/3
socat[5255] N PTY is /dev/pts/5
$ python ImuEmulator.py --serial-port=/dev/pts/3
```

## Operating Instructions
### To start the `ImuEmulator`: 
1. Navigate root project directory.
2. Launch the Python script (using default values):
```bash
$ python ImuEmulator.py
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
$ python ImuEmulator.py --serial-port=/dev/ttyS0 --little-endian
```