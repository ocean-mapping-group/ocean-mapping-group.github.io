# OMG Code Usage Guide

This guide provides information on how to use the various tools in the OMG codebase. The information here is extracted from the legacy TiddlyWiki files.

## Getting Started

### How to obtain and compile the code

The code lives on a subversion server located in the OMG offices at UNB. To download the code with read only permissions (you can't commit your changes) use the following commands:

```bash
sudo apt-get install subversion subversion-tools
mkdir ~/code
cd ~/code
svn checkout svn+ssh://omg_user@amundsen.omg.unb.ca/drives/amundsen/disk1/code
```

To enable commit permissions use your OMG account name instead of 'omg_user' or contact someone at OMG:
* Ian Church: ianc@omg.unb.ca
* James Muggah: jmuggah@unb.ca
* Steve Brucker: steveb@omg.unb.ca

### Adding new sounder tool types

This section documents how to add support for a new sonar system.

1.  **Edit `OMG_HDCS_jversion.h` to include support for a new tool**

    1a. Increment the number of tools by 1.

    ```c
    #define NO_TOOLS      47        /* currently */
    ```

    1b. Add the new tooltype in the various "tool_def" arrays in `OMG_HDCS_jversion.h`, for this you need to know the MAXIMUM number of beams that the system can support.

    1c. Add a tool number definition for the new tool.

    ```c
    #define ODOM_ES3        46
    ```

    1d. Add a human-readable tool name in the `tool_names` array.

    1e. Compile to catch any syntax errors, etc:
    ```bash
    make -B OMG_HDCS_jversion.o
    ```

2.  **Add V4 initialization support for the new tool type in `OMG_HDCS_jversion.c`** by editing the `OMG_HDCS_initiate_V4_summary` function.

3.  **Add support for new data type in SwathEd** by updating `SE_mainwin.h`, `SE_mainwin.c`, `SE_omgIOwin.c` and `SE_listwin.c`.

4.  **Write a program to convert the raw data into OMG format.** Examples can be found in `7k2omg.c`, `hypack2omg.c`, `xtf2omg_reson.c`, `gsf2omg.c`.

5.  **Add support for the tool type in `newMergeAtt`** by updating `OMG_get_rational_beams` in `OMG_HDCS_jversion.c` and `get_sounding_geometry.c` in `sonar_geometry.c`.

6.  **Recompile all the OMG programs.**

## Tool Reference

### SVP Tool & WOD

**Introduction**
The OMG SVP Toolkit is used to visualize, manipulate and analyze large volume sound speed profile data sets. It has functionality to access the World Ocean Database (WOD).

**Environment Variables**
*   `OMG_DEFAULT_MAP`: Default 8-bit mapsheet.
*   `WVS_DIR`: For World Vector Shoreline plotting.
*   `WOA01_PATH`: For World Ocean Atlas access.
*   `WOD_PATH`: For World Ocean Database access.
*   `WOD_DATABASE_NAME`: For World Ocean Database access.

**Compiling for WOD**
Requires the `libsqlite3-dev` library.

**Running `svp_tool` with WOD**
Run `svp_tool` with an 8-bit map sheet and click the 'WOD' button.

**Debugging `svp_tool` with WOD**
Use the `-debug_wod` option.

### [edhead](grid/edhead.md)
Allows editing, viewing, and dumping of data in the headers of mapsheets.

### `fixnav`
A tiny program that tests for a backwards time jump in nav data and 'fixes' it.

### `flagNav`
Flags nav fixes in an OMG `.nav` file if `flag[1]` value is greater than the `accept` value.

### [getBounds](omg/getBounds.md)
Creates an index of geographical bounding boxes from a `.merged` file.

### `getHeading`
Gets the average heading of a line from a merged file.

### [inArea](omg/inArea.md)
Checks if a merged file intersects a given geographical area.

### [jview](JV/jview.md)
Used to view omg format mapsheets, backscatter and sidescan data files.

### `mos2`
Creates a mosaic of backscatter intensity. (This seems to be `mapmos` in `sidescan/mapmos/`)

### `omg2hips`
Downgrades a `.merged` file to allow it to be imported into CARIS.

### `stripNav`
Strips details out of a `.merged` file into an ascii or `.nav` file.

### `sumNav`
Does a quick summation of distance and time spanned by a nav file.

### [useCMG](omg/useCMG.md)
Overwrites the ping profile header's heading value with one derived from a filtered course made good.