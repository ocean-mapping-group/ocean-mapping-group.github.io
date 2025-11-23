# `JV_play_WAV.c` - WAV Audio Analysis Toolkit

This C file implements an X-windows-based graphical user interface (GUI) and underlying logic for the analysis and playback of WAV audio files. Its primary focus is on performing Fast Fourier Transform (FFT) on selected audio subsets, applying filters to the audio data, and providing interactive visualizations of both the audio time series and its spectral content.

## Key Features and Functions

*   **GUI Management (`manage_WAVFFT_widget_events`, `refresh_WAVFFT_widget_window`, `make_WAVFFT_widget`):**
    *   Manages user interactions such as button clicks and key presses within the dedicated WAV Audio Analysis Toolkit widget.
    *   Controls the display and state of various GUI elements, including:
        *   **Buttons:** "play" (original audio), "filter" (filtered audio), "TestSignal" (generates a synthetic signal for testing).
        *   **Sliders:** Control audio gain (log 10), low-pass and high-pass filter frequencies, and the duration of the time series subset being analyzed.
        *   **Graphic Windows:** Dedicated areas for plotting time series and spectral data.
    *   `make_WAVFFT_widget` sets up the custom layout of these widgets and initializes the sliders with their specific ranges and links them to global variables.

*   **Audio File Handling (`WAVFFT_open_wav`, `load_WAVFFT_audio_subset`):**
    *   `WAVFFT_open_wav`: Responsible for opening a specified WAV file. It reads the file's header information using `j_read_wav_header` and, if available, extracts datetime information via `j_read_wav_datetime`.
    *   `load_WAVFFT_audio_subset`: Loads a specific segment of audio samples from the opened WAV file. The segment is defined by a fractional location within the total duration and a user-specified duration. This function handles memory reallocation for the audio data buffer if the subset size changes, calculates the average amplitude of the loaded subset, applies a user-defined gain, and manages the data to fit within 16-bit signed integer limits.

*   **WAVFFT Processing Workflow (`update_WAVFFT`, `calc_WAVFFT`, `calc_filt_WAVFFT`):**
    *   `update_WAVFFT`: Acts as an orchestrator, reloading audio subsets based on current settings, triggering the recalculation of FFTs and filtering, redrawing all graphical elements, and optionally replaying the processed audio.
    *   `calc_WAVFFT`: The primary function for FFT calculations.
        *   Automatically determines an optimal FFT size (a power of 2) suitable for the audio data.
        *   Loads segments of the audio data from `WAVFFT_audio_data` into `WAVFFT_intensities`.
        *   Applies a tapering window (e.g., Hanning window via `build_weights`) to the time-domain data before FFT to minimize spectral leakage artifacts.
        *   Performs FFT using `do_the_fft` across multiple overlapping segments (`WAVFFT_nospectra`) within the audio subset, storing the individual power spectra and their corresponding frequencies.
        *   Aggregates the power spectra into 1kHz frequency bins.
        *   Invokes `calc_filt_WAVFFT` to apply frequency-domain filtering.
    *   `calc_filt_WAVFFT`: Executes a larger FFT on the entire audio subset, applies the defined frequency filters (low-pass and high-pass), and then performs an inverse FFT to reconstruct the filtered audio signal in the time domain.

*   **FFT and Filtering Utility Functions (`do_the_fft`, `filter_and_inv_fft`, `build_weights`):**
    *   `do_the_fft`: A generic function that performs a forward FFT on a given signal (using a routine like `four1` from Numerical Recipes), calculates the magnitude (power) spectrum (with an option for logarithmic scaling), and determines the frequency corresponding to each spectral component.
    *   `filter_and_inv_fft`: Filters FFT-transformed data by setting frequency bins outside the specified `min_freq` and `max_freq` ranges to zero. Subsequently, it applies an inverse FFT (also using `four1`) to transform the filtered spectral data back into the time domain, producing a clean, filtered audio signal.
    *   `build_weights`: Generates a tapering window (e.g., a Hanning window) based on the specified type and percentage of taper. These weights are applied to the time-domain audio signal before performing the FFT to minimize unwanted spectral artifacts caused by finite data windows.

*   **Audio Playback (`play_audio`):**
    *   A function responsible for playing back the audio data, which can be either the original loaded segment or the filtered version, given the array of audio samples and the number of samples to play.

*   **Visualization (`draw_WAVFFT`, `draw_allWAVFFT`):**
    *   `draw_WAVFFT`: Renders various graphical outputs into designated X-windows:
        *   **Information Panel (Window 3):** Displays critical WAV file metadata, including the filename, total duration, sample rate, details about the currently loaded audio subset (duration, offset, start/end times), and the calculated subset start time.
        *   **Time Series Plot (Window 0):** Visualizes the raw audio time series data (original and filtered), indicating the applied gain and the boundaries of the FFT segments.
        *   **Spectral Plot (Window 1):** Presents the power spectra, encompassing both the FFT of the full subset and the binned 1kHz spectra for individual overlapping segments. This plot allows for user-adjustable power (dB) range and frequency axis scaling.

*   **Initialization (`init_WAVFFT_variables`):**
    *   Sets initial default values for all WAVFFT-specific parameters, such as the maximum and minimum frequencies, gain settings, duration of the audio subset, the fractional starting location within the entire file, and the power display range for the spectral plots.

## Dependencies

This module is built upon several internal libraries and header files, which collectively provide the necessary graphical primitives, utility functions, numerical processing capabilities, and audio handling features for the `jview` application:

*   `JV_global.h`: Provides access to global variables, shared structures, and common definitions used across the entire `jview` suite.
*   `JV_play_WAV.h`: This module's own header file, defining specific function prototypes and data structures used within `JV_play_WAV.c`.
*   **GUI and Graphics Functions (`jX_`, `jhc_` prefixed functions):** Includes functions for X-windows GUI management (`jX_is_win`, `jX_update_slider_variable`, `jX_redraw_slider`, `jX_setup_widget`), drawing primitives (`jhc_scaled_values`, `jhc_text`, `jhc_line`, `jhc_shape`, `jhc_fill_rect`, `jhc_load_font`), string manipulation (`mem_strcpy`, `mem_stripext`, `mem_strippath`, `mem_strappend`), window management (`write_icon`, `hilite_window`, `refresh_window`), and other GUI-related operations.
*   **Audio Utility Functions:** `play_audio` for sound output.
*   **Time Utilities:** `stdtime_nicetime` for displaying formatted time information.
*   **WAV File I/O:** `j_read_wav_header`, `j_read_wav_datetime` for reading WAV file metadata.
*   **Numerical Processing:** `do_the_fft`, `four1` (likely a 1D FFT routine from Numerical Recipes), `filter_and_inv_fft`, `build_weights` for all signal processing aspects.

## Usage

`JV_play_WAV.c` offers a powerful interactive environment for detailed analysis of WAV audio data. It allows users to visually inspect audio time series, explore their spectral components through FFT, apply various filters, and audition the results, making it an invaluable tool for acoustic research, signal processing, or quality control in applications where audio characteristics are critical.
