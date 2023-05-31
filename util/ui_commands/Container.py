from PySide2 import QtWidgets, QtGui

'''
# Examples: 
layout = QtWidgets.QVBoxLayout()
container = Container("Group")
layout.addWidget(container)
content_layout = QtWidgets.QGridLayout(container.contentWidget)
content_layout.addWidget(QtWidgets.QPushButton("Button"))
'''
    
    
class Header(QtWidgets.QWidget):

    def __init__(self, name, content_widget):
        super(Header, self).__init__()

        self.content = content_widget
        self.expand_ico = QtGui.QPixmap(":teDownArrow.png")
        self.collapse_ico = QtGui.QPixmap(":teRightArrow.png")
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        stacked = QtWidgets.QStackedLayout(self)
        stacked.setStackingMode(QtWidgets.QStackedLayout.StackAll)
        background = QtWidgets.QLabel()
        background.setStyleSheet("QLabel{ background-color: rgb(93, 93, 93); border-radius:2px}")

        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)

        self.icon = QtWidgets.QLabel()
        self.icon.setPixmap(self.expand_ico)
        layout.addWidget(self.icon)
        layout.setContentsMargins(11, 0, 11, 0)

        font = QtGui.QFont()
        font.setBold(True)
        label = QtWidgets.QLabel(name)
        label.setFont(font)

        layout.addWidget(label)
        layout.addItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        stacked.addWidget(widget)
        stacked.addWidget(background)
        background.setMinimumHeight(layout.sizeHint().height() * 1.5)
        
        self.collapse()

    def mousePressEvent(self, *args):
        self.expand() if not self.content.isVisible() else self.collapse()

    def expand(self):
        self.content.setVisible(True)
        self.icon.setPixmap(self.expand_ico)

    def collapse(self):
        self.content.setVisible(False)
        self.icon.setPixmap(self.collapse_ico)


class Main(QtWidgets.QWidget):
    
    def __init__(self, name, color_background=False):
        super(Main, self).__init__()
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._content_widget = QtWidgets.QWidget()
        if color_background:
            self._content_widget.setStyleSheet(".QWidget{background-color: rgb(73, 73, 73);" "margin-left: 2px; margin-right: 2px}")
        header = Header(name, self._content_widget)
        layout.addWidget(header)
        layout.addWidget(self._content_widget)
        
        self.collapse = header.collapse
        self.expand = header.expand
        self.toggle = header.mousePressEvent

    @property
    def contentWidget(self):
        """Getter for the content widget

        Returns: Content widget
        """
        return self._content_widget
    