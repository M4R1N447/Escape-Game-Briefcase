'''
PyQt6 - Widget Tester

Author: Mario Kuijpers
Version: 1.0
Last Updated: 11-09-2024
'''

# Import PyQt6 modules
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QVBoxLayout,
                             QHBoxLayout,
                             QWidget,
                             QComboBox,
                             QStackedWidget,
                             QLabel,
                             QPushButton)

# Import self written widgets
from widgets.buttonWidget import ButtonWidget as Button
from widgets.labelWidget import LabelWidget as Label
from widgets.lineEditWidget import LineEditWidget


class MainWindow(QMainWindow):
    '''
    Widget Tester to test new written widgets
    '''
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widget Tester")
        self.setMinimumSize(1024, 768)

        # Hoofd widget en lay-out
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # ComboBox om widgets te selecteren
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Widget 1", "Widget 2", "Widget 3", "Input Widget"])
        self.combo_box.currentIndexChanged.connect(self.display_widget)
        main_layout.addWidget(self.combo_box)

        # StackedWidget om geselecteerde widget weer te geven
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.create_widget_1())
        self.stacked_widget.addWidget(self.create_widget_2())
        self.stacked_widget.addWidget(self.create_widget_3())
        self.stacked_widget.addWidget(self.create_widget_4())
        main_layout.addWidget(self.stacked_widget)

        # Add widgets to main layout
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def display_widget(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def create_widget_1(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is Widget 1"))
        layout.addWidget(QPushButton("Button 1"))
        widget.setLayout(layout)
        return widget

    def create_widget_2(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is Widget 2"))
        layout.addWidget(QPushButton("Button 2"))
        widget.setLayout(layout)
        return widget

    def create_widget_3(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is Widget 3"))
        layout.addWidget(QPushButton("Button 3"))
        widget.setLayout(layout)
        return widget

    def create_widget_4(self):
        widget = QWidget()
        self.text_input = LineEditWidget(placeholder="Type here", align="center", font_size=20)
        # Voeg een knop toe om de inhoud van de QLineEdit op te halen
        self.text_input.returnPressed.connect(self.update_label)
        fetch_button = QPushButton("Fetch Input")
        fetch_button.clicked.connect(self.update_label)

        layout = QVBoxLayout()
        self.label_input = QLabel("Input will be shown here")
        layout.addWidget(self.label_input)
        layout.addWidget(self.text_input)
        layout.addWidget(fetch_button)
        widget.setLayout(layout)
        return widget

    def update_label(self):
        input_text = self.text_input.text()
        self.label_input.setText(f"Input: {input_text}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
