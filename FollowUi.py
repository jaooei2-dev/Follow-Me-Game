try:
	from PySide6 import QtCore, QtGui, QtWidgets
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtCore, QtGui, QtWidgets
	from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui 

IMAGE_DIR = 'C:/Users/ICT68/Documents/maya/2025/scripts/FollowMeGame/image'

class FollowMeToolDialog(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.setWindowTitle('Follow Me')
		self.resize(500, 200)

		self.mainLayout = QtWidgets.QVBoxLayout()
		self.setLayout(self.mainLayout)
		self.setStyleSheet(
			'''
				background-color: #FFCC66;
				font-family: Kristen ITC;
			'''
		)

		self.mainStackedWidget = QtWidgets.QStackedWidget()
		self.mainLayout.addWidget(self.mainStackedWidget)

		self.initPageHomeWidget()
		self.initPageGameWidget()

		self.mainStackedWidget.addWidget(self.homeWidget)
		self.mainStackedWidget.addWidget(self.gameWidget)

	def initPageHomeWidget(self):
		self.homeWidget = QtWidgets.QWidget()
		self.homeLayout = QtWidgets.QVBoxLayout()
		self.homeWidget.setLayout(self.homeLayout)
		
		self.imageLabel = QtWidgets.QLabel()
		self.imagePixmap = QtGui.QPixmap(f'{IMAGE_DIR}/FollowMedarf1.jpg')
		scaledPixmap = self.imagePixmap.scaled(
			QtCore.QSize(600,200),
			QtCore.Qt.KeepAspectRatio,
			QtCore.Qt.SmoothTransformation		
		)
		self.imageLabel.setPixmap(scaledPixmap)
		self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.homeLayout.addWidget(self.imageLabel)

		self.buttonLayout = QtWidgets.QHBoxLayout()
		self.homeLayout.addLayout(self.buttonLayout)

		self.playButton = QtWidgets.QPushButton('PLAY')
		self.playButton.setStyleSheet(
			'''
				QPushButton{
					background-color: #66CC66;
					border-radius: 10px;
					font-family: Kristen ITC;
					font-size 20px;
					color: black;
					font-weight: bold;
					padding: 6px;
				}
				QPushButton:hover{
					background-color: #dcedc8;
				}
				QPushButton:pressed{
					background-color: #32b566;
				}
			'''
		)
		self.playButton.clicked.connect(self.onToggleChangeWidget)

		self.quitButton = QtWidgets.QPushButton('Quit')
		self.quitButton.setStyleSheet(
			'''
				QPushButton{
					background-color: #f06292;
					border-radius: 10px;
					font-family: Kristen ITC;
					font-size 20px;
					color: black;
					font-weight: bold;
					padding: 6px;
				}
				QPushButton:hover{
					background-color: #f9bdbb;

				}
				QPushButton:pressed{
					background-color: #CC0033;
				}

			'''
		)
		self.quitButton.clicked.connect(self.close)

		self.buttonLayout.addWidget(self.playButton)
		self.buttonLayout.addWidget(self.quitButton)
		self.homeLayout.addStretch()

	def initPageGameWidget(self):
		self.gameWidget = QtWidgets.QWidget()
		self.gameLayout = QtWidgets.QVBoxLayout()
		self.gameWidget.setLayout(self.gameLayout)

		self.homeButtonContainer = QtWidgets.QWidget()
		self.homeButtonLayout = QtWidgets.QHBoxLayout(self.homeButtonContainer)
		self.gameLayout.addWidget(self.homeButtonContainer)

		self.homeButton = QtWidgets.QPushButton('🏠')
		self.homeButton.setStyleSheet(
			'''
				QPushButton{
					background-color: white;
					border-radius: 4px;
					width: 30px;
					height: 30px;
					font-size: 30px;
				}
			'''
		)
		self.homeButton.setFixedSize(30, 30)
		self.homeButton.clicked.connect(self.onToggleChangeWidget)

		self.homeButtonLayout.addWidget(self.homeButton, alignment=QtCore.Qt.AlignRight)

	def onToggleChangeWidget(self):
		if self.mainStackedWidget.currentIndex()== 0:
			self.mainStackedWidget.setCurrentIndex(1)
		else:
			self.mainStackedWidget.setCurrentIndex(0)

def run():
	global ui 
	try:
		ui.close()
	except:
		pass
	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
	ui = FollowMeToolDialog(parent=ptr)
	ui.show()