# OMG Code Wiki Information

This information is extracted from the legacy TiddlyWiki files found in the `code/wiki` directory.

## DefaultTiddlers

Welcome

## SiteSubtitle

our latest attempt at documenting the OMG code.

## SiteTitle

OMG Code Wiki

## Welcome

Welcome!  We're trying to document our code.  Wanna help?

## DefaultTiddlers

Welcome

## MainMenu

Welcome
Syntax

## SiteSubtitle

our latest attempt at documenting the OMG code.

## SiteTitle

OMG Code Wiki

## Syntax

#Inline Formatting
|!Option|!Syntax|!Output|
|bold font|```
''bold''
```|''bold''|
|italic type|```
*italic//
```|//italic*|
|underlined text|```
*underlined__
```|__underlined*|
|strikethrough text|```
~~strikethrough--
```|--strikethrough~~|
|superscript text|```
^^super^^script
```|^^super^^script|
|subscript text|```
~~sub~~script
```|~~sub~~script|
|highlighted text|```
@@highlighted@@
```|@@highlighted@@|
|preformatted text|<html><code>```
preformatted
```</code></html>|```
preformatted
```|
#Block Elements
##Headings
```

#Heading 1
##Heading 2
###Heading 3
####Heading 4
#####Heading 5

```
<<<
#Heading 1
##Heading 2
###Heading 3
####Heading 4
#####Heading 5
<<<
##Lists
```

* unordered list, level 1
** unordered list, level 2
*** unordered list, level 3

# ordered list, level 1
## ordered list, level 2
### ordered list, level 3

; definition list, term
: definition list, description

```
<<<
* unordered list, level 1
** unordered list, level 2
*** unordered list, level 3

# ordered list, level 1
## ordered list, level 2
### ordered list, level 3

; definition list, term
: definition list, description
<<<
##Blockquotes
```

> blockquote, level 1
>> blockquote, level 2
>>> blockquote, level 3

<<<
blockquote
<<<

```
<<<
> blockquote, level 1
>> blockquote, level 2
>>> blockquote, level 3

> blockquote
<<<
##Preformatted Text
<html><pre>
```

preformatted (e.g. code)

```
</pre></html>
<<<
```

preformatted (e.g. code)

```
<<<
##Tables
```

|CssClass|k
|!heading column 1|!heading column 2|
|row 1, column 1|row 1, column 2|
|row 2, column 1|row 2, column 2|
|>|COLSPAN|
|ROWSPAN| … |
|~| … |
|CssProperty:value;…| … |
|caption|c

```
''Annotation:''
* The ```
>
``` marker creates a "colspan", causing the current cell to merge with the one to the right.
* The ```
~
``` marker creates a "rowspan", causing the current cell to merge with the one above.
<<<
|CssClass|k
|!heading column 1|!heading column 2|
|row 1, column 1|row 1, column 2|
|row 2, column 1|row 2, column 2|
|>|COLSPAN|
|ROWSPAN| … |
|~| … |
|CssProperty:value;…| … |
|caption|c
<<<
##Images /% TODO %/
cf. [TiddlyWiki.com](http://www.tiddlywiki.com/#EmbeddedImages)
#Hyperlinks
* [WikiWords](WikiWord) are automatically transformed to hyperlinks to the respective tiddler
** the automatic transformation can be suppressed by preceding the respective WikiWord with a tilde (```
~
```): ```
~WikiWord
```
* PrettyLinks are enclosed in square brackets and contain the desired tiddler name: ```
tiddler name
```
** optionally, a custom title or description can be added, separated by a pipe character (```
|
```): ```
[title](target)
```<br>''N.B.:'' In this case, the target can also be any website (i.e. URL).
#Custom Styling
* ```
@@CssProperty:value;CssProperty:value;…@@
```<br>''N.B.:'' CSS color definitions should use lowercase letters to prevent the inadvertent creation of WikiWords.
* <html><code>{{customCssClass{…}}}</code></html>
* raw HTML can be inserted by enclosing the respective code in HTML tags: ```
<html> … </html>
```
#Special Markers
* ```
<br>
``` forces a manual line break
* ```
----
``` creates a horizontal ruler
* [HTML entities](http://www.tiddlywiki.com/#HtmlEntities)
* ```
<<macroName>>
``` calls the respective [macro](Macros)
* To hide text within a tiddler so that it is not displayed, it can be wrapped in ```
/%
``` and ```
%/
```.<br/>This can be a useful trick for hiding drafts or annotating complex markup.
* To prevent wiki markup from taking effect for a particular section, that section can be enclosed in three double quotes: e.g. ```
"**WikiWord**"
```.


## WOD in svp_tool

#Introduction

I've been coding up access for the World Ocean Database 2009 (WOD2009) into svp_tool and it's pretty much ready for general use.  This particular functionality is terribly useful when you need to have a peek at the range of oceanographic conditions that have been observed for any given location in the world for whatever reason.  For example, Jim Gardner is heading out on a deep water EM122 survey on the Marianas and need to confirm that his Deep Blue XBTs are going to get deep enough to capture the variability in the watermass.  We queried WOD and found that the watermass is pretty tame below ~700m so his Deep Blue XBTs would be just fine as they sample down to about that depth at the survey speeds he was planning.  If you're really bored and want to see my thought process as this was developed, check out my blog on this:  http://2bitbrain.blogspot.com/  I think this would be a tremendous teaching tool for the Oceanography classes as it allows you direct and easy access to data to help explore some of the concepts (e.g. western boundary currents, origin and distribution of water masses).  If you want to try this out, read on.  If you're never going to use any of those tools then just read the "compiling" section below so that you'll know to safely ignore the error messages when you run 'compile_every_gd_thing'.

#Compiling
The new functionality requires the libsqlite3-dev library at compilation time (and libsqlite3 at runtime, which I've found to be installed on Ubuntu by default).  If you want to 'compile_every_gd_thing', it'll choke in jonnyb/subr/ and jonnyb/wod/ and jonnyb/svp/svp_tool/ unless you have libsqlite3-dev installed.  I've been testing this on Amundsen via ssh and I can get it to compile and run.

#Download and Configuration
I'm looking for beta-testers if you want to give it a spin.  You'll find the WOD2009 downloaded into /homes/share/datasets/WOD2009/ (or something like that).  There's also a little script in there to download it to your local hard drive if you want a local copy.  You'll need access to that directory and then you'll need to set a few environment variables before running svp_tool:

For bashers, edit ~/.bash_profile and add:
>export WOD_PATH=/homes/share/datasets/WOD2009
>export WOD_DATABASE_NAME=/homes/share/datasets/WOD2009/wod.db3

For tcshers, edit ~/.cshrc and add:
>setenv WOD_PATH /homes/share/datasets/WOD2009
>setenv WOD_DATABASE_NAME /homes/share/datasets/WOD2009/wod.db3

#Running
After that's done (and you've refreshed your environment), run svp_tool with your favourite 8-bit map sheet (it's a little dumb about Lambert projections though).  Click the 'WOD' button in the top left of the map window.  A little "Query builder" window will pop up: click on the month(s) and instrument(s) of interest (currently only CTD and XBT are supported) and then right-click and drag in the geographic window to extract casts for that location.  Note that the right-click and drag will continue to do WOD lookups until you "Exit" the WOD query builder bar (at which point right-click and drag returns to its normal behaviour: selection of profiles in the map window).

#Debugging
If you want a bit more info on what it's doing, run svp_tool with the -debug_wod option and watch the command line as you make queries.  It might help you debug incorrect installations as well if it doesn't quite work out of the box. 

## Welcome

Welcome!  We're trying to document our code.  Wanna help?  Click on "new tiddler" and create an entry about whatever you feel like documenting.  Be sure to use tags so that your documentation can be easily found by others.

## DefaultTiddlers

Welcome

## MainMenu

Welcome
Syntax

## SVP Tool

#Introduction
The OMG SVP Toolkit is used to visualize, manipulate and analyze large volume sound speed profile data sets.

#Environment Variables
There are a number of environment variables that you'll want to set in order to enjoy the full functionality of the toolkit.

The default map that will come up if you don't specify a map.  Note that it must be an 8-bit mapsheet (no .r4 files!).
>export OMG_DEFAULT_MAP=/homes/share/datasets/MAPS/world_bathy.8bit

For World Vector Shoreline plotting
>export WVS_DIR=/homes/share/datasets/WVS

This is for World Ocean Atlas access
>export WOA01_PATH=/homes/share/datasets/WOA01

This is for World Ocean Database access
>export WOD_PATH=/homes/share/datasets/WOD2009
>export WOD_DATABASE_NAME=/homes/share/datasets/WOD2009/wod.db3

## SiteSubtitle

our latest attempt at documenting the OMG code.

## SiteTitle

OMG Code Wiki

## Syntax

#Inline Formatting
|!Option|!Syntax|!Output|
|bold font|```
''bold''
```|''bold''|
|italic type|```
*italic//
```|//italic*|
|underlined text|```
*underlined__
```|__underlined*|
|strikethrough text|```
~~strikethrough--
```|--strikethrough~~|
|superscript text|```
^^super^^script
```|^^super^^script|
|subscript text|```
~~sub~~script
```|~~sub~~script|
|highlighted text|```
@@highlighted@@
```|@@highlighted@@|
|preformatted text|<html><code>```
preformatted
```</code></html>|```
preformatted
```|
#Block Elements
##Headings
```

#Heading 1
##Heading 2
###Heading 3
####Heading 4
#####Heading 5

```
<<<
#Heading 1
##Heading 2
###Heading 3
####Heading 4
#####Heading 5
<<<
##Lists
```

* unordered list, level 1
** unordered list, level 2
*** unordered list, level 3

# ordered list, level 1
## ordered list, level 2
### ordered list, level 3

; definition list, term
: definition list, description

```
<<<
* unordered list, level 1
** unordered list, level 2
*** unordered list, level 3

# ordered list, level 1
## ordered list, level 2
### ordered list, level 3

; definition list, term
: definition list, description
<<<
##Blockquotes
```

> blockquote, level 1
>> blockquote, level 2
>>> blockquote, level 3

<<<
blockquote
<<<

```
<<<
> blockquote, level 1
>> blockquote, level 2
>>> blockquote, level 3

> blockquote
<<<
##Preformatted Text
<html><pre>
```

preformatted (e.g. code)

```
</pre></html>
<<<
```

preformatted (e.g. code)

```
<<<
##Tables
```

|CssClass|k
|!heading column 1|!heading column 2|
|row 1, column 1|row 1, column 2|
|row 2, column 1|row 2, column 2|
|>|COLSPAN|
|ROWSPAN| … |
|~| … |
|CssProperty:value;…| … |
|caption|c

```
''Annotation:''
* The ```
>
``` marker creates a "colspan", causing the current cell to merge with the one to the right.
* The ```
~
``` marker creates a "rowspan", causing the current cell to merge with the one above.
<<<
|CssClass|k
|!heading column 1|!heading column 2|
|row 1, column 1|row 1, column 2|
|row 2, column 1|row 2, column 2|
|>|COLSPAN|
|ROWSPAN| … |
|~| … |
|CssProperty:value;…| … |
|caption|c
<<<
##Images /% TODO %/
cf. [TiddlyWiki.com](http://www.tiddlywiki.com/#EmbeddedImages)
#Hyperlinks
* [WikiWords](WikiWord) are automatically transformed to hyperlinks to the respective tiddler
** the automatic transformation can be suppressed by preceding the respective WikiWord with a tilde (```
~
```): ```
~WikiWord
```
* PrettyLinks are enclosed in square brackets and contain the desired tiddler name: ```
tiddler name
```
** optionally, a custom title or description can be added, separated by a pipe character (```
|
```): ```
[title](target)
```<br>''N.B.:'' In this case, the target can also be any website (i.e. URL).
#Custom Styling
* ```
@@CssProperty:value;CssProperty:value;…@@
```<br>''N.B.:'' CSS color definitions should use lowercase letters to prevent the inadvertent creation of WikiWords.
* <html><code>{{customCssClass{…}}}</code></html>
* raw HTML can be inserted by enclosing the respective code in HTML tags: ```
<html> … </html>
```
#Special Markers
* ```
<br>
``` forces a manual line break
* ```
----
``` creates a horizontal ruler
* [HTML entities](http://www.tiddlywiki.com/#HtmlEntities)
* ```
<<macroName>>
``` calls the respective [macro](Macros)
* To hide text within a tiddler so that it is not displayed, it can be wrapped in ```
/%
``` and ```
%/
```.<br/>This can be a useful trick for hiding drafts or annotating complex markup.
* To prevent wiki markup from taking effect for a particular section, that section can be enclosed in three double quotes: e.g. ```
"**WikiWord**"
```.


## WOD in svp_tool

#Introduction

I've been coding up access for the World Ocean Database 2009 (WOD2009) into svp_tool and it's pretty much ready for general use.  This particular functionality is terribly useful when you need to have a peek at the range of oceanographic conditions that have been observed for any given location in the world for whatever reason.  For example, Jim Gardner is heading out on a deep water EM122 survey on the Marianas and need to confirm that his Deep Blue XBTs are going to get deep enough to capture the variability in the watermass.  We queried WOD and found that the watermass is pretty tame below ~700m so his Deep Blue XBTs would be just fine as they sample down to about that depth at the survey speeds he was planning.  If you're really bored and want to see my thought process as this was developed, check out my blog on this:  http://2bitbrain.blogspot.com/  I think this would be a tremendous teaching tool for the Oceanography classes as it allows you direct and easy access to data to help explore some of the concepts (e.g. western boundary currents, origin and distribution of water masses).  If you want to try this out, read on.  If you're never going to use any of those tools then just read the "compiling" section below so that you'll know to safely ignore the error messages when you run 'compile_every_gd_thing'.

#Compiling
The new functionality requires the libsqlite3-dev library at compilation time (and libsqlite3 at runtime, which I've found to be installed on Ubuntu by default).  If you want to 'compile_every_gd_thing', it'll choke in jonnyb/subr/ and jonnyb/wod/ and jonnyb/svp/svp_tool/ unless you have libsqlite3-dev installed.  I've been testing this on Amundsen via ssh and I can get it to compile and run.

#Download and Configuration
I'm looking for beta-testers if you want to give it a spin.  You'll find the WOD2009 downloaded into /homes/share/datasets/WOD2009/ (or something like that).  There's also a little script in there to download it to your local hard drive if you want a local copy.  You'll need access to that directory and then you'll need to set a few environment variables before running svp_tool:

For bashers, edit ~/.bash_profile and add:
>export WOD_PATH=/homes/share/datasets/WOD2009
>export WOD_DATABASE_NAME=/homes/share/datasets/WOD2009/wod.db3

For tcshers, edit ~/.cshrc and add:
>setenv WOD_PATH /homes/share/datasets/WOD2009
>setenv WOD_DATABASE_NAME /homes/share/datasets/WOD2009/wod.db3

#Running
After that's done (and you've refreshed your environment), run svp_tool with your favourite 8-bit map sheet (it's a little dumb about Lambert projections though).  Click the 'WOD' button in the top left of the map window.  A little "Query builder" window will pop up: click on the month(s) and instrument(s) of interest (currently only CTD and XBT are supported) and then right-click and drag in the geographic window to extract casts for that location.  Note that the right-click and drag will continue to do WOD lookups until you "Exit" the WOD query builder bar (at which point right-click and drag returns to its normal behaviour: selection of profiles in the map window).

#Debugging
If you want a bit more info on what it's doing, run svp_tool with the -debug_wod option and watch the command line as you make queries.  It might help you debug incorrect installations as well if it doesn't quite work out of the box. 

## Welcome

Welcome!  We're trying to document our code.  Wanna help?  Click on "new tiddler" and create an entry about whatever you feel like documenting.  Be sure to use tags so that your documentation can be easily found by others.

## Adding new sounder tool types

I'm documenting how I've added support for the Odom ES3 system so that others might be
able to add support for other systems in the future.

1. Edit OMG_HDCS_jversion.h to include support for a new tool

1a. Increment the number of tools by 1, the ES3 is the 47th tool that we support.

    #define NO_TOOLS      47        /* currently */

1b. Add the new tooltype in the various "tool_def" arrays in OMG_HDCS_jversion.h, for this you need to know the MAXIMUM number of beams that the system can support, even though it may operate in modes with fewer beams (we always need to be able to hold the maximum number).  Add the new tool type in each array at the very end of the array.  In this case, the ES3 is the 47th tool that we support, so it goes into array position 46 in all the arrays (counting from zero).  The fields you need to enter are {bytes_per_profile_header,number_beams,bytes_per_beam,dunno}.  We'll almost always be adding a V4 tooltype from now on so the actual number of bytes you assign for the profile header and beam structures is actually stored in the file summary header now (and can thus vary by file).  The one you need to get right though is the number of beams. 


    static int tool_defs[NO_TOOLS][4]
    {
    /*   0:SingleBeam,        */ {44, 1, 8, 0},
    /*   1:ELAC BottomChartMk1 */ {64, 56, 44, 0},
    ......
    /*  45:OMG GLORIA       */ {1, 1024, 1, 0},   <---- don't forget a comma after the previous tool that was added
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

1c. Add a tool number definition for the new tool so that people can use the definition to get at the appropriate array offset.  The ES3 is the 47th tool, so it's offset is 46 (counting from zero).

    #define SingleBeam        0
    #define ELAC_BottomChart  1
    #define EM12_dual         2
    .....
    #define SeaBat_7150     44
    #define OMG_GLORIA      45
    #define ODOM_ES3        46

1d. Add a nice humane tool name, again, at the end of the array in the 46th array position:

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

1e. Now compile to catch any syntax errors, etc:
    make -B OMG_HDCS_jversion.o

2. Add V4 initialization support for the new tool type in OMG_HDCS_jversion.c.

Edit the OMG_HDCS_initiate_V4_summary to add support for a tool type.  This is the spot
where you choose exactly what gets stored in the beam profile header and the beam structures.
You can choose amongst the existing fields, e.g. roll, pitch, heading, heave at time of transmit.
You can also add your own fields that are specific to the new sensor, e.g. special run time settings
that would be meaningless to other systems.  A good way to start is to copy and paste the settings for
a system that you're familiar with, in this case we'll copy from the 7125 settings.  I've copied the
relevant section for the 7125 settings and pasted it below with comments inline to explain the logic.

Once you're done modifying OMG_HDCS_jversion.{c,h}, you should probably recompile all the source code so that
all programs will know about the new tool type, e.g. mergeNav.

  ....
  else if (summary->toolType == ODOM_ES3)
    {

      /* ~~----------- THE PROFILE FIELD BITS ----------~~ */
      /* this tells us what fields will actually be stored */

      /* zero'th 32 bits.... */
    * Keeping the basic navigation and time fields
      summary->Profile_BitsDefining[0] =
    PROF_ui_status +
    PROF_ui_numDepths +
    PROF_ui_timeOffset +
    PROF_ui_vesselLatOffset +
    PROF_ui_vesselLongOffset +
    PROF_ui_vesselHeading +
    PROF_si_vesselHeave +
    PROF_si_vesselPitch + PROF_si_vesselRoll + PROF_si_tide +
    /* PROF_ui_vesselVelocity + */  * nobody ever uses this
    0;

/* ~~--------------------------------------------------~~ */
      /* one'th 32 bits.... */
    * Only going to keep the td_sound_speed for now,
    * the rest are all Kongsberg specific
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


/* ~~--------------------------------------------------~~ */
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
       PROF_uc_coverage_sector + PROF_uc_yaw_stab_mode + */ 0;

/* ~~--------------------------------------------------~~ */
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

/* ~~--------------------------------------------------~~ */


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
       PROF_ss_rxgainARRAY + */
    0;



/* ~~--------------------------------------------------~~ */
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


/* ~~--------------------------------------------------~~ */
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

/* ~~------------------------------------------------------------------ */
/* ------------- THE BEAM FIELD BITS ------------ */
/* this tells us what fields will actually be stored */

/* ----------------------------------------------------~~ */
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


/* ~~--------------------------------------------------~~ */


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


/* ~~--------------------------------------------------~~ */
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


/* ~~--------------------------------------------------~~ */
      /* three'th 32 bits.... */
    * Only going to allow for raw tx and rc steering angles
      summary->Beam_BitsDefining[3] =
    /* BEAM_ss_beam_depress_angle + BEAM_us_beam_heading_angle + */
    /* BEAM_us_other_range */
    + BEAM_ss_Tx_steer + BEAM_ss_Rc_steer +
    /* BEAM_uc_TxSector */ +0;


  /* ~~----------------------------------------------------------------~~ */

    * These are Reson 7K specific but the twtt field will be handy
      summary->Beam_BitsDefining[5] =
    BEAM_f_twtt +
    /* BEAM_ui_snippet_first_sample +
    BEAM_ui_snippet_last_sample + BEAM_f_intensity + */
    0;

      printf ("done v4 ODOM ES3 summary bits\n");
  }


3. Add support for new data type in SwathEd so that we can confirm that stuff is getting into the file as we expect when we write the conversion program afterwards.  In short, 
this consists of searching for a known tooltype in the .c and .h files and then seeing the minor tweaks that might be necessary to do the same for the new tool type.  For example, run 'fgrep 7125 *.h' to see which .h files have tool type specific lines of code for a Reson 7125.  Do the same for .c files with 'fgrep 7125 *.c'.You'll need to update SE_mainwin.h, SE_mainwin.c, SE_omgIOwin.c and SE_listwin.c.  They're all pretty obvious updates but won't make any sense in isolation here so have a look 
at the code in each of those to see what to do.  The one that's not required but most useful is the updates in SE_listwin.c.  This is the code that lets you see the contents of
 your .merged files in the SwathEd list window.  As you write the convertor program in the next step, the list window is a great way to check that things are getting written as
 you want them to be.4. Write a program to convert the raw data into OMG format.  There's no easy explanation for this, the best way to go about it is to have a look at programs like 7k2omg.c, hypa
ck2omg.c, xtf2omg_reson.c, gsf2omg.c.  You can also look at RT.c to see how things are done for Kongsberg systems but it's a pretty complicated program with lots of history so 
it'll be difficult for a newbie to figure out what's relevant and what's not.  I'd recommend looking at 7k2omg.c as it's pretty new, clean and unencumbered with history or weir
d little modifications that get hard coded over long years of dealing with funky data.

5. Add support for the tool type in newMergeAtt.

5a. Update OMG_get_rational_beams function in OMG_HDCS_jversion.c.  Have a look at other systems, you usually need to add a bit of code to help fill out rational fields such as tx/rx steering, twtt, sound speeds, etc.

5b. Update get_sounding_geometry.c in sonar_geometry.c.  This is where all the juicy bits of code are coded up that are sensor specific.  Have a look at other systems and add a
 case to deal with your new system.

5c. There's nothing really to do in newMergeAtt, other than recompile it once the above changes have been made.

6. Recompile all the OMG programs.

This is necessary as the programs won't know about the new data type until you recompile.  If you don't do this, then weird things can (and will) happen when you run programs like getBounds, mergeNav, etc.  You should do this any time you add fields and/or functions to OMG_HDCS_jversion.{c,h}.





## DefaultTiddlers

Welcome



## How to obtain and compile the code

The code lives on a subversion server located in the OMG offices at UNB. To download the code with read only permissions (you can't commit your changes) use the following commands:

sudo apt-get install subversion subversion-tools
mkdir ~/code (Make a code directory in your home folder)
cd ~/code
svn checkout svn+ssh://omg_user@amundsen.omg.unb.ca/drives/amundsen/disk1/code

To enable commit permissions use your OMG account name instead of 'omg_user' or contact someone at OMG:
Ian Church: ianc@omg.unb.ca
James Muggah: jmuggah@unb.ca
Steve Brucker: steveb@omg.unb.ca

## Howtos

How to obtain and compile the code
Adding new sounder tool types
WOD in svp_tool

## MainMenu

Welcome
Wiki Syntax
#Main Menu:
OMG Programs
Howtos

## OMG Programs

Program Wiki Template

edhead
fixnav
flagNav
getBounds
getHeading
inArea
mos2
stripNav
sumNav
SVP Tool
useCMG



## Program Wiki Template

```
''program name and quick description''
```

```
!!Summary:
```
```
*detail1
```
```
*detail2
```

```
''Note!'' Important info...
```

```
!!Options:
```
```
:-option1 (detail)
```
```
:-option2 (detail)
```

```
!!Usage (syntax):
```
```
:program -option1 filename -option2 123 123 -in filename -out filename
```

```
!!Used for:
```
```
*example of how it's used [External Link ]( http://www.omg.unb.ca)
```
```
*this program solves xxxxx problem....
```

## SVP Tool

#Introduction
The OMG SVP Toolkit is used to visualize, manipulate and analyze large volume sound speed profile data sets.

#Environment Variables
There are a number of environment variables that you'll want to set in order to enjoy the full functionality of the toolkit.

The default map that will come up if you don't specify a map.  Note that it must be an 8-bit mapsheet (no .r4 files!).
>export OMG_DEFAULT_MAP=/homes/share/datasets/MAPS/world_bathy.8bit

For World Vector Shoreline plotting
>export WVS_DIR=/homes/share/datasets/WVS

This is for World Ocean Atlas access
>export WOA01_PATH=/homes/share/datasets/WOA01

This is for World Ocean Database access
>export WOD_PATH=/homes/share/datasets/WOD2009
>export WOD_DATABASE_NAME=/homes/share/datasets/WOD2009/wod.db3

## SiteSubtitle

our latest attempt at documenting the OMG code.

## SiteTitle

OMG Code Wiki

## Syntax

#Inline Formatting
|!Option|!Syntax|!Output|
|bold font|```
''bold''
```|''bold''|
|italic type|```
*italic//
```|//italic*|
|underlined text|```
*underlined__
```|__underlined*|
|strikethrough text|```
~~strikethrough--
```|--strikethrough~~|
|superscript text|```
^^super^^script
```|^^super^^script|
|subscript text|```
~~sub~~script
```|~~sub~~script|
|highlighted text|```
@@highlighted@@
```|@@highlighted@@|
|preformatted text|<html><code>```
preformatted
```</code></html>|```
preformatted
```|
#Block Elements
##Headings
```

#Heading 1
##Heading 2
###Heading 3
####Heading 4
#####Heading 5

```
<<<
#Heading 1
##Heading 2
###Heading 3
####Heading 4
#####Heading 5
<<<
##Lists
```

* unordered list, level 1
** unordered list, level 2
*** unordered list, level 3

# ordered list, level 1
## ordered list, level 2
### ordered list, level 3

; definition list, term
: definition list, description

```
<<<
* unordered list, level 1
** unordered list, level 2
*** unordered list, level 3

# ordered list, level 1
## ordered list, level 2
### ordered list, level 3

; definition list, term
: definition list, description
<<<
##Blockquotes
```

> blockquote, level 1
>> blockquote, level 2
>>> blockquote, level 3

<<<
blockquote
<<<

```
<<<
> blockquote, level 1
>> blockquote, level 2
>>> blockquote, level 3

> blockquote
<<<
##Preformatted Text
<html><pre>
```

preformatted (e.g. code)

```
</pre></html>
<<<
```

preformatted (e.g. code)

```
<<<
##Tables
```

|CssClass|k
|!heading column 1|!heading column 2|
|row 1, column 1|row 1, column 2|
|row 2, column 1|row 2, column 2|
|>|COLSPAN|
|ROWSPAN| … |
|~| … |
|CssProperty:value;…| … |
|caption|c

```
''Annotation:''
* The ```
>
``` marker creates a "colspan", causing the current cell to merge with the one to the right.
* The ```
~
``` marker creates a "rowspan", causing the current cell to merge with the one above.
<<<
|CssClass|k
|!heading column 1|!heading column 2|
|row 1, column 1|row 1, column 2|
|row 2, column 1|row 2, column 2|
|>|COLSPAN|
|ROWSPAN| … |
|~| … |
|CssProperty:value;…| … |
|caption|c
<<<
##Images /% TODO %/
cf. [TiddlyWiki.com](http://www.tiddlywiki.com/#EmbeddedImages)
#Hyperlinks
* [WikiWords](WikiWord) are automatically transformed to hyperlinks to the respective tiddler
** the automatic transformation can be suppressed by preceding the respective WikiWord with a tilde (```
~
```): ```
~WikiWord
```
* PrettyLinks are enclosed in square brackets and contain the desired tiddler name: ```
tiddler name
```
** optionally, a custom title or description can be added, separated by a pipe character (```
|
```): ```
[title](target)
```<br>''N.B.:'' In this case, the target can also be any website (i.e. URL).
#Custom Styling
* ```
@@CssProperty:value;CssProperty:value;…@@
```<br>''N.B.:'' CSS color definitions should use lowercase letters to prevent the inadvertent creation of WikiWords.
* <html><code>{{customCssClass{…}}}</code></html>
* raw HTML can be inserted by enclosing the respective code in HTML tags: ```
<html> … </html>
```
#Special Markers
* ```
<br>
``` forces a manual line break
* ```
----
``` creates a horizontal ruler
* [HTML entities](http://www.tiddlywiki.com/#HtmlEntities)
* ```
<<macroName>>
``` calls the respective [macro](Macros)
* To hide text within a tiddler so that it is not displayed, it can be wrapped in ```
/%
``` and ```
%/
```.<br/>This can be a useful trick for hiding drafts or annotating complex markup.
* To prevent wiki markup from taking effect for a particular section, that section can be enclosed in three double quotes: e.g. ```
"**WikiWord**"
```.


## WOD in svp_tool

#Introduction

I've been coding up access for the World Ocean Database 2009 (WOD2009) into svp_tool and it's pretty much ready for general use.  This particular functionality is terribly useful when you need to have a peek at the range of oceanographic conditions that have been observed for any given location in the world for whatever reason.  For example, Jim Gardner is heading out on a deep water EM122 survey on the Marianas and need to confirm that his Deep Blue XBTs are going to get deep enough to capture the variability in the watermass.  We queried WOD and found that the watermass is pretty tame below ~700m so his Deep Blue XBTs would be just fine as they sample down to about that depth at the survey speeds he was planning.  If you're really bored and want to see my thought process as this was developed, check out my blog on this:  http://2bitbrain.blogspot.com/  I think this would be a tremendous teaching tool for the Oceanography classes as it allows you direct and easy access to data to help explore some of the concepts (e.g. western boundary currents, origin and distribution of water masses).  If you want to try this out, read on.  If you're never going to use any of those tools then just read the "compiling" section below so that you'll know to safely ignore the error messages when you run 'compile_every_gd_thing'.

#Compiling
The new functionality requires the libsqlite3-dev library at compilation time (and libsqlite3 at runtime, which I've found to be installed on Ubuntu by default).  If you want to 'compile_every_gd_thing', it'll choke in jonnyb/subr/ and jonnyb/wod/ and jonnyb/svp/svp_tool/ unless you have libsqlite3-dev installed.  I've been testing this on Amundsen via ssh and I can get it to compile and run.

#Download and Configuration
I'm looking for beta-testers if you want to give it a spin.  You'll find the WOD2009 downloaded into /homes/share/datasets/WOD2009/ (or something like that).  There's also a little script in there to download it to your local hard drive if you want a local copy.  You'll need access to that directory and then you'll need to set a few environment variables before running svp_tool:

For bashers, edit ~/.bash_profile and add:
>export WOD_PATH=/homes/share/datasets/WOD2009
>export WOD_DATABASE_NAME=/homes/share/datasets/WOD2009/wod.db3

For tcshers, edit ~/.cshrc and add:
>setenv WOD_PATH /homes/share/datasets/WOD2009
>setenv WOD_DATABASE_NAME /homes/share/datasets/WOD2009/wod.db3

#Running
After that's done (and you've refreshed your environment), run svp_tool with your favourite 8-bit map sheet (it's a little dumb about Lambert projections though).  Click the 'WOD' button in the top left of the map window.  A little "Query builder" window will pop up: click on the month(s) and instrument(s) of interest (currently only CTD and XBT are supported) and then right-click and drag in the geographic window to extract casts for that location.  Note that the right-click and drag will continue to do WOD lookups until you "Exit" the WOD query builder bar (at which point right-click and drag returns to its normal behaviour: selection of profiles in the map window).

#Debugging
If you want a bit more info on what it's doing, run svp_tool with the -debug_wod option and watch the command line as you make queries.  It might help you debug incorrect installations as well if it doesn't quite work out of the box. 

## Welcome

Welcome!  We're trying to document our code.  

Wanna help?  Click on "new tiddler" and create an entry about whatever you feel like documenting.  Be sure to use tags so that your documentation can be easily found by others. 

Add your entry to the appropriate page linked on the left.

To see a template for a new program entry, click on 'OMG Programs' on the left and view the 'Program Wiki Template'

## edhead

''edhead (allows editing, viewing, and dumping of data in the headers of mapsheets)''

##Summary:
*detail1
*detail2

''Note!'' Important info...

##Options:
:-option1 (detail)
:-option2 (detail)

##Usage (syntax):
:program -option1 filename -option2 123 123 -in filename -out filename

##Used for:
*example of how it's used [External Link ]( http://www.omg.unb.ca)
*this program solves xxxxx problem....

##Bugs:
```

Not sure if this was always the case or if the newer version of geotifcp is pickier but it is quite sensitive to a particular line of the geo_meta file.

So far this only applies to UTM geo tifs.

The following error occurs when the number in the brackets (Ascii,66) doesn't match the number of chars in the message:

Parsing Error at 'PCSCitationGeoKey (Ascii,14): "UTM Zone  2N"'
Failure in GTIFImport

In this case it needs to read: (Ascii,13) (two spaces before the 2)

The error will cause the geo tiff creation to fail and results in a file size of 8 bytes.

Thanks to Povl Abrahamsen who noticed the problem in his webgrid tarball and mentioned it. Yay bug reports!

I modded the following lines of edhead.c to fudge a fix:

if (UTM_zone)
        fprintf (outfile, "\t\tPCSCitationGeoKey (Ascii,13): \"UTM Zone %2d",
                 UTM_zone);
      else
        fprintf (outfile,
                 "\t\tPCSCitationGeoKey (Ascii,21): \"UTM...Custom Zone, ");

```

## fixnav

''fixnav. Tiny program that tests for a backwards time jump (of one day??) in nav data and 'fixes' it. This is an old program that solved this particular program in EM 100 data.''

##Summary:
*opens a nave file and runs through it looking for a backwards 'day jump'
*'corrects' the nav fix time by adding or subtracting day(s) worth of time:
*nav_rec.time -= 24 * 60 * 60 * back_flag;

##Options:
:-v (verbose)
:-testonly (don't write changes to file)
:-skip (initiallizes 'back_flag' to a predetermined value. This should enable day sized offsets??)

##Usage (syntax):
:fixnav -testonly filename.nav

##Used for:
*example of how it's used [External Link ]( http://www.omg.unb.ca)
*this program solves xxxxx problem....

## flagNav

''flagNav. A small program that is supposed to flag nav fixes (in an OMG .nav file) if it's 'flag[1] value is greater than the 'accept' value entered on the command line''

##Summary:
*opens and spins though a .nav file
*checks if (tide_rec.flag[1] >= accept) 
*sets tide_rec.flag[3] = 0; if true
*sets tide_rec.flag[3] = 1; if not

''Note!" This writes changes directly into the file!
''Note!'' This doesn't seem to work?? Not really sure what is going on... What is flag[1] value? Quality factor??


##Options:
:-v (verbose)
:-ascii (not implemented)
:-accept 2 (integer)
:-comp (not implemented)

##Usage (syntax):
:flagNav -v -accept 2 filename.nav

##Used for:
*example of how it's used [External Link ]( http://www.omg.unb.ca)
*this program solves xxxxx problem....

## getBounds

''getBounds is used to create an index of geographical bounding boxes from a .merged file. This will work for both multibeam and sub bottom & sidescan format files''

##Summary:
*will accept a series of filenames (ie: *.merged)
*opens .merged file for read + write
*creates (or opens existing) 2 files for 100 ping bounds and global bounds
*''now the good stuff:''
*each beam of a file is checked for it's lat, lon, and time.
*bounding boxes for each 100 pings are created and dumped
*a global bounds is also determined for the file
*all the 100 ping bounds (plus remainder at end) are dumped into a .100ping_bounds file with the same prefix as the .merged file
*the global bounds are dumped to a .file_bounds file
*the global bounds are also written into the .merged summary header (this is used by make_blank -boundsof (and others??)

''Note!'' 
*This program is currently succeptable (sp?) to bad nav which will propagate through into the 100 ping bounds
*the 100 ping bounds are relative to the summary header reflat and reflon etc. They must be applied to these correctly to extract a proper lat, lon, time.
*the global bounds (one set of coords per file) are stored as complete lat, lon & time.

##Options:
:-v (verbose)
:-do_anyway (needed for singlebeam?? files)
:-first 10 (start at ping 10)
:-last 200 (end at ping 200)


##Usage (syntax):
:getBounds *.merged
:getBounds -first 10 -last 100 line1.merged
:getBounds -do_anyway k320_file1.merged

##Used for:
*used always, many programs take advantage of this file to speed up searches (ie: weigh_grid)


## getHeading

''getHeading   used to get the average heading of a line (multibeam) from a merged file''

##Summary:
*reads merged files from the command line
*outputs the line name and average heading to the output text file

''Note!'' This is average heading on a ping by ping basis, turns will still have an average heading

##Options:
:-xyzlist path to line list (a text file with the path(s) to a list of merged file(s))
:-skip 10 (Skips 10 pings, useful for longer lines)

##Usage:
:getHeading -out filename filename(s).merged

##Used for:
*get the average heading from an OMG merged file
*this program will help when trying to create a survey line list where most lines are parallel.
*example command after getHeading has been run to find lines in a specific direction. Here the survey lines run were 58 degrees and 238 degrees.
```

cat outfilename | awk '{if ($2 > 52 && $2 < 64 || $2 > 232 && $2 < 244) print $1,$2}'

```
This command looks for lines with a heading between 52 and 64 degrees or a heading between 232 and 244 degrees. It will then print out the filename and the heading that meet that criteria. The range of headings is used because survey line running is never exact.

## inArea

''inArea, by default, prompts the user for top left and bottom right coordinates of a mapsheet and check to see if a command line supplied merged file intersects it.''

##Summary
*reads merged file names from command line.
*also accepts merged_input.list (xyzlist) as input.
*prompts user for coordinates or reads a header from a supplied OMG map header.
*spins through merged file and checks to see if any beams(?) fall inside the map bounds.
*it can also utilize 100 ping bounds files to speed the process up.

##Options:
:-v (verbose, more output!)
:-usebounds (program will look for a 100 ping bounds file of same prefix as merged file. Uses it to speed things up)
:-exact (this option is passed to external function that checks a merged file manually. This isn't needed if you use -usebounds option)
:-array filename (will read a box header or mapsheet header to get search coordinates).
:-area filename (same as -array)
:-xyzlist filename (reads names/paths of merged files from file)

##Used for:
*Checking whether a merged file(s) intersect a mapsheet or geographical area


## jview

''jview is used to view omg format mapsheets (both 8 bit and floating point) as well as backscatter and sidescan data files.''

##Summary:
*detail1
*detail2

''Note!'' Important info...

##Options:
:-option1 (detail)
:-option2 (detail)

##Usage:
:program -option1 filename -option2 123 123 -in filename -out filename

##Used for:
*example of how it's used [External Link ]( http://www.omg.unb.ca)
*this program solves xxxxx problem....

## mos2

''mos2   creates a mosaic of backscatter intensity''

##Summary:
*reads ss files from the command line
*by default lists the options for creating a mosaic of backscatter intensity


##Options:
:-v (verbose output)
:-fresh_start (use this when mosaicing a new mos file or overwriting an existing mos file)
:-xyzlist path_to_line_list (a text file with the path to a list of ss file(s))
:-swap_dirs ss/ merged/ (if you have a merged xyzlist from weigh_grid, use swap_dirs rather than creating a new ss list)
:-custom_weight asciicustomweightsfile (mosaic using a custom weight file, can provide more emphasis on nadir beams for example)
:-gloria or -beam or -mr1 (defaults to gloria) 
:(-addDN 4 (only works on -aibs data !!(now sidescan too)) 
:(-pulselenDNshift 700 5 (in microsecs in DN's)
:(-aibs or -calb or -refl for -beam option) 
:(-apply_shifts) ... apply DN shifts found in .dn_shift file for each line
:(-dBwrap -10) 
:(-just_drop) 
:(-MINinvalid 254) 
:(-MAXinvalid 100) 
:(-azirange 200 300 ***NOTE low to high including 340 20(380) logic!) 
:(-time_start 2000 145 16 22 00 -time_end 2000 145 16 28 30 ) 
:(-mergedpath ../merged/ ) 
:(-subtract ) 
:(-useallss) 
:(-skip 10 ) 
:(-maxdist 100 (def. 5m)) 
:(-maxtime 100 (def. 10se)) 
:(-maxazi 10 (def. 5deg)) 
:(-maxacross 900 (m))
:(-declin 21.0 ) 
:(-pixshift x y ) 
:(-no_autoseam) 
:(-no_auto_dg) 
:-select (will ask you for the first and last ping of each file )

##Usage:
:mos2 mos_prefix omg_ss_file(s)
:mos2 -fresh_start -maxdist 30 mos_prefix omg_ss_file(s)

##Used for:
*Creating a mosaic from multibeam ss file(s)

##Troubleshooting:
*if a mos2: malloc.c:3096 error occurs, check how big the array size is of your mapsheet. If it is less than 500 in either x or y, edit your local code:
:code/subr/cache.h
locate the lines:
```

#define CACHE_MAXBLOCKS 1500
#define CACHE_BLOCKSIZE 1024

```
now edit the CACHE_BLOCKSIZE smaller (ie. 512 or 256...) and then double however many halves you did to the CACHE_MAXBLOCKS (3000 or 6000...). Another solution would be to just increase your array size.
*Short explaination: When mosaicing in the early 90's there was not enough memory to load in a large array so Guy Carpenter wrote a program to work on a subset of the mosaic at one time. The cache_blocksize is this subset size and the maxblocks is how many of these subsets you can have (I think). Anyway, if your x or y array size is too small, the subset will wrap around the image and weird things start to happen.

## omg2hips

omg2hips will downgrade a .merged file to allow it to be imported into CARIS.

A new field Ifremer_q_factor was added, changing the byte order by 4. Unflagged the Ifremer_q_factor in the summary header and subtracted 4 from the totalBeamBytes.
NOTE: Do not run this on a file you previously downgraded.

Updated the OMG_HDCS_jversion files to add a new OMG_HDCS_dump_summary_hips function.

Program is run as follows:

omg2hips -in filename.merged -out filename_HIPS.merged

## stripNav

''stripNav. Strips various details out of an OMG .merged file and drops it into either an ascii file or an OMG .nav file.''

##Summary:
*opens a .nav file for writing
*opens .merged file(s) for reading
*if the file is gloria format (sidescan, etc.) it spins through and extracts time, lat, lon, azi, depth and writes them as desired
*if the file is a .merged file (HDCS) it spins through and extracts time, tide, and one of: (roll, pitch, heave, heading(default)) if indicated in options
*writes the results out to an ascii file or .nav (binary) file
*ascii format is: JD hh mm intsec decsec timesince1970 heading roll pitch heave (time is that of ping):
**228 23 9 46 0.520 1187305786.520 206.76   0.68   0.51 -0.400*

''Note:'' If you specify ascii file output, all of the above fields are output. If you don't specify ascii then a binary file is output (.nav format) with only the one selected field (heading is default) inserted into the azi field.

''Output of navedit after stripNav run (modified field in bold)'': //58.99755773  -93.82780642  -669  0.000 ''206.729'' 2007 228 ( 8 16) 23  9 46.81 0 0 0 0//


##Options:
:-v (verbose)
:-ss (work on a gloria format ss file)
:-unique (prevents non-unique nav solutions from being considered)
:-roll (selects roll to be inserted into azi field in .nav format output file) (not needed if -ascii selected)
:-pitch (selects pitch to be inserted into azi field in .nav format output file) (not needed if -ascii selected)
:-heave (selects heave to be inserted into azi field in .nav format output file) (not needed if -ascii selected)
:-heading (selects heading to be inserted into azi field in .nav format output file) (not needed if -ascii selected)
:-ascii (the output file will be ascii and in the format shown above)
:-skip 10 (only reads every 10th ping and outputs its info)
:-comp filename.nav (or filename.txt, etc) (This is the name of the output file)


##Usage (syntax):
:stripNav -comp test.nav 0099_20070816_230946.merged
:stripNav -roll -comp test.nav 0099_20070816_230946.merged
:stripNav -ascii -comp test.ascii 0099_20070816_230946.merged

##Used for:
*example of how it's used [External Link ]( http://www.omg.unb.ca)
*this program solves xxxxx problem....

## sumNav

''sumNav does a quick summation of distance and time spanned by nav file''

##Summary:
*opens the nav or ascii file for reading
*spins through the file(s), calculating distance and time elapsed between nav entries
*sums the totals both by file and by total of the files supplied
*spits the results out to the terminal

''Note!'' 
*If you read an ascii nav file you must supply the speed of the ship to calculate an elapsed time (default is 8.0 knots)
*ascii format: lat lon float (decimal degrees. the last (floating point) value is required but not used !?)

##Options:
:-v (verbose)
:-ascii (read an ascii nav file)
:-speed_knots 8 (ship speed, used for ascii files. Default is 8.0 kts)
:-skip 10 (reads only every 10th nav entry (binary .nav only), default is 1)
:-maxjump 0.2 (ignores distance changes larger than 0.2 km, default is 0.5)

Note!! There is a -comp option in the code, this is not used for anything!

##Usage (syntax):
:sumNav *.nav
:sumNav -ascii file.txt
:sumNav -maxjump 0.6 -skip 10 file.nav


##Used for:
*example of how it's used [External Link ]( http://www.omg.unb.ca)
*this program solves xxxxx problem....

## useCMG

''useCMG, by default, overwrites the value of the ping profile header with one derived from a 3 ping filtered course made good (position in ping headers).''

##Summary: 
*Reads heading and position from each ping.
*Low pass filters the course made good (from the position changes).
*Low pass filters the heading.
*Subtracts the low pass filtered heading from the heading to provide a high pass filtered heading.
*Merges the high pass filtered heading with the low pass filtered course made good.
*Write the ping header with the new heading to file.

‘’Note!'’ If there is no heading stored (in knudsen sidescan data for example) the value stored in the heading field will be only the low pass filtered course made good.

##Options:
:-filtlen 7 (changes the filter length to 7 samples, 3 is default)
:-test (don’t actually save the new heading to the ping profile header)
:-v (verbose, dumps out info on a per ping basis)

##Used for:
*outputting values for various testing needs. See [Amundsen Heading Analysis ]( http://www.omg.unb.ca/~steveb/heading_processing/)
*create a heading from the position info where no heading previously existed (needed for knudsen sidescan for example)
*filter a bad heading that has a good high frequency component with course made good

