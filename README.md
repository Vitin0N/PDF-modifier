# PDF Modifier

Modern desktop application for PDF manipulation built with Python and PySide6.

PDF Modifier provides a clean interface for performing common PDF operations such as merging files, extracting pages, deleting pages, and previewing document thumbnails.

---

## Features

* Merge multiple PDF files into a single document
* Extract selected pages from PDFs
* Delete pages from existing documents
* Preview pages with generated thumbnails
* Drag & drop to change the order of pages or files
* Background workers for smooth UI performance
* Multi-screen workflow for PDF operations

---

## Tech Stack

* **Python**
* **PySide6**
* **pypdf**
* **PyInstaller**

---

## Installation

Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
python main.py
```

---

## Project Structure

```text
PDF-modifier/
├── assets/                  # Images, icons, and animations
├── components/              # Reusable UI components
├── core/
│   ├── workers/             # Background threads for PDF processing
│   └── utils/               # Utility functions
├── interface/
│   └── appWindow.py         # Main application window
├── ui/
│   ├── layouts/             # Layout definitions
│   ├── views/               # Application screens
│   └── widgets/             # Custom widgets
├── tests/                   # Unit tests
├── main.py                  # Application entry point
├── requirements.txt         # Dependencies
└── PDFModifier.spec         # PyInstaller build configuration
```

---

## Architecture

The project follows a modular structure to separate interface logic from processing logic.

### UI Layer

Responsible for:

* Rendering the interface
* Navigation between screens
* User interaction handling

### Core Layer

Responsible for:

* PDF processing
* File operations
* Background task execution

### Component Layer

Responsible for:

* Shared widgets
* Reusable interface elements
* Consistent UI behavior

---

## Build Executable

Generate a standalone executable with:

```bash
pyinstaller PDFModifier.spec
```

---

## Requirements

* Python 3.10+
* PySide6
* pypdf

---
