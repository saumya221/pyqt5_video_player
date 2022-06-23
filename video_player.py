from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QApplication,
                             QLabel, QFileDialog, QStyle, QVBoxLayout,QHBoxLayout)
import sys
import random
import time 
from threading import Thread
class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Player") 
 
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        
        videoWidget = QVideoWidget()
 
        self.playButton = QPushButton()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
 
        self.openButton = QPushButton()   
        self.openButton.setIcon(QIcon(('play.png')))
        self.openButton.clicked.connect(self.openFile)
 
        self.mutebutton = QPushButton()   
        self.mutebutton.setIcon(QIcon(('mute.png')))
        self.mutebutton.clicked.connect(self.muteVideo)
        self.muted=1

        self.forwardButton=QPushButton()
        self.forwardButton.clicked.connect(self.play_forward)
        self.forwardButton.setIcon(QIcon(('forward_icon.png')))

        self.backwardButton=QPushButton()
        self.backwardButton.clicked.connect(self.play_backward)
        self.backwardButton.setIcon(QIcon(('back_icon.png')))

        self.exitButton=QPushButton()
        self.exitButton.clicked.connect(self.on_exit)
        self.exitButton.setIcon(QIcon(('power_off.png')))


        self.count=None 
        self.shuffle=1
        self.start_video=0
        self.key_event=0
        self.stopped=0
        self.total=0
        self.hands_free=0

        widget = QWidget(self)
        self.setCentralWidget(widget)
 
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout1=QHBoxLayout()
        
        layout1.addWidget(self.backwardButton)
        layout1.addWidget(self.playButton)
        layout1.addWidget(self.openButton)
        layout1.addWidget(self.forwardButton)
        layout1.addWidget(self.mutebutton)
        layout1.addWidget(self.exitButton)
        
        layout.addLayout(layout1)
 
        widget.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.mediaStatusChanged.connect(self.status_changed)

    def status_changed(self,status):
        if status==QMediaPlayer.EndOfMedia:
            self.start_video=1
            self.play_video()





    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.key_event=1
            self.hands_free=1
            self.play_backward()
        elif event.key() == Qt.Key_Right:
            self.key_event=1
            self.hands_free=1
            self.play_forward()
        elif event.key() == Qt.Key_Space:
            self.key_event=1
            self.hands_free=1
            self.play()
        else:
            pass


    def openFile(self):
        dialog=QFileDialog()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.files, _ = dialog.getOpenFileNames(self,"Open video files", "","Video files (*.avi *.mp4 *.wmv *.mkv)",options=options)
        list_of_valid_extn=["avi","mp4","wmv","mkv"]

        if self.files is not None:
            file1=[]
            for k in self.files:
                k1=k.split(".")
                if k1[-1] not in list_of_valid_extn:
                    pass
                else:
                    file1.append(k)
            self.file1_copy=file1.copy()
            if self.shuffle==1:
                random.shuffle(file1)
            self.files=file1
            self.total=len(self.files)
            self.count=0
        self.play_video()

    def play_video(self):
        if self.total>0:
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.files[self.count])))
            self.mutebutton.setIcon(QIcon(('mute.png')))
            self.play()




    def muteVideo(self):
        if self.muted==0:
            self.mediaPlayer.setMuted(True)
            self.mutebutton.setIcon(QIcon(('mute.png')))
            self.muted=1
        else:
            self.muted=0
            self.hands_free=0
            self.mediaPlayer.setMuted(False)
            self.mutebutton.setIcon(QIcon(('volume.png')))

    def play_backward(self):
        self.scale=1
        if self.key_event==1:
            self.start_video=1
        else:
            self.start_video=0
        if self.count ==0:
            self.count=self.total - 1
        else:
            self.count -=1
        self.play_video()

    def play_forward(self):
        self.scale=1
        if self.key_event==1:

            self.start_video=1
        else:
            self.start_video=0
        if self.count == self.total -1:
            self.count =0
        else:
            self.count +=1
        self.play_video()


    def play(self):
        if self.start_video==0:
            self.mediaPlayer.pause()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.start_video=1
        else:
            self.mediaPlayer.play()
            if self.key_event==1 or self.hands_free==1:
                self.key_event=0
                self.mediaPlayer.setMuted(False)
                self.muted=0
                self.mutebutton.setIcon(QIcon(('volume.png')))

            else:
                self.muted=1
                self.mediaPlayer.setMuted(True)
                self.mutebutton.setIcon(QIcon(('mute.png')))

            self.playButton.setIcon(QIcon(('video-pause-button.png')))
            self.start_video=0

    def on_exit(self):
        self.stopped=1
        sys.exit(0)
 
 
app = QApplication(sys.argv)
videoplayer = VideoPlayer()
videoplayer.resize(800, 620)
videoplayer.show()
sys.exit(app.exec_())