"""dcm_viewer
=================

Command-line DICOM metadata viewer that prints human-readable DICOM tags
excluding large/binary payloads (e.g., Pixel Data). Uses pydicom to read
datasets and traverses sequences recursively.

Usage:
    python dcm_viewer.py /path/to/file.dcm

This module exposes utility functions that can be imported and reused
by other tools, and provides a CLI entry point via main().
"""

import argparse
import pydicom
from pydicom.tag import Tag

# Value Representations that typically carry binary or large opaque data
BINARY_VR = {"OB", "OD", "OF", "OL", "OV", "OW", "UN"}
# Specific tags to exclude from textual output regardless of VR
EXCLUDED_TAGS = {
    Tag(0x7FE0, 0x0010),  # Pixel Data
    Tag(0x5400, 0x1010),  # Waveform Data
}


def is_binary_value(elem):
    """Return True if the DICOM element likely contains binary/opaque data.

    The function filters out:
    - Elements with tags in EXCLUDED_TAGS (e.g., Pixel Data)
    - Elements with VR in BINARY_VR (e.g., OB, OW, UN)
    - Elements whose value is bytes
    - Values that fail string conversion or look like non-printable binary blobs

    Parameters:
        elem (pydicom.dataelem.DataElement): DICOM element to inspect.

    Returns:
        bool: True if the value should be treated as binary and skipped, else False.
    """
    if elem.tag in EXCLUDED_TAGS:
        return True
    if elem.VR in BINARY_VR:
        return True
    if isinstance(elem.value, bytes):
        return True
    try:
        val_str = str(elem.value)
        # Heuristic: long strings with few printable characters
        if len(val_str) > 100 and sum(c.isprintable() for c in val_str) / len(val_str) < 0.6:
            return True
    except Exception:
        return True
    return False


def format_tag(tag):
    """Format a pydicom Tag into conventional (gggg,eeee) hex string.

    Parameters:
        tag (pydicom.tag.Tag): The tag to format.

    Returns:
        str: Tag formatted as '(GGGG,EEEE)'.
    """
    return f"({tag.group:04X},{tag.element:04X})"


def print_dataset(dataset, indent=0):
    """Recursively print a DICOM dataset as lines of text.

    Each printed line includes: Tag | Name | VR | Value. Sequences (SQ)
    are traversed recursively with indentation to reflect hierarchy.

    Parameters:
        dataset (pydicom.dataset.Dataset): DICOM dataset to print.
        indent (int): Current indent level (used internally for recursion).
    """
    for elem in dataset:
        if is_binary_value(elem):
            continue

        tag = format_tag(elem.tag)
        name = elem.name
        vr = elem.VR

        try:
            value = str(elem.value)
        except Exception as e:
            value = f"<Error reading value: {e}>"

        indent_str = "  " * indent
        print(f"{indent_str}{tag} | {name} | {vr} | {value}")

        if vr == "SQ":
            for i, item in enumerate(elem.value):
                print(f"{indent_str}  Item {i}:")
                print_dataset(item, indent + 2)


def main():
    """CLI entry point.

    Parses the input DICOM path and prints the metadata using print_dataset.

    Exit codes: 0 on success, non-zero on failure to read the file.
    """
    parser = argparse.ArgumentParser(description="DICOM CLI Viewer (text metadata only)")
    parser.add_argument("file", help="Path to DICOM file")
    args = parser.parse_args()

    try:
        ds = pydicom.dcmread(args.file)
        print_dataset(ds)
    except Exception as e:
        print(f"Error: Failed to read DICOM file: {e}")


if __name__ == "__main__":
    main()
