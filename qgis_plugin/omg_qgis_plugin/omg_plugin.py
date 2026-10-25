"""
Main QGIS Plugin Controller for OMG Multibeam Survey & Processing Monitor.
Compatible with both QGIS 3.x (PyQt5) and QGIS 4.x (PyQt6).
"""

import os
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon

try:
    from qgis.PyQt.QtGui import QAction
except ImportError:
    from qgis.PyQt.QtWidgets import QAction

from .omg_dockwidget import OmgMonitorDockWidget


RIGHT_DOCK_AREA = getattr(Qt, "RightDockWidgetArea", None)
if RIGHT_DOCK_AREA is None:
    RIGHT_DOCK_AREA = Qt.DockWidgetArea.RightDockWidgetArea


class OmgMultibeamMonitorPlugin:
    """QGIS Plugin glue class connecting the toolbar/menu action to OmgMonitorDockWidget."""

    def __init__(self, iface):
        self.iface = iface
        self.dock_widget = None
        self.action = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        icon = QIcon(icon_path) if os.path.isfile(icon_path) else QIcon()
        self.action = QAction(icon, "OMG Multibeam Monitor", self.iface.mainWindow())
        self.action.setToolTip(
            "Open the UNB Ocean Mapping Group (OMG) Multibeam Survey & Processing Monitor (Qimera/HIPS style)"
        )
        self.action.triggered.connect(self.toggle_dock)

        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToRasterMenu("&OMG Multibeam Monitor", self.action)

    def unload(self):
        if self.action:
            self.iface.removePluginRasterMenu("&OMG Multibeam Monitor", self.action)
            self.iface.removeToolBarIcon(self.action)
            self.action = None

        if self.dock_widget:
            self.iface.removeDockWidget(self.dock_widget)
            self.dock_widget.deleteLater()
            self.dock_widget = None

    def toggle_dock(self):
        if self.dock_widget is None:
            self.dock_widget = OmgMonitorDockWidget(self.iface, self.iface.mainWindow())
            self.iface.addDockWidget(RIGHT_DOCK_AREA, self.dock_widget)
        self.dock_widget.show()
        self.dock_widget.raise_()
