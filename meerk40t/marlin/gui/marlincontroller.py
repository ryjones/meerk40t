#!/usr/bin/env python3
#
# generated by wxGlade 1.0.0 on Thu Feb  3 06:49:54 2022
#
import threading

import wx

from meerk40t.gui.icons import icons8_connected_50, icons8_disconnected_50
from meerk40t.gui.mwindow import MWindow
from meerk40t.gui.wxutils import dip_size
from meerk40t.kernel import signal_listener

_ = wx.GetTranslation

realtime_commands = (
    "!",  # pause
    "~",  # resume
    "?",  # status report
    # "$X",
)


class MarlinControllerPanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        self.service = context
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.state = None
        self.button_device_connect = wx.Button(self, wx.ID_ANY, _("Connection"))
        self.button_device_connect.SetBackgroundColour(wx.Colour(102, 255, 102))
        self.button_device_connect.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                "Segoe UI",
            )
        )
        self.button_device_connect.SetToolTip(
            _("Force connection/disconnection from the device.")
        )
        self.button_device_connect.SetBitmap(
            icons8_connected_50.GetBitmap(use_theme=False)
        )
        sizer_1.Add(self.button_device_connect, 0, wx.EXPAND, 0)

        static_line_2 = wx.StaticLine(self, wx.ID_ANY)
        static_line_2.SetMinSize(dip_size(self, 483, 5))
        sizer_1.Add(static_line_2, 0, wx.EXPAND, 0)

        self.data_exchange = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        sizer_1.Add(self.data_exchange, 1, wx.EXPAND, 0)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.gcode_commands = list()
        self.gcode_commands.append(
            ("G28", _("Home"), _("Send laser to logical home-position"), None)
        )
        for entry in self.gcode_commands:
            btn = wx.Button(self, wx.ID_ANY, entry[1])
            btn.Bind(wx.EVT_BUTTON, self.send_gcode(entry[0]))
            btn.SetToolTip(entry[2])
            if entry[3] is not None:
                btn.SetBitmap(entry[3].GetBitmap(size=25, use_theme=False))
            sizer_2.Add(btn, 1, wx.EXPAND, 0)
        self.btn_clear = wx.Button(self, wx.ID_ANY, _("Clear"))
        self.btn_clear.SetToolTip(_("Clear log window"))
        self.btn_clear.Bind(wx.EVT_BUTTON, self.on_clear_log)
        sizer_2.Add(self.btn_clear, 0, wx.EXPAND), 0
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)

        self.gcode_text = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.gcode_text.SetToolTip(_("Enter a Gcode-Command and send it to the laser"))
        self.gcode_text.SetFocus()
        sizer_1.Add(self.gcode_text, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_1)

        self.Layout()

        self.Bind(
            wx.EVT_BUTTON, self.on_button_start_connection, self.button_device_connect
        )
        self.Bind(wx.EVT_TEXT_ENTER, self.on_gcode_enter, self.gcode_text)
        self._buffer = ""
        self._buffer_lock = threading.Lock()
        # end wxGlade

    def on_clear_log(self, event):
        self.data_exchange.SetValue("")

    def on_button_start_connection(
        self, event
    ):  # wxGlade: SerialControllerPanel.<event_handler>
        if self.state == "connected":
            self.service.controller.stop()
        else:
            self.service.controller.start()

    def send_gcode(self, gcode_cmd):
        def handler(event):
            self.service(f"gcode_realtime {gcode_cmd}")

        return handler

    def on_gcode_enter(self, event):  # wxGlade: SerialControllerPanel.<event_handler>
        cmd = self.gcode_text.GetValue()
        if cmd in realtime_commands:
            self.service(f"gcode_realtime {cmd}")
        else:
            self.service(f"gcode {cmd}")
        self.gcode_text.Clear()

    def update(self, data, type):
        if type == "send":
            # Quick judgement call: first character extended ascii?
            # Then show all in hex:
            if len(data) > 0 and ord(data[0]) >= 128:
                display = "0x"
                idx = 0
                for c in data:
                    if idx > 0:
                        display += " "
                    display += f"{ord(c):02x}"
                    idx += 1
            else:
                display = data
            with self._buffer_lock:
                self._buffer += f"<--{display}\n"
            self.service.signal("marlin_controller_update", True)
        elif type == "recv":
            with self._buffer_lock:
                self._buffer += f"-->\t{data}\n"
            self.service.signal("marlin_controller_update", True)
        elif type == "event":
            with self._buffer_lock:
                self._buffer += f"{data}\n"
            self.service.signal("marlin_controller_update", True)
        elif type == "connection":
            with self._buffer_lock:
                self._buffer += f"{data}\n"
            self.service.signal("marlin_controller_update", True)

    @signal_listener("marlin_controller_update")
    def update_text_gui(self, origin, *args):
        with self._buffer_lock:
            buffer = self._buffer
            self._buffer = ""
        self.data_exchange.AppendText(buffer)

    def on_status(self, origin, state):
        self.state = state
        if state == "uninitialized" or state == "disconnected":
            self.button_device_connect.SetBackgroundColour("#ffff00")
            self.button_device_connect.SetLabel(_("Connect"))
            self.button_device_connect.SetBitmap(
                icons8_disconnected_50.GetBitmap(use_theme=False)
            )
            self.button_device_connect.Enable()
        elif state == "connected":
            self.button_device_connect.SetBackgroundColour("#00ff00")
            self.button_device_connect.SetLabel(_("Disconnect"))
            self.button_device_connect.SetBitmap(
                icons8_connected_50.GetBitmap(use_theme=False)
            )
            self.button_device_connect.Enable()

    def pane_show(self):
        if (
            self.state is None
            or self.state == "uninitialized"
            or self.state == "disconnected"
        ):
            self.button_device_connect.SetBackgroundColour("#ffff00")
            self.button_device_connect.SetLabel(_("Connect"))
            self.button_device_connect.SetBitmap(
                icons8_disconnected_50.GetBitmap(use_theme=False)
            )
            self.button_device_connect.Enable()
        elif self.state == "connected":
            self.button_device_connect.SetBackgroundColour("#00ff00")
            self.button_device_connect.SetLabel(_("Disconnect"))
            self.button_device_connect.SetBitmap(
                icons8_connected_50.GetBitmap(use_theme=False)
            )
            self.button_device_connect.Enable()

    def pane_hide(self):
        return


class MarlinController(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(499, 357, *args, **kwds)
        self.service = self.context.device
        self.SetTitle(_("Marlin Controller"))
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_connected_50.GetBitmap())
        self.SetIcon(_icon)

        self.serial_panel = MarlinControllerPanel(self, wx.ID_ANY, context=self.service)
        self.Layout()
        self._opened_port = None
        # end wxGlade

    @signal_listener("marlin;status")
    def on_serial_status(self, origin, state):
        self.serial_panel.on_status(origin, state)

    def window_open(self):
        try:
            self.service.controller.add_watcher(self.serial_panel.update)
        except AttributeError:
            pass
        self.serial_panel.pane_show()

    def window_close(self):
        try:
            self.service.controller.remove_watcher(self.serial_panel.update)
        except AttributeError:
            pass
        self.serial_panel.pane_hide()

    def delegates(self):
        yield self.serial_panel

    @staticmethod
    def submenu():
        return "Device-Control", "Marlin Controller"
