---
layout: default
title: EK_funcs (Internal Functions for EKlook)
parent: EKlook Tools
nav_order: 110
---
# EK_funcs (Internal Functions for EKlook)

## Description
`EK_funcs.c` is a collection of internal helper functions primarily used by the interactive `EKlook` application and its associated command-line utilities (like `BatchProcEK` and `comboCalibEK_ARCs`). These functions handle the low-level tasks of reading, processing, and managing EK series echosounder data, particularly focusing on matched-filtered traces. They provide the core computational and data management logic, supporting various aspects of EK data analysis such as backdrop and area loading, target strength processing, trace file handling, coordinate projections, bottom strike localization, ensonified area calculations, and angular response curve (ARC) management.

This module is not a standalone executable; its functions are called internally by other `EKlook` components.

## Functions

### `float get_Mean_SphereTS_in_Bandwidth()`
Calculates the average Target Strength (TS) of a theoretical sphere within the pulse bandwidth.
*   **Purpose:** Used for calibration and comparison against measured target strengths.

### `void load_Backdrop()`
Loads an 8-bit JHC image file to be used as a geographic backdrop in the `EKlook` application.
*   **Purpose:** Provides spatial context for plotted data. It also downsamples the image to fit into the display area.

### `void load_Areas()`
Loads geographic area definition files (e.g., map sheets) into memory.
*   **Purpose:** Used for spatial filtering or defining regions of interest within `EKlook`.

### `void proj_Areas()`
Projects the corner coordinates of loaded geographic areas into a local pseudo-Cartesian coordinate system.
*   **Purpose:** Prepares area boundaries for display and spatial checks within `EKlook`'s geographic views.

### `void read_sphereTS()`
Reads a sphere Target Strength (TS) vs. frequency file.
*   **Purpose:** Loads reference TS data for comparison and spectral analysis within `EKlook`. It also calculates the spectral gradient.

### `void read_relevant_tracefiles(int forEKlook)`
Orchestrates the loading of various EK trace data files (Raw dB, MF dB, PS phase, FA phase, MF IQ) and associated merged and orientation files.
*   **Purpose:** Prepares all necessary data streams for processing and display in `EKlook` or related utilities.

### `int ekload_MatchedFilter()`
Loads the matched filter pulse characteristics from a `.pulse` file.
*   **Purpose:** Initializes parameters related to the matched filter, including size, frequency range, power, and transducer depth. It also calculates the matched filter's autocorrelation and normalization factors.

### `int calc_AvAtten()`
Calculates the average attenuation coefficient (dB/km) for the center frequency of the matched filter pulse.
*   **Purpose:** Used for propagation loss corrections in backscatter calculations, based on water temperature, salinity, depth, and pH.

### `int ekload_BottomTrackGuide()`
Loads previously defined bottom tracking parameters (e.g., min/max target depth, mount angles) from a `.BottomTrackGuide` file.
*   **Purpose:** Configures `EKlook`'s bottom detection algorithms with custom or saved settings.

### `int ekload_AllocTraces_Build_TL(int forEKlook)`
Allocates memory for all trace data arrays (e.g., `power`, `powermatch`, `angPS`, `angFA`, `sumtrace`) and pre-calculates Transmission Loss (TL) arrays.
*   **Purpose:** Prepares the data structures for storing and processing raw and matched-filtered EK traces. Validates consistency of trace file headers.

### `int ekload_Trace_Raw_dB()`
Loads the pre-matched filtered logarithmic intensity envelope data from a `.Raw_dB` file.
*   **Purpose:** Provides access to the raw (unfiltered) acoustic intensity traces.

### `int ekload_Trace_MF_dB(int forEKlook)`
Loads the matched-filtered logarithmic intensity envelope data from a `.MF_dB` file.
*   **Purpose:** Provides the primary processed intensity traces. It also applies forgotten normalization factors and performs a low-pass filter (`lowpassPM`) on the data, and builds a histogram for display optimization.

### `int ekload_Trace_ping_Params()`
Loads ping parameters (e.g., valid sample count per trace, bottom track bounds flags) from a `.ping_Params` file.
*   **Purpose:** Provides metadata about each ping's data extent and quality, supporting dynamic adjustment of processing windows. If the file doesn't exist, it creates one with default parameters.

### `int ekload_Trace_PS_phase(int forEKlook)`
Loads port-starboard phase angle data from a `.PS_phase` file.
*   **Purpose:** Provides data for across-track angle estimation from phase differences.

### `int ekload_Trace_FA_phase(int forEKlook)`
Loads fore-aft phase angle data from a `.FA_phase` file.
*   **Purpose:** Provides data for along-track angle estimation from phase differences.

### `int ekload_Trace_MF_IQ(int forEKlook)`
Loads complex (In-phase and Quadrature - IQ) matched-filtered trace data from a `.MF_IQ` file.
*   **Purpose:** Provides access to the raw complex signal for advanced processing (e.g., FFT, phase detection). It also calculates magnitudes (`magtrace`) for quick access.

### `int ekload_MergedFile()`
Loads navigation and orientation data from the associated OMG-HDCS `.merged` file.
*   **Purpose:** Extracts ping-specific metadata such as time, geographic location, vessel attitude (roll, pitch, heave, heading), and various sonar settings (pulse form, frequency, bandwidth). It also calculates track bounds and converts geographic coordinates to local Cartesian coordinates.

### `int ekload_Orientation()`
Loads asynchronous orientation data (roll, pitch, heave, heading) from a `.orientation` file (e.g., from an MRU0 sensor).
*   **Purpose:** Provides high-rate motion data for motion compensation and comparison with internal sonar attitude. It calculates average sample rates and bounds for motion parameters.

### `int ekload_OtherOrientation()`
Loads asynchronous orientation data from a secondary source, typically a `.POS_orient` file (e.g., from a POS MV system).
*   **Purpose:** Provides an alternative motion data stream for comparison or use in processing, supporting latency analysis.

### `int freetraces_for_NextFile()`
Frees dynamically allocated memory for all loaded trace data and related structures.
*   **Purpose:** Cleans up memory before loading a new set of data files.

### `float proj_lalo_m(double cenlat, double cenlon, PosOrient *aNav)`
Projects geographic coordinates (latitude, longitude) into a local Cartesian (meters East, meters North) coordinate system relative to a central latitude and longitude.
*   **Purpose:** Simplifies spatial calculations by converting spherical coordinates to planar approximations.

### `float proj_m_lalo(double cenlat, double cenlon, PosOrient *aNav, Polar_Target *target)`
Performs the inverse projection, converting local Cartesian coordinates (meters East, meters North) back to geographic coordinates (latitude, longitude).
*   **Purpose:** Determines the geographic location of bottom strikes or other features from their local projected positions.

### `int search_for_Targets()`
Searches for acoustic targets (or bottom detections) within the loaded traces.
*   **Purpose:** Identifies peaks in the filtered power envelope and regresses phase sweeps to refine bottom picks. It also classifies targets based on validity.

### `int isBottomStrikeinArea(int areano, int traceno)`
Checks if a detected bottom strike falls within a specified geographic area.
*   **Purpose:** Filters valid detections based on user-defined spatial regions of interest.

### `int get_TxRxOrientation(int traceno)`
Retrieves and interpolates the vessel's Transmit (Tx) and Receive (Rx) orientation (roll, pitch, heave, heading) for a specific trace.
*   **Purpose:** Ensures accurate attitude data is available for each ping at both transmit and receive times for motion compensation. It prioritizes asynchronous motion data if available.

### `int locate_Bottom_Strike(int traceno)`
Locates the geographic position of the bottom strike for a given trace.
*   **Purpose:** Rotates a nadir beam vector based on mount angles and vessel orientation to determine the beam's position in geographic coordinates (XYZ) and then projects this to latitude/longitude.

### `int locate_Bottom_Footprint(int traceno)`
Simulates and locates the geographic footprint of the sonar beam on the seafloor.
*   **Purpose:** Helps visualize sonar coverage and assess the impact of beamwidth and motion on the insonified area. It plots an outline of the footprint.

### `float calc_Ensonified_Area(float range, float soundspeed, float twowayBWdeg, float effpulselensec, float grazing_angle)`
Calculates the ensonified area on the seafloor for a given sonar beam.
*   **Purpose:** A crucial component for backscatter strength calculations, accounting for geometric spreading and pulse characteristics.

### `void find_Zero_Phase(int trace_no, int start_no, int end_no)`
Analyzes the phase data within an echo envelope to identify zero-phase crossings and regresses a linear fit to the phase sweep.
*   **Purpose:** Refines bottom detection by finding precise phase-derived angles, providing an alternative or complementary method to amplitude-based detection.

### `float calc_BP_rolloff_model(float phaseangle, float nominalF, float thisF)`
Calculates a beam pattern (BP) rolloff model based on a powered cosine function, adjusting for nominal and specific FFT bin frequencies.
*   **Purpose:** Estimates the angular dependence of the beam pattern relative to boresight, used in backscatter correction.

### `float calc_highincid_BP_rolloff_model(float thedBdrop, int totsam, int censam, int thissam)`
Calculates a beam pattern rolloff model for high incidence angles, typically used when phase data is unreliable.
*   **Purpose:** Provides a simplified rolloff model to correct backscatter in regions where phase-based corrections are difficult.

### `int calc3_Incidence(int trace_no)`
Calculates across-track seafloor incidence (grazing) angles.
*   **Purpose:** Determines the angle at which the acoustic pulse hits the seafloor, using either regressed phase information (if valid) or a simplified amplitude-based method. This is fundamental for quantitative backscatter analysis.

### `int calc_Envelope_Ensonified(int trace_no)`
Calculates the ensonified area for each sample in the echo envelope.
*   **Purpose:** Essential for backscatter normalization, accounting for the spread of acoustic energy on the seafloor across the envelope.

### `void find_POLAR_peak(int trace_no, int start_no, int end_no, int whichtrace)`
Locates the peak in the filtered power envelope (matched-filtered or low-pass filtered) within a specified time/sample window.
*   **Purpose:** Identifies the strongest acoustic return, which is typically used as a preliminary bottom or target detection.

### `int calc_EnvWinFFTs(int traceno)`
Calculates Fast Fourier Transforms (FFTs) for multiple overlapping sub-windows within the echo envelope.
*   **Purpose:** Allows for spectral analysis of the echo, to understand frequency-dependent characteristics of the target or bottom. Stacks and normalizes the spectra.

### `int flush_ARC(ARC_combo *thearc)`
Initializes an `ARC_combo` (Angular Response Curve) structure, zeroing out all accumulated sums and counts.
*   **Purpose:** Clears previous ARC data before starting a new accumulation.

### `int add_to_ARC(ARC_combo *thearc, float BSdB, float IncidAngle)`
Adds a backscatter (BS) measurement and its corresponding incidence angle to an `ARC_combo` structure.
*   **Purpose:** Accumulates data points for building an angular response curve. The BS is converted to linear intensity and summed.

### `int reduce_ARC(ARC_combo *thearc)`
Reduces the accumulated data in an `ARC_combo` structure into mean dB values and stores the maximum count for normalization.
*   **Purpose:** Computes the average backscatter strength for each incidence angle bin.

### `int load_BStrack( FILE *file)`
Loads bottom tracking guide parameters from a file (e.g., `min_target_depth`, `max_target_depth`, `MountAnglesRPY`, `NadirDepth`).
*   **Purpose:** Configures the bottom detection algorithm with pre-defined or custom settings.

### `int load_pingParams(FILE *file)`
Loads ping-specific parameters, such as valid sample counts and predicted slant ranges, from a `.ping_Params` file.
*   **Purpose:** Provides metadata for each ping's data extent and allows for dynamic adjustment of processing windows. Includes error handling for corrupted files.

### `int dump_pingParams()`
Dumps the current ping parameters to a `.ping_Params` file.
*   **Purpose:** Saves ping-specific metadata for future use or verification.

### `int dump_BStrack()`
Dumps the current bottom/target tracking guide parameters to a `.BottomTrackGuide` file.
*   **Purpose:** Saves the configuration of the bottom detection algorithm.

### `void init_BOTTOM_variables()`
Initializes various global variables and structures related to bottom detection and ARC processing.
*   **Purpose:** Sets up default values for `EKlook`'s bottom detection features, including `envWinSize` and `EKMountAngle`.

### `int load_ARC(char *name, ARC_combo ARCarray[], int *noarcs)`
Loads 2D Angular Response Curves (ARCs) from an ASCII file.
*   **Purpose:** Reads pre-computed ARCs for use in calibration or comparison.

### `int load_ARC_3D(char *name, ARC_combo ARCarray[], int *noarcs)`
Loads 3D Angular Response Curves (ARCs) from an ASCII file.
*   **Purpose:** Reads more complex ARCs that include frequency-dependent information. (Note: The provided source indicates it only parses, not fully fills the `ARC_combo` yet).

### `int dump_ARC_3D(char *prefix, char *suffix, ARC_combo ARCarray[], int noarcs, float minfrac)`
Dumps 3D Angular Response Curves (ARCs) to an ASCII file.
*   **Purpose:** Saves frequency-dependent ARCs for external analysis or visualization.

### `int dump_ARC(char *prefix, char *suffix, ARC_combo ARCarray[], int noarcs)`
Dumps 2D Angular Response Curves (ARCs) to an ASCII file.
*   **Purpose:** Saves the average backscatter response vs. angle.

### `int stack_all_Envelopes_into_ARC(ARC_combo *thearc, int flushit, int reduceit)`
Iterates through all traces, calculates backscatter and grazing angles for each sample within the echo envelope, and accumulates these into a single `ARC_combo` structure.
*   **Purpose:** Builds a comprehensive angular response curve by stacking data from many pings. Applies various corrections (Area, TL, BP).

### `int stack_all_Broadband_Envelopes_into_ARC(ARC_combo manyarcs[], int flushit, int reduceit)`
Stacks broadband echo envelopes into an array of `ARC_combo` structures, where each `ARC_combo` represents the angular response for a specific frequency bin (or sub-window).
*   **Purpose:** Generates frequency-dependent angular response curves, useful for detailed spectral analysis of the seafloor.

### `int dump_Calib_Values(char *name)`
Dumps calibration values (e.g., Sphere TS, ripple correction) to a file.
*   **Purpose:** Stores intermediate calibration results for debugging or external use.

### `int load_Calib_Values(char *name, float *calfreq, float *calgain, int *nocalvals)`
Loads calibration values (frequency and gain) from a file, filtering for "GOOD" quality entries.
*   **Purpose:** Retrieves pre-determined calibration data to be applied to spectra.
