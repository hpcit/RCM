# python import
from datetime import timedelta, datetime

# pyqt5
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QFrame, QLabel, \
    QVBoxLayout, QHBoxLayout, QPushButton

# local includes
from client.utils.pyinstaller_utils import resource_path
from client.log.logger import logger


class QDisplayWidget(QWidget):
    """
    Create a new row (display widget) to be put inside the table shown in the session widget
    """

    terminate = pyqtSignal(str)

    def __init__(self,
                 parent,
                 display_id,
                 display_name,
                 status="Not defined",
                 resources="Not defined",
                 timeleft=None):
        super().__init__(parent)

        self.parent = parent
        self.display_id = display_id
        self.display_name = display_name
        self.status = status
        self.resources = resources

        if timeleft is not None:
            strp_time = datetime.strptime(timeleft, "%H:%M:%S")
            self.timeleft = timedelta(hours=strp_time.hour,
                                      minutes=strp_time.minute,
                                      seconds=strp_time.second)
        else:
            self.timeleft = timeleft

        # icons
        self.connect_ico = QIcon()
        self.kill_ico = QIcon()
        self.share_ico = QIcon()

        self.init_ui()

    def init_ui(self):
        """
        Initialize the interface
        """

        self.connect_ico.addFile(resource_path('gui/icons/connect.png'))
        self.kill_ico.addFile(resource_path('gui/icons/kill.png'))
        self.share_ico.addFile(resource_path('gui/icons/share.png'))

        display_hor_layout = QHBoxLayout()
        display_hor_layout.setContentsMargins(0, 2, 0, 2)
        display_hor_layout.setSpacing(2)

        display_ver_layout = QVBoxLayout()
        display_ver_layout.setContentsMargins(0, 0, 0, 0)
        display_ver_layout.setSpacing(0)

        display_ver_layout.addLayout(display_hor_layout)

        self.setLayout(display_ver_layout)

        name = QLabel(self)
        name.setText(str(self.display_name)[:16])
        display_hor_layout.addWidget(name)

        self.status_label = QLabel(self)
        self.status_label.setText(self.status)
        display_hor_layout.addWidget(self.status_label)

        self.time = QLabel(self)
        if self.timeleft is not None:
            self.time.setText(str(self.timeleft))
        else:
            self.time.setText("Not defined")
        display_hor_layout.addWidget(self.time)

        timer = QTimer(self)
        timer.timeout.connect(self.time_update)
        timer.start(1000)

        resources_label = QLabel(self)
        resources_label.setText(self.resources)
        display_hor_layout.addWidget(resources_label)

        self.connect_btn = QPushButton(self)
        self.connect_btn.setIcon(self.connect_ico)
        self.connect_btn.setToolTip('Connect to the remote display')
        self.connect_btn.clicked.connect(self.connect_display)
        display_hor_layout.addWidget(self.connect_btn)

        self.share_btn = QPushButton(self)
        self.share_btn.setIcon(self.share_ico)
        self.share_btn.setToolTip('Share the remote display via file')
        self.share_btn.clicked.connect(self.share_display)
        display_hor_layout.addWidget(self.share_btn)

        self.kill_btn = QPushButton(self)
        self.kill_btn.setIcon(self.kill_ico)
        self.kill_btn.setToolTip('Kill the remote display')
        self.kill_btn.clicked.connect(self.kill_display)
        self.terminate.connect(self.parentWidget().remove_display)

        display_hor_layout.addWidget(self.kill_btn)

        separator = QFrame(self)
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        display_ver_layout.addWidget(separator)

    def connect_display(self):
        logger.info("Connected to remote display " + str(self.display_name))

    def share_display(self):
        logger.info("Shared display " + str(self.display_name))

    def kill_display(self):
        """
        Kill the display running on the server
        :return:
        """
        self.terminate.emit(self.display_id)

    def time_update(self):
        """
        Update the time left of the job running on the server in the gui
        :return:
        """
        if self.status == "valid":
            self.timeleft = self.timeleft - timedelta(seconds=1)
            self.time.setText(str(self.timeleft))
            self.time.update()

    def status_update(self, status):
        """
        Update the status of the job running on the server in the gui
        and set the buttons enabled True/False accordingly
        :return:
        """
        if status is status.PENDING:
            self.connect_btn.setEnabled(False)
            self.share_btn.setEnabled(False)
            self.kill_btn.setEnabled(False)
        if status is status.RUNNING:
            self.time.setText(str(self.parent.rcm_client_connection.hash('timeleft')))
            self.connect_btn.setEnabled(True)
            self.share_btn.setEnabled(True)
            self.kill_btn.setEnabled(True)
        if status is status.FINISHED:
            self.connect_btn.setEnabled(False)
            self.share_btn.setEnabled(False)
            self.kill_btn.setEnabled(True)

        self.status_label.setText(str(status))
        self.status_label.update()
