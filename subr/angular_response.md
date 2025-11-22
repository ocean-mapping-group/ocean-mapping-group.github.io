---
layout: default
title: angular_response
parent: Subr Tools
grand_parent: code
nav_order: 2
---
# angular_response

## Description
`angular_response.c` is a C utility library for managing and processing Angular Response (AR) maps. These maps are used to characterize the relationship between backscatter strength and grazing angle for different seafloor types or conditions. The library provides a set of functions to initialize, read from/write to disk, and free `AR_Map` structures. It also includes functionalities to accumulate individual response samples into the map, compile the stored data into statistical summaries (mean and standard deviation of response versus grazing angle), query the map for a response at a given location and angle, and normalize the map based on a specified angular range.

## Data Structures

### `AR_Map`
```c
typedef struct {
    JHC_header header;        // Header containing map dimensions, projection info, etc.
    unsigned char *code_map;  // A 2D map (image) where each pixel contains a code representing a seafloor type/class.
    unsigned char encoded[256]; // Flags if an AR code has valid data.
    float sum[256][90];       // Sum of responses for each code and angle bin.
    float sum_sqr[256][90];   // Sum of squared responses for each code and angle bin.
    int count[256][90];       // Count of samples for each code and angle bin.
    float response[256][90];  // Compiled mean response (dB) for each code and angle bin.
    float std_deviation[256][90]; // Compiled standard deviation (dB) for each code and angle bin.
} AR_Map;
```

## Functions

### `int init_AR_map(AR_Map *map)`
Initializes an `AR_Map` structure by setting all its members to zero.
*   `map`: Pointer to the `AR_Map` structure to initialize.
*   **Returns:** `0` on success.

### `int read_AR_map(AR_Map *map, char *filename)`
Reads an `AR_Map` from a specified file.
*   `map`: Pointer to the `AR_Map` structure to populate.
*   `filename`: Path to the AR map file.
*   **Returns:** `0` on success, `1` on error (file not found, corrupt, or memory allocation failure).

### `int print_AR_map(AR_Map *map)`
Prints a summary of the compiled angular responses to standard output.
*   `map`: Pointer to the `AR_Map` structure to print.

### `int free_AR_map(AR_Map *map)`
Frees dynamically allocated memory within an `AR_Map` structure and re-initializes it.
*   `map`: Pointer to the `AR_Map` structure to free.
*   **Returns:** `0` on success.

### `int write_AR_map(AR_Map *map, char *filename)`
Writes an `AR_Map` to a specified file.
*   `map`: Pointer to the `AR_Map` structure to write.
*   `filename`: Path to the output AR map file.
*   **Returns:** `0` on success, `1` on error (file creation failure).

### `int add_response(AR_Map *map, double lat, double lon, float incidence_angle, float response)`
Adds an individual backscatter response sample to the `AR_Map`.
*   `map`: Pointer to the `AR_Map` structure.
*   `lat, lon`: Latitude and longitude of the sample.
*   `incidence_angle`: Incidence (grazing) angle of the sample (0-89 degrees).
*   `response`: The backscatter response value (e.g., in linear units).
*   **Returns:** `0` on success, `1` if the coordinates are outside the map extent or angle is invalid.

### `int compile_response(AR_Map *map)`
Compiles the accumulated sum and sum_sqr values into mean (`response`) and standard deviation (`std_deviation`) for each code and angle bin. Converts results to dB.
*   `map`: Pointer to the `AR_Map` structure.
*   **Returns:** `0` on success.

### `int get_response(AR_Map *map, double lat, double lon, float incidence_angle, float *response)`
Queries the `AR_Map` for the mean angular response at a given geographic location and incidence angle.
*   `map`: Pointer to the `AR_Map` structure.
*   `lat, lon`: Latitude and longitude of the query point.
*   `incidence_angle`: Incidence (grazing) angle of the query.
*   `response`: Pointer to a `float` to store the retrieved response (in dB).
*   **Returns:** `0` on success, `1` if outside map extent, invalid angle, or no data for the code/angle.

### `int normalize_AR_map(AR_Map *map, int inner_angle, int outer_angle)`
Normalizes the compiled responses in the `AR_Map` by subtracting the average response within a specified angular range from each response curve.
*   `map`: Pointer to the `AR_Map` structure.
*   `inner_angle, outer_angle`: The angular range (in degrees) to use for calculating the normalization average.
*   **Returns:** `0` on success.

## How It Works
The `angular_response` library uses a grid (`code_map`) overlaid on a geographic area. Each cell in this grid can be assigned a "code" (e.g., representing a seafloor type). For each code, and for each 1-degree bin of incidence angle (0-89 degrees), the `AR_Map` stores the sum of backscatter responses, the sum of squared responses, and a count of samples.
1.  **Data Accumulation:** When `add_response` is called with a sample (lat/lon, angle, response), it first projects the lat/lon to map coordinates to find the corresponding `code` from `code_map`. Then, it increments `sum`, `sum_sqr`, and `count` for that `code` and `angle_index`.
2.  **Compilation:** `compile_response` iterates through all codes and angle bins. For each bin with sufficient data (`count > 0`), it calculates the mean response (`response`) and standard deviation (`std_deviation`) from the accumulated sums. These values are then converted to dB.
3.  **Normalization:** `normalize_AR_map` calculates an average response over a specified `inner_angle` to `outer_angle` range for each code. This average is then subtracted from all `response` values for that code, effectively flattening the angular response curves to a common baseline.
4.  **Query:** `get_response` retrieves the pre-compiled mean `response` (in dB) for a given location (code) and incidence angle.
This modular approach allows for efficient storage, compilation, and retrieval of seafloor angular backscatter characteristics.
