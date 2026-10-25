"""
OMG Multibeam Survey & Processing Monitor — QGIS Plugin Entry Point.
"""


def classFactory(iface):
    """Load OmgMultibeamMonitorPlugin class from omg_plugin."""
    from .omg_plugin import OmgMultibeamMonitorPlugin
    return OmgMultibeamMonitorPlugin(iface)
