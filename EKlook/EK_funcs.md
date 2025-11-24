---
layout: default
title: EK_funcs (Internal Functions for EKlook)
parent: EKlook Tools
nav_order: 10
---
# EK_funcs (Internal Functions for EKlook)

## Description
`EK_funcs.c` is a collection of internal helper functions primarily used by the interactive `EKlook` application and its associated command-line utilities (like `BatchProcEK` and `comboCalibEK_ARCs`). These functions handle the low-level tasks of reading, processing, and managing EK series echosounder data, particularly focusing on matched-filtered traces. They provide the core computational and data management logic, supporting various aspects of EK data analysis such as backdrop and area loading, target strength processing, trace file handling, coordinate projections, bottom strike localization, ensonified area calculations, and angular response curve (ARC) management.

This module is not a standalone executable; its functions are called internally by other `EKlook` components.

## Functions

*   `float get_Mean_SphereTS_in_Bandwidth()`: Calculates the average Target Strength (TS) of a theoretical sphere within the pulse bandwidth. Used for calibration and comparison against measured target strengths.
*   `void load_Backdrop()`: Loads an 8-bit JHC image file to be used as a geographic backdrop in the `EKlook` application. Provides spatial context for plotted data and downsamples the image.
*   `void load_Areas()`: Loads geographic area definition files (e.g., map sheets) into memory. Used for spatial filtering or defining regions of interest within `EKlook`.
*   `void proj_Areas()`: Projects the corner coordinates of loaded geographic areas into a local pseudo-Cartesian coordinate system. Prepares area boundaries for display and spatial checks within `EKlook`'s geographic views.
*   `void read_sphereTS()`: Reads a sphere Target Strength (TS) vs. frequency file. Loads reference TS data for comparison and spectral analysis and calculates the spectral gradient.
*   `void read_relevant_tracefiles(int forEKlook)`: Orchestrates the loading of various EK trace data files (Raw dB, MF dB, PS phase, FA phase, MF IQ) and associated merged and orientation files. Prepares all necessary data streams for processing and display.
*   `int ekload_MatchedFilter()`: Loads the matched filter pulse characteristics from a `.pulse` file. Initializes parameters related to the matched filter, including size, frequency range, power, and transducer depth. Calculates the matched filter's autocorrelation and normalization factors.
*   `int calc_AvAtten()`: Calculates the average attenuation coefficient (dB/km) for the center frequency of the matched filter pulse. Used for propagation loss corrections in backscatter calculations.
*   `int ekload_BottomTrackGuide()`: Loads previously defined bottom tracking parameters from a `.BottomTrackGuide` file. Configures `EKlook`'s bottom detection algorithms with custom or saved settings.
*   `int ekload_AllocTraces_Build_TL(int forEKlook)`: Allocates memory for all trace data arrays and pre-calculates Transmission Loss (TL) arrays. Prepares data structures for storing and processing raw and matched-filtered EK traces.
*   `int ekload_Trace_Raw_dB()`: Loads the pre-matched filtered logarithmic intensity envelope data from a `.Raw_dB` file. Provides access to the raw (unfiltered) acoustic intensity traces.
*   `int ekload_Trace_MF_dB(int forEKlook)`: Loads the matched-filtered logarithmic intensity envelope data from a `.MF_dB` file. Provides the primary processed intensity traces and performs low-pass filtering.
*   `int ekload_Trace_ping_Params()`: Loads ping parameters (e.g., valid sample count per trace, bottom track bounds flags) from a `.ping_Params` file. Provides metadata about each ping's data extent and quality.
*   `int ekload_Trace_PS_phase(int forEKlook)`: Loads port-starboard phase angle data from a `.PS_phase` file. Provides data for across-track angle estimation from phase differences.
*   `int ekload_Trace_FA_phase(int forEKlook)`: Loads fore-aft phase angle data from a `.FA_phase` file. Provides data for along-track angle estimation from phase differences.
*   `int ekload_Trace_MF_IQ(int forEKlook)`: Loads complex (In-phase and Quadrature - IQ) matched-filtered trace data from a `.MF_IQ` file. Provides access to the raw complex signal for advanced processing.
*   `int ekload_MergedFile()`: Loads navigation and orientation data from the associated OMG-HDCS `.merged` file. Extracts ping-specific metadata such as time, geographic location, vessel attitude, and sonar settings.
*   `int ekload_Orientation()`: Loads asynchronous orientation data from a `.orientation` file. Provides high-rate motion data for motion compensation.
*   `int ekload_OtherOrientation()`: Loads asynchronous orientation data from a secondary source (e.g., `.POS_orient` file). Provides an alternative motion data stream.
*   `int freetraces_for_NextFile()`: Frees dynamically allocated memory for all loaded trace data and related structures. Cleans up memory before loading a new set of data files.
*   `float proj_lalo_m(double cenlat, double cenlon, PosOrient *aNav)`: Projects geographic coordinates (latitude, longitude) into a local Cartesian coordinate system.
*   `float proj_m_lalo(double cenlat, double cenlon, PosOrient *aNav, Polar_Target *target)`: Performs the inverse projection, converting local Cartesian coordinates back to geographic coordinates.
*   `int search_for_Targets()`: Searches for acoustic targets (or bottom detections) within the loaded traces. Identifies peaks and regresses phase sweeps.
*   `int isBottomStrikeinArea(int areano, int traceno)`: Checks if a detected bottom strike falls within a specified geographic area.
*   `int get_TxRxOrientation(int traceno)`: Retrieves and interpolates the vessel's Transmit (Tx) and Receive (Rx) orientation for a specific trace.
*   `int locate_Bottom_Strike(int traceno)`: Locates the geographic position of the bottom strike for a given trace.
*   `int locate_Bottom_Footprint(int traceno)`: Simulates and locates the geographic footprint of the sonar beam on the seafloor.
*   `float calc_Ensonified_Area(float range, float soundspeed, float twowayBWdeg, float effpulselensec, float grazing_angle)`: Calculates the ensonified area on the seafloor for a given sonar beam.
*   `void find_Zero_Phase(int trace_no, int start_no, int end_no)`: Analyzes the phase data within an echo envelope to identify zero-phase crossings.
*   `float calc_BP_rolloff_model(float phaseangle, float nominalF, float thisF)`: Calculates a beam pattern (BP) rolloff model based on a powered cosine function.
*   `float calc_highincid_BP_rolloff_model(float thedBdrop, int totsam, int censam, int thissam)`: Calculates a beam pattern rolloff model for high incidence angles.
*   `int calc3_Incidence(int trace_no)`: Calculates across-track seafloor incidence (grazing) angles.
*   `int calc_Envelope_Ensonified(int trace_no)`: Calculates the ensonified area for each sample in the echo envelope.
*   `void find_POLAR_peak(int trace_no, int start_no, int end_no, int whichtrace)`: Locates the peak in the filtered power envelope within a specified time/sample window.
*   `int calc_EnvWinFFTs(int traceno)`: Calculates Fast Fourier Transforms (FFTs) for multiple overlapping sub-windows within the echo envelope.
*   `int flush_ARC(ARC_combo *thearc)`: Initializes an `ARC_combo` (Angular Response Curve) structure.
*   `int add_to_ARC(ARC_combo *thearc, float BSdB, float IncidAngle)`: Adds a backscatter (BS) measurement and its corresponding incidence angle to an `ARC_combo` structure.
*   `int reduce_ARC(ARC_combo *thearc)`: Reduces the accumulated data in an `ARC_combo` structure into mean dB values.
*   `int load_BStrack( FILE *file)`: Loads bottom tracking guide parameters from a file.
*   `int load_pingParams(FILE *file)`: Loads ping-specific parameters from a `.ping_Params` file.
*   `int dump_pingParams()`: Dumps the current ping parameters to a `.ping_Params` file.
*   `int dump_BStrack()`: Dumps the current bottom/target tracking guide parameters to a `.BottomTrackGuide` file.
*   `void init_BOTTOM_variables()`: Initializes various global variables and structures related to bottom detection and ARC processing.
*   `int load_ARC(char *name, ARC_combo ARCarray[], int *noarcs)`: Loads 2D Angular Response Curves (ARCs) from an ASCII file.
*   `int load_ARC_3D(char *name, ARC_combo ARCarray[], int *noarcs)`: Loads 3D Angular Response Curves (ARCs) from an ASCII file.
*   `int dump_ARC_3D(char *prefix, char *suffix, ARC_combo ARCarray[], int noarcs, float minfrac)`: Dumps 3D Angular Response Curves (ARCs) to an ASCII file.
*   `int dump_ARC(char *prefix, char *suffix, ARC_combo ARCarray[], int noarcs)`: Dumps 2D Angular Response Curves (ARCs) to an ASCII file.
*   `int stack_all_Envelopes_into_ARC(ARC_combo *thearc, int flushit, int reduceit)`: Iterates through all traces, calculates backscatter and grazing angles, and accumulates them into a single `ARC_combo` structure.
*   `int stack_all_Broadband_Envelopes_into_ARC(ARC_combo manyarcs[], int flushit, int reduceit)`: Stacks broadband echo envelopes into an array of `ARC_combo` structures.
*   `int dump_Calib_Values(char *name)`: Dumps calibration values (e.g., Sphere TS, ripple correction) to a file.
*   `int load_Calib_Values(char *name, float *calfreq, float *calgain, int *nocalvals)`: Loads calibration values (frequency and gain) from a file.

## How It Works
This module consists of numerous internal functions that provide the underlying data processing capabilities for the `EKlook` application. These functions are called by `EKlook`'s various interactive widgets and batch processing tools to handle tasks such as reading and writing EK data files, performing acoustic calculations (e.g., attenuation, ensonified area, incidence angles), managing bottom detection parameters, and accumulating/reducing angular response curves. The module acts as a computational backbone, abstracting complex data manipulations from the user-facing GUI.

## Notes
This module is not a standalone executable; its functions are called internally by other `EKlook` components and related command-line utilities. Users do not directly interact with these functions via command-line arguments.
