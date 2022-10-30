def plugin(kernel, lifecycle=None):
    if lifecycle == "plugins":
        from .gui import gui

        return [gui.plugin]
    elif lifecycle == "invalidate":
        try:
            import serial  # pylint: disable=unused-import
            from serial import SerialException  # pylint: disable=unused-import
        except ImportError:
            print("GRBL plugin could not load because pyserial is not installed.")
            return True
    elif lifecycle == "register":
        _ = kernel.translation

        from .device import GRBLDevice, GRBLDriver

        kernel.register("provider/device/grbl", GRBLDevice)
        kernel.register("driver/grbl", GRBLDriver)

        from .grblemulator import GRBLEmulator

        kernel.register("emulator/grbl", GRBLEmulator)

        from .gcodeloader import GCodeLoader

        kernel.register("load/GCodeLoader", GCodeLoader)

        @kernel.console_option(
            "port", "p", type=int, default=23, help=_("port to listen on.")
        )
        @kernel.console_option(
            "verbose",
            "v",
            type=bool,
            action="store_true",
            help=_("do not watch server channels"),
        )
        @kernel.console_option(
            "quit",
            "q",
            type=bool,
            action="store_true",
            help=_("shutdown current grblserver"),
        )
        @kernel.console_command(
            ("grblcontrol", "grbldesign", "grblemulator"),
            help=_("activate the grblserver."),
            hidden=True,
        )
        def grblserver(
            command,
            channel,
            _,
            port=23,
            verbose=False,
            quit=False,
            **kwargs,
        ):
            root = kernel.root
            try:
                server = root.open_as("module/TCPServer", "grbl", port=port)
                emulator = root.open("emulator/grbl")
                if quit:
                    root.close("grbl")
                    root.close("emulator/grbl")
                    return
                root.channel("grbl/send").greet = "Grbl 1.1e ['$' for help]\r"
                channel(_("GRBL Mode."))
                if verbose:
                    console = kernel.channel("console")
                    root.channel("grbl").watch(console)
                    server.events_channel.watch(console)
                # Link emulator and server.
                root.channel("grbl/recv").watch(emulator.write)
                emulator.reply = root.channel("grbl/send")

                channel(
                    _("TCP Server for GRBL Emulator on port: {port}").format(port=port)
                )

                if command == "grbldesign":
                    emulator.design = True
                elif command == "grblcontrol":
                    emulator.control = True
                elif command == "grblemulator":
                    pass
            except OSError as e:
                channel(_("Server failed on port: {port}").format(port=port))
                channel(str(e.strerror))
            return

        @kernel.console_command(
            "grblinterpreter", help=_("activate the grbl interpreter.")
        )
        def lhyemulator(channel, _, **kwargs):
            try:
                kernel.device.open_as("emulator/grbl", "grblinterpreter")
                channel(
                    _("Grbl Interpreter attached to {device}").format(
                        device=str(kernel.device)
                    )
                )
            except KeyError:
                channel(_("Interpreter cannot be attached to any device."))
            return

    elif lifecycle == "preboot":
        suffix = "grbl"
        for d in kernel.derivable(suffix):
            kernel.root(f"service device start -p {d} {suffix}\n")
