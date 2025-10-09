try:
	from PySide6 import QtCore, QtGui, QtWidgets
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtCore, QtGui, QtWidgets
	from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui 

class FollowMeToolDialog(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init(parent)

		self.setWindowTitle('Follow Me')
		self.resize(300, 500)

		self.mainLayout = QtWidgets.QVBoxLayout()
		self.setLayout(self.mainLayout)
		self.setStyleSheet(
			'''
				background-color: #FFCC66;
			'''
		)
		self.buttonLayout = QtWidgets.QHBoxLayout()
		self.mainLayout.addLayout(self.buttonLayout)
		self.playButton = QtWidgets.QPushButton('PLAY')
		self.playButton.setStyleSheet(
			'''
				QPushButton{
					background-color: #66CC66;
					border-radius: 12px;
					font-size 20px;
					color: black;
					font-weight: bold;
					padding: 4 px;
				}
			'''
		)
		self.quitButton = QtWidgets.QPushButton('Quit')
		self.quitButton.setStyleSheet(
			'''
				QPushButton{
					background-color: #CC0033;
					border-radius: 12px;
					font-size 20px;
					color: black;
					font-weight: bold;
					padding: 4 px;
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