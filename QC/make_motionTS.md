---
layout: default
title: make_motionTS
parent: QC Tools
nav_order: 157
---
---
layout: default
title: make_motionTS
parent: QC Tools
nav_order: 157
---

# make_motionTS

## Description
`make_motionTS` is a utility designed to generate synthetic time-series data for vessel motion (roll, pitch, heading, heave). It allows users to define various "motion packets," each specifying a type of motion, its duration, period, and peak amplitude. The tool then superimposes these sinusoidal motion components to create a composite motion time series, which is output to an ASCII file.

This tool is useful for creating controlled test data for Quality Control (QC) purposes, such as testing motion compensation algorithms or analyzing the response of processing routines to specific types of vessel motion.

## Usage
```bash
make_motionTS [-v] [-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>] [-pitch ...] [-heading ...] [-heave ...]
```

## Arguments

| Option | Description |
|---|---|
| `-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>` | Defines a sinusoidal roll motion component. Parameters are:
    *   `start_time`: Time (seconds) when this motion starts.
    *   `stop_time`: Time (seconds) when this motion stops.
    *   `start_period`: Period (seconds) of the sinusoidal motion at `start_time`.
    *   `stop_period`: Period (seconds) of the sinusoidal motion at `stop_time`.
    *   `peak_amplitude`: Maximum amplitude (e.g., in degrees for roll/pitch/heading, meters for heave).
| `-pitch` | Same parameters as `-roll`, but for pitch motion. |
| `-heading` | Same parameters as `-roll`, but for heading motion. |
| `-heave` | Same parameters as `-roll`, but for heave motion. |
| `-v` | Enable verbose output. |

## How It Works
1.  **Initialization:** Parses command-line arguments to define `motion_packet` structures. It supports multiple `motion_packet` definitions for various types of motion.
2.  **Time Series Generation:**
    *   Initializes a `motion_sample` array (`timeSeries`) of `numSECONDS * perSECOND` elements (currently 600 seconds with 10 samples/second, totaling 6000 samples).
    *   Each `motion_sample` has fields for `time`, `roll`, `pitch`, `heading`, and `heave`.
    *   For each defined `motion_packet`:
        *   It iterates through the `timeSeries` array.
        *   If a sample's `time` falls within the `start_time` and `stop_time` of the packet:
            *   It calculates a sinusoidal `value` based on the packet's `peak_amplitude` and a phase derived from `time`, `start_time`, and `start_period`.
            *   A cosine-squared `taper` is applied to the `value` to smooth the onset and offset of the motion.
            *   This `value` is added to the corresponding motion component (roll, pitch, heading, or heave) in the `timeSeries` array.
3.  **Output:** Writes the generated `timeSeries` to an ASCII file named `fake.ts`. The output format is:
    ```
    <total_number_of_samples>
    <time> <roll> <pitch> <heading> <heave>
    ...
    ```
4.  **Cleanup:** Closes the output file.

## Output File Format (`fake.ts`)
The output file is an ASCII text file with the first line indicating the total number of samples, followed by lines of space-separated values:
`time roll pitch heading heave`
(All float values)
```
```
---
layout: default
title: make_motionTS
parent: QC Tools
nav_order: 157
---

# make_motionTS

## Description
`make_motionTS` is a utility designed to generate synthetic time-series data for vessel motion (roll, pitch, heading, heave). It allows users to define various "motion packets," each specifying a type of motion, its duration, period, and peak amplitude. The tool then superimposes these sinusoidal motion components to create a composite motion time series, which is output to an ASCII file.

This tool is useful for creating controlled test data for Quality Control (QC) purposes, such as testing motion compensation algorithms or analyzing the response of processing routines to specific types of vessel motion.

## Usage
```bash
make_motionTS [-v] [-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>] [-pitch ...] [-heading ...] [-heave ...]
```

## Arguments

| Option | Description |
|---|---|
| `-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>` | Defines a sinusoidal roll motion component. Parameters are:
    *   `start_time`: Time (seconds) when this motion starts.
    *   `stop_time`: Time (seconds) when this motion stops.
    *   `start_period`: Period (seconds) of the sinusoidal motion at `start_time`.
    *   `stop_period`: Period (seconds) of the sinusoidal motion at `stop_time`.
    *   `peak_amplitude`: Maximum amplitude (e.g., in degrees for roll/pitch/heading, meters for heave).
| `-pitch` | Same parameters as `-roll`, but for pitch motion. |
| `-heading` | Same parameters as `-roll`, but for heading motion. |
| `-heave` | Same parameters as `-roll`, but for heave motion. |
| `-v` | Enable verbose output. |

## How It Works
1.  **Initialization:** Parses command-line arguments to define `motion_packet` structures. It supports multiple `motion_packet` definitions for various types of motion.
2.  **Time Series Generation:**
    *   Initializes a `motion_sample` array (`timeSeries`) of `numSECONDS * perSECOND` elements (currently 600 seconds with 10 samples/second, totaling 6000 samples).
    *   Each `motion_sample` has fields for `time`, `roll`, `pitch`, `heading`, and `heave`.
    *   For each defined `motion_packet`:
        *   It iterates through the `timeSeries` array.
        *   If a sample's `time` falls within the `start_time` and `stop_time` of the packet:
            *   It calculates a sinusoidal `value` based on the packet's `peak_amplitude` and a phase derived from `time`, `start_time`, and `start_period`.
            *   A cosine-squared `taper` is applied to the `value` to smooth the onset and offset of the motion.
            *   This `value` is added to the corresponding motion component (roll, pitch, heading, or heave) in the `timeSeries` array.
3.  **Output:** Writes the generated `timeSeries` to an ASCII file named `fake.ts`. The output format is:
    ```
    <total_number_of_samples>
    <time> <roll> <pitch> <heading> <heave>
    ...
    ```
4.  **Cleanup:** Closes the output file.

## Output File Format (`fake.ts`)
The output file is an ASCII text file with the first line indicating the total number of samples, followed by lines of space-separated values:
`time roll pitch heading heave`
(All float values)
```
```
---
layout: default
title: make_motionTS
parent: QC Tools
nav_order: 157
---

# make_motionTS

## Description
`make_motionTS` is a utility designed to generate synthetic time-series data for vessel motion (roll, pitch, heading, heave). It allows users to define various "motion packets," each specifying a type of motion, its duration, period, and peak amplitude. The tool then superimposes these sinusoidal motion components to create a composite motion time series, which is output to an ASCII file.

This tool is useful for creating controlled test data for Quality Control (QC) purposes, such as testing motion compensation algorithms or analyzing the response of processing routines to specific types of vessel motion.

## Usage
```bash
make_motionTS [-v] [-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>] [-pitch ...] [-heading ...] [-heave ...]
```

## Arguments

| Option | Description |
|---|---|
| `-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>` | Defines a sinusoidal roll motion component. Parameters are:
    *   `start_time`: Time (seconds) when this motion starts.
    *   `stop_time`: Time (seconds) when this motion stops.
    *   `start_period`: Period (seconds) of the sinusoidal motion at `start_time`.
    *   `stop_period`: Period (seconds) of the sinusoidal motion at `stop_time`.
    *   `peak_amplitude`: Maximum amplitude (e.g., in degrees for roll/pitch/heading, meters for heave).
| `-pitch` | Same parameters as `-roll`, but for pitch motion. |
| `-heading` | Same parameters as `-roll`, but for heading motion. |
| `-heave` | Same parameters as `-roll`, but for heave motion. |
| `-v` | Enable verbose output. |

## How It Works
1.  **Initialization:** Parses command-line arguments to define `motion_packet` structures. It supports multiple `motion_packet` definitions for various types of motion.
2.  **Time Series Generation:**
    *   Initializes a `motion_sample` array (`timeSeries`) of `numSECONDS * perSECOND` elements (currently 600 seconds with 10 samples/second, totaling 6000 samples).
    *   Each `motion_sample` has fields for `time`, `roll`, `pitch`, `heading`, and `heave`.
    *   For each defined `motion_packet`:
        *   It iterates through the `timeSeries` array.
        *   If a sample's `time` falls within the `start_time` and `stop_time` of the packet:
            *   It calculates a sinusoidal `value` based on the packet's `peak_amplitude` and a phase derived from `time`, `start_time`, and `start_period`.
            *   A cosine-squared `taper` is applied to the `value` to smooth the onset and offset of the motion.
            *   This `value` is added to the corresponding motion component (roll, pitch, heading, or heave) in the `timeSeries` array.
3.  **Output:** Writes the generated `timeSeries` to an ASCII file named `fake.ts`. The output format is:
    ```
    <total_number_of_samples>
    <time> <roll> <pitch> <heading> <heave>
    ...
    ```
4.  **Cleanup:** Closes the output file.

## Output File Format (`fake.ts`)
The output file is an ASCII text file with the first line indicating the total number of samples, followed by lines of space-separated values:
`time roll pitch heading heave`
(All float values)
```
```
---
layout: default
title: make_motionTS
parent: QC Tools
nav_order: 157
---

# make_motionTS

## Description
`make_motionTS` is a utility designed to generate synthetic time-series data for vessel motion (roll, pitch, heading, heave). It allows users to define various "motion packets," each specifying a type of motion, its duration, period, and peak amplitude. The tool then superimposes these sinusoidal motion components to create a composite motion time series, which is output to an ASCII file.

This tool is useful for creating controlled test data for Quality Control (QC) purposes, such as testing motion compensation algorithms or analyzing the response of processing routines to specific types of vessel motion.

## Usage
```bash
make_motionTS [-v] [-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>] [-pitch ...] [-heading ...] [-heave ...]
```

## Arguments

| Option | Description |
|---|---|
| `-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>` | Defines a sinusoidal roll motion component. Parameters are:
    *   `start_time`: Time (seconds) when this motion starts.
    *   `stop_time`: Time (seconds) when this motion stops.
    *   `start_period`: Period (seconds) of the sinusoidal motion at `start_time`.
    *   `stop_period`: Period (seconds) of the sinusoidal motion at `stop_time`.
    *   `peak_amplitude`: Maximum amplitude (e.g., in degrees for roll/pitch/heading, meters for heave).
| `-pitch` | Same parameters as `-roll`, but for pitch motion. |
| `-heading` | Same parameters as `-roll`, but for heading motion. |
| `-heave` | Same parameters as `-roll`, but for heave motion. |
| `-v` | Enable verbose output. |

## How It Works
1.  **Initialization:** Parses command-line arguments to define `motion_packet` structures. It supports multiple `motion_packet` definitions for various types of motion.
2.  **Time Series Generation:**
    *   Initializes a `motion_sample` array (`timeSeries`) of `numSECONDS * perSECOND` elements (currently 600 seconds with 10 samples/second, totaling 6000 samples).
    *   Each `motion_sample` has fields for `time`, `roll`, `pitch`, `heading`, and `heave`.
    *   For each defined `motion_packet`:
        *   It iterates through the `timeSeries` array.
        *   If a sample's `time` falls within the `start_time` and `stop_time` of the packet:
            *   It calculates a sinusoidal `value` based on the packet's `peak_amplitude` and a phase derived from `time`, `start_time`, and `start_period`.
            *   A cosine-squared `taper` is applied to the `value` to smooth the onset and offset of the motion.
            *   This `value` is added to the corresponding motion component (roll, pitch, heading, or heave) in the `timeSeries` array.
3.  **Output:** Writes the generated `timeSeries` to an ASCII file named `fake.ts`. The output format is:
    ```
    <total_number_of_samples>
    <time> <roll> <pitch> <heading> <heave>
    ...
    ```
4.  **Cleanup:** Closes the output file.

## Output File Format (`fake.ts`)
The output file is an ASCII text file with the first line indicating the total number of samples, followed by lines of space-separated values:
`time roll pitch heading heave`
(All float values)
```
```
---
layout: default
title: make_motionTS
parent: QC Tools
nav_order: 157
---

# make_motionTS

## Description
`make_motionTS` is a utility designed to generate synthetic time-series data for vessel motion (roll, pitch, heading, heave). It allows users to define various "motion packets," each specifying a type of motion, its duration, period, and peak amplitude. The tool then superimposes these sinusoidal motion components to create a composite motion time series, which is output to an ASCII file.

This tool is useful for creating controlled test data for Quality Control (QC) purposes, such as testing motion compensation algorithms or analyzing the response of processing routines to specific types of vessel motion.

## Usage
```bash
make_motionTS [-v] [-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>] [-pitch ...] [-heading ...] [-heave ...]
```

## Arguments

| Option | Description |
|---|---|
| `-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>` | Defines a sinusoidal roll motion component. Parameters are:
    *   `start_time`: Time (seconds) when this motion starts.
    *   `stop_time`: Time (seconds) when this motion stops.
    *   `start_period`: Period (seconds) of the sinusoidal motion at `start_time`.
    *   `stop_period`: Period (seconds) of the sinusoidal motion at `stop_time`.
    *   `peak_amplitude`: Maximum amplitude (e.g., in degrees for roll/pitch/heading, meters for heave).
| `-pitch` | Same parameters as `-roll`, but for pitch motion. |
| `-heading` | Same parameters as `-roll`, but for heading motion. |
| `-heave` | Same parameters as `-roll`, but for heave motion. |
| `-v` | Enable verbose output. |

## How It Works
1.  **Initialization:** Parses command-line arguments to define `motion_packet` structures. It supports multiple `motion_packet` definitions for various types of motion.
2.  **Time Series Generation:**
    *   Initializes a `motion_sample` array (`timeSeries`) of `numSECONDS * perSECOND` elements (currently 600 seconds with 10 samples/second, totaling 6000 samples).
    *   Each `motion_sample` has fields for `time`, `roll`, `pitch`, `heading`, and `heave`.
    *   For each defined `motion_packet`:
        *   It iterates through the `timeSeries` array.
        *   If a sample's `time` falls within the `start_time` and `stop_time` of the packet:
            *   It calculates a sinusoidal `value` based on the packet's `peak_amplitude` and a phase derived from `time`, `start_time`, and `start_period`.
            *   A cosine-squared `taper` is applied to the `value` to smooth the onset and offset of the motion.
            *   This `value` is added to the corresponding motion component (roll, pitch, heading, or heave) in the `timeSeries` array.
3.  **Output:** Writes the generated `timeSeries` to an ASCII file named `fake.ts`. The output format is:
    ```
    <total_number_of_samples>
    <time> <roll> <pitch> <heading> <heave>
    ...
    ```
4.  **Cleanup:** Closes the output file.

## Output File Format (`fake.ts`)
The output file is an ASCII text file with the first line indicating the total number of samples, followed by lines of space-separated values:
`time roll pitch heading heave`
(All float values)
```
```
---
layout: default
title: make_motionTS
parent: QC Tools
nav_order: 157
---

# make_motionTS

## Description
`make_motionTS` is a utility designed to generate synthetic time-series data for vessel motion (roll, pitch, heading, heave). It allows users to define various "motion packets," each specifying a type of motion, its duration, period, and peak amplitude. The tool then superimposes these sinusoidal motion components to create a composite motion time series, which is output to an ASCII file.

This tool is useful for creating controlled test data for Quality Control (QC) purposes, such as testing motion compensation algorithms or analyzing the response of processing routines to specific types of vessel motion.

## Usage
```bash
make_motionTS [-v] [-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>] [-pitch ...] [-heading ...] [-heave ...]
```

## Arguments

| Option | Description |
|---|---|
| `-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>` | Defines a sinusoidal roll motion component. Parameters are:
    *   `start_time`: Time (seconds) when this motion starts.
    *   `stop_time`: Time (seconds) when this motion stops.
    *   `start_period`: Period (seconds) of the sinusoidal motion at `start_time`.
    *   `stop_period`: Period (seconds) of the sinusoidal motion at `stop_time`.
    *   `peak_amplitude`: Maximum amplitude (e.g., in degrees for roll/pitch/heading, meters for heave).
| `-pitch` | Same parameters as `-roll`, but for pitch motion. |
| `-heading` | Same parameters as `-roll`, but for heading motion. |
| `-heave` | Same parameters as `-roll`, but for heave motion. |
| `-v` | Enable verbose output. |

## How It Works
1.  **Initialization:** Parses command-line arguments to define `motion_packet` structures. It supports multiple `motion_packet` definitions for various types of motion.
2.  **Time Series Generation:**
    *   Initializes a `motion_sample` array (`timeSeries`) of `numSECONDS * perSECOND` elements (currently 600 seconds with 10 samples/second, totaling 6000 samples).
    *   Each `motion_sample` has fields for `time`, `roll`, `pitch`, `heading`, and `heave`.
    *   For each defined `motion_packet`:
        *   It iterates through the `timeSeries` array.
        *   If a sample's `time` falls within the `start_time` and `stop_time` of the packet:
            *   It calculates a sinusoidal `value` based on the packet's `peak_amplitude` and a phase derived from `time`, `start_time`, and `start_period`.
            *   A cosine-squared `taper` is applied to the `value` to smooth the onset and offset of the motion.
            *   This `value` is added to the corresponding motion component (roll, pitch, heading, or heave) in the `timeSeries` array.
3.  **Output:** Writes the generated `timeSeries` to an ASCII file named `fake.ts`. The output format is:
    ```
    <total_number_of_samples>
    <time> <roll> <pitch> <heading> <heave>
    ...
    ```
4.  **Cleanup:** Closes the output file.

## Output File Format (`fake.ts`)
The output file is an ASCII text file with the first line indicating the total number of samples, followed by lines of space-separated values:
`time roll pitch heading heave`
(All float values)
```
```
---
layout: default
title: make_motionTS
parent: QC Tools
nav_order: 157
---

# make_motionTS

## Description
`make_motionTS` is a utility designed to generate synthetic time-series data for vessel motion (roll, pitch, heading, heave). It allows users to define various "motion packets," each specifying a type of motion, its duration, period, and peak amplitude. The tool then superimposes these sinusoidal motion components to create a composite motion time series, which is output to an ASCII file.

This tool is useful for creating controlled test data for Quality Control (QC) purposes, such as testing motion compensation algorithms or analyzing the response of processing routines to specific types of vessel motion.

## Usage
```bash
make_motionTS [-v] [-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>] [-pitch ...] [-heading ...] [-heave ...]
```

## Arguments

| Option | Description |
|---|---|
| `-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>` | Defines a sinusoidal roll motion component. Parameters are:
    *   `start_time`: Time (seconds) when this motion starts.
    *   `stop_time`: Time (seconds) when this motion stops.
    *   `start_period`: Period (seconds) of the sinusoidal motion at `start_time`.
    *   `stop_period`: Period (seconds) of the sinusoidal motion at `stop_time`.
    *   `peak_amplitude`: Maximum amplitude (e.g., in degrees for roll/pitch/heading, meters for heave).
| `-pitch` | Same parameters as `-roll`, but for pitch motion. |
| `-heading` | Same parameters as `-roll`, but for heading motion. |
| `-heave` | Same parameters as `-roll`, but for heave motion. |
| `-v` | Enable verbose output. |

## How It Works
1.  **Initialization:** Parses command-line arguments to define `motion_packet` structures. It supports multiple `motion_packet` definitions for various types of motion.
2.  **Time Series Generation:**
    *   Initializes a `motion_sample` array (`timeSeries`) of `numSECONDS * perSECOND` elements (currently 600 seconds with 10 samples/second, totaling 6000 samples).
    *   Each `motion_sample` has fields for `time`, `roll`, `pitch`, `heading`, and `heave`.
    *   For each defined `motion_packet`:
        *   It iterates through the `timeSeries` array.
        *   If a sample's `time` falls within the `start_time` and `stop_time` of the packet:
            *   It calculates a sinusoidal `value` based on the packet's `peak_amplitude` and a phase derived from `time`, `start_time`, and `start_period`.
            *   A cosine-squared `taper` is applied to the `value` to smooth the onset and offset of the motion.
            *   This `value` is added to the corresponding motion component (roll, pitch, heading, or heave) in the `timeSeries` array.
3.  **Output:** Writes the generated `timeSeries` to an ASCII file named `fake.ts`. The output format is:
    ```
    <total_number_of_samples>
    <time> <roll> <pitch> <heading> <heave>
    ...
    ```
4.  **Cleanup:** Closes the output file.

## Output File Format (`fake.ts`)
The output file is an ASCII text file with the first line indicating the total number of samples, followed by lines of space-separated values:
`time roll pitch heading heave`
(All float values)
```
---
layout: default
title: make_motionTS
parent: QC Tools
nav_order: 157
---

# make_motionTS

## Description
`make_motionTS` is a utility designed to generate synthetic time-series data for vessel motion (roll, pitch, heading, heave). It allows users to define various "motion packets," each specifying a type of motion, its duration, period, and peak amplitude. The tool then superimposes these sinusoidal motion components to create a composite motion time series, which is output to an ASCII file.

This tool is useful for creating controlled test data for Quality Control (QC) purposes, such as testing motion compensation algorithms or analyzing the response of processing routines to specific types of vessel motion.

## Usage
```bash
make_motionTS [-v] [-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>] [-pitch ...] [-heading ...] [-heave ...]
```

## Arguments

| Option | Description |
|---|---|
| `-roll <start_time> <stop_time> <start_period> <stop_period> <peak_amplitude>` | Defines a sinusoidal roll motion component. Parameters are:
    *   `start_time`: Time (seconds) when this motion starts.
    *   `stop_time`: Time (seconds) when this motion stops.
    *   `start_period`: Period (seconds) of the sinusoidal motion at `start_time`.
    *   `stop_period`: Period (seconds) of the sinusoidal motion at `stop_time`.
    *   `peak_amplitude`: Maximum amplitude (e.g., in degrees for roll/pitch/heading, meters for heave).
| `-pitch` | Same parameters as `-roll`, but for pitch motion. |
| `-heading` | Same parameters as `-roll`, but for heading motion. |
| `-heave` | Same parameters as `-roll`, but for heave motion. |
| `-v` | Enable verbose output. |

## How It Works
1.  **Initialization:** Parses command-line arguments to define `motion_packet` structures. It supports multiple `motion_packet` definitions for various types of motion.
2.  **Time Series Generation:**
    *   Initializes a `motion_sample` array (`timeSeries`) of `numSECONDS * perSECOND` elements (currently 600 seconds with 10 samples/second, totaling 6000 samples).
    *   Each `motion_sample` has fields for `time`, `roll`, `pitch`, `heading`, and `heave`.
    *   For each defined `motion_packet`:
        *   It iterates through the `timeSeries` array.
        *   If a sample's `time` falls within the `start_time` and `stop_time` of the packet:
            *   It calculates a sinusoidal `value` based on the packet's `peak_amplitude` and a phase derived from `time`, `start_time`, and `start_period`.
            *   A cosine-squared `taper` is applied to the `value` to smooth the onset and offset of the motion.
            *   This `value` is added to the corresponding motion component (roll, pitch, heading, or heave) in the `timeSeries` array.
3.  **Output:** Writes the generated `timeSeries` to an ASCII file named `fake.ts`. The output format is:
    ```
    <total_number_of_samples>
    <time> <roll> <pitch> <heading> <heave>
    ...
    ```
4.  **Cleanup:** Closes the output file.

## Output File Format (`fake.ts`)
The output file is an ASCII text file with the first line indicating the total number of samples, followed by lines of space-separated values:
`time roll pitch heading heave`
(All float values)
```
```