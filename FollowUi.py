try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance
except:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance

import random
import time
import threading
import maya.OpenMayaUI as omui 
import os
import maya.cmds as cmds
from FollowMeGame import FollowUtil as util

IMAGE_DIR = "C:/Users/LOQ/OneDrive/Documents/maya/2024/scripts/FollowMeGame/image"
ICON_PATH = "C:/Users/LOQ/OneDrive/Documents/maya/2024/scripts/FollowMeGame/ICON"

class FollowMeToolDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Follow Me')
        self.resize(500, 200)

        self.objects = []
        self.round = 1

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.setStyleSheet(
            '''
            QWidget {
                background-color: #FFD580;
                font-family: "Kristen ITC";
            }
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
        self.homeWidget.setStyleSheet(
            '''
                QWidget{
                    background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FFD580,
                    stop:1 #B57EDC;)
                }

            '''
        )
        
        self.homeLayout = QtWidgets.QVBoxLayout(self.homeWidget)
        self.homeLayout.setContentsMargins(0, 0, 0, 0)
        self.homeLayout.setSpacing(0)
        self.imageLabel = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(f'{IMAGE_DIR}/FollowMe.jpg')
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setFixedSize(1000, 300)
        self.homeLayout.addWidget(self.imageLabel, alignment=QtCore.Qt.AlignCenter)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setContentsMargins(30, 20, 30, 20)
        self.buttonLayout.setSpacing(40)
        self.homeLayout.addLayout(self.buttonLayout)

        self.playButton = QtWidgets.QPushButton('PLAY')
        self.playButton.setStyleSheet(
            '''
                QPushButton {
                    background-color: #66CC66;
                    border-radius: 15px;
                    font-family: Kristen ITC;
                    font-size: 22px;
                    color: black;
                    font-weight: bold;
                    padding: 10px 20px;
            }
            QPushButton:hover { background-color: #99EE99; }
            QPushButton:pressed { background-color: #32b566; }
            '''
        )
        self.playButton.clicked.connect(self.onToggleChangeWidget)
        self.playButton.clicked.connect(self.start_game)

        self.quitButton = QtWidgets.QPushButton('Quit')
        self.quitButton.setStyleSheet(
            '''
                QPushButton {
                background-color: #f06292;
                border-radius: 15px;
                font-family: Kristen ITC;
                font-size: 22px;
                color: black;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover { background-color: #f9bdbb; }
            QPushButton:pressed { background-color: #CC0033; }
            '''
        )
        self.quitButton.clicked.connect(self.close)

        self.buttonLayout.addWidget(self.playButton)
        self.buttonLayout.addWidget(self.quitButton)
        self.homeLayout.addStretch()

    def initPageGameWidget(self):
        self.gameWidget = QtWidgets.QWidget()
        self.gameWidget.setStyleSheet('''
            QWidget {
                background-color: #FFD580
            }
            '''
        )

        self.gameLayout = QtWidgets.QVBoxLayout(self.gameWidget)
        self.gameLayout.setContentsMargins(30, 20, 30, 20)
        self.gameLayout.setSpacing(15)

        topLayout = QtWidgets.QHBoxLayout()
        topLayout.setContentsMargins(10, 0, 10, 0)

        self.roundLabel = QtWidgets.QLabel('Round: 1')
        self.roundLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.roundLabel.setStyleSheet('''
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #4a148c;
                background-color: rgba(255, 255, 255, 180);
                border-radius: 10px;
                padding: 6px 12px;
                min-width: 120px;
                text-align: center;
            }
        ''')

        self.scoreLabel = QtWidgets.QLabel('Score: 0')
        self.scoreLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.scoreLabel.setStyleSheet('''
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2e7d32;
                background-color: rgba(255, 255, 255, 180);
                border-radius: 10px;
                padding: 6px 12px;
                min-width: 120px;
                text-align: center;
            }
        ''')

        topLayout.addWidget(self.roundLabel)
        topLayout.addStretch()
        topLayout.addWidget(self.scoreLabel)
        self.gameLayout.addLayout(topLayout)

        self.count_label = QtWidgets.QLabel('')
        self.count_label.setAlignment(QtCore.Qt.AlignCenter)
        self.count_label.setFixedHeight(70)
        self.gameLayout.addWidget(self.count_label)

        iconContainer = QtWidgets.QWidget()
        iconLayout = QtWidgets.QHBoxLayout(iconContainer)
        iconLayout.setAlignment(QtCore.Qt.AlignCenter)
        iconLayout.setSpacing(12)
        self.noteButtons = {}

        notes = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Ti']
        for name in notes:
            btn = QtWidgets.QPushButton()
            btn.setFixedSize(90, 90)
            gray_path = os.path.join(ICON_PATH, f"{name}_gray.png").replace("\\", "/")
            color_path = os.path.join(ICON_PATH, f"{name}_color.png").replace("\\", "/")
            btn.gray_path = gray_path
            btn.color_path = color_path
            btn.setIcon(QtGui.QIcon(gray_path))
            btn.setIconSize(QtCore.QSize(90, 90))
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            btn.setStyleSheet('''
                QPushButton {
                    border: none;
                    background-color: transparent;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: rgba(255,255,255,50);
                }
            ''')
            btn.pressed.connect(lambda checked=False, b=btn: self.on_icon_pressed(b))
            btn.released.connect(lambda checked=False, b=btn: self.on_icon_released(b))
            btn.enterEvent = lambda event, b=btn: self.on_icon_hover(b)
            btn.leaveEvent = lambda event, b=btn: self.on_icon_unhover(b)
            iconLayout.addWidget(btn)
            self.noteButtons[name] = btn

        self.gameLayout.addWidget(iconContainer)
        bottomLayout = QtWidgets.QHBoxLayout()
        bottomLayout.addStretch()
        self.homeButton = QtWidgets.QPushButton('🏠')
        self.homeButton.setFixedSize(45, 45)
        self.homeButton.setStyleSheet('''
            QPushButton {
                background-color: rgba(255,255,255,220);
                border-radius: 8px;
                font-size: 26px;
            }
            QPushButton:hover {
                background-color: #f2f2f2;
            }
        ''')
        self.homeButton.clicked.connect(self.onToggleChangeWidget)
        bottomLayout.addWidget(self.homeButton)
        self.gameLayout.addLayout(bottomLayout)


    def onToggleChangeWidget(self):
        if self.mainStackedWidget.currentIndex()== 0:
            self.mainStackedWidget.setCurrentIndex(1)
        else:
            util.clear_scene()
            self.mainStackedWidget.setCurrentIndex(0)

    def start_game(self):
        util.clear_scene()
        self.objects = util.create_object()
        self.round = 1
        self.score = 0
        self.roundLabel.setText('Round: 1')
        self.roundLabel.setStyleSheet(
                '''
                    QLabel {
                        color: black;
                    }
                '''
            )
        self.mainStackedWidget.setCurrentIndex(1)
        self.countdown_and_play()

    def next_round(self):
        self.roundLabel.setText(f'Round: {self.round}')
        util.shuffle_object_positions(self.objects)
        self.countdown_and_play()

    def countdown_and_play(self):
        self.set_note_buttons_enabled(False)
        self.count_label = QtWidgets.QLabel('Starting in 5')
        self.count_label.setAlignment(QtCore.Qt.AlignCenter)
        self.count_label.setStyleSheet('font-size: 40px; font-weight: bold; color: green;')
        self.gameLayout.insertWidget(1, self.count_label)

        def update_countdown(i):
            if i <= 0:
                self.gameLayout.removeWidget(self.count_label)
                self.count_label.deleteLater()
                delattr(self, 'count_label')
                QtCore.QTimer.singleShot(0, self.play_round)
            else:
                self.count_label.setText(f'Starting in {i}')
                self.count_label.repaint()
                QtWidgets.QApplication.processEvents()
                QtCore.QTimer.singleShot(1000, lambda i=i-1: update_countdown(i))

        update_countdown(5)

    def play_round(self):
        blink_count = min(self.round, len(self.objects))
        targets = random.sample(self.objects, blink_count)
        self.sequence = [note for (_, note) in targets]

        self.set_note_buttons_enabled(False)
        self.is_player_turn=False

        self.play_sequence(targets, 0)  

    def play_sequence(self, targets, idx=0):
        if idx >= len(targets):
            self.start_player_turn()
            return

        obj, note = targets[idx]
        print(f'[FollowMe] playing idx={idx} obj={obj} note="{note}"')

        note_clean = note.strip().capitalize()
        print(f'[FollowMe] note_clean="{note_clean}"')
        color = util.NOTE_COLORS.get(note_clean)
        if color is None:
            print(f'[FollowMe] Warning: note "{note_clean}" not found in NOTE_COLORS. Using default gray.')
            color = util.GRAY

        try:
            util.set_color(obj, color)
            util.play_note(note)
            cmds.refresh(f=True)
        except Exception as e:
            print('[FollowMe] Error setting color:', e)

        duration_ms = 1000

        def restore_and_next():
            try:
                util.set_color(obj, util.GRAY)
                cmds.refresh(f=True)
            except Exception as e:
                print('[FollowMe] Error restoring color:', e)
            QtCore.QTimer.singleShot(400, lambda: self.play_sequence(targets, idx + 1))
        QtCore.QTimer.singleShot(duration_ms, restore_and_next)

    def set_note_buttons_enabled(self, enabled: bool):
        for name, btn in self.noteButtons.items():
            btn.setEnabled(enabled)
            if enabled:
                icon = QtGui.QIcon(btn.gray_path)
            else:
                pix = QtGui.QPixmap(btn.gray_path)
                disabled_pix = pix.copy()
                painter = QtGui.QPainter(disabled_pix)
                painter.fillRect(disabled_pix.rect(), QtGui.QColor(255,255,255,150))
                painter.end()
                icon = QtGui.QIcon(disabled_pix)
            btn.setIcon(icon)


    def start_player_turn(self):
        self.is_player_turn = True
        self.user_sequence = []
        self.set_note_buttons_enabled(True)

    def quit_game(self):
        util.clear_scene()
        self.close()

    def on_icon_pressed(self, button):
        if not getattr(self,'is_player_turn', False):
            return
        if not button.isEnabled():
            return

        icon = QtGui.QIcon(button.color_path)
        button.setIcon(icon)

        for name, btn in self.noteButtons.items():
            if btn == button:
                self.user_sequence.append(name)
                util.play_note(name)
                break

        self.check_user_input()

    def check_user_input(self):
        current_index = len(self.user_sequence) - 1

        if self.user_sequence[current_index] != self.sequence[current_index]:
            self.score = max(0, self.score - 1)
            self.update_score_label()
            self.roundLabel.setStyleSheet('font-size: 22px; font-weight: bold; color: red;')
            self.roundLabel.setText(f'Wrong! Round: {self.round}')
            self.is_player_turn = False
            self.set_note_buttons_enabled(False)
            QtCore.QTimer.singleShot(2000, self.next_round)
            return

        if len(self.user_sequence) < len(self.sequence):
            return

        self.score += len(self.sequence)
        self.update_score_label()
        self.round += 1
        self.roundLabel.setStyleSheet('font-size: 22px; font-weight: bold; color: black;')
        QtCore.QTimer.singleShot(2000, self.next_round)


    def update_score_label(self):
        self.scoreLabel.setText(f'Score: {self.score}')


    def on_icon_released(self, button):
        icon = QtGui.QIcon(button.gray_path)
        button.setIcon(icon)

    def on_icon_hover(self, button):
        icon = QtGui.QIcon(button.color_path)
        button.setIcon(icon)

    def on_icon_unhover(self, button):
        icon = QtGui.QIcon(button.gray_path)
        button.setIcon(icon)


def run():
    global ui 
    try:
        ui.close()
    except:
        pass
    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = FollowMeToolDialog(parent=ptr)
    ui.show()
