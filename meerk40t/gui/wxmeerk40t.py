# -*- coding: utf-8 -*-

import os
import platform
import sys
import traceback

from wx import aui

from meerk40t.gui.wxmscene import SceneWindow
from .devicepanel import DeviceManager
from .icons import (
    icons8_gas_industry_50,
    icons8_emergency_stop_button_50,
    icons8_home_filled_50,
    icons8_pause_50,
)
from .operationpropertymain import ParameterPanel

try:
    import wx
except ImportError as e:
    from ..core.exceptions import Mk40tImportAbort

    raise Mk40tImportAbort("wxpython")

from ..kernel import Module, ConsoleFunction
from ..main import APPLICATION_NAME, APPLICATION_VERSION
from .about import About
from .bufferview import BufferView
from .executejob import ExecuteJob
from .groupproperties import GroupProperty
from .imageproperty import ImageProperty
from .keymap import Keymap
from .laserrender import LaserRender
from .notes import Notes
from .operationproperty import OperationProperty

from meerk40t.gui.consolepanel import Console
from meerk40t.gui.navigationpanels import Navigation
from meerk40t.gui.spoolerpanel import JobSpooler
from .pathproperty import PathProperty
from .preferences import Preferences
from .rasterwizard import RasterWizard
from .simulation import Simulation
from .textproperty import TextProperty
from .wxmmain import MeerK40t

"""
Laser software for the Stock-LIHUIYU laserboard.

MeerK40t (pronounced MeerKat) is a built-from-the-ground-up MIT licensed
open-source laser cutting software. See https://github.com/meerk40t/meerk40t
for full details.

wxMeerK40t is the primary gui addon for MeerK40t. It requires wxPython for the interface.
The Transformations work in Windows/OSX/Linux for wxPython 4.0+ (and likely before)

"""

GUI_START = True

_ = wx.GetTranslation


def plugin(kernel, lifecycle):
    global GUI_START
    kernel_root = kernel.root
    if lifecycle == "init" and kernel.args.no_gui:
        GUI_START = False

        @kernel.console_command("gui", help=_("starts the gui"))
        def gui_start(**kwargs):
            kernel.console_command_remove("gui")
            meerk40tgui = kernel_root.open("module/wxMeerK40t")
            kernel.console("window open MeerK40t\n")
            meerk40tgui.MainLoop()

    elif lifecycle == "preregister":
        kernel.register("module/wxMeerK40t", wxMeerK40t)
        kernel_root.open("module/wxMeerK40t")

        # Registers the render-op make_raster. This is used to do cut planning.
        renderer = LaserRender(kernel_root)
        kernel_root.register("render-op/make_raster", renderer.make_raster)
    elif lifecycle == "postboot":
        choices = [
            {
                "attr": "show_negative_guide",
                "object": kernel.root,
                "default": True,
                "type": bool,
                "label": _("Show Negative Guide"),
                "tip": _(
                    "Extend the Guide rulers with negative values to assist lining up objects partially outside the left/top of the bed"
                ),
            },
            {
                "attr": "windows_save",
                "object": kernel.root,
                "default": True,
                "type": bool,
                "label": _("Save Window Positions"),
                "tip": _("Open Windows at the same place they were last closed"),
            },
            {
                "attr": "auto_spooler",
                "object": kernel.root,
                "default": True,
                "type": bool,
                "label": _("Launch Spooler on Job Start"),
                "tip": _(
                    "Open the Spooler window automatically when you Execute a Job"
                ),
            },
            {
                "attr": "mouse_wheel_pan",
                "object": kernel.root,
                "default": False,
                "type": bool,
                "label": _("MouseWheel Pan"),
                "tip": "\n".join(
                    (
                        _("Unset: MouseWheel=Zoom. Shift+MouseWheel=Horizontal pan."),
                        _(
                            "Set: MouseWheel=Vertical pan. Ctrl+MouseWheel=Zoom. Shift+MouseWheel=Horizontal pan."
                        ),
                    )
                ),
            },
            {
                "attr": "mouse_pan_invert",
                "object": kernel.root,
                "default": False,
                "type": bool,
                "label": _("Invert MouseWheel Pan"),
                "tip": _(
                    "Reverses the direction of the MouseWheel for horizontal & vertical pan"
                ),
            },
            {
                "attr": "mouse_zoom_invert",
                "object": kernel.root,
                "default": False,
                "type": bool,
                "label": _("Invert MouseWheel Zoom"),
                "tip": _("Reverses the direction of the MouseWheel for zoom"),
            },
            {
                "attr": "disable_tool_tips",
                "object": kernel.root,
                "default": False,
                "type": bool,
                "label": _("Disable ToolTips"),
                "tip": "\n".join(
                    (
                        _(
                            "If you do not want to see tooltips like this one, check this box."
                        ),
                        _("Particularly useful if you have a touch screen."),
                        _(
                            "Note: You will need to restart MeerK40t for any change to take effect."
                        ),
                    )
                ),
            },
        ]
        kernel.register_choices("preferences", choices)

    elif lifecycle == "mainloop":
        # Replace the default kernel data prompt for a wx Popup.

        def prompt_popup(data_type, prompt):
            with wx.TextEntryDialog(None, prompt, _("Information Required:"), "") as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    value = dlg.GetValue()
                else:
                    return
            try:
                return data_type(value)
            except ValueError:
                return None
        kernel.prompt = prompt_popup

        def interrupt_popup():
            dlg = wx.MessageDialog(
                None,
                _("Spooling Interrupted. Press OK to Continue."),
                _("Interrupt"),
                wx.OK,
            )
            dlg.ShowModal()
            dlg.Destroy()

        kernel_root.planner.register("function/interrupt", interrupt_popup)

        def interrupt():
            yield "wait_finish"
            yield "function", kernel_root.lookup("function/interrupt")

        kernel_root.planner.register("plan/interrupt", interrupt)

        if GUI_START:
            meerk40tgui = kernel_root.open("module/wxMeerK40t")
            kernel.console("window open MeerK40t\n")
            for window in kernel.derivable("window"):
                wsplit = window.split(":")
                window_name = wsplit[0]
                window_index = wsplit[-1] if len(wsplit) > 1 else None
                if kernel.read_persistent(
                    bool, "window/%s/open_on_start" % window, False
                ):
                    if window_index is not None:
                        kernel.console("window open -m {index} {window} {index}\n".format(index=window_index, window=window_name))
                    else:
                        kernel.console("window open {window}\n".format(window=window_name))
            meerk40tgui.MainLoop()


def register_panel_go(window, context):
    # Define Go
    go = wx.BitmapButton(window, wx.ID_ANY, icons8_gas_industry_50.GetBitmap())

    def busy_go_plan(*args):
        with wx.BusyInfo(_("Processing and sending...")):
            context(
                "plan clear copy preprocess validate blob preopt optimize spool\nplan clear\n"
            )

    window.Bind(
        wx.EVT_BUTTON,
        busy_go_plan,
        go,
    )
    go.SetBackgroundColour(wx.Colour(0, 127, 0))
    go.SetToolTip(_("One Touch: Send Job To Laser "))
    go.SetSize(go.GetBestSize())
    pane = (
        aui.AuiPaneInfo()
        .Bottom()
        .Caption(_("Go"))
        .MinSize(40, 40)
        .FloatingSize(98, 98)
        .Name("go")
        .CaptionVisible(not context.pane_lock)
        .Hide()
    )
    pane.dock_proportion = 98
    pane.control = go

    window.on_pane_add(pane)
    context.register("pane/go", pane)


def register_panel_stop(window, context):
    # Define Stop.
    stop = wx.BitmapButton(
        window, wx.ID_ANY, icons8_emergency_stop_button_50.GetBitmap()
    )
    window.Bind(
        wx.EVT_BUTTON,
        ConsoleFunction(context, "estop\n"),
        stop,
    )
    stop.SetBackgroundColour(wx.Colour(127, 0, 0))
    stop.SetToolTip(_("Emergency stop/reset the controller."))
    stop.SetSize(stop.GetBestSize())
    pane = (
        aui.AuiPaneInfo()
        .Bottom()
        .Caption(_("Stop"))
        .MinSize(40, 40)
        .FloatingSize(98, 98)
        .Name("stop")
        .Hide()
        .CaptionVisible(not context.pane_lock)
    )
    pane.dock_proportion = 98
    pane.control = stop

    window.on_pane_add(pane)
    context.register("pane/stop", pane)


def register_panel_home(window, context):
    # Define Home.
    home = wx.BitmapButton(window, wx.ID_ANY, icons8_home_filled_50.GetBitmap())
    # home.SetBackgroundColour((200, 225, 250))
    window.Bind(wx.EVT_BUTTON, lambda e: context("home\n"), home)
    pane = (
        aui.AuiPaneInfo()
        .Bottom()
        .Caption(_("Home"))
        .MinSize(40, 40)
        .FloatingSize(98, 98)
        .Name("home")
        .Hide()
        .CaptionVisible(not context.pane_lock)
    )
    pane.dock_proportion = 98
    pane.control = home
    window.on_pane_add(pane)
    context.register("pane/home", pane)


def register_panel_pause(window, context):
    # Define Pause.
    pause = wx.BitmapButton(
        window, wx.ID_ANY, icons8_pause_50.GetBitmap(use_theme=False)
    )

    def on_pause_button(event=None):
        try:
            context("pause\n")
            # if self.pipe_state != 3:
            #     pause.SetBitmap(icons8_play_50.GetBitmap())
            # else:
            # pause.SetBitmap(icons8_pause_50.GetBitmap(use_theme=False))
        except AttributeError:
            pass

    window.Bind(
        wx.EVT_BUTTON,
        on_pause_button,
        pause,
    )
    pause.SetBackgroundColour(wx.Colour(255, 255, 0))
    pause.SetToolTip(_("Pause/Resume the controller"))
    pause.SetSize(pause.GetBestSize())
    pane = (
        aui.AuiPaneInfo()
        .Caption(_("Pause"))
        .Bottom()
        .MinSize(40, 40)
        .FloatingSize(98, 98)
        .Name("pause")
        .Hide()
        .CaptionVisible(not context.pane_lock)
    )
    pane.dock_proportion = 98
    pane.control = pause

    window.on_pane_add(pane)
    context.register("pane/pause", pane)


supported_languages = (
    ("en", u"English", wx.LANGUAGE_ENGLISH),
    ("it", u"italiano", wx.LANGUAGE_ITALIAN),
    ("fr", u"français", wx.LANGUAGE_FRENCH),
    ("de", u"Deutsch", wx.LANGUAGE_GERMAN),
    ("es", u"español", wx.LANGUAGE_SPANISH),
    ("zh", u"中文", wx.LANGUAGE_CHINESE),
    ("hu", u"Magyar", wx.LANGUAGE_HUNGARIAN),
    ("pt", u"português", wx.LANGUAGE_PORTUGUESE),
    ("pt-br", u"português brasileiro", wx.LANGUAGE_PORTUGUESE_BRAZILIAN),
)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class wxMeerK40t(wx.App, Module):
    """
    wxMeerK40t is the wx.App main class and a qualified Module for the MeerK40t kernel.
    Running MeerK40t without the wxMeerK40t gui is both possible and reasonable. This should not change the way the
    underlying code runs. It should just be a series of frames held together with the kernel.
    """

    def __init__(self, context, path):
        wx.App.__init__(self, 0)
        self.supported_languages = supported_languages
        import meerk40t.gui.icons as icons

        def run_later(command, *args):
            if wx.IsMainThread():
                command(*args)
            else:
                wx.CallAfter(command, *args)

        context._kernel.run_later = run_later

        icons.DARKMODE = wx.SystemSettings().GetColour(wx.SYS_COLOUR_WINDOW)[0] < 127
        icons.icon_r = 230
        icons.icon_g = 230
        icons.icon_b = 230
        Module.__init__(self, context, path)
        self.locale = None
        self.Bind(wx.EVT_CLOSE, self.on_app_close)
        self.Bind(wx.EVT_QUERY_END_SESSION, self.on_app_close)  # MAC DOCK QUIT.
        self.Bind(wx.EVT_END_SESSION, self.on_app_close)
        self.Bind(wx.EVT_END_PROCESS, self.on_app_close)
        # This catches events when the app is asked to activate by some other process
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)

        # App started add the except hook
        sys.excepthook = handleGUIException

    def on_app_close(self, event=None):
        try:
            if self.context is not None:
                self.context("quit\n")
        except AttributeError:
            pass

    def OnInit(self):
        return True

    def BringWindowToFront(self):
        try:  # it's possible for this event to come when the frame is closed
            self.GetTopWindow().Raise()
        except Exception:
            pass

    def OnActivate(self, event):
        # if this is an activate event, rather than something else, like iconize.
        if event.GetActive():
            self.BringWindowToFront()
        event.Skip()

    def MacReopenApp(self):
        """Called when the doc icon is clicked, and ???"""
        self.BringWindowToFront()

    def MacNewFile(self):
        try:
            if self.context is not None:
                self.context.elements.clear_all()
        except AttributeError:
            pass

    def MacPrintFile(self, file_path):
        pass

    def MacOpenFile(self, filename):
        try:
            if self.context is not None:
                self.context.elements.load(os.path.realpath(filename))
        except AttributeError:
            pass

    def MacOpenFiles(self, filenames):
        try:
            if self.context is not None:
                for filename in filenames:
                    self.context.elements.load(os.path.realpath(filename))
        except AttributeError:
            pass

    @staticmethod
    def sub_register(kernel):
        kernel.register("window/MeerK40t", MeerK40t)
        kernel.register("window/PathProperty", PathProperty)
        kernel.register("window/TextProperty", TextProperty)
        kernel.register("window/ImageProperty", ImageProperty)
        kernel.register("window/OperationProperty", OperationProperty)
        kernel.register("operationproperty/Main", ParameterPanel)
        kernel.register("window/GroupProperty", GroupProperty)
        kernel.register("window/Console", Console)
        kernel.register("window/Preferences", Preferences)
        kernel.register("window/About", About)
        kernel.register("window/Keymap", Keymap)
        kernel.register("window/Navigation", Navigation)
        kernel.register("window/Notes", Notes)
        kernel.register("window/JobSpooler", JobSpooler)
        kernel.register("window/ExecuteJob", ExecuteJob)
        kernel.register("window/BufferView", BufferView)
        kernel.register("window/RasterWizard", RasterWizard)
        kernel.register("window/Simulation", Simulation)
        kernel.register("window/Scene", SceneWindow)
        kernel.register("window/DeviceManager", DeviceManager)

        from meerk40t.gui.wxmribbon import register_panel

        kernel.register("wxpane/Ribbon", register_panel)

        from meerk40t.gui.wxmscene import register_panel

        kernel.register("wxpane/ScenePane", register_panel)

        from meerk40t.gui.wxmtree import register_panel

        kernel.register("wxpane/Tree", register_panel)

        from meerk40t.gui.laserpanel import register_panel

        kernel.register("wxpane/LaserPanel", register_panel)

        from meerk40t.gui.position import register_panel

        kernel.register("wxpane/Position", register_panel)

        if kernel.root.setting(bool, "developer_mode", False):
            from meerk40t.gui.auitoolbars import register_toolbars

            kernel.register("wxpane/Toolbars", register_toolbars)
            #
            # from meerk40t.gui.toolbarmodify import register_modify_tools
            #
            # kernel.register("wxpane/Tool-Modify", register_modify_tools)
            #
            # from meerk40t.gui.toolbaralign import register_align_tools
            #
            # kernel.register("wxpane/Tool-Align", register_align_tools)
            #
            # from meerk40t.gui.toolbarshapes import register_shapes_tools
            #
            # kernel.register("wxpane/Tool-Shape", register_shapes_tools)

        kernel.register("wxpane/Go", register_panel_go)
        kernel.register("wxpane/Stop", register_panel_stop)
        kernel.register("wxpane/Home", register_panel_home)
        kernel.register("wxpane/Pause", register_panel_pause)

        context = kernel.root

        @kernel.console_option(
            "path",
            "p",
            type=str,
            default="/",
            help=_("Context Path at which to open the window"),
        )
        @kernel.console_command(
            "window", output_type="window", help=_("Base window command")
        )
        def window_base(channel, _, path=None, remainder=None, **kwargs):
            """
            Opens a MeerK40t window or provides information. This command is restricted to use with the wxMeerK40t gui.
            This also allows use of a -p flag that sets the context path for this window to operate at. This should
            often be restricted to where the windows are typically opened since their function and settings usually
            depend on the context used. Windows often cannot open multiple copies of the same window at the same context
            The default root path is "/". Eg. "window -p / open Preferences"
            """
            context = kernel.root
            if path is None:
                path = context
            else:
                path = kernel.get_context(path)

            if remainder is None:
                channel(_("----------"))
                channel(_("Loaded Windows in Context %s:") % str(context.path))
                for i, name in enumerate(context.opened):
                    if not name.startswith("window"):
                        continue
                    module = context.opened[name]
                    channel(_("%d: %s as type of %s") % (i + 1, name, type(module)))

                channel(_("----------"))
                channel(_("Loaded Windows in Device %s:") % str(path.path))
                for i, name in enumerate(path.opened):
                    if not name.startswith("window"):
                        continue
                    module = path.opened[name]
                    channel(_("%d: %s as type of %s") % (i + 1, name, type(module)))
                channel(_("----------"))
            return "window", path

        @kernel.console_command(
            "list",
            input_type="window",
            output_type="window",
            help=_("List available windows."),
        )
        def window_list(channel, _, data, **kwargs):
            channel(_("----------"))
            channel(_("Windows Registered:"))
            for i, name in enumerate(context.match("window")):
                name = name[7:]
                channel("%d: %s" % (i + 1, name))
            return "window", data

        @kernel.console_option(
            "multi",
            "m",
            type=int,
            help=_("Multi window flag for launching multiple copies of this window."),
        )
        @kernel.console_argument("window", type=str, help=_("window to be opened"))
        @kernel.console_command(
            ("open", "toggle"),
            input_type="window",
            help=_("open/toggle the supplied window"),
        )
        def window_open(command, channel, _, data, multi=None, window=None, args=(), **kwargs):
            path = data
            try:
                parent = context.gui
            except AttributeError:
                parent = None
            window_uri = "window/%s" % window
            window_class = context.lookup(window_uri)
            if isinstance(window_class, str):
                window_uri = window_class
                window_class = context.lookup(window_uri)

            if hasattr(window_class, "required_path"):
                path = context.get_context(window_class.required_path)

            window_name = (
                "{window}:{multi}".format(window=window_uri, multi=multi)
                if multi is not None
                else window_uri
            )

            def window_open(*a, **k):
                path.open_as(window_uri, window_name, parent, *args)

            def window_close(*a, **k):
                path.close(window_name, *args)

            if command == "open":
                if context.lookup(window_uri) is not None:
                    kernel.run_later(window_open, None)
                    channel(_("Window opened: {window}").format(window=window))
                else:
                    channel(_("No such window as %s" % window))
                    raise SyntaxError
            else:
                if window_class is not None:
                    if window_name in path.opened:
                        kernel.run_later(window_close, None)
                        channel(_("Window closed: {window}").format(window=window))
                    else:
                        kernel.run_later(window_open, None)
                        channel(_("Window opened: {window}").format(window=window))
                else:
                    channel(_("No such window as %s" % window))
                    raise SyntaxError

        @kernel.console_argument("window", type=str, help=_("window to be closed"))
        @kernel.console_command(
            "close",
            input_type="window",
            output_type="window",
            help=_("close the supplied window"),
        )
        def window_close(channel, _, data, window=None, args=(), **kwargs):
            path = data
            try:
                parent = context.gui if hasattr(context, "gui") else None
                kernel.run_later(
                    lambda e: path.close("window/%s" % window, parent, *args), None
                )
                channel(_("Window closed."))
            except (KeyError, ValueError):
                channel(_("No such window as %s" % window))
            except IndexError:
                raise SyntaxError

        @kernel.console_argument("window", type=str, help=_("window to be reset"))
        @kernel.console_command(
            "reset",
            input_type="window",
            output_type="window",
            help=_("reset the supplied window, or '*' for all windows"),
        )
        def window_reset(channel, _, data, window=None, **kwargs):
            for section in list(kernel.derivable('')):
                if section.startswith("window"):
                    kernel.clear_persistent(section)
                    try:
                        del kernel.contexts[section]
                    except KeyError:
                        pass  # No open context for that window, nothing will save out.

        @kernel.console_command("refresh", help=_("Refresh the main wxMeerK40 window"))
        def scene_refresh(command, channel, _, **kwargs):
            context.signal("refresh_scene", "Scene")
            context.signal("rebuild_tree")
            channel(_("Refreshed."))

        @kernel.console_command("tooltips_enable", hidden=True)
        def tooltip_enable(command, channel, _, **kwargs):
            context.setting(bool, "disable_tool_tips", False)
            context.disable_tool_tips = False
            wx.ToolTip.Enable(not context.disable_tool_tips)

        @kernel.console_command("tooltips_disable", hidden=True)
        def tooltip_disable(command, channel, _, **kwargs):
            context.setting(bool, "disable_tool_tips", False)
            context.disable_tool_tips = True
            wx.ToolTip.Enable(not context.disable_tool_tips)

    def module_open(self, *args, **kwargs):
        context = self.context
        kernel = context.kernel

        try:  # pyinstaller internal location
            _resource_path = os.path.join(sys._MEIPASS, "locale")
            wx.Locale.AddCatalogLookupPathPrefix(_resource_path)
        except Exception:
            pass

        try:  # Mac py2app resource
            _resource_path = os.path.join(os.environ["RESOURCEPATH"], "locale")
            wx.Locale.AddCatalogLookupPathPrefix(_resource_path)
        except Exception:
            pass

        wx.Locale.AddCatalogLookupPathPrefix("locale")

        # Default Locale, prepended. Check this first.
        basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
        localedir = os.path.join(basepath, "locale")
        wx.Locale.AddCatalogLookupPathPrefix(localedir)

        kernel.translation = wx.GetTranslation

        context.app = self  # Registers self as kernel.app

        context.setting(int, "language", None)
        language = context.language
        if language is not None and language != 0:
            self.update_language(language)

        @context.console_argument("sure", type=str, help="Are you sure? 'yes'?")
        @context.console_command("nuke_settings", hidden=True)
        def nuke_settings(command, channel, _, sure=None, **kwargs):
            if sure == "yes":
                kernel = self.context.kernel
                kernel.delete_all_persistent()
                kernel.shutdown()
            else:
                channel(
                    'Argument "sure" is required. Requires typing: "nuke_settings yes"'
                )

    def update_language(self, lang):
        """
        Update language to the requested language.
        """
        context = self.context
        try:
            language_code, language_name, language_index = supported_languages[lang]
        except (IndexError, ValueError):
            return
        context.language = lang

        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale
        self.locale = wx.Locale(language_index)
        # wxWidgets is broken. IsOk()==false and pops up error dialog, but it translates fine!
        if self.locale.IsOk() or platform.system() == "Linux":
            self.locale.AddCatalog("meerk40t")
        else:
            self.locale = None
        context.signal("language", (lang, language_code, language_name, language_index))


# end of class MeerK40tGui
def send_file_to_developers(filename):
    """
    Loads a file to send data to the developers.

    @param filename: file to send
    @return:
    """
    try:
        with open(filename, "r") as f:
            data = f.read()
    except:
        if data is None:
            return  # There is no file, there is no data.
    send_data_to_developers(filename, data)


def send_data_to_developers(filename, data):
    """
    Sends crash log to a server using rfc1341 7.2 The multipart Content-Type
    https://www.w3.org/Protocols/rfc1341/7_2_Multipart.html

    @param filename: filename to use when sending file
    @param data: data to send
    @return:
    """
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipaddr = socket.gethostbyname("api.anonfiles.com")
    s.connect((ipaddr, 80))
    boundary = "----------------meerk40t-boundary"
    file_head = list()
    file_head.append("--" + boundary)
    file_head.append(
        'Content-Disposition: form-data; name="file"; filename="%s"' % filename
    )
    file_head.append("Content-Type: text/plain")
    file_head.append("")
    part = "\x0D\x0A".join(file_head)
    terminal = "--" + boundary + "--"
    payload = "\x0D\x0A".join((part, data, terminal, ""))
    http_req = list()
    http_req.append("POST /upload?token=630f908431136ef4 HTTP/1.1")
    http_req.append("Host: api.anonfiles.com")
    http_req.append("User-Agent: meerk40t/0.0.1")
    http_req.append("Accept: */*")
    http_req.append("Content-Length: %d" % (len(payload)))
    http_req.append("Content-Type: multipart/form-data; boundary=%s" % boundary)
    http_req.append("")
    header = "\x0D\x0A".join(http_req)
    request = "\x0D\x0A".join((header, payload))
    s.send(bytes(request, "utf-8"))
    response = s.recv(4096)
    response = response.decode("utf-8")
    s.close()

    if response is None or len(response) == 0:
        http_code = "No Response."
    else:
        http_code = response.split("\n")[0]

    if http_code.startswith("HTTP/1.1 200 OK"):
        print(http_code)
        http_code = response.split("\n")[0]
        dlg = wx.MessageDialog(
            None,
            _("We got your message. Thank you for helping\n\n") + str(http_code),
            _("Thanks"),
            wx.OK,
        )
        dlg.ShowModal()
        dlg.Destroy()
    else:
        print(response)
        MEERK40T_ISSUES = "https://github.com/meerk40t/meerk40t/issues"
        dlg = wx.MessageDialog(
            None,
            _(
                "We're sorry, that didn't work. Raise an issue on the github please.\n\n The log file will be in your working directory.\n"
            )
            + MEERK40T_ISSUES
            + "\n\n"
            + str(http_code),
            _("Thanks"),
            wx.OK,
        )
        dlg.ShowModal()
        dlg.Destroy()


def handleGUIException(exc_type, exc_value, exc_traceback):
    """
    Handler for errors. Save error to a file, and create dialog.

    :param exc_type:
    :param exc_value:
    :param exc_traceback:
    :return:
    """
    wxversion = "wx"
    try:
        wxversion = wx.version()
    except:
        pass

    error_log = "MeerK40t crash log. Version: %s on %s:%s - %s\n" % (
        APPLICATION_VERSION,
        platform.system(),
        platform.machine(),
        wxversion,
    )
    error_log += "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print("\n")
    print(error_log)
    try:
        import datetime

        filename = "MeerK40t-{date:%Y-%m-%d_%H_%M_%S}.txt".format(
            date=datetime.datetime.now()
        )
    except Exception:  # I already crashed once, if there's another here just ignore it.
        filename = "MeerK40t-Crash.txt"

    try:
        try:
            with open(filename, "w") as file:
                file.write(error_log)
                print(file)
        except PermissionError:
            from meerk40t.kernel import get_safe_path

            filename = get_safe_path(APPLICATION_NAME).joinpath(filename)
            with open(filename, "w") as file:
                file.write(error_log)
                print(file)
    except Exception:
        # I already crashed once, if there's another here just ignore it.
        pass

    # Ask to send file.
    git = branch = False
    if " " in APPLICATION_VERSION:
        ver, exec_type = APPLICATION_VERSION.split(" ", 1)
        git = exec_type == "git"

    if git:
        head_file = os.path.join(sys.path[0], ".git", "HEAD")
        if os.path.isfile(head_file):
            ref_prefix = "ref: refs/heads/"
            ref = ""
            try:
                with open(head_file, "r") as f:
                    ref = f.readline()
            except Exception:
                pass
            if ref.startswith(ref_prefix):
                branch = ref[len(ref_prefix) :].strip("\n")

    if git and branch and branch != "main":
        message = _("Meerk40t has encountered a crash.")
        ext_msg = _(
            """It appears that you are running Meerk40t from source managed by Git,
from a branch '{branch}' which is not 'main',
and that you are therefore running a development version of Meerk40t.

To avoid reporting crashes during development, automated submission of this crash has
been disabled. If this is a crash which is unrelated to any development work that you are
undertaking, please recreate this crash under main or if you are certain that this is not
caused by any code changes you have made, then you can manually create a new Github
issue indicating the branch you are runing from and using the traceback below which can
be found in "{filename}".

"""
        ).format(
            filename=filename,
            branch=branch,
        )
        caption = _("Crash Detected!")
        style = wx.OK | wx.ICON_WARNING
    else:
        message = _(
            """The bad news is that MeerK40t encountered a crash, and the developers apologise for this bug!

The good news is that you can help us fix this bug by anonymously sending us the crash details."""
        )
        ext_msg = _(
            """Only the crash details below are sent. No data from your MeerK40t project is sent. No
personal information is sent either.

Send the following data to the MeerK40t team?
------
"""
        )
        caption = _("Crash Detected! Send Log?")
        style = wx.YES_NO | wx.CANCEL | wx.ICON_WARNING
    ext_msg += error_log
    dlg = wx.MessageDialog(
        None,
        message,
        caption=caption,
        style=style,
    )
    dlg.SetExtendedMessage(ext_msg)
    answer = dlg.ShowModal()
    if answer in (wx.YES, wx.ID_YES):
        send_data_to_developers(filename, error_log)
