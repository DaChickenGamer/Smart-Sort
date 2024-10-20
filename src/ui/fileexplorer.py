import sys
import os
from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import QSize, Qt, QDir, QTimer
import qtawesome as qta
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QTreeView, QListView,
    QFileSystemModel, QHBoxLayout, QSplitter, QPushButton, QStyledItemDelegate, QLineEdit
)

from src.backend.file_search import search_files


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
                    return self.color_icon(qta.icon('fa.image'), 'orange')
                elif file_path.endswith(('.mp4', '.mkv')):
                    return self.color_icon(qta.icon('fa.file-video'), 'red')
                else:
                    return self.color_icon(qta.icon('fa.file'), 'gray')
        return super().data(index, role)

    def append_row(self, parent_index, name, is_directory=False):
        parent_path = self.filePath(parent_index)
        if is_directory:
            new_path = os.path.join(parent_path, name)
            try:
                os.makedirs(new_path)
                self.refresh(parent_index)
            except FileExistsError:
                print("Directory already exists")
        else:
            new_path = os.path.join(parent_path, name)
            try:
                with open(new_path, 'w') as f:
                    f.write("")
                self.refresh(parent_index)
            except FileExistsError:
                print("File already exists")

    def refresh(self, index):
        """Refresh the model to reflect the changes."""
        self.setRootPath(self.rootPath())  # Reset the root path

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

        self.search_results_model = QStandardItemModel(self)  # Create a model for search results

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

        # This does it when text is changed
        #self.search_bar.textChanged.connect(self.filter_files)

        # Connect the returnPressed signal to the filter_files method
        self.search_bar.returnPressed.connect(self.filter_files)

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

        # Add this in the __init__ method of FileExplorer
        self.create_file_button = QPushButton("Create File")
        self.create_dir_button = QPushButton("Create Directory")
        self.create_file_button.clicked.connect(self.create_file)
        self.create_dir_button.clicked.connect(self.create_directory)

        # Add buttons to the button layout
        button_layout.addWidget(self.create_file_button)
        button_layout.addWidget(self.create_dir_button)

        # Set the list view model to the file system model initially
        self.list_view.setModel(self.model)

        # Connect search bar's returnPressed signal to filter_files
        self.search_bar.returnPressed.connect(self.filter_files)

        # Enable the context menu on the list view
        self.list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.context_menu)

        # Connect the double-click signal to open files or directories
        self.list_view.doubleClicked.connect(self.open_item)

    def context_menu(self, position):
        index = self.list_view.indexAt(position)
        if index.isValid():
            menu = QtWidgets.QMenu(self)
            rename_action = menu.addAction("Rename")
            action = menu.exec_(self.list_view.viewport().mapToGlobal(position))  # Position it at the cursor
            if action == rename_action:
                self.rename_file(index)

    def context_menu(self, position):
        index = self.list_view.indexAt(position)
        if index.isValid():
            menu = QtWidgets.QMenu(self)
            rename_action = menu.addAction("Rename")
            action = menu.exec_(self.list_view.viewport().mapToGlobal(position))  # Correct positioning
            if action == rename_action:
                self.rename_file(index)

    def open_item(self, index):
        if index.isValid():
            # Only open on double-click
            QTimer.singleShot(250, lambda: self.check_for_double_click(index))

    def check_for_double_click(self, index):
        if index == self.list_view.currentIndex():
            path = self.model.filePath(index)
            if self.model.isDir(index):
                self.list_view.setRootIndex(self.model.index(path))
                self.dir_stack.append(path)
                self.back_button.setEnabled(True)
            else:
                self.open_file(path)

    def rename_file(self, index):
        if not index.isValid():
            return

        file_path = self.model.filePath(index)
        self.rename_edit = QLineEdit(self)
        self.rename_edit.setText(os.path.basename(file_path))

        self.rename_edit.setStyleSheet("background-color: rgba(173, 216, 230, 0.7); color: black; font-size: 16px;")

        self.rename_edit.setToolTip(file_path)

        # Calculate width based on text length
        text_width = self.rename_edit.fontMetrics().width(self.rename_edit.text())
        min_width = 100  # Minimum width
        max_width = 400  # Maximum width
        self.rename_edit.setFixedWidth(max(min_width, min(max_width, text_width + 20)))  # Add some padding

        # Get the item's rect in the list view
        rect = self.list_view.visualRect(index)

        # Map the item rect position to global coordinates
        global_pos = self.list_view.viewport().mapToGlobal(rect.topLeft())

        # Set the geometry of QLineEdit
        self.rename_edit.setGeometry(global_pos.x(), global_pos.y(), self.rename_edit.width(), rect.height())
        self.rename_edit.show()
        self.rename_edit.selectAll()
        self.rename_edit.setFocus()

        # Connect signals to handle commit or cancel
        self.rename_edit.returnPressed.connect(lambda: self.commit_rename(file_path, index))
        self.rename_edit.editingFinished.connect(self.rename_edit.hide)

    def commit_rename(self, old_path, index):
        new_name = self.rename_edit.text()
        new_path = os.path.join(os.path.dirname(old_path), new_name)

        try:
            os.rename(old_path, new_path)  # Rename the file
            self.model.refresh(index.parent())  # Refresh the model to reflect changes
        except Exception as e:
            print(f"Error renaming file: {e}")
        finally:
            self.rename_edit.hide()  # Hide the QLineEdit after renaming

    def commit_data(self, editor):
        index = self.list_view.currentIndex()
        if index.isValid():
            new_name = editor.text()
            old_path = self.model.filePath(index)
            new_path = os.path.join(os.path.dirname(old_path), new_name)

            try:
                os.rename(old_path, new_path)  # Rename the file
                self.model.refresh(index.parent())  # Refresh the model to reflect changes
            except Exception as e:
                print(f"Error renaming file: {e}")

    def create_file(self):
        current_index = self.list_view.rootIndex()
        if current_index.isValid():
            self.model.append_row(current_index, "new_file.txt", is_directory=False)

    def create_directory(self):
        current_index = self.list_view.rootIndex()
        if current_index.isValid():
            self.model.append_row(current_index, "New Directory", is_directory=True)

    def on_tree_view_clicked(self, index):
        path = self.model.filePath(index)
        self.list_view.setRootIndex(self.model.index(path))
        if self.model.isDir(index):
            self.dir_stack.append(path)  # Save the current path to the stack
            self.back_button.setEnabled(True)  # Enable back button

    def on_list_view_clicked(self, index):
        if index.isValid():
            path = self.model.filePath(index)
            if self.model.isDir(index):
                # If it's a directory, change the view to that directory
                self.list_view.setRootIndex(self.model.index(path))
                self.dir_stack.append(path)
                self.back_button.setEnabled(True)
            else:
                # If it's a file and already selected, open it
                if self.list_view.currentIndex() == index:
                    self.open_file(path)
                else:
                    # Update current index without opening
                    self.list_view.setCurrentIndex(index)

    def open_file(self, path):
        import subprocess
        if sys.platform == "darwin":
            subprocess.call(["open", path])
        else:
            os.startfile(path)

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
        search_text = self.search_bar.text().lower()

        # Clear the search results model
        self.search_results_model.clear()

        # If the search bar is empty, reset to the original model
        if not search_text:
            self.list_view.setModel(self.model)
            self.list_view.setRootIndex(self.model.index(os.path.expanduser("~")))
            return

        # Perform the search and populate the search results model
        for file_path in search_files(search_text):
            item = QStandardItem(os.path.basename(file_path))  # Get the file name
            item.setData(file_path)  # Store the full path in the item's data
            self.search_results_model.appendRow(item)

        # Set the list view to display the search results
        self.list_view.setModel(self.search_results_model)

    def toggle_hidden_items(self, checked):
            if checked:
                self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot | QDir.Hidden)  # Show hidden
            else:
                self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)  # Hide hidden
            self.list_view.setRootIndex(self.model.index(self.model.rootPath()))  # Refresh the view