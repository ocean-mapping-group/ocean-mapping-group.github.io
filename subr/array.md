---
layout: default
title: array
parent: Subr Tools
grand_parent: code
nav_order: 3
---
# array

## Description
`array.c` is a comprehensive C utility library designed for managing and manipulating 2D array data, typically representing geographic grids, Digital Terrain Models (DTMs), or images, stored in a custom JHC (John Hughes Clarke) header format. It provides a wide range of functionalities, including:
*   Reading from and writing to files with custom `JHC_header` structures, handling endianness differences.
*   Bilinear interpolation for querying values from 2D arrays.
*   Loading and freeing entire map structures (`Map` struct) for easier data management.
*   Drawing raster lines onto both 8-bit `unsigned char` and `float` arrays, implementing a Digital Differential Analyzer (DDA) algorithm for vector-to-raster conversion.
*   Calculating "sun illumination" effects for DTMs, simulating Lambertian surface shading.
*   Extracting 2D profiles (cross-sections) from map data.
*   Determining if a swathfile's geographic extent intersects with a given map area.

This library serves as a foundational component for many tools within the GEMINI project that process and visualize gridded or image-based spatial data.

## Data Structures

### `SW_header` (Swath Header)
```c
typedef struct {
    int dx, dy;                 // Dimensions (width, height)
    double xmin, xmax, ymin, ymax; // Geographic bounds
    double xinc, yinc;          // Cell increments
} SW_header;
```

### `JHC_header` (JHC Generic Header)
```c
typedef struct {
    char header_name[4];        // Identifier, e.g., "OMG1"
    int dx, dy;                 // Dimensions (width, height) in pixels/cells
    double xmin, xmax, ymin, ymax; // Geographic bounds (e.g., longitude, latitude)
    double xstep, ystep;        // Step size (e.g., meters/pixel)
    char data_type;             // Type of data: 1=8bit, 2=16bit, 3=float
    char rgb_bw;                // Color/grayscale type: 1=R, 2=G, 3=B, 4=grayscale, 5=false color (8-30), etc.
    char projection;            // Projection type: 1=Mercator, 2=UTM, 10=Lambert, etc.
    char ellipsoid;             // Ellipsoid: 1=WGS84, 2=NAD27, etc.
    float proj_merid;           // Projection meridian (for Mercator/UTM)
    float sun_elev, sun_azi, sun_exag; // Sun illumination parameters
    float view_elev, view_azi, view_exag; // View parameters
    float max_value, min_value; // Data value range
    char hemisphere;            // Hemisphere for UTM
    char unass2, unass3, unass4; // Unassigned bytes
    char unassigned[4];         // Unassigned bytes
    char label_1[72];           // Label string 1
    // ... more fields added later for TX/RX parameters and Lambert projection ...
    double TX_RP_lat, TX_RP_lon; // Transducer reference point lat/lon
    double TX_sonar_lat, TX_sonar_lon; // Transducer sonar head lat/lon
    float TX_heading, TX_roll, TX_pitch, TX_heave; // Transducer attitude
    double TX_1970_time;        // Transducer time (Unix 1970 epoch)
    double spare_doubles[2];    // Spare double fields
    unsigned char rgb_cmap[768]; // RGB color map (256 * 3 bytes)
    float lat_std1, lat_std2;   // Standard parallels for Lambert
    float false_easting, false_northing; // False easting/northing for Lambert
} JHC_header;
```

### `Map` (Generic Map Structure)
```c
typedef struct {
    JHC_header header;          // Associated JHC header
    float *data_float;          // Pointer to float data array
    unsigned char *data_8bit;   // Pointer to 8-bit data array
} Map;
```

### `bin_vect` (Binary Vector Structure - commented out in source but referenced)
Likely used to define start/end points of a vector or line in map coordinates.

## Functions

### `SW_header get_print_SW_header(FILE *file, int print_flag)`
Reads an `SW_header` from a file and optionally prints its contents.

### `float interp_JHCarray_value(JHC_header *head, float *array_pointer, float x, float y)`
Performs bilinear interpolation to get a float value from a `float` array at `(x, y)` coordinates, using the `JHC_header` for scaling.

### `float get_JHC_lookup_value(JHC_header *head, float *array_pointer, float depth, float range)`
A specialized bilinear interpolation for lookup tables where `y` is depth and `x` is range. Returns `0.0` for out-of-bounds.

### `int write_JHC_header(FILE *file, JHC_header head)`
Writes a `JHC_header` to a file, performing byte-swapping if necessary.

### `JHC_header get_print_JHC_header(FILE *file, int print_flag)`
Reads a `JHC_header` from a file, performs byte-swapping, and optionally prints a verbose summary of its contents.

### `void packto8bit(float *fbuf, int novals, unsigned char *bbuf, float low_limit, float high_limit)`
Converts a `float` array (`fbuf`) to an 8-bit `unsigned char` array (`bbuf`), linearly scaling values between `low_limit` and `high_limit`. If limits are 0.0, it automatically finds min/max.

### `void get_8bitSUN(float *JHCbuf, JHC_header JHChead, float azi, float elev, float vert_exag, unsigned char *grey_buf)`
Calculates "sun illumination" (Lambertian shading) for a DTM (float array `JHCbuf`) and generates an 8-bit grayscale image (`grey_buf`).

### `void get_2D_profile(float *fdata, JHC_header *head, bin_vect coords, int *nosam, float *step, float *profile, float *min, float *max, double *proflat, double *proflon)`
Extracts a 2D profile (cross-section) from a map (`fdata`) along a line defined by `coords`.

### `int is_swathfile_inarea(JHC_header *arr_head, FILE *file, int exact)`
Checks if the geographic bounding box of an OMG_HDCS swath file (`file`) intersects with the area defined by a `JHC_header` (`arr_head`).

### `void do_DDA_raster_line(JHC_header *head, unsigned char *raster, int x0, int y0, int x1, int y1, int col)`
Draws a rasterized line onto an `unsigned char` array (`raster`) using the Digital Differential Analyzer (DDA) algorithm.

### `void do_raster_line(JHC_header *head, unsigned char *raster, int x0, int y0, int x1, int y1, int col)`
Draws a rasterized line onto an `unsigned char` array, with options for line thickness.

### `void fill_blob(JHC_header *head, unsigned char *raster, int radpix, int x, int y, int col)`
Fills a circular "blob" of a given radius (`radpix`) at `(x, y)` in an `unsigned char` array with a specified color.

### `void do_raster_float_line(JHC_header *head, float *raster, int x0, int y0, int x1, int y1, float col)`
Draws a rasterized line onto a `float` array.

### `void write_map(Map *outmap, char *outname)`
Writes a `Map` structure (header + data) to a file.

### `Map load_map(char *inname)`
Loads a `Map` structure (header + data) from a file.

### `int free_map(Map *map)`
Frees dynamically allocated memory associated with a `Map` structure.

### `int check_in_map(Map *map, double latitude, double longitude)`
Checks if a given geographic coordinate (`latitude`, `longitude`) falls within the bounds of a `Map`.

### `int map_interp(Map *map, double latitude, double longitude, float *val)`
Performs bilinear interpolation to get a value from a `Map` at a given geographic coordinate.

### `float map_bilinear(float x, float y, float data[4])`
A helper function for bilinear interpolation of a 2x2 grid of values.

## How It Works
The `array` library works by abstracting 2D spatial data into `JHC_header` and `Map` structures.
1.  **Header Management:** Functions like `read_JHC_header` and `write_JHC_header` handle the binary serialization/deserialization of metadata, including dimensions, geographic bounds, data types, and projection information. Byte swapping functions (e.g., `swap_int`, `swap_double`) from `jb_endian.h` are used to ensure cross-platform compatibility.
2.  **Coordinate Transformation:** It relies on external `Project` (from `j_proj.h`) and `inv_proj` (inverse projection) functions to convert between geographic (lat/lon) and map (x/y pixel/grid) coordinates.
3.  **Data Access and Interpolation:** `interp_JHCarray_value` and `get_JHC_lookup_value` implement bilinear interpolation, allowing querying of continuous values from discrete gridded data.
4.  **Rasterization:** `do_DDA_raster_line`, `do_raster_line`, and `fill_blob` provide primitives for drawing vector-like elements onto raster images, essential for annotations or visualizing linear features on maps.
5.  **Map Operations:** `load_map`, `write_map`, and `free_map` offer convenient ways to manage entire map datasets in memory.
This library provides the core functionalities for handling geographic raster data, which is fundamental to many oceanographic processing tasks.
