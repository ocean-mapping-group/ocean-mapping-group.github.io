# Welcome to the Ocean Mapping Group Tools Documentation

This documentation aims to provide comprehensive guides and references for the powerful suite of command-line tools developed by the Ocean Mapping Group. These tools are designed for processing, modifying, and interacting with various types of oceanographic data, including multibeam sonar, ADCP, navigation, attitude, and tide records.

## Getting Started

You can navigate through the different tool categories using the sidebar. Each tool's documentation includes a description, usage examples, and detailed explanations of its arguments.

## How to Use This Documentation

*   **Browse by Category:** Tools are organized by their primary function (e.g., ADCP, Navigation, Grid).
*   **Search:** Use the search bar (if enabled by the theme) to quickly find specific tools or functionalities.

### Building and Deploying the Documentation

This documentation is built using [MkDocs](https://www.mkdocs.org/) with the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

To build and preview the documentation locally:

1.  **Install MkDocs:**
    ```bash
    pip install mkdocs mkdocs-material pymdown-extensions
    ```
2.  **Serve the documentation:**
    ```bash
    mkdocs serve
    ```
    This will start a local web server (usually at `http://127.0.0.1:8000`), allowing you to view the documentation in your browser.

3.  **Deploy to GitHub Pages:**
    ```bash
    mkdocs gh-deploy
    ```
    This command will build the documentation and push it to the `gh-pages` branch of your GitHub repository, making it available at your GitHub Pages URL (e.g., `https://username.github.io/repository-name/`).

---

We encourage contributions and feedback to improve this documentation.