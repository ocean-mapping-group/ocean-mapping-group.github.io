---
layout: default
title: about.c
parent: BPdemo
nav_order: 1
---

# about.c

## Description
`about.c` is a source code file from the `bpdemo` application. It is not a standalone command-line tool.

This file contains the C code responsible for creating the "About" dialog box within the `bpdemo` graphical user interface (GUI). It uses the Motif (Xm) widget toolkit to construct a simple message box that displays information about the application, including its name, version, author, and affiliation.

## Functionality
The primary function in this file, `create_AboutShell`, builds and configures the "About" dialog. When called, it creates a window with the following text:

```
Beam Pattern Phase Stacker Demo v0.1
by
J.E. Hughes Clarke
Ocean Mapping Group
University of New Brunswick, CANADA
```

The dialog also includes an "OK" button that, when clicked, closes the dialog. This is a standard feature in GUI applications to provide credit and version information to the user.