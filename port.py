import subprocess
import os

def get_matching_usb_devices(keyword):
    try:
        result = subprocess.run(['lsusb'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("Error running lsusb:", result.stderr)
            return []

        # Filter lines that contain the keyword
        matching_lines = [line for line in result.stdout.splitlines() if keyword.lower() in line.lower()]
        return matching_lines

    except FileNotFoundError:
        print("lsusb not found. Install it with: sudo apt install usbutils")
        return []

def find_tty_devices():
    # Look in /dev for serial USB devices
    tty_devices = []
    for dev in os.listdir('/dev'):
        if dev.startswith('ttyUSB') or dev.startswith('ttyACM'):
            tty_devices.append('/dev/' + dev)
    return tty_devices

def main(keyword):
    matching_devices = get_matching_usb_devices(keyword)
    if not matching_devices:
        print(f"No USB devices found with keyword '{keyword}'")
        return

    print(f"Matched USB devices for '{keyword}':\n")
    for line in matching_devices:
        print("  " + line)

    print("\nLooking for serial ports (ttyUSB*/ttyACM*):")
    tty_ports = find_tty_devices()
    if tty_ports:
        for port in tty_ports:
            print("  " + port)
    else:
        print("  No serial ports found.")

if __name__ == '__main__':
    # Example: change this to whatever keyword you want
    main(keyword="Mirion")