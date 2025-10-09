try:
	from PySide6 import QtCore, QtGui, QtWidgets
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtCore, QtGui, QtWidgets
	from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui 

IMAGE_DIR = 'C:/Users/LOQ/OneDrive/Documents/maya/2024/scripts/FollowMeGame/image'

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
			'''
		)

		self.imageLabel = QtWidgets.QLabel()
		self.imagePixmap = QtGui.QPixmap(f'{IMAGE_DIR}/FollowMedarf1.jpg')
		scaledPixmap = self.imagePixmap.scaled(
			QtCore.QSize(600,200),
			QtCore.Qt.KeepAspectRatio,
			QtCore.Qt.SmoothTransformation		
		)
		self.imageLabel.setPixmap(scaledPixmap)
		self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.mainLayout.addWidget(self.imageLabel)

		self.buttonLayout = QtWidgets.QHBoxLayout()
		self.mainLayout.addLayout(self.buttonLayout)
		self.playButton = QtWidgets.QPushButton('PLAY')
		self.playButton.setStyleSheet(
			'''
				QPushButton{
					background-color: #66CC66;
					border-radius: 20px;
					font-size 20px;
					color: black;
					font-weight: bold;
					padding: 6px;
				}
			'''
		)
		self.quitButton = QtWidgets.QPushButton('Quit')
		self.quitButton.setStyleSheet(
			'''
				QPushButton{
					background-color: #CC0033;
					border-radius: 20px;
					font-size 20px;
					color: black;
					font-weight: bold;
					padding: 6px;
				}
			'''
		)
		self.buttonLayout.addWidget(self.playButton)
		self.buttonLayout.addWidget(self.quitButton)

		self.mainLayout.addStretch()

def run():
	global ui 
	try:
		ui.close()
	except:
		pass
	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
	ui = FollowMeToolDialog(parent=ptr)
	ui.show()