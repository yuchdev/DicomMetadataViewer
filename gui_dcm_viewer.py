__doc__ = """DICOM Metadata GUI Viewer

Simple Qt-based GUI to explore DICOM metadata as a hierarchical tree.
Relies on pydicom for reading datasets and PySide6 for the UI.

Usage:
    python gui_dcm_viewer.py

Then click "Open DICOM File" and pick a .dcm file.
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QTreeWidget, QTreeWidgetItem, QMessageBox, QScrollArea
)
import pydicom


class DICOMViewer(QMainWindow):
    """Main window for the DICOM metadata tree viewer.

    Displays a single-column QTreeWidget where each node shows:
    Tag | Name | VR | Value. Sequences are expandable with nested items.
    """

    def __init__(self):
        """Initialize the UI and its widgets."""
        super().__init__()
        self.setWindowTitle("DICOM Viewer - Hierarchy Explorer")
        self.setGeometry(100, 100, 1000, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Open file button
        self.open_button = QPushButton("Open DICOM File")
        self.open_button.clicked.connect(self.browse_file)
        layout.addWidget(self.open_button)

        # DICOM tree viewer
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Tag | Name | VR | Value"])
        self.tree.setColumnCount(1)
        self.tree.setAlternatingRowColors(True)
        layout.addWidget(self.tree)

    def browse_file(self):
        """Open a file dialog, read the selected DICOM, and populate the tree."""
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Open DICOM file", "", "DICOM Files (*.dcm);;All Files (*)"
        )
        if filepath:
            try:
                ds = pydicom.dcmread(filepath)
                self.tree.clear()
                self.insert_dataset(self.tree.invisibleRootItem(), ds)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read DICOM file:\n{str(e)}")

    def insert_dataset(self, parent_item, dataset, level=0):
        """Insert a Dataset into the tree widget recursively.

        Parameters:
            parent_item (QTreeWidgetItem): Parent node to attach children to.
            dataset (pydicom.dataset.Dataset): Dataset to traverse.
            level (int): Current depth; used only for internal recursion.
        """
        for elem in dataset:
            tag = f"{elem.tag}"
            name = elem.name
            vr = elem.VR
            value = str(elem.value)

            if len(value) > 80:
                value = value[:77] + "..."

            node_text = f"{tag} | {name} | {vr} | {value}"
            node_item = QTreeWidgetItem([node_text])
            parent_item.addChild(node_item)

            if vr == "SQ":  # Handle sequences
                for i, item in enumerate(elem.value):
                    item_node = QTreeWidgetItem([f"Item {i}"])
                    node_item.addChild(item_node)
                    self.insert_dataset(item_node, item, level + 1)


def main():
    """Run the Qt application and show the viewer window."""
    app = QApplication(sys.argv)
    viewer = DICOMViewer()
    viewer.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
