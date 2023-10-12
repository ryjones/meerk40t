"""
These are external plugins. They are dynamically found by entry points. This file is replaced with the build file during
builds, since compiled versions do not have access to entry points. External plugins therefore must be hard-coded for
builds. See the external_plugin_build.py file for regular built plugins.
"""

import sys


def plugin(kernel, lifecycle):
    if lifecycle == "plugins":
        if getattr(sys, "frozen", False):
            return
        if kernel.args.no_plugins:
            return

        plugins = list()
        import importlib.metadata as pkg_resources

        entry_points = pkg_resources.entry_points().get("meerk40t.extension", [])

        for entry_point in entry_points:
            try:
                plugin = entry_point.load()
            except pkg_resources.DistributionNotFound:
                pass
            except pkg_resources.VersionConflict as e:
                print(
                    "Cannot install plugin - '{entrypoint}' due to version conflict.".format(
                        entrypoint=str(entry_point)
                    )
                )
                print(e)
            else:
                plugins.append(plugin)
        return plugins
    if lifecycle == "invalidate":
        return True
