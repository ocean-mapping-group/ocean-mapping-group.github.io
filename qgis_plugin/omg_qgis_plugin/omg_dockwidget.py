"""
Qimera / CARIS HIPS-style Dockable Map & Processing Monitor Widget for QGIS.

Provides:
  1. Survey Line Processing Status Table (Raw -> WC -> Merged -> Nav -> DecNav -> Att -> SVP -> SS)
     with live file-system watcher that auto-refreshes tracklines and grids as background scripts run.
  2. Zero-Copy OMG1 Raster Loader (.r4, .sun, .8bit, .mos, .weight) via GDAL VRTRawRasterBand sidecars
     with automatic pseudocolor bathymetry, hillshade blending, and backscatter styling.
  3. Interactive Inspector for .param vessel lever-arm offsets and .sv_filtered sound velocity casts.
  4. Integrated Command Runner (QProcess) to execute tor4, addSUN, r4to8bit, mos2, swathed -locate, and jview.
"""

import os
from typing import List, Optional

from qgis.PyQt.QtCore import Qt, QProcess, QTimer, QFileSystemWatcher, QVariant
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
    QgsStyle,
    QgsRectangle,
)

from .omg_binary_io import (
    JhcHeaderInfo,
    LineProcessingStatus,
    create_gdal_vrt_for_jhc,
    export_tracklines_geojson,
    parse_jhc_header,
    parse_omg_param,
    scan_survey_workspace,
)


class OmgMonitorDockWidget(QDockWidget):
    """Qimera / HIPS-style dockable workspace monitor and raster manager for OMG."""

    def __init__(self, iface, parent=None):
        super().__init__("OMG Multibeam Survey & Processing Monitor", parent)
        self.iface = iface
        self.setObjectName("OmgMonitorDockWidget")
        self.workspace_dir: str = ""
        self.lines: List[LineProcessingStatus] = []
        self.rasters: List[JhcHeaderInfo] = []
        self.proc: Optional[QProcess] = None

        self.fs_watcher = QFileSystemWatcher(self)
        self.fs_watcher.directoryChanged.connect(self._on_directory_changed)

        self.debounce_timer = QTimer(self)
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.setInterval(1200)
        self.debounce_timer.timeout.connect(self.refresh_workspace)

        self._init_ui()

    def _init_ui(self):
        container = QWidget(self)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(6, 6, 6, 6)

        # Top workspace selector bar
        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("Survey Workspace:"))
        self.ws_edit = QLineEdit()
        self.ws_edit.setPlaceholderText("/path/to/survey_project (containing raw/, merged/, decnav/, ss/)")
        top_bar.addWidget(self.ws_edit, 1)

        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_workspace)
        top_bar.addWidget(browse_btn)

        refresh_btn = QPushButton("Scan / Refresh")
        refresh_btn.clicked.connect(self.refresh_workspace)
        top_bar.addWidget(refresh_btn)

        self.watch_cb = QCheckBox("Live Auto-Refresh")
        self.watch_cb.setChecked(True)
        self.watch_cb.setToolTip(
            "Automatically watch raw/, merged/, decnav/, ss/ and refresh QGIS layers as unravel/gridding scripts run."
        )
        top_bar.addWidget(self.watch_cb)
        main_layout.addLayout(top_bar)

        # Tabs: 1. Survey Lines & Pipeline Status, 2. Grids & Mosaics (.r4/.sun/.8bit/.mos), 3. Run OMG Tools & QC
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
        self.status_summary_lbl = QLabel("No workspace loaded.")
        btn_bar.addWidget(self.status_summary_lbl, 1)

        load_tracks_btn = QPushButton("Update Tracklines Layer on Map")
        load_tracks_btn.clicked.connect(self.load_or_update_tracklines_layer)
        btn_bar.addWidget(load_tracks_btn)
        upper_layout.addLayout(btn_bar)

        cols = [
            "Survey Line",
            "Stage",
            "Raw",
            "WC",
            ".merged",
            ".nav",
            "decnav",
            ".orient",
            "SVP",
            "deTVG",
            ".ss",
            "Pings",
            "Beams",
            "Depth (m)",
        ]
        self.lines_table = QTableWidget(0, len(cols))
        self.lines_table.setHorizontalHeaderLabels(cols)
        self.lines_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.lines_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.lines_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.lines_table.itemSelectionChanged.connect(self._on_line_selected)
        upper_layout.addWidget(self.lines_table, 1)

        splitter.addWidget(upper_widget)

        # Lower: .param Lever Arms & .sv_filtered SVP Cast Inspector
        lower_widget = QWidget()
        lower_layout = QHBoxLayout(lower_widget)
        lower_layout.setContentsMargins(0, 0, 0, 0)

        self.param_inspector = QPlainTextEdit()
        self.param_inspector.setReadOnly(True)
        self.param_inspector.setFont(QFont("Monospace", 9))
        self.param_inspector.setPlaceholderText("Select a survey line above to inspect its .param lever arms...")
        lower_layout.addWidget(self.param_inspector, 1)

        self.svp_inspector = QPlainTextEdit()
        self.svp_inspector.setReadOnly(True)
        self.svp_inspector.setFont(QFont("Monospace", 9))
        self.svp_inspector.setPlaceholderText("Select a survey line above to inspect its .sv_filtered cast...")
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
            QLabel("Discovered OMG1 Rasters (.r4, .sun, .8bit, .mos, .weight) — Loaded Zero-Copy via GDAL VRT:")
        )
        top_bar.addStretch(1)

        load_selected_btn = QPushButton("Load Selected Raster in QGIS")
        load_selected_btn.clicked.connect(self.load_selected_raster_in_qgis)
        top_bar.addWidget(load_selected_btn)

        load_any_btn = QPushButton("Open Any .r4 / .sun / .8bit / .mos File...")
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
                "getBounds -nav merged/*.merged",
                "make_blank area -float -Dx 5.0 -Dy 5.0 -boundsof -nav merged/*.merged",
                "tor4 area 2.0 merged/*.merged",
                "r4to8bit -in area.r4",
                "addSUN area.r4 area.sun 315 35 4",
                "swathed -locate area.r4 merged/*.merged",
                "jview -sun area.8bit area.sun area.r4",
                "make_blank area_mos -8bit -prime 255 -Dx 1.0 -Dy 1.0 -boundsof -nav merged/*.merged",
                "mos2 -in area_mos.mos -ran area_mos.ran -smf 1.5 -weight_by_dist -swap_dirs ss/ merged/ -files ss/*.ss",
            ]
        )
        self.preset_combo.currentTextChanged.connect(lambda txt: self.cmd_input.setText(txt))
        cmd_bar.addWidget(self.preset_combo, 1)
        layout.addLayout(cmd_bar)

        exec_bar = QHBoxLayout()
        exec_bar.addWidget(QLabel("Command:"))
        self.cmd_input = QLineEdit(self.preset_combo.currentText())
        exec_bar.addWidget(self.cmd_input, 1)

        run_btn = QPushButton("Run in Workspace")
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
        if not self.workspace_dir or not os.path.isdir(self.workspace_dir):
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
        self._update_watched_dirs()

        self.lines, self.rasters = scan_survey_workspace(self.workspace_dir)
        self._populate_lines_table()
        self._populate_rasters_table()

        total = len(self.lines)
        n_merged = sum(1 for l in self.lines if l.has_merged)
        n_nav = sum(1 for l in self.lines if l.has_decnav)
        n_att = sum(1 for l in self.lines if l.has_orientation_active)
        n_ss = sum(1 for l in self.lines if l.has_ss_gloria)
        self.status_summary_lbl.setText(
            f"Lines: {total} | Unpacked (.merged): {n_merged}/{total} | "
            f"DecNav: {n_nav}/{total} | Attitude: {n_att}/{total} | "
            f"Sidescan (.ss): {n_ss}/{total} | Rasters: {len(self.rasters)}"
        )

    def _populate_lines_table(self):
        self.lines_table.setRowCount(len(self.lines))
        for row, st in enumerate(self.lines):
            def chk(val: bool) -> QTableWidgetItem:
                it = QTableWidgetItem("✔" if val else "—")
                it.setTextAlignment(Qt.AlignCenter)
                it.setForeground(QColor("#1b7837") if val else QColor("#999999"))
                return it

            name_it = QTableWidgetItem(st.line_name)
            stage_it = QTableWidgetItem(st.stage_summary)
            if st.stage_summary.startswith("COMPLETE"):
                stage_it.setBackground(QColor("#d9f0d3"))
            elif st.stage_summary.startswith("BATHY READY"):
                stage_it.setBackground(QColor("#e7d4e8"))
            elif st.stage_summary.startswith("UNPACKED"):
                stage_it.setBackground(QColor("#fee0b6"))
            else:
                stage_it.setBackground(QColor("#f7f7f7"))

            self.lines_table.setItem(row, 0, name_it)
            self.lines_table.setItem(row, 1, stage_it)
            self.lines_table.setItem(row, 2, chk(st.has_raw_kmall or st.has_raw_all))
            self.lines_table.setItem(row, 3, chk(st.has_watercol or st.has_raw_kmwcd or st.has_raw_wcd))
            self.lines_table.setItem(row, 4, chk(st.has_merged))
            self.lines_table.setItem(row, 5, chk(st.has_nav_active or st.has_nav_1))
            self.lines_table.setItem(row, 6, chk(st.has_decnav))
            self.lines_table.setItem(
                row, 7, chk(st.has_orientation_active or st.has_net_att_2 or st.has_net_att_1 or st.has_orientation_1)
            )
            self.lines_table.setItem(row, 8, chk(st.has_sv_filtered))
            self.lines_table.setItem(row, 9, chk(st.has_ss_detvg))
            self.lines_table.setItem(row, 10, chk(st.has_ss_gloria))
            self.lines_table.setItem(row, 11, QTableWidgetItem(str(st.num_pings) if st.num_pings else "—"))
            self.lines_table.setItem(row, 12, QTableWidgetItem(str(st.num_beams) if st.num_beams else "—"))
            depth_str = f"{st.min_depth_m:.1f} – {st.max_depth_m:.1f}" if st.max_depth_m > 0 else "—"
            self.lines_table.setItem(row, 13, QTableWidgetItem(depth_str))

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

    def _on_line_selected(self):
        rows = self.lines_table.selectionModel().selectedRows()
        if not rows:
            return
        idx = rows[0].row()
        if idx < 0 or idx >= len(self.lines):
            return
        st = self.lines[idx]

        # 1. Populate .param inspector
        if st.param_path and os.path.isfile(st.param_path):
            params = parse_omg_param(st.param_path)
            lines_txt = [f"=== {os.path.basename(st.param_path)} Lever Arms ==="]
            for k, v in params.items():
                lines_txt.append(f"{k:<18} : {v}")
            self.param_inspector.setPlainText("\n".join(lines_txt))
        else:
            self.param_inspector.setPlainText(f"No .param file found for {st.line_name}")

        # 2. Populate .sv_filtered inspector
        sv_path = os.path.join(self.workspace_dir, "merged", f"{st.line_name}.sv_filtered")
        if os.path.isfile(sv_path):
            with open(sv_path, "r", encoding="utf-8", errors="replace") as f:
                sv_txt = f.read(4096)
            self.svp_inspector.setPlainText(f"=== {st.line_name}.sv_filtered (Depth_m  SV_m/s) ===\n{sv_txt}")
        else:
            self.svp_inspector.setPlainText(f"No .sv_filtered file found for {st.line_name}")

        # 3. Zoom map canvas to selected line bounds if valid
        if st.bounds_wesn and self.iface and self.iface.mapCanvas():
            w, e, s, n = st.bounds_wesn
            if -180.0 <= w < e <= 180.0 and -90.0 <= s < n <= 90.0:
                rect = QgsRectangle(w, s, e, n)
                rect.scale(1.25)
                self.iface.mapCanvas().setExtent(rect)
                self.iface.mapCanvas().refresh()

    def load_or_update_tracklines_layer(self):
        if not self.workspace_dir or not self.lines:
            return
        geojson_path = os.path.join(self.workspace_dir, "omg_survey_tracklines.geojson")
        export_tracklines_geojson(self.lines, geojson_path, nav_stride=10)

        layer_name = "OMG Survey Tracklines (By Stage)"
        existing = QgsProject.instance().mapLayersByName(layer_name)
        if existing:
            for lyr in existing:
                lyr.dataProvider().reloadData()
                lyr.triggerRepaint()
            return

        vlayer = QgsVectorLayer(geojson_path, layer_name, "ogr")
        if not vlayer.isValid():
            return

        # Apply Qimera/HIPS-style categorized color symbology by stage_summary
        categories = []
        stage_colors = [
            ("COMPLETE (Bathy + Nav + Att + SS)", "#1b7837", 0.8),
            ("BATHY READY (Nav + Att Merged)", "#2166ac", 0.7),
            ("UNPACKED (Pending Att / Ray-Trace)", "#f46d43", 0.6),
            ("UNPACKED (Pending .nav / .orientation Copy)", "#d73027", 0.6),
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
            "Select OMG Raster (.r4, .sun, .8bit, .mos, .weight)",
            self.workspace_dir or os.path.expanduser("~"),
            "OMG Rasters (*.r4 *.sun* *.8bit *.mos *.weight *.blank);;All Files (*)",
        )
        if fpath:
            self._load_jhc_raster_via_vrt(fpath)

    def _load_jhc_raster_via_vrt(self, filepath: str):
        try:
            hdr = parse_jhc_header(filepath)
            vrt_path = create_gdal_vrt_for_jhc(filepath)
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

        # Style 32-bit float .r4 bathymetric grids with a Spectral / Turbo pseudocolor ramp
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
        workdir = self.workspace_dir if (self.workspace_dir and os.path.isdir(self.workspace_dir)) else os.getcwd()
        self.cmd_log.appendPlainText(f"\n$ (cd {workdir} && {cmd})")

        self.proc = QProcess(self)
        self.proc.setWorkingDirectory(workdir)
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
        self.refresh_workspace()
