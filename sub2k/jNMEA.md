---
layout: default
title: jNMEA
parent: SUB2K Tools
grand_parent: code
nav_order: 3
---
# jNMEA

## Description
`jNMEA` is a C utility library designed for parsing various NMEA 0183 telegrams (GPS messages) into structured C data types. It provides dedicated functions for interpreting common NMEA sentences such as GPVTG (Course Over Ground and Ground Speed), GPZDA (Time, Date, and Local Zone Data), PTNL (Trimble Navigation proprietary message for attitude), GPGLL (Geographic Position - Latitude/Longitude), and GPRMC (Recommended Minimum Specific GPS/TRANSIT Data). The library extracts and converts comma-delimited fields from the raw NMEA strings, handling parsing errors and offering verbose output for debugging.

## Functions

### `void jnmea_read_GPVTG(char *telegram, int tot_char, int verbose_flag, NMEA_GPVTG_telegram *gpvtg_str)`
Parses a GPVTG (Track Made Good and Ground Speed) NMEA telegram.
*   `telegram`: The raw NMEA string.
*   `tot_char`: Total number of characters in the telegram.
*   `verbose_flag`: If `1`, enables verbose output during parsing.
*   `gpvtg_str`: Pointer to an `NMEA_GPVTG_telegram` structure to populate.

### `void jnmea_read_INZDA(char *telegram, int tot_char, int verbose_flag, NMEA_GPZDA_telegram *gpzda_str)`
Parses a GPZDA (Time, Date, and Local Zone Data) NMEA telegram.
*   `telegram`: The raw NMEA string.
*   `tot_char`: Total number of characters in the telegram.
*   `verbose_flag`: If `1`, enables verbose output during parsing.
*   `gpzda_str`: Pointer to an `NMEA_GPZDA_telegram` structure to populate.

### `void jnmea_read_PTNL(char *telegram, int tot_char, int verbose_flag, TRIM_PTNL_telegram *ptnl_str)`
Parses a PTNL (Trimble Navigation proprietary) NMEA telegram, typically containing attitude information like yaw, tilt, and baseline.
*   `telegram`: The raw NMEA string.
*   `tot_char`: Total number of characters in the telegram.
*   `verbose_flag`: If `1`, enables verbose output during parsing.
*   `ptnl_str`: Pointer to a `TRIM_PTNL_telegram` structure to populate.

### `void jnmea_read_GPGLL(char *telegram, int tot_char, int verbose_flag, NMEA_GPGLL_telegram *gpgll_str)`
Parses a GPGLL (Geographic Position - Latitude/Longitude) NMEA telegram.
*   `telegram`: The raw NMEA string.
*   `tot_char`: Total number of characters in the telegram.
*   `verbose_flag`: If `1`, enables verbose output during parsing.
*   `gpgll_str`: Pointer to an `NMEA_GPGLL_telegram` structure to populate.

### `void jnmea_read_INRMC(char *telegram, int tot_char, int verbose_flag, NMEA_GPRMC_telegram *gprmc_str)`
Parses a GPRMC (Recommended Minimum Specific GPS/TRANSIT Data) NMEA telegram.
*   `telegram`: The raw NMEA string.
*   `tot_char`: Total number of characters in the telegram.
*   `verbose_flag`: If `1`, enables verbose output during parsing.
*   `gprmc_str`: Pointer to an `NMEA_GPRMC_telegram` structure to populate.

### `void jnmea_read_INGGA(char *telegram, int tot_char, int verbose_flag, NMEA_GPGGA_telegram *gpgga_str)`
Parses a GPGGA (GPS Fix Data) NMEA telegram.
*   `telegram`: The raw NMEA string.
*   `tot_char`: Total number of characters in the telegram.
*   `verbose_flag`: If `1`, enables verbose output during parsing.
*   `gpgga_str`: Pointer to an `NMEA_GPGGA_telegram` structure to populate.

## How It Works
Each `jnmea_read_*` function follows a similar parsing logic:
1.  **Header Check:** It first checks for the specific NMEA sentence identifier (e.g., "GPVTG", "INZDA") at the beginning of the `telegram` string.
2.  **Field Extraction:** It then iteratively extracts comma-delimited substrings (fields) from the `telegram`.
3.  **Data Conversion:** Based on the field's position (`which_string`), it attempts to convert the extracted substring into the appropriate data type (e.g., `float`, `short`, `int`) and stores it in the corresponding member of the NMEA structure (`gpvtg_str`, `gpzda_str`, etc.).
    *   For latitude and longitude, it parses degrees and minutes, then combines them with direction (N/S, E/W) to form a decimal degree value.
    *   For time fields, it extracts hours, minutes, seconds, and milliseconds.
4.  **Error Handling:** It includes basic error checking, such as detecting unrecognized direction signs or incomplete telegrams, and prints warnings if `verbose_flag` is enabled. If a critical error is found, it typically clears the structure and returns.
5.  **Verbose Output:** If `verbose_flag` is set, it prints intermediate parsing steps and final values to standard output, which is useful for debugging NMEA streams.
