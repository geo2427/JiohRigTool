import sys
#from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QComboBox, QCheckBox, QTextEdit, QProgressBar, QSlider, QVBoxLayout, QHBoxLayout, QWidget, QButtonGroup
from PySide2.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 윈도우 타이틀 설정
        self.setWindowTitle("PySide2 Example")

        # 라벨 생성
        label = QLabel("Hello World!", self)
        label.setAlignment(Qt.AlignCenter)

        # 텍스트 입력 필드 생성
        line_edit = QLineEdit(self)

        # 콤보 박스 생성
        combo_box = QComboBox(self)
        combo_box.addItems(["Apple", "Banana", "Orange"])
        combo_box.setCurrentText("Orange")

        # 체크박스 생성
        check_box = QCheckBox("I agree to the terms and conditions.", self)

        # 텍스트 에디터 생성
        text_edit = QTextEdit(self)
        text_edit.setPlaceholderText("Enter your text here...")

        # 프로그레스 바 생성
        progress_bar = QProgressBar(self)
        progress_bar.setRange(0, 100)
        progress_bar.setValue(50)

        # 슬라이더 생성
        slider = QSlider(Qt.Horizontal, self)
        slider.setRange(0, 100)
        slider.setValue(50)

        # 버튼 생성
        button = QPushButton("Click Me!", self)
        button2 = QPushButton("Helllo", self)

        # 버튼 클릭 시 실행할 함수 연결
        button.clicked.connect(self.on_button_click)
        button2.clicked.connect(self.on_button2_click)
		        
        # 버튼 그룹 생성
        button_group = QButtonGroup()
        button_group.addButton(button)
        button_group.addButton(button2)

        # 수직 박스 레이아웃 생성
        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(line_edit)
        vbox_layout.addWidget(combo_box)
        vbox_layout.addWidget(check_box)
        vbox_layout.addWidget(text_edit)
        vbox_layout.addWidget(progress_bar)
        vbox_layout.addWidget(slider)
        vbox_layout.addWidget(button)
        vbox_layout.addWidget(button2)
        # vbox_layout.addWidget(button_group)

        # 수평 박스 레이아웃 생성
        hbox_layout = QHBoxLayout()
        hbox_layout.addStretch(1)
        hbox_layout.addLayout(vbox_layout)
        hbox_layout.addStretch(1)

        # 위젯 생성 및 수평 박스 레이아웃 설정
        widget = QWidget(self)
        widget.setLayout(hbox_layout)

        # 윈도우에 위젯 추가
        self.setCentralWidget(widget)

    def on_button_click(self):
        print("Button Clicked!")
        
    def on_button2_click(self):
        print("Hellow Buddy!")

# if __name__ == "__main__":
#     # QApplication 인스턴스 생성
#     app = QApplication(sys.argv)

#     # 메인 윈도우 생성
#     window = MainWindow()
#     window.show()

#     # 이벤트 루프 실행
#     sys.exit(app.exec_())

window = MainWindow()
window.show()
