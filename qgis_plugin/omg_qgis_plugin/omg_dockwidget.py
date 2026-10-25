"""
Qimera / CARIS HIPS-style Dockable Map & Processing Monitor Widget for QGIS.

Supports both flat workspaces and multi-day Julian-Day subdirectory workspaces
(e.g., 2026_Antarctica/OMG_Care2026/02_Bransfield with subdirs 74..81).

Read-Only Master Archive Safety:
  All generated GeoJSON tracklines and GDAL .vrt sidecar files are written to a
  local output/cache directory (defaulting to ~/coding/bransfield_qgis_outputs or
  ~/.cache/omg_qgis_plugin) so master archive drives (such as W:) are never modified.
"""

import os
from typing import List, Optional

from qgis.PyQt.QtCore import Qt, QProcess, QTimer, QFileSystemWatcher
from qgis.PyQt.QtGui import QColor, QFont
from qgis.PyQt.QtWidgets import (
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
    QgsWkbTypes,
    QgsSingleBandPseudoColorRenderer,
    QgsColorRampShader,
    QgsRasterShader,
    QgsRectangle,
)

from .omg_binary_io import (
    JhcHeaderInfo,
    LineProcessingStatus,
    create_gdal_vrt_for_jhc,
    export_tracklines_geojson,
    parse_jhc_header,
    parse_omg_merged_summary,
    parse_omg_param,
    scan_survey_workspace,
)


DEFAULT_CACHE_DIR = (
    "/home/iwc/coding/bransfield_qgis_outputs"
    if os.path.isdir("/home/iwc/coding")
    else os.path.expanduser("~/.cache/omg_qgis_plugin")
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
        self.ws_edit = QLineEdit("/mnt/w/data/2026_Antarctica/OMG_Care2026/02_Bransfield")
        self.ws_edit.setPlaceholderText("/path/to/survey_project (containing raw/, merged/, decnav/, ss/)")
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
        refresh_btn.clicked.connect(self.refresh_workspace)
        top_bar.addWidget(refresh_btn)

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

        splitter = QSplitter(Qt.Vertical)

        # Upper: Qimera/HIPS-style processing stage matrix table
        upper_widget = QWidget()
        upper_layout = QVBoxLayout(upper_widget)
        upper_layout.setContentsMargins(0, 0, 0, 0)

        btn_bar = QHBoxLayout()
        self.status_summary_lbl = QLabel("Click 'Scan Workspace' to load multibeam lines.")
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
        self.lines_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.lines_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.lines_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
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

        top_bar = QHBoxLayout()
        top_bar.addWidget(
            QLabel("Discovered OMG1 Rasters (.r4, .sun, .8bit, .mos, .vert_prof) — Loaded Zero-Copy via GDAL VRT:")
        )
        top_bar.addStretch(1)

        load_selected_btn = QPushButton("Load Selected Raster in QGIS")
        load_selected_btn.clicked.connect(self.load_selected_raster_in_qgis)
        top_bar.addWidget(load_selected_btn)

        load_any_btn = QPushButton("Open Any .r4 / .sun / .8bit / .mos / .vert_prof File...")
        load_any_btn.clicked.connect(self.browse_and_load_single_raster)
        top_bar.addWidget(load_any_btn)
        layout.addLayout(top_bar)

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
        self.rasters_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.rasters_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.rasters_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.rasters_table.horizontalHeader().setSectionResizeMode(8, QHeaderView.Stretch)
        self.rasters_table.itemDoubleClicked.connect(lambda _item: self.load_selected_raster_in_qgis())
        layout.addWidget(self.rasters_table, 1)

        self.tabs.addTab(tab, "2. Grids & Mosaics (.r4 / .sun / .8bit / .mos)")

    def _build_runner_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        cmd_bar = QHBoxLayout()
        cmd_bar.addWidget(QLabel("Quick Action:"))
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(
            [
                "getBounds -nav merged/*/*.merged",
                "make_blank bransfield -float -Dx 25.0 -Dy 25.0 -boundsof -nav merged/*/*.merged",
                "tor4 bransfield 2.0 merged/*/*.merged",
                "r4to8bit -in bransfield.r4",
                "addSUN bransfield.r4 bransfield.sun 315 35 4",
                "swathed -locate bransfield.r4 merged/*/*.merged",
                "jview -sun bransfield.8bit bransfield.sun bransfield.r4",
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
        self.fs_watcher.addPaths(watch_list)

    def refresh_workspace(self):
        ws = self.ws_edit.text().strip()
        if not ws or not os.path.isdir(ws):
            return
        self.workspace_dir = os.path.abspath(ws)
        self.output_dir = self.out_dir_edit.text().strip() or DEFAULT_CACHE_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        self._update_watched_dirs()

        self.lines, self.rasters = scan_survey_workspace(
            self.workspace_dir, read_merged_headers=False, read_decnav_summaries=True
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
            f"WC: {n_wc}/{total} | Att: {n_att}/{total} | .ss: {n_ss}/{total}"
        )

    def _get_filtered_lines(self) -> List[LineProcessingStatus]:
        day_sel = self.day_filter_combo.currentText()
        if not day_sel or day_sel == "All Days":
            return self.lines
        return [l for l in self.lines if l.subdir == day_sel]

    def _apply_table_filter(self):
        self._populate_lines_table()

    def _populate_lines_table(self):
        filtered = self._get_filtered_lines()
        self.lines_table.setRowCount(len(filtered))
        for row, st in enumerate(filtered):
            def chk(val: bool) -> QTableWidgetItem:
                it = QTableWidgetItem("✔" if val else "—")
                it.setTextAlignment(Qt.AlignCenter)
                it.setForeground(QColor("#1b7837") if val else QColor("#999999"))
                return it

            day_it = QTableWidgetItem(st.subdir or "—")
            day_it.setTextAlignment(Qt.AlignCenter)
            name_it = QTableWidgetItem(st.line_name)
            name_it.setData(Qt.UserRole, st)

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

    def _get_selected_line(self) -> Optional[LineProcessingStatus]:
        rows = self.lines_table.selectionModel().selectedRows()
        if not rows:
            return None
        row = rows[0].row()
        name_item = self.lines_table.item(row, 1)
        if not name_item:
            return None
        return name_item.data(Qt.UserRole)

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

        self.output_dir = self.out_dir_edit.text().strip() or DEFAULT_CACHE_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        ws_name = os.path.basename(self.workspace_dir.rstrip("/"))
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
                sym = QgsSymbol.defaultSymbol(QgsWkbTypes.LineGeometry)
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
                sym = QgsSymbol.defaultSymbol(QgsWkbTypes.LineGeometry)
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
            "Select OMG Raster (.r4, .sun, .8bit, .mos, .vert_prof, .weight)",
            self.workspace_dir or os.path.expanduser("~"),
            "OMG Rasters (*.r4 *.sun* *.8bit *.mos *.vert_prof *.weight *.blank);;All Files (*)",
        )
        if fpath:
            self._load_jhc_raster_via_vrt(fpath)

    def _load_jhc_raster_via_vrt(self, filepath: str):
        self.output_dir = self.out_dir_edit.text().strip() or DEFAULT_CACHE_DIR
        try:
            hdr = parse_jhc_header(filepath)
            vrt_path = create_gdal_vrt_for_jhc(filepath, output_dir=self.output_dir)
        except Exception as exc:
            QMessageBox.warning(self, "Error Reading OMG1 Raster", str(exc))
            return

        layer_name = os.path.basename(filepath)
        existing = QgsProject.instance().mapLayersByName(layer_name)
        if existing:
            for lyr in existing:
                lyr.dataProvider().reloadData()
                lyr.triggerRepaint()
            return

        rlayer = QgsRasterLayer(vrt_path, layer_name, "gdal")
        if not rlayer.isValid():
            QMessageBox.warning(self, "GDAL Load Error", f"Could not load VRT {vrt_path}")
            return

        if hdr.data_type == 3 and hdr.max_value > hdr.min_value:
            shader = QgsRasterShader()
            color_ramp = QgsColorRampShader()
            color_ramp.setColorRampType(QgsColorRampShader.Interpolated)
            zmin, zmax = hdr.min_value, hdr.max_value
            span = max(0.01, zmax - zmin)
            items = [
                QgsColorRampShader.ColorRampItem(zmin, QColor("#d7191c"), f"{zmin:.1f} m"),
                QgsColorRampShader.ColorRampItem(zmin + 0.25 * span, QColor("#fdae61"), f"{zmin + 0.25 * span:.1f} m"),
                QgsColorRampShader.ColorRampItem(zmin + 0.50 * span, QColor("#ffffbf"), f"{zmin + 0.50 * span:.1f} m"),
                QgsColorRampShader.ColorRampItem(zmin + 0.75 * span, QColor("#abdda4"), f"{zmin + 0.75 * span:.1f} m"),
                QgsColorRampShader.ColorRampItem(zmax, QColor("#2b83ba"), f"{zmax:.1f} m"),
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
        self.output_dir = self.out_dir_edit.text().strip() or DEFAULT_CACHE_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        self.cmd_log.appendPlainText(f"\n$ (cd {self.output_dir} && {cmd})")

        self.proc = QProcess(self)
        self.proc.setWorkingDirectory(self.output_dir)
        self.proc.setProcessChannelMode(QProcess.MergedChannels)
        self.proc.readyReadStandardOutput.connect(
            lambda: self.cmd_log.appendPlainText(
                bytes(self.proc.readAllStandardOutput()).decode("utf-8", errors="replace").rstrip()
            )
        )
        self.proc.finished.connect(self._on_process_finished)
        self.proc.start("bash", ["-c", cmd])

    def _on_process_finished(self, exit_code: int, _exit_status):
        self.cmd_log.appendPlainText(f"[Process finished with exit code {exit_code}]")
