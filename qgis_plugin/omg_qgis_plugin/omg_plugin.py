"""
Main QGIS Plugin Controller for OMG Multibeam Survey & Processing Monitor.
"""

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAction

from .omg_dockwidget import OmgMonitorDockWidget


class OmgMultibeamMonitorPlugin:
    """QGIS Plugin glue class connecting the toolbar/menu action to OmgMonitorDockWidget."""

    def __init__(self, iface):
        self.iface = iface
        self.dock_widget = None
        self.action = None

    def initGui(self):
        self.action = QAction("OMG Multibeam Monitor", self.iface.mainWindow())
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
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.dock_widget.show()
        self.dock_widget.raise_()
