import sys
import os
from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import QSize, Qt, QDir
import qtawesome as qta
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QTreeView, QListView,
    QFileSystemModel, QHBoxLayout, QSplitter, QPushButton, QStyledItemDelegate, QLineEdit
)

class CustomFileSystemModel(QFileSystemModel):
    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DecorationRole:
            icon = super().data(index, role)
            if self.isDir(index):
                return self.color_icon(qta.icon('fa.folder'), 'blue')
            else:
                file_path = self.filePath(index)
                if file_path.endswith(('.pdf', '.docx', '.txt')):
                    return self.color_icon(qta.icon('fa.file'), 'green')
                elif file_path.endswith(('.jpg', '.png', '.gif')):
                    return self.color_icon(qta.icon('fa.file-image'), 'orange')
                elif file_path.endswith(('.mp4', '.mkv')):
                    return self.color_icon(qta.icon('fa.file-video'), 'red')
                else:
                    return self.color_icon(qta.icon('fa.file'), 'gray')
        return super().data(index, role)

    def color_icon(self, icon, color):
        pixmap = icon.pixmap(64, 64)  # Increase size to 64x64
        colored_pixmap = pixmap.copy()
        painter = QtGui.QPainter(colored_pixmap)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        painter.fillRect(colored_pixmap.rect(), QtGui.QColor(color))
        painter.end()
        return QtGui.QIcon(colored_pixmap)

class CustomDelegate(QStyledItemDelegate):
    def __init__(self, icon_size, parent=None):
        super().__init__(parent)
        self.icon_size = icon_size

    def sizeHint(self, option, index):
        return QSize(self.icon_size.width() + 10, self.icon_size.height() + 10)  # Add padding

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        icon = index.data(Qt.DecorationRole)
        if icon:
            # Draw icon
            rect = option.rect.adjusted(5, 5, -5, -5)  # Adjust rect for padding
            icon.paint(painter, rect, Qt.AlignCenter)

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Sort File Explorer")
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(sys.path[0]), "assets", "SmartSortIcon.png")))

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QHBoxLayout(self.central_widget)
        self.setMinimumHeight(500)

        windowMinimumWidth = 900
        self.model = CustomFileSystemModel()
        self.model.setRootPath(os.path.expanduser("~"))  # Start from the home directory

        # Initialize the directory stack
        self.dir_stack = [os.path.expanduser("~")]  # Start with home directory

        # Create a splitter
        self.splitter = QSplitter(self)

        # Tree View for directories
        self.tree_view = QTreeView()
        self.tree_view.setMinimumWidth(int(windowMinimumWidth / 7) * 2)
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.path.expanduser("~")))
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setFont(QtGui.QFont('SansSerif', 14))
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)

        # List View for files with button on top right
        self.list_view_widget = QWidget()
        list_layout = QVBoxLayout(self.list_view_widget)

        # Back button with Font Awesome icon
        self.back_button = QPushButton()
        self.back_button.setIcon(qta.icon('fa.arrow-left'))  # Use Font Awesome left arrow icon
        self.back_button.setToolTip("Go back")
        self.back_button.setEnabled(False)  # Initially disabled
        self.back_button.clicked.connect(self.go_back)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.filter_files)

        # Show Hidden Items button
        self.show_hidden_button = QPushButton("Show Hidden Items")
        self.show_hidden_button.setCheckable(True)
        self.show_hidden_button.toggled.connect(self.toggle_hidden_items)

        # Add buttons and search bar to layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.search_bar)
        button_layout.addWidget(self.show_hidden_button)

        # List View for files
        self.list_view = QListView()
        self.list_view.setMinimumWidth(int(windowMinimumWidth / 7) * 5)
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(os.path.expanduser("~")))  # Start in home directory
        self.list_view.setFont(QtGui.QFont('SansSerif', 14))

        # Set view mode to grid
        self.list_view.setViewMode(QListView.IconMode)
        self.list_view.setIconSize(QSize(64, 64))
        self.list_view.setSpacing(10)  # Set spacing between items

        # Set custom delegate for consistent item sizes
        self.list_view.setItemDelegate(CustomDelegate(QSize(64, 64)))

        # Add the button layout and the list view to the main layout
        list_layout.addLayout(button_layout)
        list_layout.addWidget(self.list_view)

        # Add the list view widget to the splitter
        self.splitter.addWidget(self.tree_view)
        self.splitter.addWidget(self.list_view_widget)

        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 4)

        layout.addWidget(self.splitter)

        self.tree_view.clicked.connect(self.on_tree_view_clicked)
        self.list_view.clicked.connect(self.on_list_view_clicked)

    def on_tree_view_clicked(self, index):
        path = self.model.filePath(index)
        self.list_view.setRootIndex(self.model.index(path))
        if self.model.isDir(index):
            self.dir_stack.append(path)  # Save the current path to the stack
            self.back_button.setEnabled(True)  # Enable back button

    def on_list_view_clicked(self, index):
        path = self.model.filePath(index)
        if self.model.isDir(index):
            self.list_view.setRootIndex(self.model.index(path))
            self.dir_stack.append(path)  # Save the current path to the stack
            self.back_button.setEnabled(True)  # Enable back button
        else:
            # Optional: Handle file opening or displaying file info
            print(f"File selected: {path}")

    def go_back(self):
        if len(self.dir_stack) > 1:
            self.dir_stack.pop()  # Remove the current directory
            previous_path = self.dir_stack[-1]  # Get the previous directory
            self.list_view.setRootIndex(self.model.index(previous_path))
            if len(self.dir_stack) == 1:
                self.back_button.setEnabled(False)  # Disable back button if at home directory
        else:
            # If at home directory, disable back button
            self.back_button.setEnabled(False)

    def filter_files(self):
        search_text = self.search_bar.text()
        # Implement filtering logic based on the search_text
        # This could involve filtering the model's data or adjusting the list view items.

    def toggle_hidden_items(self, checked):
        if checked:
            self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot | QDir.Hidden)  # Show hidden
        else:
            self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)  # Hide hidden
        self.list_view.setRootIndex(self.model.index(self.model.rootPath()))  # Refresh the view