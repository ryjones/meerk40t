"""
Serial Connection

Registers the serial connection using pyserial to talk with the serial devices.
"""

import serial
from serial import SerialException


class SerialConnection:
    def __init__(self, service, controller):
        self.service = service
        self.controller = controller
        self.laser = None
        self.read_buffer = bytearray()

    @property
    def connected(self):
        return self.laser is not None

    def read(self):
        try:
            self.read_buffer += self.laser.read(self.laser.in_waiting)
        except (SerialException, AttributeError, OSError, TypeError):
            pass
        f = self.read_buffer.find(b"\n")
        if f == -1:
            return None
        response = self.read_buffer[:f]
        self.read_buffer = self.read_buffer[f + 1 :]
        str_response = str(response, "raw_unicode_escape")
        str_response = str_response.strip()
        return str_response

    def write(self, line):
        try:
            self.laser.write(bytes(line, "utf-8"))
        except (SerialException, PermissionError) as e:
            self.controller.log(
                f"Error when writing '{line}: {str(e)}'", type="connection"
            )

    def connect(self):
        if self.laser:
            self.controller.log("Already connected", type="connection")
            return

        signal_load = "uninitialized"
        try:
            self.controller.log("Attempting to Connect...", type="connection")
            serial_port = self.service.serial_port
            if serial_port == "UNCONFIGURED":
                self.controller.log("Laser port is not set.", type="connection")
                signal_load = "error"
                self.service.signal(
                    "warning",
                    "Serial Port is not set. Go to config, select the serial port for this device.",
                    "Serial Port: UNCONFIGURED",
                )
                return

            baud_rate = self.service.baud_rate
            self.laser = serial.Serial(
                serial_port,
                baud_rate,
                timeout=0,
            )
            self.controller.log("Connected", type="connection")
            signal_load = "connected"
        except ConnectionError:
            self.controller.log("Connection Failed.", type="connection")
        except SerialException as e:
            self.controller.log(
                "Serial connection could not be established.", type="connection"
            )
            self.controller.log(str(e), type="connection")

        self.service.signal("marlin;status", signal_load)

    def disconnect(self):
        self.controller.log("Disconnected", type="connection")
        if self.laser:
            self.laser.close()
            del self.laser
            self.laser = None
        self.service.signal("marlin;status", "disconnected")
