"""
OMG Multibeam Survey & Processing Monitor — QGIS Plugin Entry Point.
"""

import importlib


def classFactory(iface):
    """Load (and hot-reload on update) OmgMultibeamMonitorPlugin class from omg_plugin."""
    from . import omg_binary_io, omg_dockwidget, omg_plugin

    importlib.reload(omg_binary_io)
    importlib.reload(omg_dockwidget)
    importlib.reload(omg_plugin)
    return omg_plugin.OmgMultibeamMonitorPlugin(iface)
