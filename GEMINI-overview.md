# GEMINI Project Overview: Oceanographic Data Processing Toolkit

This project is a comprehensive suite of C-based command-line tools for processing and analyzing oceanographic and hydrographic data. It appears to be a long-standing project managed under the Subversion (SVN) version control system.

The toolkit is organized into a collection of subdirectories, each containing specialized tools for different data types and processing tasks. The names of these directories suggest a focus on data from various sonar systems (multibeam, sidescan, ADCP) and related data types (navigation, tide, attitude).

## Building the Project

The project is built using `make`. A top-level script, `makeall`, orchestrates the build process by descending into the various subdirectories and compiling the tools.

To build all the tools, run the following command from the project root:

```bash
./makeall
```

A `makesome` script also exists, which appears to build a subset of the tools.

## Project Structure and Key Tools

The project is divided into numerous subdirectories, each serving a specific purpose. Here is a summary of some of the key directories and their likely functions based on file and directory names:

-   `adcp/`: Tools for processing Acoustic Doppler Current Profiler (ADCP) data (e.g., `readADCP`).
-   `att/`: Utilities for handling attitude data (roll, pitch, heave).
-   `class/`: Tools for classifying or analyzing data.
-   `doc/`: Documentation, including notes on the use of Subversion for version control.
-   `EKlook/`: Tools for visualizing and processing Simrad EK-series echosounder data.
-   `elac/`: Tools for Elac multibeam data.
-   `grid/`: A suite of tools for gridding, filtering, and manipulating grid files.
-   `gsf/`: Tools for the Generic Sensor Format (GSF).
-   `image/`: Utilities for image manipulation, likely for sonar imagery.
-   `nav/`: A collection of tools for processing and manipulating navigation data.
-ai-sender:
-   `omg/`: Appears to be a central directory, possibly for the "Ocean Mapping Group" (OMG), with a wide range of tools for multibeam data processing.
-   `plot/`: Plotting utilities.
-   `sidescan/`: A comprehensive set of tools for sidescan sonar data processing.
-   `subr/`: A directory of subroutines, likely containing a library of common functions used by the other tools.
-   `tide/`: Tools for tide data processing and correction.
-   `xtf/`: Tools for the Extended Triton Format (XTF), a common format for sonar data.

## Development Conventions

-   **Language:** The project is written in C.
-   **Build System:** The project uses `make` for compilation. Each subdirectory typically contains a `makefile`.
-   **Version Control:** The project is managed using Subversion (SVN).
-   **Coding Style:** Based on a brief review of the code, the style appears to be consistent with traditional C programming practices. Header files (`.h`) are used for declarations, and source files (`.c`) contain the implementations. A common set of libraries appears to be located in the `subr` directory.
