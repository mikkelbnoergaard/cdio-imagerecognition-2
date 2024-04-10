import bluetooth

# Replace "XX:XX:XX:XX:XX:XX" with the actual Bluetooth address of your LEGO Mindstorms
server_address = "A8E2C1A11C64"
port = 1  # Standard RFCOMM port for serial communication

try:
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((server_address, port))

    # Communication logic here (send commands to trigger functions on the robot)

    sock.close()
except Exception as e:
    print("Error connecting:", e)