import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QTreeView, QListView, QFileSystemModel, QHBoxLayout
)


class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom File Explorer")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QHBoxLayout(self.central_widget)

        # Create the file system model
        self.model = QFileSystemModel()
        self.model.setRootPath(os.path.expanduser("~"))  # Start from the home directory

        # Tree view for directories
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.path.expanduser("~")))
        self.tree_view.setHeaderHidden(True)
        self.tree_view.clicked.connect(self.on_tree_view_clicked)

        # List view for files
        self.list_view = QListView()
        self.list_view.setModel(QFileSystemModel())

        # Add widgets to layout
        layout.addWidget(self.tree_view)
        layout.addWidget(self.list_view)

    def on_tree_view_clicked(self, index):
        # Update list view based on the selected directory
        path = self.model.filePath(index)
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(path))