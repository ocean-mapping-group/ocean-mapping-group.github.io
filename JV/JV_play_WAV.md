---
layout: default
title: JV_play_WAV (Module within jview)
parent: JV Tools
nav_order: 5
---
# JV_play_WAV (Module within jview)

## Description
`JV_play_WAV.c` implements an X-windows-based graphical user interface (GUI) and underlying logic for the analysis and playback of WAV audio files. Its primary focus is on performing Fast Fourier Transform (FFT) on selected audio subsets, applying filters to the audio data, and providing interactive visualizations of both the audio time series and its spectral content.

## Key Features and Functions

*   **GUI Management (`manage_WAVFFT_widget_events`, `refresh_WAVFFT_widget_window`, `make_WAVFFT_widget`):**
    *   Manages user interactions such as button clicks and key presses within the dedicated WAV Audio Analysis Toolkit widget.
    *   Controls the display and state of various GUI elements, including:
        *   **Buttons:** "play" (original audio), "filter" (filtered audio), "TestSignal" (generates a synthetic signal for testing).
        *   **Sliders:** Control audio gain (log 10), low-pass and high-pass filter frequencies, and the duration of the time series subset being analyzed.
        *   **Graphic Windows:** Dedicated areas for plotting time series and spectral data.
    *   `make_WAVFFT_widget` sets up the custom layout of these widgets and initializes the sliders with their specific ranges and links them to global variables.
*   **Audio File Handling (`WAVFFT_open_wav`, `load_WAVFFT_audio_subset`):**
    *   `WAVFFT_open_wav`: Opens a specified WAV file, reads its header information, and extracts datetime.
    *   `load_WAVFFT_audio_subset`: Loads a specific segment of audio samples from the opened WAV file, handles memory reallocation, calculates average amplitude, applies gain, and manages data to fit within 16-bit signed integer limits.
*   **WAVFFT Processing Workflow (`update_WAVFFT`, `calc_WAVFFT`, `calc_filt_WAVFFT`):**
    *   `update_WAVFFT`: Reloads audio subsets, triggers FFT recalculation and filtering, redraws graphical elements, and optionally replays processed audio.
    *   `calc_WAVFFT`: Performs FFT calculations. Automatically determines optimal FFT size, loads audio segments, applies tapering windows, performs FFT across multiple overlapping segments, aggregates power spectra, and invokes `calc_filt_WAVFFT`.
    *   `calc_filt_WAVFFT`: Executes a larger FFT on the entire audio subset, applies defined frequency filters, and performs an inverse FFT to reconstruct the filtered audio signal.
*   **FFT and Filtering Utility Functions (`do_the_fft`, `filter_and_inv_fft`, `build_weights`):**
    *   `do_the_fft`: Performs a forward FFT on a given signal, calculates the magnitude (power) spectrum, and determines frequency components.
    *   `filter_and_inv_fft`: Filters FFT-transformed data by zeroing frequency bins outside specified ranges, then applies an inverse FFT to transform filtered spectral data back into the time domain.
    *   `build_weights`: Generates a tapering window (e.g., Hanning window) to minimize spectral artifacts.
*   **Audio Playback (`play_audio`):**
    *   Plays back audio data (original or filtered).
*   **Visualization (`draw_WAVFFT`, `draw_allWAVFFT`):**
    *   Renders various graphical outputs into designated X-windows: information panel (WAV file metadata), time series plot (original and filtered audio), and spectral plot (power spectra).
*   **Initialization (`init_WAVFFT_variables`):**
    *   Sets initial default values for all WAVFFT-specific parameters, such as the maximum and minimum frequencies, gain settings, duration of the audio subset, the fractional starting location within the entire file, and the power display range for the spectral plots.

## How It Works
The `JV_play_WAV` module provides an interactive environment within `jview` for analyzing WAV audio data. It allows users to load audio files, apply signal processing techniques like FFT and filtering, and visualize the results in both the time and frequency domains. User interactions with buttons and sliders control the processing parameters (e.g., gain, filter frequencies, audio subset duration). The module dynamically updates its graphical displays, providing real-time feedback on the audio signal and its spectral characteristics, and also supports playback of the original or filtered audio.

## Dependencies

*   `JV_global.h`: Provides access to global variables, shared structures, and common definitions used across the entire `jview` suite.
*   `JV_play_WAV.h`: This module's own header file, defining specific function prototypes and data structures used within `JV_play_WAV.c`.
*   **GUI and Graphics Functions (`jX_`, `jhc_` prefixed functions):** Includes functions for X-windows GUI management (`jX_is_win`, `jX_update_slider_variable`, `jX_redraw_slider`, `jX_setup_widget`), drawing primitives (`jhc_scaled_values`, `jhc_text`, `jhc_line`, `jhc_shape`, `jhc_fill_rect`, `jhc_load_font`), string manipulation (`mem_strcpy`, `mem_stripext`, `mem_strippath`, `mem_strappend`), window management (`write_icon`, `hilite_window`, `refresh_window`), and other GUI-related operations.
*   **Audio Utility Functions:** `play_audio` for sound output.
*   **Time Utilities:** `stdtime_nicetime` for displaying formatted time information.
*   **WAV File I/O:** `j_read_wav_header`, `j_read_wav_datetime` for reading WAV file metadata.
*   **Numerical Processing:** `do_the_fft`, `four1` (likely a 1D FFT routine from Numerical Recipes), `filter_and_inv_fft`, `build_weights` for all signal processing aspects.

## Notes
`JV_play_WAV.c` offers a powerful interactive environment for detailed analysis of WAV audio data. It allows users to visually inspect audio time series, explore their spectral components through FFT, apply various filters, and audition the results, making it an invaluable tool for acoustic research, signal processing, or quality control in applications where audio characteristics are critical.