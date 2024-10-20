import sys
import os
from PySide6 import QtGui
from .sidebar import Sidebar

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTreeView, QListView, QFileSystemModel, QHBoxLayout, QSplitter

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Sort File Explorer")
        self.setWindowIcon(QtGui.QIcon(sys.path[0] + "/assets/SmartSortIcon.png"))

        # Main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QHBoxLayout(self.central_widget)
        self.setMinimumHeight(500)

        windowMinimumWidth = 900

        # Sidebar
        # Hidden for now, no use
        #self.sidebar = Sidebar()
        #layout.addWidget(self.sidebar)

        # Create the file system model
        self.model = QFileSystemModel()
        self.model.setRootPath(os.path.expanduser("~"))  # Start from the home directory

        # Create a splitter
        self.splitter = QSplitter(self)

        # Tree view for directories
        self.tree_view = QTreeView()
        self.tree_view.setMinimumWidth(int(windowMinimumWidth / 7) * 2)
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.path.expanduser("~")))
        self.tree_view.setHeaderHidden(True)

        # Hide unwanted columns (Date, Size, Type)
        self.tree_view.setColumnHidden(1, True)  # Hide Date Modified
        self.tree_view.setColumnHidden(2, True)  # Hide Size
        self.tree_view.setColumnHidden(3, True)  # Hide Type

        # List view for files
        self.list_view = QListView()
        self.list_view.setMinimumWidth(int(windowMinimumWidth / 7) * 5)
        self.list_view.setModel(QFileSystemModel())

        # Add views to the splitter
        self.splitter.addWidget(self.tree_view)
        self.splitter.addWidget(self.list_view)

        # Set stretch factors for the splitter
        self.splitter.setStretchFactor(0, 2)  # Give more space to tree_view
        self.splitter.setStretchFactor(1, 4)  # Give less space to list_view

        # Add the splitter to the layout
        layout.addWidget(self.splitter)

        # Connect the tree view click signal
        self.tree_view.clicked.connect(self.on_tree_view_clicked)

    def on_tree_view_clicked(self, index):
        # Update list view based on the selected directory
        path = self.model.filePath(index)
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(path))
