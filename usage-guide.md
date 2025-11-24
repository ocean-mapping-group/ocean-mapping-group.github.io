# OMG Code Usage Guide

This guide provides information on how to use the various tools in the OMG codebase. The information here is extracted from the legacy TiddlyWiki files.

## How-To Guides

### How to obtain and compile the code

The code lives on a subversion server located in the OMG offices at UNB. To download the code with read only permissions (you can't commit your changes) use the following commands:

```bash
sudo apt-get install subversion subversion-tools
mkdir ~\/code
cd ~\/code
svn checkout svn+ssh://omg_user@amundsen.omg.unb.ca/drives/amundsen/disk1/code
```

To enable commit permissions use your OMG account name instead of 'omg_user' or contact someone at OMG:
* Ian Church: ianc@omg.unb.ca
* James Muggah: jmuggah@unb.ca
* Steve Brucker: steveb@omg.unb.ca

### Adding new sounder tool types

I'm documenting how I've added support for the Odom ES3 system so that others might be able to add support for other systems in the future.

1.  **Edit OMG_HDCS_jversion.h to include support for a new tool**

    1a. Increment the number of tools by 1, the ES3 is the 47th tool that we support.

    ```c
    #define NO_TOOLS      47        /* currently */
    ```

    1b. Add the new tooltype in the various "tool_def" arrays in OMG_HDCS_jversion.h, for this you need to know the MAXIMUM number of beams that the system can support, even though it may operate in modes with fewer beams (we always need to be able to hold the maximum number). Add the new tool type in each array at the very end of the array. In this case, the ES3 is the 47th tool that we support, so it goes into array position 46 in all the arrays (counting from zero). The fields you need to enter are {bytes_per_profile_header,number_beams,bytes_per_beam,dunno}. We'll almost always be adding a V4 tooltype from now on so the actual number of bytes you assign for the profile header and beam structures is actually stored in the file summary header now (and can thus vary by file). The one you need to get right though is the number of beams.

    ```c
    static int tool_defs[NO_TOOLS][4] = {
        /*   0:SingleBeam,        */ {44, 1, 8, 0},
        /*   1:ELAC BottomChartMk1 */ {64, 56, 44, 0},
        ......
        /*  45:OMG GLORIA        */ {1, 1024, 1, 0},   // don't forget a comma after the previous tool that was added
        /*  46:ODOM ES3       */ {64, 480, 64, 0}
    };

    static int packed_tool_defs[NO_TOOLS][4] = {
        /*   0:SingleBeam,        */ {32, 1, 20, 0},
        /*   1:ELAC Bottom_Chart  */ {32, 56, 12, 0},
        .......
        /*  44:SeaBat 7150        */ {32, 880, 12, 0},
        /*  45:OMG GLORIA        */ {32, 1024, 1, 0},
        /*  46:ODOM ES3        */ {64, 480, 64, 0}
    };

    static int packed_tool_defs_v3[NO_TOOLS][4] = {
        /*   0:SingleBeam,        */ {32, 1, 20, 0},
        /*   1:ELAC Bottom_Chart  */ {32, 56, 12, 0},
        ......
        /*  44:SeaBat 7150        */ {272, 880, 28, 0},
        /*  45:OMG GLORIA        */ {1, 480, 1, 0},
        /*  46:ODOM ES3        */ {32, 480, 32, 0}
    };
    ```

    1c. Add a tool number definition for the new tool so that people can use the definition to get at the appropriate array offset. The ES3 is the 47th tool, so it's offset is 46 (counting from zero).

    ```c
    #define SingleBeam        0
    #define ELAC_BottomChart  1
    #define EM12_dual         2
    .....
    #define SeaBat_7150     44
    #define OMG_GLORIA      45
    #define ODOM_ES3        46
    ```

    1d. Add a nice humane tool name, again, at the end of the array in the 46th array position:

    ```c
    static char *tool_names[NO_TOOLS] = {
        "Single Beam Echo-Sounder",
        "HoneyWell Elac BottomChart Mk I",
        "Simrad EM-12 (dual system)",
        "Kongsberg - EM302",
        .....
        "Reson 7125",
        "R2Sonic 2024",
        "Reson 7150",
        "OMG GLORIA",
        "ODOM ES3"
    };
    ```

    1e. Now compile to catch any syntax errors, etc:

    ```bash
    make -B OMG_HDCS_jversion.o
    ```

2.  **Add V4 initialization support for the new tool type in OMG_HDCS_jversion.c.**

    Edit the `OMG_HDCS_initiate_V4_summary` to add support for a tool type. This is the spot where you choose exactly what gets stored in the beam profile header and the beam structures. You can choose amongst the existing fields, e.g. roll, pitch, heading, heave at time of transmit. You can also add your own fields that are specific to the new sensor, e.g. special run time settings that would be meaningless to other systems. A good way to start is to copy and paste the settings for a system that you're familiar with, in this case we'll copy from the 7125 settings. I've copied the relevant section for the 7125 settings and pasted it below with comments inline to explain the logic.

    Once you're done modifying OMG_HDCS_jversion.{c,h}, you should probably recompile all the source code so that all programs will know about the new tool type, e.g. mergeNav.

    ```c
      else if (summary->toolType == ODOM_ES3)
        {

          /* ------------- THE PROFILE FIELD BITS ------------ */
          /* this tells us what fields will actually be stored */

          /* zero'th 32 bits.... */
        // Keeping the basic navigation and time fields
          summary->Profile_BitsDefining[0] =
        PROF_ui_status +
        PROF_ui_numDepths +
        PROF_ui_timeOffset +
        PROF_ui_vesselLatOffset +
        PROF_ui_vesselLongOffset +
        PROF_ui_vesselHeading +
        PROF_si_vesselHeave +
        PROF_si_vesselPitch + PROF_si_vesselRoll + PROF_si_tide +
        /* PROF_ui_vesselVelocity + */  // nobody ever uses this
        0;

    /* ------------------------------------------------------ */
          /* one'th 32 bits.... */
        // Only going to keep the td_sound_speed for now,
        // the rest are all Kongsberg specific
          summary->Profile_BitsDefining[1] =
        /* PROF_uc_power + PROF_uc_TVG + PROF_uc_attenuation + */
        /* PROF_uc_edflag + */
        /* PROF_ui_soundVelocity + */
        /* PROF_ui_lengthImageDataField + */
        /* PROF_ui_pingNo + */
        /* PROF_uc_mode + */
        /* PROF_uc_Q_factor + */
        /* PROF_uc_pulseLength + */
        /* PROF_uc_unassigned + */
        PROF_us_td_sound_speed +
        /* PROF_us_samp_rate +  */
        /* PROF_uc_z_res_cm + PROF_uc_xy_res_cm */ +0;


    /* ------------------------------------------------------ */
          /* two'th 32 bits.... */
        // These are all Kongsberg specific so not using any
          summary->Profile_BitsDefining[2] =
        /* PROF_uc_ssp_source +
           PROF_uc_filter_ID +
           PROF_us_absorp_coeff +
           PROF_us_tx_pulse_len +
           PROF_us_tx_beam_width +
           PROF_us_max_swath_width +
           PROF_uc_tx_power_reduction +
           PROF_uc_rx_beam_width +
           PROF_uc_rx_bandwidth +
           PROF_uc_rx_gain_reduction +
           PROF_uc_tvg_crossover +
           PROF_uc_beam_spacing +
           PROF_uc_coverage_sector + PROF_uc_yaw_stab_mode */ 0;

    /* ------------------------------------------------------ */
          /* three'th 32 bits.... */
        // Keeping some of these in case somebody wants to play with RTK, etc
          summary->Profile_BitsDefining[3] =
        PROF_ss_longperiod_heaveCorrection +
        PROF_ss_dynamic_draftCorrection +
        PROF_ss_deepdraftoffset_in_metres +
        PROF_ss_draft_at_Tx +
    /*
        PROF_ss_alternateRoll +
        PROF_ss_alternatePitch +
        PROF_ss_alternateHeave +
        PROF_us_alternateHeading +
    */
        PROF_us_standaloneHeading +
        PROF_ss_RTK_at_RP +
        PROF_ss_Lowpass_RTK_at_RP +
        PROF_ss_WLZ +
        /* PROF_us_samp_rate_SecondHead +
           PROF_si_clock_drift_millis +
           PROF_ui_watercol_offset +
           PROF_ui_watercol_size +
           PROF_us_range_to_normal_incidence +
           PROF_ui_tx_sector_offset + PROF_us_num_tx_sectors + */ 0;

    /* -------------------------------------------------------------------- */
          /* four'th 32 bits.... */
        // None of these are applicable for the ES3
          summary->Profile_BitsDefining[4] =
        /*PROF_st_params_PORT +
          PROF_st_params_STBD +
          PROF_us_txBeamIndex +
           PROF_us_txLevel +
           PROF_ss_txBeamAngle +
           PROF_us_txPulseLength +
           PROF_ui_ss_offset
           PROF_us_no_skipped_ss +
           PROF_us_no_acquired_ss +
           PROF_us_ss_sample_interval +
           PROF_us_bscatClass +
           PROF_us_nrActualGainSets +
           PROF_ss_rxGup +
           PROF_ss_rxGain +
           PROF_ss_ar +
           PROF_us_rxtimeARRAY +
           PROF_ss_rxgainARRAY */
        0;


    /* -------------------------------------------------------------------- */
          /* five'th 32 bits.... */
        // This stuff's all stored in the .param file anyway
          summary->Profile_BitsDefining[5] =
        /*
           PROF_si_transducerDepth +
           PROF_si_transducerPitch +
           PROF_si_transducerRoll +
           PROF_ui_transducerHeading +
           PROF_si_transducerLatOffset +
           PROF_si_transducerLongOffset +
           PROF_ui_transducerSlantRange +
           PROF_si_transducerAcross +
           PROF_si_transducerAlong +
           PROF_ui_transducerBearing +
         */
        0;


    /* -------------------------------------------------------------------- */
          /* six'th 32 bits.... */
        // These are Reson 7K specific
          summary->Profile_BitsDefining[6] =
        /* PROF_ui_sonar_settings_offset +
        PROF_ui_ping_number +
        PROF_us_multi_ping_sequence +
        PROF_ui_num_beams +
        PROF_uc_layer_compensation_flag +
        PROF_f_bs_beam_position +
        PROF_ui_bs_control_flags +
        PROF_us_bs_num_beams_per_side +
        PROF_us_bs_current_beam_number +
        PROF_uc_bs_sample_descriptor + PROF_ui_snippet_sample_descriptor */
         + 0;

          /* all the unused bit long words....  wiped again just to be sure ... */
          for (i = 7; i < 20; i++)
        summary->Profile_BitsDefining[i] = 0;

    /* -------------------------------------------------------------------- */
    /* ------------- THE BEAM FIELD BITS ------------ */
    /* this tells us what fields will actually be stored */

    /* ------------------------------------------------------ */
          /* zero'th 32 bits.... */
          summary->Beam_BitsDefining[0] = BEAM_ui_status + BEAM_uc_scaling_factor + /* this is just used in the unpack */
        /* but MUST set this bit!!!!!! */
        BEAM_si_observedDepth + BEAM_si_acrossTrack + BEAM_si_alongTrack +
        /* we don't really store the lat and lon on disk  */
        /* BEAM_si_latOffset + */
        /* BEAM_si_longOffset + */
        /* BEAM_si_processedDepth + */
        BEAM_si_timeOffset +
        /* BEAM_si_depthAccuracy + */
        0;


    /* ------------------------------------------------------ */


          /* one'th 32 bits.... */
        // Don't have any backscatter goodies for the ES3 (not that I can tell anyway)
          summary->Beam_BitsDefining[1] =
        /* BEAM_uc_reflectivity + */
        /* BEAM_sc_Q_factor + */
        /* BEAM_uc_beam_no + */
        /* BEAM_uc_freq + */
        /* BEAM_uc_calibratedBackscatter + */
        /* BEAM_uc_mindB + */
        /* BEAM_uc_maxdB + */
        /* BEAM_uc_pseudoAngleIndependentBackscatter */
        +0;


    /* ------------------------------------------------------ */
          /* two'th 32 bits.... */
        // A lot of these are Kongsberg specific but many routines check to see if there's a
        // range measurement to ensure it's a valid beam so should keep this field AND populate
        // it with a non-zero value in the data conversion program
          summary->Beam_BitsDefining[2] =
        BEAM_ui_range +
        /* BEAM_ui_no_samples + BEAM_ui_offset + BEAM_si_centre_no + */
        /* BEAM_uc_sample_unit + */
        /* BEAM_uc_sample_interval + */
        /* BEAM_uc_dummy0 + */
        /* BEAM_uc_dummy1 + */
        /* BEAM_uc_samp_win_length */ +0;


    /* ------------------------------------------------------ */
          /* three'th 32 bits.... */
        * Only going to allow for raw tx and rc steering angles
          summary->Beam_BitsDefining[3] =
        /* BEAM_ss_beam_depress_angle + BEAM_us_beam_heading_angle + */
        /* BEAM_us_other_range */
        + BEAM_ss_Tx_steer + BEAM_ss_Rc_steer +
        /* BEAM_uc_TxSector */ +0;


      /* -------------------------------------------------------------------- */

        * These are Reson 7K specific but the twtt field will be handy
          summary->Beam_BitsDefining[5] =
        BEAM_f_twtt +
        /* BEAM_ui_snippet_first_sample +
        BEAM_ui_snippet_last_sample + BEAM_f_intensity + */
        0;

          printf ("done v4 ODOM ES3 summary bits\n");
      }
    ```

3.  **Add support for new data type in SwathEd** so that we can confirm that stuff is getting into the file as we expect when we write the conversion program afterwards. In short, this consists of searching for a known tooltype in the .c and .h files and then seeing the minor tweaks that might be necessary to do the same for the new tool type. For example, run `fgrep 7125 *.h` to see which .h files have tool type specific lines of code for a Reson 7125. Do the same for .c files with `fgrep 7125 *.c`.You'll need to update SE_mainwin.h, SE_mainwin.c, SE_omgIOwin.c and SE_listwin.c. They're all pretty obvious updates but won't make any sense in isolation here so have a look at the code in each of those to see what to do. The one that's not required but most useful is the updates in SE_listwin.c. This is the code that lets you see the contents of your .merged files in the SwathEd list window. As you write the convertor program in the next step, the list window is a great way to check that things are getting written as you want them to be.

4.  **Write a program to convert the raw data into OMG format.** There's no easy explanation for this, the best way to go about it is to have a look at programs like `7k2omg.c`, `hypack2omg.c`, `xtf2omg_reson.c`, `gsf2omg.c`. You can also look at `RT.c` to see how things are done for Kongsberg systems but it's a pretty complicated program with lots of history so it'll be difficult for a newbie to figure out what's relevant and what's not. I'd recommend looking at `7k2omg.c` as it's pretty new, clean and unencumbered with history or weird little modifications that get hard coded over long years of dealing with funky data.

5.  **Add support for the tool type in newMergeAtt.**

    5a. Update `OMG_get_rational_beams` function in `OMG_HDCS_jversion.c`. Have a look at other systems, you usually need to add a bit of code to help fill out rational fields such as tx/rx steering, twtt, sound speeds, etc.

    5b. Update `get_sounding_geometry.c` in `sonar_geometry.c`. This is where all the juicy bits of code are coded up that are sensor specific. Have a look at other systems and add a case to deal with your new system.

    5c. There's nothing really to do in `newMergeAtt`, other than recompile it once the above changes have been made.

6.  **Recompile all the OMG programs.**

    This is necessary as the programs won't know about the new data type until you recompile. If you don't do this, then weird things can (and will) happen when you run programs like getBounds, mergeNav, etc. You should do this any time you add fields and/or functions to OMG_HDCS_jversion.{c,h}.

## WOD in svp_tool

### Introduction

I've been coding up access for the World Ocean Database 2009 (WOD2009) into svp_tool and it's pretty much ready for general use. This particular functionality is terribly useful when you need to have a peek at the range of oceanographic conditions that have been observed for any given location in the world for whatever reason. For example, Jim Gardner is heading out on a deep water EM122 survey on the Marianas and need to confirm that his Deep Blue XBTs are going to get deep enough to capture the variability in the watermass. We queried WOD and found that the watermass is pretty tame below ~700m so his Deep Blue XBTs would be just fine as they sample down to about that depth at the survey speeds he was planning. If you're really bored and want to see my thought process as this was developed, check out my blog on this: http://2bitbrain.blogspot.com/ I think this would be a tremendous teaching tool for the Oceanography classes as it allows you direct and easy access to data to help explore some of the concepts (e.g. western boundary currents, origin and distribution of water masses). If you want to try this out, read on. If you're never going to use any of those tools then just read the "compiling" section below so that you'll know to safely ignore the error messages when you run 'compile_every_gd_thing'.

### Compiling

The new functionality requires the `libsqlite3-dev` library at compilation time (and `libsqlite3` at runtime, which I've found to be installed on Ubuntu by default). If you want to 'compile_every_gd_thing', it'll choke in `jonnyb/subr/` and `jonnyb/wod/` and `jonnyb/svp/svp_tool/` unless you have `libsqlite3-dev` installed. I've been testing this on Amundsen via ssh and I can get it to compile and run.

### Download and Configuration

I'm looking for beta-testers if you want to give it a spin. You'll find the WOD2009 downloaded into `/homes/share/datasets/WOD2009/` (or something like that). There's also a little script in there to download it to your local hard drive if you want a local copy. You'll need access to that directory and then you'll need to set a few environment variables before running `svp_tool`:

For bashers, edit `~/.bash_profile` and add:
>export WOD_PATH=/homes/share/datasets/WOD2009
>export WOD_DATABASE_NAME=/homes/share/datasets/WOD2009/wod.db3

For tcshers, edit `~/.cshrc` and add:
>setenv WOD_PATH /homes/share/datasets/WOD2009
>setenv WOD_DATABASE_NAME /homes/share/datasets/WOD2009/wod.db3

### Running

After that's done (and you've refreshed your environment), run `svp_tool` with your favourite 8-bit map sheet (it's a little dumb about Lambert projections though). Click the 'WOD' button in the top left of the map window. A little "Query builder" window will pop up: click on the month(s) and instrument(s) of interest (currently only CTD and XBT are supported) and then right-click and drag in the geographic window to extract casts for that location. Note that the right-click and drag will continue to do WOD lookups until you "Exit" the WOD query builder bar (at which point right-click and drag returns to its normal behaviour: selection of profiles in the map window).

### Debugging

If you want a bit more info on what it's doing, run `svp_tool` with the `-debug_wod` option and watch the command line as you make queries. It might help you debug incorrect installations as well if it doesn't quite work out of the box.

## SVP Tool

### Introduction
The OMG SVP Toolkit is used to visualize, manipulate and analyze large volume sound speed profile data sets.

### Environment Variables
There are a number of environment variables that you'll want to set in order to enjoy the full functionality of the toolkit.

The default map that will come up if you don't specify a map. Note that it must be an 8-bit mapsheet (no .r4 files!).
>export OMG_DEFAULT_MAP=/homes/share/datasets/MAPS/world_bathy.8bit

For World Vector Shoreline plotting
>export WVS_DIR=/homes/share/datasets/WVS

This is for World Ocean Atlas access
>export WOA01_PATH=/homes/share/datasets/WOA01

This is for World Ocean Database access
>export WOD_PATH=/homes/share/datasets/WOD2009
>export WOD_DATABASE_NAME=/homes/share/datasets/WOD2009/wod.db3

## OMG Programs

- [edhead](grid/edhead.md)
- [fixnav]()
- [flagNav]()
- [getBounds](omg/getBounds.md)
- [getHeading]()
- [inArea](omg/inArea.md)
- [mos2]()
- [stripNav]()
- [sumNav]()
- [SVP Tool]()
- [useCMG](omg/useCMG.md)

---
*More to come...*