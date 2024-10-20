from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame

class Sidebar(QFrame):  # Change QWidget to QFrame if you want to use setFrameStyle
    def __init__(self):
        super().__init__()

        # Set layout for the sidebar
        layout = QVBoxLayout(self)

        # Example buttons for favorites
        self.add_button("Favorites")
        self.add_button("Documents")
        self.add_button("Downloads")
        self.add_button("Pictures")
        self.add_button("Music")

        self.setFrameStyle(QFrame.StyledPanel)  # Optional, if you are using QFrame

    def add_button(self, name):
        button = QPushButton(name)
        button.clicked.connect(self.on_button_clicked)
        self.layout().addWidget(button)

    def on_button_clicked(self):
        button = self.sender()
        if button:
            print(f"{button.text()} button clicked")  # Placeholder action
