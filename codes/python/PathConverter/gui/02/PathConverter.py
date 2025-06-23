import re
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt

def convert_path():
    path = entry.text()
    # Convert to d:/... format
    path_format1 = re.sub(r'\\', '/', path)
    # Convert to /d/... format
    path_format2 = re.sub(r'\\', '/', path)
    if re.match(r'^[a-zA-Z]:/', path_format2):
        path_format2 = f"/{path_format2[0]}{path_format2[2:]}"
    
    output_text1.setPlainText(path_format1)  # Set first output
    output_text2.setPlainText(path_format2)  # Set second output

# Create application
app = QApplication([])

# Create window
window = QWidget()
window.setWindowTitle("Path Converter")
window.resize(600, 400)  # Adjust window size for additional output

# Create layout
layout = QVBoxLayout()
layout.setSpacing(10)  # Set spacing between widgets

# Create input field
entry = QLineEdit()
entry.setPlaceholderText("Enter path (e.g., d:\\work\\gmsh_work\\gmsh-gmsh_4_13_1\\contrib)")
entry.setFixedHeight(30)  # Set input height
layout.addWidget(entry)

# Create convert button
convert_button = QPushButton("Convert Path")
convert_button.setFixedHeight(30)  # Set button height
convert_button.clicked.connect(convert_path)
layout.addWidget(convert_button)

# Create label and output for d:/... format
label1 = QLabel("Converted Path (d:/... format):")
layout.addWidget(label1)
output_text1 = QTextEdit()
output_text1.setReadOnly(True)  # Set as read-only
output_text1.setFixedHeight(100)  # Set text box height
output_text1.setPlaceholderText("Converted path in d:/... format will appear here")
layout.addWidget(output_text1)

# Create label and output for /d/... format
label2 = QLabel("Converted Path (/d/... format):")
layout.addWidget(label2)
output_text2 = QTextEdit()
output_text2.setReadOnly(True)  # Set as read-only
output_text2.setFixedHeight(100)  # Set text box height
output_text2.setPlaceholderText("Converted path in /d/... format will appear here")
layout.addWidget(output_text2)

# Set layout
window.setLayout(layout)

# Show window
window.show()

# Run application
app.exec()