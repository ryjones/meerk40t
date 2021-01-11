# -*- coding: ISO-8859-1 -*-
#
# generated by wxGlade 0.9.3 on Thu Jun 27 21:45:40 2019
#

import wx

from Kernel import Module
from icons import icons8_administrative_tools_50

_ = wx.GetTranslation


# begin wxGlade: dependencies
# end wxGlade

class Preferences(wx.Frame, Module):
    def __init__(self, parent, *args, **kwds):
        # begin wxGlade: Preferences.__init__
        wx.Frame.__init__(self, parent, -1, "",
                          style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT | wx.TAB_TRAVERSAL)
        Module.__init__(self)
        self.SetSize((395, 424))
        self.combobox_board = wx.ComboBox(self, wx.ID_ANY, choices=["M2", "B2", "M", "M1", "A", "B", "B1"], style=wx.CB_DROPDOWN)
        self.checkbox_flip_x = wx.CheckBox(self, wx.ID_ANY, _("Flip X"))
        self.checkbox_home_right = wx.CheckBox(self, wx.ID_ANY, _("Homes Right"))
        self.checkbox_flip_y = wx.CheckBox(self, wx.ID_ANY, _("Flip Y"))
        self.checkbox_home_bottom = wx.CheckBox(self, wx.ID_ANY, _("Homes Bottom"))
        self.checkbox_swap_xy = wx.CheckBox(self, wx.ID_ANY, _("Swap X and Y"))
        self.checkbox_mock_usb = wx.CheckBox(self, wx.ID_ANY, _("Mock USB Connection Mode"))
        self.spin_device_index = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1, max=5)
        self.spin_device_address = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1, max=5)
        self.spin_device_bus = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1, max=5)
        self.spin_device_version = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1, max=255)
        self.spin_home_x = wx.SpinCtrlDouble(self, wx.ID_ANY, "0.0", min=-50000.0, max=50000.0)
        self.spin_home_y = wx.SpinCtrlDouble(self, wx.ID_ANY, "0.0", min=-50000.0, max=50000.0)
        self.button_home_by_current = wx.Button(self, wx.ID_ANY, _("Set Current"))
        self.spin_bedwidth = wx.SpinCtrlDouble(self, wx.ID_ANY, "330.0", min=1.0, max=1000.0)
        self.spin_bedheight = wx.SpinCtrlDouble(self, wx.ID_ANY, "230.0", min=1.0, max=1000.0)
        self.checkbox_autolock = wx.CheckBox(self, wx.ID_ANY, _("Automatically lock rail"))
        self.checkbox_autohome = wx.CheckBox(self, wx.ID_ANY, _("Home after job complete"))
        self.checkbox_autobeep = wx.CheckBox(self, wx.ID_ANY, _("Beep after job complete"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_COMBOBOX, self.on_combobox_boardtype, self.combobox_board)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_swap_xy, self.checkbox_swap_xy)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_flip_x, self.checkbox_flip_x)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_home_right, self.checkbox_home_right)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_flip_y, self.checkbox_flip_y)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_home_bottom, self.checkbox_home_bottom)
        self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_mock_usb, self.checkbox_mock_usb)
        self.Bind(wx.EVT_SPINCTRL, self.spin_on_device_index, self.spin_device_index)
        self.Bind(wx.EVT_TEXT, self.spin_on_device_index, self.spin_device_index)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_device_index, self.spin_device_index)
        self.Bind(wx.EVT_SPINCTRL, self.spin_on_device_address, self.spin_device_address)
        self.Bind(wx.EVT_TEXT, self.spin_on_device_address, self.spin_device_address)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_device_address, self.spin_device_address)
        self.Bind(wx.EVT_SPINCTRL, self.spin_on_device_bus, self.spin_device_bus)
        self.Bind(wx.EVT_TEXT, self.spin_on_device_bus, self.spin_device_bus)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_device_bus, self.spin_device_bus)
        self.Bind(wx.EVT_SPINCTRL, self.spin_on_device_version, self.spin_device_version)
        self.Bind(wx.EVT_TEXT, self.spin_on_device_version, self.spin_device_version)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_device_version, self.spin_device_version)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.spin_on_home_x, self.spin_home_x)
        self.Bind(wx.EVT_TEXT, self.spin_on_home_x, self.spin_home_x)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_home_x, self.spin_home_x)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.spin_on_home_y, self.spin_home_y)
        self.Bind(wx.EVT_TEXT, self.spin_on_home_y, self.spin_home_y)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_home_y, self.spin_home_y)
        self.Bind(wx.EVT_BUTTON, self.on_button_set_home_current, self.button_home_by_current)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.spin_on_bedwidth, self.spin_bedwidth)
        self.Bind(wx.EVT_TEXT, self.spin_on_bedwidth, self.spin_bedwidth)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_bedwidth, self.spin_bedwidth)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.spin_on_bedheight, self.spin_bedheight)
        self.Bind(wx.EVT_TEXT, self.spin_on_bedheight, self.spin_bedheight)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_bedheight, self.spin_bedheight)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_autolock, self.checkbox_autolock)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_autohome, self.checkbox_autohome)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_autobeep, self.checkbox_autobeep)
        # end wxGlade
        self.Bind(wx.EVT_CLOSE, self.on_close, self)

    def on_close(self, event):
        if self.state == 5:
            event.Veto()
        else:
            self.state = 5
            self.device.close('window', self.name)
            event.Skip()  # Call destroy as regular.

    def initialize(self, channel=None):
        self.device.close('window', self.name)
        self.Show()

        self.device.setting(bool, "swap_xy", False)
        self.device.setting(bool, "flip_x", False)
        self.device.setting(bool, "flip_y", False)
        self.device.setting(bool, "home_right", False)
        self.device.setting(bool, "home_bottom", False)
        self.device.setting(int, "home_adjust_x", 0)
        self.device.setting(int, "home_adjust_y", 0)

        self.device.setting(bool, "mock", False)
        self.device.setting(bool, "autobeep", False)
        self.device.setting(bool, "autohome", False)
        self.device.setting(bool, "autolock", True)
        self.device.setting(str, "board", 'M2')
        self.device.setting(int, "bed_width", 280)
        self.device.setting(int, "bed_height", 200)
        self.device.setting(int, "units_index", 0)
        self.device.setting(int, "usb_index", -1)
        self.device.setting(int, "usb_bus", -1)
        self.device.setting(int, "usb_address", -1)
        self.device.setting(int, "usb_version", -1)

        self.checkbox_swap_xy.SetValue(self.device.swap_xy)
        self.checkbox_flip_x.SetValue(self.device.flip_x)
        self.checkbox_flip_y.SetValue(self.device.flip_y)
        self.checkbox_home_right.SetValue(self.device.home_right)
        self.checkbox_home_bottom.SetValue(self.device.home_bottom)
        self.checkbox_mock_usb.SetValue(self.device.mock)
        self.checkbox_autobeep.SetValue(self.device.autobeep)
        self.checkbox_autohome.SetValue(self.device.autohome)
        self.checkbox_autolock.SetValue(self.device.autolock)
        self.combobox_board.SetValue(self.device.board)
        self.spin_bedwidth.SetValue(self.device.bed_width)
        self.spin_bedheight.SetValue(self.device.bed_height)
        self.spin_device_index.SetValue(self.device.usb_index)
        self.spin_device_bus.SetValue(self.device.usb_bus)
        self.spin_device_address.SetValue(self.device.usb_address)
        self.spin_device_version.SetValue(self.device.usb_version)
        self.spin_home_x.SetValue(self.device.home_adjust_x)
        self.spin_home_y.SetValue(self.device.home_adjust_y)

    def finalize(self, channel=None):
        self.SetFocus()
        try:
            self.Close()
        except RuntimeError:
            pass

    def shutdown(self,  channel=None):
        try:
            self.Close()
        except RuntimeError:
            pass

    def __set_properties(self):
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_administrative_tools_50.GetBitmap())
        self.SetIcon(_icon)
        # begin wxGlade: Preferences.__set_properties
        self.SetTitle(_("Preferences"))
        self.combobox_board.SetToolTip(_("Select the board to use. This has affects the speedcodes used."))
        self.combobox_board.SetSelection(0)
        self.checkbox_swap_xy.SetToolTip(_("Swaps the X and Y axis. This happens before the FlipX and FlipY."))
        self.checkbox_flip_x.SetToolTip(_("Flip the Right and Left commands sent to the controller"))
        self.checkbox_home_right.SetToolTip(_("Indicates the device Home is on the right"))
        self.checkbox_flip_y.SetToolTip(_("Flip the Top and Bottom commands sent to the controller"))
        self.checkbox_home_bottom.SetToolTip(_("Indicates the device Home is on the bottom"))
        self.checkbox_mock_usb.SetToolTip(
            _("DEBUG. Without a K40 connected continue to process things as if there was one."))
        self.spin_device_index.SetToolTip(_("-1 match anything. 0-5 match exactly that value."))
        self.spin_device_address.SetToolTip(_("-1 match anything. 0-5 match exactly that value."))
        self.spin_device_bus.SetToolTip(_("-1 match anything. 0-5 match exactly that value."))
        self.spin_device_version.SetToolTip(_("-1 match anything. 0-255 match exactly that value."))
        self.spin_home_x.SetMinSize((80, 23))
        self.spin_home_x.SetToolTip(_("Translate Home X"))
        self.spin_home_y.SetMinSize((80, 23))
        self.spin_home_y.SetToolTip(_("Translate Home Y"))
        self.button_home_by_current.SetToolTip(_("Set Home Position based on the current position"))
        self.spin_bedwidth.SetMinSize((80, 23))
        self.spin_bedwidth.SetToolTip(_("Width of the laser bed."))
        self.spin_bedheight.SetMinSize((80, 23))
        self.spin_bedheight.SetToolTip(_("Height of the laser bed."))
        self.checkbox_autolock.SetToolTip(_("Lock rail after operations are finished."))
        self.checkbox_autolock.SetValue(1)
        self.checkbox_autohome.SetToolTip(_("Home the machine after job is finished"))
        self.checkbox_autobeep.SetToolTip(_("Beep after the job is finished."))
        self.checkbox_autobeep.SetValue(1)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Preferences.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_general = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("General Options")), wx.VERTICAL)
        sizer_bed = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Bed Dimensions")), wx.HORIZONTAL)
        sizer_home = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Shift Home Position")), wx.HORIZONTAL)
        sizer_usb = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("USB Settings")), wx.VERTICAL)
        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_board = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Board Setup")), wx.HORIZONTAL)
        sizer_16 = wx.BoxSizer(wx.VERTICAL)
        sizer_17 = wx.BoxSizer(wx.VERTICAL)
        sizer_board.Add(self.combobox_board, 0, 0, 0)
        sizer_board.Add((20, 20), 0, 0, 0)
        sizer_17.Add(self.checkbox_flip_x, 0, 0, 0)
        sizer_17.Add(self.checkbox_home_right, 0, 0, 0)
        sizer_board.Add(sizer_17, 1, wx.EXPAND, 0)
        sizer_16.Add(self.checkbox_flip_y, 0, 0, 0)
        sizer_16.Add(self.checkbox_home_bottom, 0, 0, 0)
        sizer_board.Add(sizer_16, 1, wx.EXPAND, 0)
        sizer_board.Add(self.checkbox_swap_xy, 0, 0, 0)
        sizer_1.Add(sizer_board, 1, wx.EXPAND, 0)
        sizer_usb.Add(self.checkbox_mock_usb, 0, 0, 0)
        label_6 = wx.StaticText(self, wx.ID_ANY, _("Device Index:"))
        sizer_3.Add(label_6, 1, 0, 0)
        sizer_3.Add(self.spin_device_index, 1, 0, 0)
        sizer_usb.Add(sizer_3, 1, wx.EXPAND, 0)
        label_7 = wx.StaticText(self, wx.ID_ANY, _("Device Address:"))
        sizer_10.Add(label_7, 1, 0, 0)
        sizer_10.Add(self.spin_device_address, 1, 0, 0)
        sizer_usb.Add(sizer_10, 1, wx.EXPAND, 0)
        label_8 = wx.StaticText(self, wx.ID_ANY, _("Device Bus:"))
        sizer_11.Add(label_8, 1, 0, 0)
        sizer_11.Add(self.spin_device_bus, 1, 0, 0)
        sizer_usb.Add(sizer_11, 1, wx.EXPAND, 0)
        label_13 = wx.StaticText(self, wx.ID_ANY, _("Chip Version:"))
        sizer_12.Add(label_13, 1, 0, 0)
        sizer_12.Add(self.spin_device_version, 1, 0, 0)
        sizer_usb.Add(sizer_12, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_usb, 1, wx.EXPAND, 0)
        label_9 = wx.StaticText(self, wx.ID_ANY, _("X"))
        sizer_home.Add(label_9, 0, 0, 0)
        sizer_home.Add(self.spin_home_x, 0, 0, 0)
        label_12 = wx.StaticText(self, wx.ID_ANY, _("mil"))
        sizer_home.Add(label_12, 0, 0, 0)
        sizer_home.Add((20, 20), 0, 0, 0)
        label_10 = wx.StaticText(self, wx.ID_ANY, _("Y"))
        sizer_home.Add(label_10, 0, 0, 0)
        sizer_home.Add(self.spin_home_y, 0, 0, 0)
        label_11 = wx.StaticText(self, wx.ID_ANY, _("mil"))
        sizer_home.Add(label_11, 0, 0, 0)
        sizer_home.Add((20, 20), 0, 0, 0)
        sizer_home.Add(self.button_home_by_current, 0, 0, 0)
        sizer_1.Add(sizer_home, 1, wx.EXPAND, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, _("Width"))
        sizer_bed.Add(label_2, 0, 0, 0)
        sizer_bed.Add(self.spin_bedwidth, 0, 0, 0)
        label_17 = wx.StaticText(self, wx.ID_ANY, _("mm"))
        sizer_bed.Add(label_17, 0, 0, 0)
        sizer_bed.Add((20, 20), 0, 0, 0)
        label_3 = wx.StaticText(self, wx.ID_ANY, _("Height"))
        sizer_bed.Add(label_3, 0, 0, 0)
        sizer_bed.Add(self.spin_bedheight, 0, 0, 0)
        label_18 = wx.StaticText(self, wx.ID_ANY, _("mm"))
        sizer_bed.Add(label_18, 0, 0, 0)
        sizer_1.Add(sizer_bed, 1, wx.EXPAND, 0)
        sizer_general.Add(self.checkbox_autolock, 0, 0, 0)
        sizer_general.Add(self.checkbox_autohome, 0, 0, 0)
        sizer_general.Add(self.checkbox_autobeep, 0, 0, 0)
        sizer_1.Add(sizer_general, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def calc_home_position(self):
        x = 0
        y = 0
        if self.device.home_right:
            x = int(self.device.bed_width * 39.3701)
        if self.device.home_bottom:
            y = int(self.device.bed_height * 39.3701)
        return x, y

    def on_combobox_boardtype(self, event):  # wxGlade: Preferences.<event_handler>
        self.device.board = self.combobox_board.GetValue()

    def on_check_swap_xy(self, event):  # wxGlade: Preferences.<event_handler>
        self.device.swap_xy = self.checkbox_swap_xy.GetValue()
        self.device.execute("Update Codes")

    def on_check_flip_x(self, event):  # wxGlade: Preferences.<event_handler>
        self.device.flip_x = self.checkbox_flip_x.GetValue()
        self.device.execute("Update Codes")

    def on_check_home_right(self, event):  # wxGlade: Preferences.<event_handler>
        self.device.home_right = self.checkbox_home_right.GetValue()

    def on_check_flip_y(self, event):  # wxGlade: Preferences.<event_handler>
        self.device.flip_y = self.checkbox_flip_y.GetValue()
        self.device.execute("Update Codes")

    def on_check_home_bottom(self, event):  # wxGlade: Preferences.<event_handler>
        self.device.home_bottom = self.checkbox_home_bottom.GetValue()

    def spin_on_home_x(self, event):  # wxGlade: Preferences.<event_handler>
        if self.device is None:
            return
        self.device.home_adjust_x = int(self.spin_home_x.GetValue())

    def spin_on_home_y(self, event):  # wxGlade: Preferences.<event_handler>
        if self.device is None:
            return
        self.device.home_adjust_y = int(self.spin_home_y.GetValue())

    def on_button_set_home_current(self, event):  # wxGlade: Preferences.<event_handler>
        x, y = self.calc_home_position()
        current_x = self.device.current_x - x
        current_y = self.device.current_y - y
        self.device.home_adjust_x = int(current_x)
        self.device.home_adjust_y = int(current_y)
        self.spin_home_x.SetValue(self.device.home_adjust_x)
        self.spin_home_y.SetValue(self.device.home_adjust_y)

    def spin_on_bedwidth(self, event):  # wxGlade: Preferences.<event_handler>
        if self.device is None:
            return
        self.device.bed_width = int(self.spin_bedwidth.GetValue())
        self.device.bed_height = int(self.spin_bedheight.GetValue())
        self.device.signal('bed_size', (self.device.bed_width, self.device.bed_height))

    def spin_on_bedheight(self, event):  # wxGlade: Preferences.<event_handler>
        if self.device is None:
            return
        self.device.bed_width = int(self.spin_bedwidth.GetValue())
        self.device.bed_height = int(self.spin_bedheight.GetValue())
        self.device.signal('bed_size', (self.device.bed_width, self.device.bed_height))

    def on_check_autolock(self, event):  # wxGlade: Preferences.<event_handler>
        self.device.autolock = self.checkbox_autolock.GetValue()

    def on_check_autohome(self, event):  # wxGlade: Preferences.<event_handler>
        self.device.autohome = self.checkbox_autohome.GetValue()

    def on_check_autobeep(self, event):  # wxGlade: Preferences.<event_handler>
        self.device.autobeep = self.checkbox_autobeep.GetValue()

    def spin_on_device_index(self, event):  # wxGlade: Preferences.<event_handler>
        if self.device is None:
            return
        self.device.usb_index = int(self.spin_device_index.GetValue())

    def spin_on_device_address(self, event):  # wxGlade: Preferences.<event_handler>
        if self.device is None:
            return
        self.device.usb_address = int(self.spin_device_address.GetValue())

    def spin_on_device_bus(self, event):  # wxGlade: Preferences.<event_handler>
        if self.device is None:
            return
        self.device.usb_bus = int(self.spin_device_bus.GetValue())

    def spin_on_device_version(self, event):  # wxGlade: Preferences.<event_handler>
        if self.device is None:
            return
        self.device.usb_version = int(self.spin_device_version.GetValue())

    def on_checkbox_mock_usb(self, event):  # wxGlade: Preferences.<event_handler>
        self.device.mock = self.checkbox_mock_usb.GetValue()