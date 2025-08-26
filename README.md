# DICOM Metadata Viewer

Lightweight utilities to inspect DICOM metadata via:

- CLI: print human-readable tags to stdout (no pixel data)
- GUI: browse tags in a hierarchical tree (PySide6)

## What is DICOM?

DICOM (Digital Imaging and Communications in Medicine) is a standard for storing
and transmitting medical images and related information. A DICOM file typically
contains two parts:
- Metadata (a set of elements identified by Tags and Value Representations/VRs)
- Pixel/Waveform data (image or signal samples)

Each metadata element is identified by a Tag written as (GGGG,EEEE) in hex and
has a VR indicating data type (e.g., PN for Person Name, DA for Date, SQ for
Sequence, etc.). Sequences (VR "SQ") contain nested datasets, forming a
hierarchy. Large binary payloads like Pixel Data are typically not suitable for
plain-text output.

## Project layout

- dcm_viewer.py: CLI for printing DICOM metadata (text only).
- gui_dcm_viewer.py: Qt-based GUI for interactive browsing of DICOM tags.

## Installation

Python 3.9+ is recommended.

1) Create/activate a virtual environment (optional but recommended)

```
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\\Scripts\\activate
```

2) Install dependencies

```
pip install -r requirements.txt
```

## CLI usage

Basic command:

```
python dcm_viewer.py /path/to/file.dcm
```

Example output (truncated):
```
(0008,0008) | Image Type | CS | ORIGINAL\\PRIMARY
(0008,0018) | SOP Instance UID | UI | 1.2.840....
(0010,0010) | Patient's Name | PN | DOE^JOHN
(0010,0020) | Patient ID | LO | 123456
(0020,000D) | Study Instance UID | UI | 1.2.840....
...
```

Notes:

- Pixel Data and known binary VRs are skipped to keep output readable.
- Sequences (`SQ`) are traversed and printed with indentation and item indexes.

Exit codes:

- 0: success
- non-zero: failure to read the file

## GUI usage

Run the GUI:

```
python gui_dcm_viewer.py
```

Then click "Open DICOM File" and select a .dcm file. The left pane shows a
single-column tree with entries in the form:

```
Tag | Name | VR | Value
```

Sequences are shown as expandable items; large values are truncated for display.

## Programmatic API

You can import functions from dcm_viewer.py in your own scripts:

```
from dcm_viewer import print_dataset, format_tag, is_binary_value
import pydicom

ds = pydicom.dcmread("/path/to/file.dcm")
print_dataset(ds)
```

## Limitations

- Only metadata is printed/browsed; pixel data visualization is out of scope.
- Heuristics are used to skip likely-binary values; edge cases may occur.

## License

This repository is provided as-is for demonstration/utility purposes.
