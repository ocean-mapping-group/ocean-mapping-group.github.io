---
layout: default
title: printmos
parent: Print Tools
grand_parent: sidescan
nav_order: 1
---
# printmos

## Description
`printmos` is a utility designed for printing mosaics generated from ACRES format image files to a DeskJet printer. It is capable of handling large images by tiling them across multiple pages. The tool adds page numbers and other annotations to the output, making it suitable for producing hardcopy maps of sidescan data.

## Usage
```bash
printmos <acresfile>
```

## Arguments

| Option | Description |
|---|---|
| `<acresfile>` | **Required.** The input ACRES format image file containing the mosaic data. |

## How It Works
1.  **Input File Reading:**
    *   The tool opens the specified `<acresfile>` (an ACRES format image file).
    *   It reads the `acres_header` to get the image dimensions (`dx`, `dy`).
2.  **Page Calculation:**
    *   It calculates the number of horizontal (`x_pages`) and vertical (`y_pages`) pages required to print the entire image, based on predefined maximum dimensions per page (`MAX_DX`, `MAX_DY`).
    *   It also determines the dimensions of each "page" segment (`page_dx`, `page_dy`) and the potentially different dimensions of the last page segments (`last_dx`, `last_dy`).
3.  **Output File Creation:**
    *   It creates an output file (`.las` extension) for the printer commands.
4.  **Page Iteration:** The tool then iterates through each logical page required for printing:
    *   **Page Numbering:** For each page, `pageno` function is called to draw a page number illustration onto a buffer. This illustration indicates the current page's position within the overall grid of pages.
    *   **DeskJet Dithering Setup:** It initializes the DeskJet printer dithering process (`dj_start_dither`) for the current page segment.
    *   **Image Segment Reading:** It seeks within the `acresfile` to the correct position for the current page segment's image data.
    *   **Line-by-Line Dithering:** It reads the image data line by line for the current segment and sends it to the DeskJet printer using `dj_dither_line`.
    *   **Form Feed:** After printing a full page, a form feed command (`dj_formfeed`) is sent to the printer.
5.  **`dmsstring` Function:** A helper function to format degrees, minutes, and seconds into a string for labels (e.g., latitude/longitude annotations).
6.  **Loop:** This process continues until all page segments of the mosaic have been printed.
