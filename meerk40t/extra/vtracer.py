"""
Vtracer
"""


def plugin(kernel, lifecycle=None):
    if lifecycle == "invalidate":
        try:
            import vtracer
        except ImportError:
            # print("vtracer plugin could not load because vtracer is not installed.")
            return True

    if lifecycle == "register":
        _ = kernel.translation

        @kernel.console_command(
            "vtracer",
            help=_("return paths around image"),
            input_type=("image", "elements"),
            output_type="elements",
        )
        def do_vtracer(
            channel,
            data=None,
            **kwargs,
        ):
            try:
                import os
                from time import perf_counter
                from vtracer import convert_image_to_svg_py
                from meerk40t.kernel import get_safe_path
                from meerk40t.core.units import Length
            except ImportError:
                channel ("vtracer isn't installed, use 'pip install vtracer'")
                return None
            elements = kernel.root.elements
            if data is None:
                data = list(elements.elems(emphasized=True))
            paths = []
            safe_dir = os.path.realpath(get_safe_path(kernel.name))
            input_file = os.path.join(safe_dir, "_vtrace_input.png")
            output_file = os.path.join(safe_dir, "_vtrace_output.svg")
            for node in data:
                if not hasattr(node, "image"):
                    continue
                kernel.root.signal("freeze_tree", True)
                t0 = perf_counter()
                bb = node.bounds
                image = node.image
                image.save(input_file)
                convert_image_to_svg_py(image_path=input_file, out_path=output_file, colormode="bw")
                cmd = (
                    f'xload "{output_file}"' +
                    f' {Length(bb[0]).length_mm}' +
                    f' {Length(bb[1]).length_mm}' +
                    f' {Length(bb[2] - bb[0]).length_mm}' +
                    f' {Length(bb[3] - bb[1]).length_mm}'
                )
                t1 = perf_counter()
                # print (f"Vectorization took {t1-t0:.1f}sec, now loading file, executing {cmd}")
                # elements.suppress_updates = True
                kernel.root(f"{cmd}\n")
                t2 = perf_counter()
                # print (f"Loading took {t2-t1:.1f}sec")
                try:
                    os.remove(input_file)
                    os.remove(output_file)
                except (PermissionError, OSError):
                    pass
                except Exception as e:
                    channel(f"Could not remove temporary files: {e}")
                kernel.root.signal("freeze_tree", False)
                t3 = perf_counter()
                channel(f"Time needed for vectorisation: {t3-t0:.1f}sec (analysis: {t1-t0:.1f}sec, loading: {t2-t1:.1f}sec)")
            return "elements", None
