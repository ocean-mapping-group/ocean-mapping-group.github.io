"""
Qimera / CARIS HIPS-style Dockable Map & Processing Monitor Widget for QGIS 3.x & 4.x.

Supports both flat workspaces and multi-day Julian-Day subdirectory workspaces
(e.g., W:\\data\\2026_Antarctica\\OMG_Care2026\\02_Bransfield or /mnt/w/data/... with subdirs 74..81).

Key Capabilities:
  1. Automatically plots `.decnav` (or `.merged`) multibeam tracklines on the QGIS map canvas
     immediately after scanning a workspace (and updates live when filtering by Julian Day
     or switching color mode).
  2. Creates `.blank` and `.r4` / `.8bit` / `.sun` grids using `make_blank`, `tor4`, `weigh_grid`,
     `r4to8bit`, and `addSUN` (or pure-Python `make_blank_grid_from_bounds` when running on a
     machine without the compiled C binaries) and interprets the 1024-byte `OMG1` (`JHC_header`)
     header identically to `code/grid/edhead.c` and `code/subr/j_proj.c`.
  3. Read-Only Master Archive Safety: All generated GeoJSON tracklines, blank/gridded rasters,
     and GDAL `.vrt` sidecar files are written to a local output/cache directory so master
     archive drives (such as W:) are never modified.
"""

import os
import re
import shutil
from typing import List, Optional, Tuple

from qgis.PyQt.QtCore import Qt, QProcess, QTimer, QFileSystemWatcher
from qgis.PyQt.QtGui import QColor, QFont
from qgis.PyQt.QtWidgets import (
    QAbstractItemView,
    QDockWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
    QPlainTextEdit,
    QSplitter,
    QComboBox,
    QMessageBox,
)
from qgis.core import (
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsCategorizedSymbolRenderer,
    QgsRendererCategory,
    QgsSymbol,
    QgsSingleBandPseudoColorRenderer,
    QgsColorRampShader,
    QgsRasterShader,
    QgsRectangle,
)

try:
    from qgis.core import Qgis
except ImportError:
    Qgis = None

try:
    from qgis.core import QgsWkbTypes
except ImportError:
    QgsWkbTypes = None

from .omg_binary_io import (
    JhcHeaderInfo,
    LineProcessingStatus,
    create_gdal_vrt_for_jhc,
    export_tracklines_geojson,
    format_edhead_report,
    make_blank_grid_from_bounds,
    parse_jhc_header,
    parse_omg_merged_summary,
    parse_omg_param,
    scan_survey_workspace,
)

# Qt5 / Qt6 (QGIS 3.x / 4.x) Dual-Compatible Enum Helpers
QT_VERTICAL = getattr(Qt, "Vertical", None) or Qt.Orientation.Vertical
QT_ALIGN_CENTER = getattr(Qt, "AlignCenter", None) or Qt.AlignmentFlag.AlignCenter
QT_USER_ROLE = getattr(Qt, "UserRole", None) or Qt.ItemDataRole.UserRole
SELECT_ROWS = getattr(QAbstractItemView, "SelectRows", None) or QAbstractItemView.SelectionBehavior.SelectRows
NO_EDIT_TRIGGERS = getattr(QAbstractItemView, "NoEditTriggers", None) or QAbstractItemView.EditTrigger.NoEditTriggers
HEADER_STRETCH = getattr(QHeaderView, "Stretch", None) or QHeaderView.ResizeMode.Stretch
HEADER_RESIZE_CONTENTS = getattr(QHeaderView, "ResizeToContents", None) or QHeaderView.ResizeMode.ResizeToContents
PROC_MERGED_CHANNELS = getattr(QProcess, "MergedChannels", None) or QProcess.ProcessChannelMode.MergedChannels
RAMP_INTERPOLATED = getattr(QgsColorRampShader, "Interpolated", None) or QgsColorRampShader.Type.Interpolated

OMG_BIN_DIRS = [
    "/home/iwc/local/linux/bin",
    os.path.expanduser("~/local/linux/bin"),
]


def _find_omg_binary(name: str) -> Optional[str]:
    """Locate a compiled OMG binary on PATH or in standard OMG bin directories."""
    found = shutil.which(name)
    if found:
        return found
    for d in OMG_BIN_DIRS:
        candidate = os.path.join(d, name)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def _default_line_symbol():
    """Return a default line symbol across both QGIS 3.x and QGIS 4.x APIs."""
    if Qgis is not None and hasattr(Qgis, "GeometryType"):
        return QgsSymbol.defaultSymbol(Qgis.GeometryType.Line)
    if QgsWkbTypes is not None:
        geom_type = getattr(QgsWkbTypes, "LineGeometry", None) or QgsWkbTypes.GeometryType.LineGeometry
        return QgsSymbol.defaultSymbol(geom_type)
    return None


def _normalize_platform_path(raw_path: str) -> str:
    """
    Seamlessly translate between Windows drive paths (e.g. W:\\data\\...) and
    WSL mount paths (e.g. /mnt/w/data/...) depending on the OS running QGIS.
    """
    p = raw_path.strip()
    if not p:
        return p
    if os.name == "nt":
        # Running native Windows QGIS: convert /mnt/w/... -> W:\...
        m = re.match(r"^/mnt/([a-zA-Z])/(.*)$", p)
        if m:
            drive = m.group(1).upper()
            rest = m.group(2).replace("/", "\\")
            return f"{drive}:\\{rest}"
    else:
        # Running Linux / WSL QGIS: convert W:\... -> /mnt/w/...
        m = re.match(r"^([a-zA-Z]):[\\/](.*)$", p)
        if m:
            drive = m.group(1).lower()
            rest = m.group(2).replace("\\", "/")
            return f"/mnt/{drive}/{rest}"
    return p


DEFAULT_WORKSPACE_DIR = (
    r"W:\data\2026_Antarctica\OMG_Care2026\02_Bransfield"
    if os.name == "nt"
    else "/mnt/w/data/2026_Antarctica/OMG_Care2026/02_Bransfield"
)

DEFAULT_CACHE_DIR = (
    "/home/iwc/coding/bransfield_qgis_outputs"
    if os.path.isdir("/home/iwc/coding")
    else os.path.join(os.path.expanduser("~"), "omg_qgis_outputs")
)


class OmgMonitorDockWidget(QDockWidget):
    """Qimera / HIPS-style dockable workspace monitor and raster manager for OMG."""

    def __init__(self, iface, parent=None):
        super().__init__("OMG Multibeam Survey & Processing Monitor", parent)
        self.iface = iface
        self.setObjectName("OmgMonitorDockWidget")
        self.workspace_dir: str = ""
        self.output_dir: str = DEFAULT_CACHE_DIR
        self.lines: List[LineProcessingStatus] = []
        self.rasters: List[JhcHeaderInfo] = []
        self.proc: Optional[QProcess] = None
        self._pending_autoload_rasters: List[str] = []

        self.fs_watcher = QFileSystemWatcher(self)
        self.fs_watcher.directoryChanged.connect(self._on_directory_changed)

        self.debounce_timer = QTimer(self)
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.setInterval(1500)
        self.debounce_timer.timeout.connect(self.refresh_workspace)

        self._init_ui()

    def _init_ui(self):
        container = QWidget(self)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(6, 6, 6, 6)

        # Row 1: Survey Workspace selector (read-only safe)
        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("Survey Workspace:"))
        self.ws_edit = QLineEdit(DEFAULT_WORKSPACE_DIR)
        self.ws_edit.setPlaceholderText("W:\\data\\... or /path/to/survey_project (containing raw/, merged/, decnav/, ss/)")
        top_bar.addWidget(self.ws_edit, 1)

        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_workspace)
        top_bar.addWidget(browse_btn)

        top_bar.addWidget(QLabel("Day/Subdir:"))
        self.day_filter_combo = QComboBox()
        self.day_filter_combo.addItem("All Days")
        self.day_filter_combo.currentTextChanged.connect(self._apply_table_filter)
        top_bar.addWidget(self.day_filter_combo)

        refresh_btn = QPushButton("Scan Workspace")
        refresh_btn.setToolTip("Scan workspace and automatically plot .decnav / .merged tracklines on the QGIS map")
        refresh_btn.clicked.connect(self.refresh_workspace)
        top_bar.addWidget(refresh_btn)

        self.auto_plot_cb = QCheckBox("Auto-Plot DecNav")
        self.auto_plot_cb.setChecked(True)
        self.auto_plot_cb.setToolTip("Automatically plot/update .decnav tracklines on the QGIS map after scanning.")
        top_bar.addWidget(self.auto_plot_cb)

        self.watch_cb = QCheckBox("Live Watch")
        self.watch_cb.setChecked(False)
        self.watch_cb.setToolTip(
            "Enable when actively running unravel/gridding scripts on a local workspace to auto-refresh layers."
        )
        top_bar.addWidget(self.watch_cb)
        main_layout.addLayout(top_bar)

        # Row 2: Local Cache / Output Directory (ensures master archive W: is never modified)
        cache_bar = QHBoxLayout()
        cache_bar.addWidget(QLabel("Local Output/VRT Cache Dir (Archive-Safe):"))
        self.out_dir_edit = QLineEdit(self.output_dir)
        cache_bar.addWidget(self.out_dir_edit, 1)

        color_by_lbl = QLabel("Color Tracklines By:")
        cache_bar.addWidget(color_by_lbl)
        self.color_mode_combo = QComboBox()
        self.color_mode_combo.addItems(["Julian Day (subdir)", "Processing Stage"])
        self.color_mode_combo.currentTextChanged.connect(self._on_color_mode_changed)
        cache_bar.addWidget(self.color_mode_combo)
        main_layout.addLayout(cache_bar)

        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs, 1)

        self._build_lines_tab()
        self._build_rasters_tab()
        self._build_runner_tab()

        self.setWidget(container)

    def _build_lines_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        splitter = QSplitter(QT_VERTICAL)

        # Upper: Qimera/HIPS-style processing stage matrix table
        upper_widget = QWidget()
        upper_layout = QVBoxLayout(upper_widget)
        upper_layout.setContentsMargins(0, 0, 0, 0)

        btn_bar = QHBoxLayout()
        self.status_summary_lbl = QLabel("Click 'Scan Workspace' to load multibeam lines and plot .decnav tracks.")
        btn_bar.addWidget(self.status_summary_lbl, 1)

        load_wc_btn = QPushButton("Load Selected Line Water Column (.vert_prof)")
        load_wc_btn.clicked.connect(self.load_selected_line_vert_prof)
        btn_bar.addWidget(load_wc_btn)

        load_tracks_btn = QPushButton("Plot / Update Tracklines on QGIS Map")
        load_tracks_btn.clicked.connect(self.load_or_update_tracklines_layer)
        btn_bar.addWidget(load_tracks_btn)
        upper_layout.addLayout(btn_bar)

        cols = [
            "Day",
            "Survey Line",
            "Stage",
            "Raw",
            "WC",
            ".merged",
            ".nav",
            "decnav",
            ".orient",
            "SVP",
            ".ss",
            "Start UTC",
            "Hdg (°)",
            "Spd (kts)",
            "Depth (m)",
        ]
        self.lines_table = QTableWidget(0, len(cols))
        self.lines_table.setHorizontalHeaderLabels(cols)
        self.lines_table.setSelectionBehavior(SELECT_ROWS)
        self.lines_table.setEditTriggers(NO_EDIT_TRIGGERS)
        self.lines_table.horizontalHeader().setSectionResizeMode(1, HEADER_STRETCH)
        self.lines_table.itemSelectionChanged.connect(self._on_line_selected)
        upper_layout.addWidget(self.lines_table, 1)

        splitter.addWidget(upper_widget)

        # Lower: .param / .param_km Lever Arms & .svp_001 / .sv_filtered SVP Cast Inspector
        lower_widget = QWidget()
        lower_layout = QHBoxLayout(lower_widget)
        lower_layout.setContentsMargins(0, 0, 0, 0)

        self.param_inspector = QPlainTextEdit()
        self.param_inspector.setReadOnly(True)
        self.param_inspector.setFont(QFont("Monospace", 9))
        self.param_inspector.setPlaceholderText(
            "Select a survey line above to inspect its .param / .param_km lever arms & merged header..."
        )
        lower_layout.addWidget(self.param_inspector, 1)

        self.svp_inspector = QPlainTextEdit()
        self.svp_inspector.setReadOnly(True)
        self.svp_inspector.setFont(QFont("Monospace", 9))
        self.svp_inspector.setPlaceholderText(
            "Select a survey line above to inspect its .svp_001 / .sv_filtered sound velocity cast..."
        )
        lower_layout.addWidget(self.svp_inspector, 1)

        splitter.addWidget(lower_widget)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)
        self.tabs.addTab(tab, "1. Survey Lines & Pipeline Monitor")

    def _build_rasters_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Row 1: Make Blank / Grid / 8-bit / Sun Maps bar (make_blank + tor4 + weigh_grid + r4to8bit + addSUN)
        grid_bar = QHBoxLayout()
        grid_bar.addWidget(QLabel("Grid Prefix:"))
        self.grid_prefix_edit = QLineEdit("bransfield_grid")
        self.grid_prefix_edit.setMaximumWidth(150)
        grid_bar.addWidget(self.grid_prefix_edit)

        grid_bar.addWidget(QLabel("Pixel Size mpp (m):"))
        self.grid_mpp_edit = QLineEdit("100.0")
        self.grid_mpp_edit.setMaximumWidth(75)
        grid_bar.addWidget(self.grid_mpp_edit)

        make_blank_btn = QPushButton("1. Make .blank + .r4 from .decnav Bounds (make_blank + tor4)")
        make_blank_btn.setToolTip(
            "Create <prefix>.blank, <prefix>.r4, <prefix>.r4_weights, and <prefix>.r4_weight_depth "
            "from the bounding box of the currently filtered .decnav / .merged lines."
        )
        make_blank_btn.clicked.connect(self.create_blank_grid_for_current_lines)
        grid_bar.addWidget(make_blank_btn)

        build_maps_btn = QPushButton("2. Grid & Render .r4 + .8bit + .sun (weigh_grid + r4to8bit + addSUN)")
        build_maps_btn.setToolTip(
            "Run weigh_grid -> r4to8bit -nozero -no255 -> addSUN -elev 45 -azi 315 -vert_exag 4.0 "
            "on the filtered .merged lines and load the resulting rasters into QGIS."
        )
        build_maps_btn.clicked.connect(self.build_r4_8bit_sun_maps)
        grid_bar.addWidget(build_maps_btn)
        grid_bar.addStretch(1)
        layout.addLayout(grid_bar)

        # Row 2: Discovered Rasters controls
        top_bar = QHBoxLayout()
        top_bar.addWidget(
            QLabel("Discovered OMG1 Rasters (.blank, .r4, .8bit, .sun, .mos, .vert_prof) — Interpreted via edhead.c:")
        )
        top_bar.addStretch(1)

        load_selected_btn = QPushButton("Load Selected Raster in QGIS")
        load_selected_btn.clicked.connect(self.load_selected_raster_in_qgis)
        top_bar.addWidget(load_selected_btn)

        load_any_btn = QPushButton("Open Any .blank / .r4 / .8bit / .sun / .mos / .vert_prof File...")
        load_any_btn.clicked.connect(self.browse_and_load_single_raster)
        top_bar.addWidget(load_any_btn)
        layout.addLayout(top_bar)

        splitter = QSplitter(QT_VERTICAL)

        cols = [
            "Filename",
            "Type",
            "Dimensions (dx × dy)",
            "Resolution (m)",
            "Projection",
            "Min Value",
            "Max Value",
            "Sun (Azi / Elev)",
            "Full Path",
        ]
        self.rasters_table = QTableWidget(0, len(cols))
        self.rasters_table.setHorizontalHeaderLabels(cols)
        self.rasters_table.setSelectionBehavior(SELECT_ROWS)
        self.rasters_table.setEditTriggers(NO_EDIT_TRIGGERS)
        self.rasters_table.horizontalHeader().setSectionResizeMode(0, HEADER_RESIZE_CONTENTS)
        self.rasters_table.horizontalHeader().setSectionResizeMode(8, HEADER_STRETCH)
        self.rasters_table.itemSelectionChanged.connect(self._on_raster_selected)
        self.rasters_table.itemDoubleClicked.connect(lambda _item: self.load_selected_raster_in_qgis())
        splitter.addWidget(self.rasters_table)

        # Lower: edhead.c Header & World-File / GeoTIFF Georeferencing Inspector
        self.edhead_inspector = QPlainTextEdit()
        self.edhead_inspector.setReadOnly(True)
        self.edhead_inspector.setFont(QFont("Monospace", 9))
        self.edhead_inspector.setPlaceholderText(
            "Select any .blank, .r4, .8bit, .sun, .mos, or .vert_prof raster above to inspect its "
            "1024-byte OMG1 (JHC_header) metadata, projection, and TFW world-file affine transform (edhead.c)..."
        )
        splitter.addWidget(self.edhead_inspector)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        layout.addWidget(splitter, 1)
        self.tabs.addTab(tab, "2. Grids & Mosaics (.blank / .r4 / .8bit / .sun)")

    def _build_runner_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        cmd_bar = QHBoxLayout()
        cmd_bar.addWidget(QLabel("Quick Action:"))
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(
            [
                "edhead -show bransfield_test.r4",
                "edhead -dump_tfw bransfield_test.r4",
                "echo 100.0 | make_blank -float bransfield_day74 -boundsof_nav /mnt/w/data/2026_Antarctica/OMG_Care2026/02_Bransfield/decnav/74/*.decnav",
                "tor4 bransfield_test",
                "weigh_grid bransfield_test /mnt/w/data/2026_Antarctica/OMG_Care2026/02_Bransfield/merged/74/0029*.merged /mnt/w/data/2026_Antarctica/OMG_Care2026/02_Bransfield/merged/74/0030*.merged",
                "r4to8bit -nozero -no255 bransfield_test",
                "addSUN -elev 45 -azi 315 -vert_exag 4.0 bransfield_test.r4 bransfield_test.sun",
                "swathed -locate bransfield_test.r4 /mnt/w/data/2026_Antarctica/OMG_Care2026/02_Bransfield/merged/74/0029*.merged",
                "jview -sun bransfield_test.8bit bransfield_test.sun bransfield_test.r4",
            ]
        )
        self.preset_combo.currentTextChanged.connect(lambda txt: self.cmd_input.setText(txt))
        cmd_bar.addWidget(self.preset_combo, 1)
        layout.addLayout(cmd_bar)

        exec_bar = QHBoxLayout()
        exec_bar.addWidget(QLabel("Command (Runs in Local Output Dir):"))
        self.cmd_input = QLineEdit(self.preset_combo.currentText())
        exec_bar.addWidget(self.cmd_input, 1)

        run_btn = QPushButton("Execute Command")
        run_btn.clicked.connect(self.run_custom_command)
        exec_bar.addWidget(run_btn)
        layout.addLayout(exec_bar)

        self.cmd_log = QPlainTextEdit()
        self.cmd_log.setReadOnly(True)
        self.cmd_log.setFont(QFont("Monospace", 9))
        layout.addWidget(self.cmd_log, 1)

        self.tabs.addTab(tab, "3. Run OMG Tools & Launch swathed / jview")

    def _browse_workspace(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select OMG Survey Workspace Directory", self.workspace_dir or os.path.expanduser("~")
        )
        if folder:
            self.ws_edit.setText(folder)
            self.refresh_workspace()

    def _on_directory_changed(self, _path: str):
        if self.watch_cb.isChecked():
            self.debounce_timer.start()

    def _update_watched_dirs(self):
        old_dirs = self.fs_watcher.directories()
        if old_dirs:
            self.fs_watcher.removePaths(old_dirs)
        if not self.watch_cb.isChecked() or not self.workspace_dir or not os.path.isdir(self.workspace_dir):
            return
        watch_list = [self.workspace_dir]
        for sub in ("raw", "merged", "decnav", "ss", "grids"):
            p = os.path.join(self.workspace_dir, sub)
            if os.path.isdir(p):
                watch_list.append(p)
        if self.output_dir and os.path.isdir(self.output_dir):
            watch_list.append(self.output_dir)
        self.fs_watcher.addPaths(watch_list)

    def refresh_workspace(self):
        ws = _normalize_platform_path(self.ws_edit.text())
        if not ws or not os.path.isdir(ws):
            QMessageBox.warning(
                self,
                "Directory Not Found",
                f"Could not find survey workspace directory:\n{ws}\n\nPlease check that the drive is mounted or browse to the folder.",
            )
            return
        self.ws_edit.setText(ws)
        self.workspace_dir = os.path.abspath(ws)
        self.output_dir = _normalize_platform_path(self.out_dir_edit.text()) or DEFAULT_CACHE_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        self._update_watched_dirs()

        self.lines, self.rasters = scan_survey_workspace(
            self.workspace_dir,
            read_merged_headers=False,
            read_decnav_summaries=True,
            extra_raster_dirs=[self.output_dir],
        )

        # Update Day/Subdir filter dropdown
        subdirs = sorted({l.subdir for l in self.lines if l.subdir})
        current_sel = self.day_filter_combo.currentText()
        self.day_filter_combo.blockSignals(True)
        self.day_filter_combo.clear()
        self.day_filter_combo.addItem("All Days")
        for sd in subdirs:
            self.day_filter_combo.addItem(sd)
        if current_sel in subdirs:
            self.day_filter_combo.setCurrentText(current_sel)
        self.day_filter_combo.blockSignals(False)

        self._populate_lines_table()
        self._populate_rasters_table()

        total = len(self.lines)
        n_merged = sum(1 for l in self.lines if l.has_merged)
        n_decnav = sum(1 for l in self.lines if l.has_decnav)
        n_att = sum(1 for l in self.lines if l.has_orientation_active)
        n_wc = sum(1 for l in self.lines if l.has_watercol)
        n_ss = sum(1 for l in self.lines if l.has_ss_gloria)
        self.status_summary_lbl.setText(
            f"Lines: {total} (Days: {', '.join(subdirs) if subdirs else 'flat'}) | "
            f"DecNav: {n_decnav}/{total} | .merged: {n_merged}/{total} | "
            f"WC: {n_wc}/{total} | Att: {n_att}/{total} | .ss: {n_ss}/{total} | "
            f"Rasters: {len(self.rasters)}"
        )

        # Automatically plot .decnav / .merged tracklines on the QGIS map canvas after scanning!
        if self.auto_plot_cb.isChecked() and self.lines:
            self.load_or_update_tracklines_layer()

    def _get_filtered_lines(self) -> List[LineProcessingStatus]:
        day_sel = self.day_filter_combo.currentText()
        if not day_sel or day_sel == "All Days":
            return self.lines
        return [l for l in self.lines if l.subdir == day_sel]

    def _apply_table_filter(self):
        self._populate_lines_table()
        if self.auto_plot_cb.isChecked() and self.lines:
            self.load_or_update_tracklines_layer()

    def _on_color_mode_changed(self, _text: str):
        if self.lines:
            self.load_or_update_tracklines_layer()

    def _populate_lines_table(self):
        filtered = self._get_filtered_lines()
        self.lines_table.setRowCount(len(filtered))
        for row, st in enumerate(filtered):
            def chk(val: bool) -> QTableWidgetItem:
                it = QTableWidgetItem("✔" if val else "—")
                it.setTextAlignment(QT_ALIGN_CENTER)
                it.setForeground(QColor("#1b7837") if val else QColor("#999999"))
                return it

            day_it = QTableWidgetItem(st.subdir or "—")
            day_it.setTextAlignment(QT_ALIGN_CENTER)
            name_it = QTableWidgetItem(st.line_name)
            name_it.setData(QT_USER_ROLE, st)

            stage_it = QTableWidgetItem(st.stage_summary)
            if st.stage_summary.startswith("COMPLETE"):
                stage_it.setBackground(QColor("#d9f0d3"))
            elif st.stage_summary.startswith("BATHY READY"):
                stage_it.setBackground(QColor("#e7d4e8"))
            elif st.stage_summary.startswith("UNPACKED"):
                stage_it.setBackground(QColor("#fee0b6"))
            else:
                stage_it.setBackground(QColor("#f7f7f7"))

            self.lines_table.setItem(row, 0, day_it)
            self.lines_table.setItem(row, 1, name_it)
            self.lines_table.setItem(row, 2, stage_it)
            self.lines_table.setItem(row, 3, chk(st.has_raw_kmall or st.has_raw_all))
            self.lines_table.setItem(row, 4, chk(st.has_watercol or st.has_vert_prof))
            self.lines_table.setItem(row, 5, chk(st.has_merged))
            self.lines_table.setItem(row, 6, chk(st.has_nav_active or st.has_nav_1))
            self.lines_table.setItem(row, 7, chk(st.has_decnav))
            self.lines_table.setItem(
                row, 8, chk(st.has_orientation_active or st.has_net_att_2 or st.has_net_att_1 or st.has_orientation_1)
            )
            self.lines_table.setItem(row, 9, chk(st.has_sv_filtered))
            self.lines_table.setItem(row, 10, chk(st.has_ss_gloria))
            self.lines_table.setItem(row, 11, QTableWidgetItem(st.start_time_utc or "—"))
            self.lines_table.setItem(
                row, 12, QTableWidgetItem(f"{st.mean_heading_deg:.1f}°" if st.mean_heading_deg else "—")
            )
            self.lines_table.setItem(
                row, 13, QTableWidgetItem(f"{st.mean_speed_kts:.1f}" if st.mean_speed_kts else "—")
            )
            depth_str = f"{st.min_depth_m:.0f}–{st.max_depth_m:.0f}" if st.max_depth_m > 0 else "—"
            self.lines_table.setItem(row, 14, QTableWidgetItem(depth_str))

    def _populate_rasters_table(self):
        self.rasters_table.setRowCount(len(self.rasters))
        for row, hdr in enumerate(self.rasters):
            self.rasters_table.setItem(row, 0, QTableWidgetItem(os.path.basename(hdr.filepath)))
            self.rasters_table.setItem(row, 1, QTableWidgetItem(hdr.data_type_name))
            self.rasters_table.setItem(row, 2, QTableWidgetItem(f"{hdr.dx} × {hdr.dy}"))
            self.rasters_table.setItem(row, 3, QTableWidgetItem(f"{hdr.xstep:.2f} × {hdr.ystep:.2f}"))
            self.rasters_table.setItem(row, 4, QTableWidgetItem(hdr.projection_name))
            self.rasters_table.setItem(row, 5, QTableWidgetItem(f"{hdr.min_value:.2f}"))
            self.rasters_table.setItem(row, 6, QTableWidgetItem(f"{hdr.max_value:.2f}"))
            sun_str = f"{hdr.sun_azi:.0f}° / {hdr.sun_elev:.0f}°" if hdr.sun_elev > 0 else "—"
            self.rasters_table.setItem(row, 7, QTableWidgetItem(sun_str))
            self.rasters_table.setItem(row, 8, QTableWidgetItem(hdr.filepath))
        if self.rasters and not self.rasters_table.selectionModel().selectedRows():
            self.rasters_table.selectRow(0)

    def _on_raster_selected(self):
        rows = self.rasters_table.selectionModel().selectedRows()
        if not rows:
            return
        idx = rows[0].row()
        if 0 <= idx < len(self.rasters):
            self.edhead_inspector.setPlainText(format_edhead_report(self.rasters[idx]))

    def _get_selected_line(self) -> Optional[LineProcessingStatus]:
        rows = self.lines_table.selectionModel().selectedRows()
        if not rows:
            return None
        row = rows[0].row()
        name_item = self.lines_table.item(row, 1)
        if not name_item:
            return None
        return name_item.data(QT_USER_ROLE)

    def _on_line_selected(self):
        st = self._get_selected_line()
        if not st:
            return

        # 1. On-demand inspect .merged header + .param + .param_km lever arms
        info_lines = [f"=== Line: {st.display_id} ===", f"Stage      : {st.stage_summary}"]
        if st.merged_path and os.path.isfile(st.merged_path):
            try:
                summ = parse_omg_merged_summary(st.merged_path)
                info_lines.append(
                    f"Merged Hdr : v{summ.file_version} (toolType={summ.tool_type}), "
                    f"{summ.num_profiles} pings × {summ.num_depths} beams/ping"
                )
                info_lines.append(
                    f"Bounds     : Lat [{summ.min_lat_deg:.5f}, {summ.max_lat_deg:.5f}], "
                    f"Lon [{summ.min_lon_deg:.5f}, {summ.max_lon_deg:.5f}]"
                )
            except Exception as e:
                info_lines.append(f"Merged Hdr : {e}")

        if st.param_path and os.path.isfile(st.param_path):
            info_lines.append(f"\n--- {os.path.basename(st.param_path)} ---")
            for k, v in parse_omg_param(st.param_path).items():
                info_lines.append(f"{k:<12} = {v}")

        if st.param_km_path and os.path.isfile(st.param_km_path) and st.param_km_path != st.param_path:
            info_lines.append(f"\n--- {os.path.basename(st.param_km_path)} ---")
            with open(st.param_km_path, "r", encoding="utf-8", errors="replace") as f:
                info_lines.append(f.read(2048).strip())

        self.param_inspector.setPlainText("\n".join(info_lines))

        # 2. Populate SVP inspector (.svp_001 / .sv_filtered)
        if st.svp_path and os.path.isfile(st.svp_path):
            with open(st.svp_path, "r", encoding="utf-8", errors="replace") as f:
                sv_txt = f.read(4096)
            self.svp_inspector.setPlainText(f"=== {os.path.basename(st.svp_path)} ===\n{sv_txt}")
        else:
            self.svp_inspector.setPlainText(f"No SVP file found for {st.display_id}")

        # 3. Zoom map canvas to selected line bounds
        if st.bounds_wesn and self.iface and self.iface.mapCanvas():
            w, e, s, n = st.bounds_wesn
            if -180.0 <= w < e <= 180.0 and -90.0 <= s < n <= 90.0:
                rect = QgsRectangle(w, s, e, n)
                rect.scale(1.35)
                self.iface.mapCanvas().setExtent(rect)
                self.iface.mapCanvas().refresh()

    def _compute_filtered_bounds_wesn(self) -> Optional[Tuple[float, float, float, float]]:
        filtered = self._get_filtered_lines()
        ws, es, ss, ns = [], [], [], []
        for l in filtered:
            if l.bounds_wesn:
                w, e, s, n = l.bounds_wesn
                if -180.0 <= w < e <= 180.0 and -90.0 <= s < n <= 90.0:
                    ws.append(w)
                    es.append(e)
                    ss.append(s)
                    ns.append(n)
        if not ws:
            return None
        return (min(ws), max(es), min(ss), max(ns))

    def create_blank_grid_for_current_lines(self):
        """
        Create `<prefix>.blank` and `<prefix>.r4` / `.r4_weights` / `.r4_weight_depth`
        from the bounding box of the currently filtered `.decnav` / `.merged` lines.
        """
        if not self.lines:
            self.refresh_workspace()
        bounds = self._compute_filtered_bounds_wesn()
        if not bounds:
            QMessageBox.warning(
                self,
                "No Navigation Bounds Found",
                "Scan a workspace with .decnav or .merged files first to compute grid bounds.",
            )
            return

        prefix_name = self.grid_prefix_edit.text().strip() or "bransfield_grid"
        try:
            mpp = float(self.grid_mpp_edit.text().strip())
            if mpp <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid Pixel Size", "Pixel size mpp (m) must be a positive number.")
            return

        self.output_dir = _normalize_platform_path(self.out_dir_edit.text()) or DEFAULT_CACHE_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        out_prefix = os.path.join(self.output_dir, prefix_name)

        try:
            hdr = make_blank_grid_from_bounds(
                out_prefix, bounds_wesn=bounds, mpp=mpp, float_flag=True, create_tor4_files=True
            )
        except Exception as exc:
            QMessageBox.warning(self, "Error Creating Blank Grid", str(exc))
            return

        self.edhead_inspector.setPlainText(format_edhead_report(hdr))
        self.refresh_workspace()
        self._load_jhc_raster_via_vrt(hdr.filepath)

    def build_r4_8bit_sun_maps(self):
        """
        Run `make_blank` -> `tor4` -> `weigh_grid` -> `r4to8bit -nozero -no255` -> `addSUN`
        on the currently filtered `.merged` lines (or selected lines if rows are highlighted).
        """
        if not self.lines:
            self.refresh_workspace()

        # If specific rows are selected in Tab 1, use those; otherwise use all filtered lines with .merged
        sel_rows = self.lines_table.selectionModel().selectedRows() if self.lines_table.selectionModel() else []
        target_lines: List[LineProcessingStatus] = []
        if sel_rows:
            for r in sel_rows:
                item = self.lines_table.item(r.row(), 1)
                if item:
                    st = item.data(QT_USER_ROLE)
                    if st and st.merged_path and os.path.isfile(st.merged_path):
                        target_lines.append(st)
        if not target_lines:
            target_lines = [
                l for l in self._get_filtered_lines() if l.merged_path and os.path.isfile(l.merged_path)
            ]

        if not target_lines:
            QMessageBox.warning(
                self,
                "No .merged Files Found",
                "No .merged swath files found in the current selection to grid with weigh_grid.",
            )
            return

        prefix_name = self.grid_prefix_edit.text().strip() or "bransfield_grid"
        try:
            mpp = float(self.grid_mpp_edit.text().strip())
            if mpp <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid Pixel Size", "Pixel size mpp (m) must be a positive number.")
            return

        # Compute bounds across target_lines
        ws, es, ss, ns = [], [], [], []
        for l in target_lines:
            if l.bounds_wesn:
                w, e, s, n = l.bounds_wesn
                ws.append(w)
                es.append(e)
                ss.append(s)
                ns.append(n)
        if not ws:
            bounds = self._compute_filtered_bounds_wesn()
        else:
            bounds = (min(ws), max(es), min(ss), max(ns))

        if not bounds:
            QMessageBox.warning(self, "No Bounds", "Could not determine geographic bounding box for lines.")
            return

        self.output_dir = _normalize_platform_path(self.out_dir_edit.text()) or DEFAULT_CACHE_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        out_prefix = os.path.join(self.output_dir, prefix_name)

        # Step 1 & 2: Create .blank + .r4 + .r4_weights + .r4_weight_depth
        hdr = make_blank_grid_from_bounds(
            out_prefix, bounds_wesn=bounds, mpp=mpp, float_flag=True, create_tor4_files=True
        )
        self.edhead_inspector.setPlainText(format_edhead_report(hdr))

        weigh_bin = _find_omg_binary("weigh_grid")
        r4to8bit_bin = _find_omg_binary("r4to8bit")
        addsun_bin = _find_omg_binary("addSUN")

        if not (weigh_bin and r4to8bit_bin and addsun_bin):
            self.refresh_workspace()
            self._load_jhc_raster_via_vrt(hdr.filepath)
            QMessageBox.information(
                self,
                "Blank & .r4 Initialized",
                f"Created {prefix_name}.blank and {prefix_name}.r4 ({hdr.dx} × {hdr.dy} @ {mpp} m).\n\n"
                "Note: Compiled Linux C binaries (weigh_grid, r4to8bit, addSUN) were not found on PATH; "
                "loaded the blank grid into QGIS.",
            )
            return

        merged_args = " ".join(f'"{l.merged_path}"' for l in target_lines[:50])
        pipeline_cmd = (
            f'"{weigh_bin}" "{prefix_name}" {merged_args} && '
            f'"{r4to8bit_bin}" -nozero -no255 "{prefix_name}" && '
            f'"{addsun_bin}" -elev 45 -azi 315 -vert_exag 4.0 "{prefix_name}.r4" "{prefix_name}.sun"'
        )
        self._pending_autoload_rasters = [
            os.path.join(self.output_dir, f"{prefix_name}.r4"),
            os.path.join(self.output_dir, f"{prefix_name}.8bit"),
            os.path.join(self.output_dir, f"{prefix_name}.sun"),
        ]
        self.cmd_input.setText(pipeline_cmd)
        self.run_custom_command()

    def load_selected_line_vert_prof(self):
        st = self._get_selected_line()
        if not st or not st.vert_prof_path or not os.path.isfile(st.vert_prof_path):
            QMessageBox.information(self, "No Water Column Curtain", "Selected line has no .vert_prof file.")
            return
        self._load_jhc_raster_via_vrt(st.vert_prof_path)

    def load_or_update_tracklines_layer(self):
        filtered = self._get_filtered_lines()
        if not self.workspace_dir or not filtered:
            return

        self.output_dir = _normalize_platform_path(self.out_dir_edit.text()) or DEFAULT_CACHE_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        ws_name = os.path.basename(self.workspace_dir.rstrip("/\\"))
        geojson_path = os.path.join(self.output_dir, f"{ws_name}_tracklines.geojson")
        export_tracklines_geojson(filtered, geojson_path, nav_stride=1)

        layer_name = f"OMG Tracklines ({ws_name})"
        existing = QgsProject.instance().mapLayersByName(layer_name)
        if existing:
            for lyr in existing:
                QgsProject.instance().removeMapLayer(lyr.id())

        vlayer = QgsVectorLayer(geojson_path, layer_name, "ogr")
        if not vlayer.isValid():
            return

        color_by_day = self.color_mode_combo.currentText().startswith("Julian Day")
        categories = []
        palette = [
            "#1f78b4", "#33a02c", "#e31a1c", "#ff7f00",
            "#6a3d9a", "#b15928", "#a6cee3", "#b2df8a",
            "#fb9a99", "#fdbf6f", "#cab2d6", "#ffff99",
        ]

        if color_by_day:
            days = sorted({l.subdir for l in filtered})
            for idx, day in enumerate(days):
                sym = _default_line_symbol()
                if sym:
                    sym.setColor(QColor(palette[idx % len(palette)]))
                    sym.setWidth(0.75)
                label = f"Julian Day {day}" if day else "Root"
                categories.append(QgsRendererCategory(day, sym, label))
            renderer = QgsCategorizedSymbolRenderer("subdir", categories)
        else:
            stage_colors = [
                ("COMPLETE (Bathy + WC + Nav + Att + SS)", "#1b7837", 0.8),
                ("COMPLETE (Bathy + Nav + Att + SS)", "#33a02c", 0.8),
                ("BATHY READY (Nav + Att Merged)", "#2166ac", 0.7),
                ("UNPACKED (Pending Att / Ray-Trace)", "#f46d43", 0.6),
                ("UNPACKED (Pending .nav / .orientation)", "#d73027", 0.6),
                ("DECNAV ONLY (Track Overview)", "#762a83", 0.6),
                ("RAW ONLY (Not Unravelled)", "#878787", 0.5),
            ]
            for label, hex_color, width_mm in stage_colors:
                sym = _default_line_symbol()
                if sym:
                    sym.setColor(QColor(hex_color))
                    sym.setWidth(width_mm)
                categories.append(QgsRendererCategory(label, sym, label))
            renderer = QgsCategorizedSymbolRenderer("stage_summary", categories)

        vlayer.setRenderer(renderer)
        QgsProject.instance().addMapLayer(vlayer)
        if self.iface and self.iface.mapCanvas():
            self.iface.mapCanvas().setExtent(vlayer.extent())
            self.iface.mapCanvas().refresh()

    def load_selected_raster_in_qgis(self):
        rows = self.rasters_table.selectionModel().selectedRows()
        if not rows:
            return
        idx = rows[0].row()
        if idx < 0 or idx >= len(self.rasters):
            return
        hdr = self.rasters[idx]
        self._load_jhc_raster_via_vrt(hdr.filepath)

    def browse_and_load_single_raster(self):
        fpath, _ = QFileDialog.getOpenFileName(
            self,
            "Select OMG Raster (.blank, .r4, .8bit, .sun, .mos, .vert_prof, .weight)",
            self.output_dir if os.path.isdir(self.output_dir) else (self.workspace_dir or os.path.expanduser("~")),
            "OMG Rasters (*.blank *.r4 *.sun* *.8bit *.mos *.vert_prof *.weight);;All Files (*)",
        )
        if fpath:
            self._load_jhc_raster_via_vrt(fpath)

    def _load_jhc_raster_via_vrt(self, filepath: str):
        self.output_dir = _normalize_platform_path(self.out_dir_edit.text()) or DEFAULT_CACHE_DIR
        try:
            hdr = parse_jhc_header(filepath)
            vrt_path = create_gdal_vrt_for_jhc(filepath, output_dir=self.output_dir)
        except Exception as exc:
            QMessageBox.warning(self, "Error Reading OMG1 Raster", str(exc))
            return

        self.edhead_inspector.setPlainText(format_edhead_report(hdr))

        layer_name = os.path.basename(filepath)
        existing = QgsProject.instance().mapLayersByName(layer_name)
        if existing:
            for lyr in existing:
                QgsProject.instance().removeMapLayer(lyr.id())

        rlayer = QgsRasterLayer(vrt_path, layer_name, "gdal")
        if not rlayer.isValid():
            QMessageBox.warning(self, "GDAL Load Error", f"Could not load VRT {vrt_path}")
            return

        # Style Float32 bathymetry (.r4) with pseudocolor depth ramp
        if hdr.data_type == 3:
            zmin, zmax = hdr.min_value, hdr.max_value
            if zmax <= zmin or (zmin == 0.0 and zmax == 0.0):
                try:
                    stats = rlayer.dataProvider().bandStatistics(1)
                    if stats and stats.maximumValue > stats.minimumValue:
                        zmin, zmax = float(stats.minimumValue), float(stats.maximumValue)
                except Exception:
                    pass
            if zmax > zmin:
                shader = QgsRasterShader()
                color_ramp = QgsColorRampShader()
                color_ramp.setColorRampType(RAMP_INTERPOLATED)
                span = max(0.01, zmax - zmin)
                items = [
                    QgsColorRampShader.ColorRampItem(zmin, QColor("#2b83ba"), f"{zmin:.1f} m"),
                    QgsColorRampShader.ColorRampItem(zmin + 0.25 * span, QColor("#abdda4"), f"{zmin + 0.25 * span:.1f} m"),
                    QgsColorRampShader.ColorRampItem(zmin + 0.50 * span, QColor("#ffffbf"), f"{zmin + 0.50 * span:.1f} m"),
                    QgsColorRampShader.ColorRampItem(zmin + 0.75 * span, QColor("#fdae61"), f"{zmin + 0.75 * span:.1f} m"),
                    QgsColorRampShader.ColorRampItem(zmax, QColor("#d7191c"), f"{zmax:.1f} m"),
                ]
                color_ramp.setColorRampItemList(items)
                shader.setRasterShaderFunction(color_ramp)
                renderer = QgsSingleBandPseudoColorRenderer(rlayer.dataProvider(), 1, shader)
                rlayer.setRenderer(renderer)

        QgsProject.instance().addMapLayer(rlayer)

    def run_custom_command(self):
        cmd = self.cmd_input.text().strip()
        if not cmd:
            return
        self.output_dir = _normalize_platform_path(self.out_dir_edit.text()) or DEFAULT_CACHE_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        self.cmd_log.appendPlainText(f"\n$ (cd {self.output_dir} && {cmd})")

        self.proc = QProcess(self)
        self.proc.setWorkingDirectory(self.output_dir)
        self.proc.setProcessChannelMode(PROC_MERGED_CHANNELS)
        self.proc.readyReadStandardOutput.connect(
            lambda: self.cmd_log.appendPlainText(
                bytes(self.proc.readAllStandardOutput()).decode("utf-8", errors="replace").rstrip()
            )
        )
        self.proc.finished.connect(self._on_process_finished)
        if os.name == "nt":
            self.proc.start("cmd.exe", ["/c", cmd])
        else:
            env_prefix = "export PATH=\"/home/iwc/local/linux/bin:$HOME/local/linux/bin:$PATH\"; "
            self.proc.start("bash", ["-c", env_prefix + cmd])

    def _on_process_finished(self, exit_code: int, _exit_status):
        self.cmd_log.appendPlainText(f"[Process finished with exit code {exit_code}]")
        self.refresh_workspace()
        if exit_code == 0 and self._pending_autoload_rasters:
            to_load = list(self._pending_autoload_rasters)
            self._pending_autoload_rasters.clear()
            for rpath in to_load:
                if os.path.isfile(rpath):
                    self._load_jhc_raster_via_vrt(rpath)
