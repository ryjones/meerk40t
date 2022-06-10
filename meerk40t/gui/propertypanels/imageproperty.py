import wx

from ..icons import icons8_image_50
from ..mwindow import MWindow

_ = wx.GetTranslation


class ImagePropertyPanel(wx.Panel):
    def __init__(self, *args, context=None, node=None, **kwargs):
        # begin wxGlade: ConsolePanel.__init__
        kwargs["style"] = kwargs.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwargs)
        self.context = context
        self.node = node
        self.text_dpi = wx.TextCtrl(self, wx.ID_ANY, "500")
        self.text_x = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_y = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_width = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_height = wx.TextCtrl(self, wx.ID_ANY, "")

        self.check_enable_dither = wx.CheckBox(self, wx.ID_ANY, _("Dither"))
        self.choices = [
            "Floyd-Steinberg",
            "Atkinson",
            "Jarvis-Judice-Ninke",
            "Stucki",
            "Burkes",
            "Sierra3",
            "Sierra2",
            "Sierra-2-4a",
        ]
        self.combo_dither = wx.ComboBox(
            self,
            wx.ID_ANY,
            choices=self.choices,
            style=wx.CB_DROPDOWN,
        )

        self.check_invert_grayscale = wx.CheckBox(self, wx.ID_ANY, _("Invert"))
        self.slider_grayscale_red = wx.Slider(
            self, wx.ID_ANY, 0, -1000, 1000, style=wx.SL_AUTOTICKS | wx.SL_HORIZONTAL
        )
        self.text_grayscale_red = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.slider_grayscale_green = wx.Slider(
            self, wx.ID_ANY, 0, -1000, 1000, style=wx.SL_AUTOTICKS | wx.SL_HORIZONTAL
        )
        self.text_grayscale_green = wx.TextCtrl(
            self, wx.ID_ANY, "", style=wx.TE_READONLY
        )
        self.slider_grayscale_blue = wx.Slider(
            self, wx.ID_ANY, 0, -1000, 1000, style=wx.SL_AUTOTICKS | wx.SL_HORIZONTAL
        )
        self.text_grayscale_blue = wx.TextCtrl(
            self, wx.ID_ANY, "", style=wx.TE_READONLY
        )
        self.slider_grayscale_lightness = wx.Slider(
            self, wx.ID_ANY, 500, 0, 1000, style=wx.SL_AUTOTICKS | wx.SL_HORIZONTAL
        )
        self.text_grayscale_lightness = wx.TextCtrl(
            self, wx.ID_ANY, "", style=wx.TE_READONLY
        )

        self.__set_properties()
        self.__do_layout()

        self.Bind(
            wx.EVT_CHECKBOX, self.on_check_enable_dither, self.check_enable_dither
        )
        self.Bind(wx.EVT_COMBOBOX, self.on_combo_dither_type, self.combo_dither)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_combo_dither_type, self.combo_dither)

        self.Bind(wx.EVT_TEXT, self.on_text_dpi, self.text_dpi)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_dpi, self.text_dpi)
        self.Bind(wx.EVT_TEXT, self.on_text_x, self.text_x)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_x, self.text_x)
        self.Bind(wx.EVT_TEXT, self.on_text_y, self.text_y)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_y, self.text_y)
        self.Bind(wx.EVT_TEXT, self.on_text_width, self.text_width)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_width, self.text_width)
        self.Bind(wx.EVT_TEXT, self.on_text_height, self.text_height)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_height, self.text_height)
        self.Bind(
            wx.EVT_CHECKBOX, self.on_check_invert_grayscale, self.check_invert_grayscale
        )
        self.Bind(
            wx.EVT_SLIDER,
            self.on_slider_grayscale_component,
            self.slider_grayscale_lightness,
        )
        self.Bind(
            wx.EVT_SLIDER, self.on_slider_grayscale_component, self.slider_grayscale_red
        )
        self.Bind(
            wx.EVT_SLIDER,
            self.on_slider_grayscale_component,
            self.slider_grayscale_green,
        )
        self.Bind(
            wx.EVT_SLIDER,
            self.on_slider_grayscale_component,
            self.slider_grayscale_blue,
        )
        # self.check_enable_grayscale.SetValue(op["enable"])
        self.check_invert_grayscale.SetValue(node.invert)

        self.slider_grayscale_red.SetValue(int(node.red * 500.0))
        self.text_grayscale_red.SetValue(str(node.red))

        self.slider_grayscale_green.SetValue(int(node.green * 500.0))
        self.text_grayscale_green.SetValue(str(node.green))

        self.slider_grayscale_blue.SetValue(int(node.blue * 500.0))
        self.text_grayscale_blue.SetValue(str(node.blue))

        self.slider_grayscale_lightness.SetValue(int(node.lightness * 500.0))
        self.text_grayscale_lightness.SetValue(str(node.lightness))
        self.set_widgets()

    @staticmethod
    def accepts(node):
        if node.type == "elem image":
            return True
        return False

    def set_widgets(self, node=None):
        if node is None:
            node = self.node
        if node is None:
            return
        self.text_dpi.SetValue(str(node.dpi))
        try:
            bounds = node.bounds
            self.text_x.SetValue(str(bounds[0]))
            self.text_y.SetValue(str(bounds[1]))
            self.text_width.SetValue(str((bounds[2] - bounds[0])))
            self.text_height.SetValue(str((bounds[3] - bounds[1])))
        except AttributeError:
            pass
        self.check_enable_dither.SetValue(node.dither)
        self.combo_dither.SetValue(node.dither_type)

    def __set_properties(self):
        self.text_x.SetToolTip(_("X property of image"))
        self.text_x.Enable(False)
        self.text_y.SetToolTip(_("Y property of image"))
        self.text_y.Enable(False)
        self.text_width.SetToolTip(_("Width property of image"))
        self.text_width.Enable(False)
        self.text_height.SetToolTip(_("Height property of image"))
        self.text_height.Enable(False)
        self.check_enable_dither.SetToolTip(_("Enable Dither"))
        self.check_enable_dither.SetValue(1)
        self.combo_dither.SetToolTip(_("Select dither algorithm to use"))
        self.combo_dither.SetSelection(0)
        self.check_invert_grayscale.SetToolTip(_("Invert Grayscale"))
        self.slider_grayscale_red.SetToolTip(_("Red component amount"))
        self.text_grayscale_red.SetToolTip(_("Red Factor"))
        self.slider_grayscale_green.SetToolTip(_("Green component control"))
        self.text_grayscale_green.SetToolTip(_("Green Factor"))
        self.slider_grayscale_blue.SetToolTip(_("Blue component control"))
        self.text_grayscale_blue.SetToolTip(_("Blue Factor"))
        self.slider_grayscale_lightness.SetToolTip(_("Lightness control"))
        self.text_grayscale_lightness.SetToolTip(_("Lightness"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ImageProperty.__do_layout
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        label_8 = wx.StaticText(self, wx.ID_ANY, _("DPI:"))
        label_8.SetToolTip(_("Dots Per Inch"))
        sizer_6.Add(label_8, 1, 0, 0)
        sizer_6.Add(self.text_dpi, 5, 0, 0)
        sizer_main.Add(sizer_6, 1, wx.EXPAND, 0)
        label_1 = wx.StaticText(self, wx.ID_ANY, _("X:"))
        sizer_2.Add(label_1, 1, 0, 0)
        sizer_2.Add(self.text_x, 5, 0, 0)
        sizer_main.Add(sizer_2, 1, wx.EXPAND, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, _("Y:"))
        sizer_3.Add(label_2, 1, 0, 0)
        sizer_3.Add(self.text_y, 5, 0, 0)
        sizer_main.Add(sizer_3, 1, wx.EXPAND, 0)
        label_3 = wx.StaticText(self, wx.ID_ANY, _("Width:"))
        sizer_4.Add(label_3, 1, 0, 0)
        sizer_4.Add(self.text_width, 5, 0, 0)
        sizer_main.Add(sizer_4, 1, wx.EXPAND, 0)
        label_5 = wx.StaticText(self, wx.ID_ANY, _("Height:"))
        sizer_5.Add(label_5, 1, 0, 0)
        sizer_5.Add(self.text_height, 5, 0, 0)
        sizer_main.Add(sizer_5, 1, wx.EXPAND, 0)

        sizer_dither = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Grayscale")), wx.VERTICAL
        )
        sizer_dither.Add(self.check_enable_dither, 0, 0, 0)
        sizer_dither.Add(self.combo_dither, 0, 0, 0)

        sizer_main.Add(sizer_dither, 1, wx.EXPAND, 0)

        #-----

        sizer_grayscale = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Grayscale")), wx.VERTICAL
        )
        sizer_grayscale_lightness = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Lightness")), wx.HORIZONTAL
        )
        sizer_grayscale_blue = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Blue")), wx.HORIZONTAL
        )
        sizer_grayscale_green = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Green")), wx.HORIZONTAL
        )
        sizer_grayscale_red = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Red")), wx.HORIZONTAL
        )
        sizer_grayscale.Add(self.check_enable_grayscale, 0, 0, 0)
        sizer_grayscale.Add(self.check_invert_grayscale, 0, 0, 0)
        sizer_grayscale_red.Add(self.slider_grayscale_red, 5, wx.EXPAND, 0)
        sizer_grayscale_red.Add(self.text_grayscale_red, 1, 0, 0)
        sizer_grayscale.Add(sizer_grayscale_red, 0, wx.EXPAND, 0)
        sizer_grayscale_green.Add(self.slider_grayscale_green, 5, wx.EXPAND, 0)
        sizer_grayscale_green.Add(self.text_grayscale_green, 1, 0, 0)
        sizer_grayscale.Add(sizer_grayscale_green, 0, wx.EXPAND, 0)
        sizer_grayscale_blue.Add(self.slider_grayscale_blue, 5, wx.EXPAND, 0)
        sizer_grayscale_blue.Add(self.text_grayscale_blue, 1, 0, 0)
        sizer_grayscale.Add(sizer_grayscale_blue, 0, wx.EXPAND, 0)
        sizer_grayscale_lightness.Add(self.slider_grayscale_lightness, 5, wx.EXPAND, 0)
        sizer_grayscale_lightness.Add(self.text_grayscale_lightness, 1, 0, 0)
        sizer_grayscale.Add(sizer_grayscale_lightness, 0, wx.EXPAND, 0)

        sizer_main.Add(sizer_grayscale, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        self.Layout()
        self.Centre()
        # end wxGlade

    def on_text_dpi(self, event=None):  # wxGlade: ImageProperty.<event_handler>
        new_step = float(self.text_dpi.GetValue())
        self.node.dpi = new_step

    def on_text_x(self, event):  # wxGlade: ImageProperty.<event_handler>
        event.Skip()

    def on_text_y(self, event):  # wxGlade: ImageProperty.<event_handler>
        event.Skip()

    def on_text_width(self, event):  # wxGlade: ImageProperty.<event_handler>
        event.Skip()

    def on_text_height(self, event):  # wxGlade: ImageProperty.<event_handler>
        event.Skip()

    def on_check_enable_dither(
        self, event=None
    ):  # wxGlade: RasterWizard.<event_handler>
        self.node.dither = self.check_enable_dither.GetValue()
        self.node.update(self.context)

    def on_combo_dither_type(self, event=None):  # wxGlade: RasterWizard.<event_handler>
        self.node.dither_type = self.choices[self.combo_dither.GetSelection()]
        self.node.update(self.context)

    def on_check_invert_grayscale(
        self, event=None
    ):  # wxGlade: RasterWizard.<event_handler>
        self.node.invert = self.check_invert_grayscale.GetValue()
        self.node.update(self.context)

    def on_slider_grayscale_component(
        self, event=None
    ):  # wxGlade: GrayscalePanel.<event_handler>
        self.node.red = float(int(self.slider_grayscale_red.GetValue()) / 500.0)
        self.text_grayscale_red.SetValue(str(self.node.red))

        self.node.green = float(int(self.slider_grayscale_green.GetValue()) / 500.0)
        self.text_grayscale_green.SetValue(str(self.node.green))

        self.node.blue = float(int(self.slider_grayscale_blue.GetValue()) / 500.0)
        self.text_grayscale_blue.SetValue(str(self.node.blue))

        self.node.lightness = float(
            int(self.slider_grayscale_lightness.GetValue()) / 500.0
        )
        self.text_grayscale_lightness.SetValue(str(self.node.lightness))
        self.node.update(self.context)


class ImageProperty(MWindow):
    def __init__(self, *args, node=None, **kwds):
        super().__init__(276, 218, *args, **kwds)

        self.panel = ImagePropertyPanel(
            self, wx.ID_ANY, context=self.context, node=node
        )
        self.add_module_delegate(self.panel)
        # begin wxGlade: ImageProperty.__set_properties
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_image_50.GetBitmap())
        self.SetIcon(_icon)
        self.SetTitle(_("Image Properties"))

    def restore(self, *args, node=None, **kwds):
        self.panel.set_widgets(node)

    def window_preserve(self):
        return False

    def window_menu(self):
        return False
