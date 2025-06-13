import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QRadioButton, QButtonGroup, QHBoxLayout, QGroupBox
from PyQt6.QtGui import QPainter, QPen, QColor, QMouseEvent, QImage
from PyQt6.QtCore import Qt, QPoint

class PaintApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Paint Application")
        self.setGeometry(0, 0, 1000, 500) #set the position(0,0) and size 1000x500
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget) #create and set the central widget
        self.layout = QVBoxLayout(self.central_widget) #main layout
        self.canvas = Canvas(self)  #make the drawing area
        self.layout.addWidget(self.canvas) # add the drawing area to the main layout
        self.button_layout = QHBoxLayout() #make layout for buttons

        # pencil colors options
        draw_group = QGroupBox()
        draw_layout = QVBoxLayout()
        draw_group.setLayout(draw_layout)
        self.button_layout.addWidget(draw_group)

        self.draw_button = QPushButton("Pencil", self)
        self.draw_button.clicked.connect(self.canvas.set_draw_mode)
        draw_layout.addWidget(self.draw_button)

        # Color Options for pencil
        self.color_group = QButtonGroup(self)

        self.red_radio = QRadioButton("Red")
        self.red_radio.setStyleSheet("color: red")
        self.color_group.addButton(self.red_radio)
        self.red_radio.clicked.connect(lambda: self.canvas.set_color(Qt.GlobalColor.red))
        draw_layout.addWidget(self.red_radio)

        self.blue_radio = QRadioButton("Blue")
        self.blue_radio.setStyleSheet("color: blue")
        self.color_group.addButton(self.blue_radio)
        self.blue_radio.clicked.connect(lambda: self.canvas.set_color(Qt.GlobalColor.blue))
        draw_layout.addWidget(self.blue_radio)

        self.green_radio = QRadioButton("Green")
        self.green_radio.setStyleSheet("color: green")
        self.color_group.addButton(self.green_radio)
        self.green_radio.clicked.connect(lambda: self.canvas.set_color(Qt.GlobalColor.green))
        draw_layout.addWidget(self.green_radio)

        # Eraser Button
        self.eraser_button = QPushButton("Eraser", self)
        self.eraser_button.clicked.connect(self.canvas.set_eraser_mode)
        self.button_layout.addWidget(self.eraser_button)

        self.layout.addLayout(self.button_layout) # Add the button layout to the main layout

class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StaticContents)
        self.setFixedSize(parent.size())
        self.image = QImage(self.size(), QImage.Format.Format_RGB32)
        self.image.fill(Qt.GlobalColor.white)

        self.drawing = False
        self.brush_size = 4
        self.brush_color = QColor(Qt.GlobalColor.black)
        self.last_point = QPoint()

        self.mode = " "  # draw or erase
        self.actions = []

    def set_draw_mode(self):
        self.mode = "draw"
        self.brush_size = 4

    def set_eraser_mode(self):
        self.mode = "erase"
        self.brush_color = QColor(Qt.GlobalColor.white)
        self.brush_size = 20

    def set_color(self, color):
        self.brush_color = QColor(color)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.position().toPoint()
            # Save the current state for undo before making any changes
            self.actions.append(self.image.copy())
        elif event.button() == Qt.MouseButton.RightButton:
            self.undo_last_action()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drawing and event.buttons() & Qt.MouseButton.LeftButton:
            painter = QPainter(self.image)
            pen = QPen(self.brush_color, self.brush_size, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.position().toPoint())
            self.last_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    def paintEvent(self, event ):
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(self.rect(), self.image, self.image.rect())

    def undo_last_action(self):
        if self.actions:
            self.image = self.actions.pop()
            self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaintApp()
    window.show()
    sys.exit(app.exec())
