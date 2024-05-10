#!/usr/bin/env python3
# vim: set fileencoding=utf8 :

import sys
import mailbox
from PyQt5 import QtGui, QtCore, QtWidgets

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtWidgets.QMenu(parent)
        self.quota_menu = self.menu.addMenu("Quotas")
        self.menu.addSeparator()
        exit_action = self.menu.addAction(QtGui.QIcon.fromTheme("application-exit"), "Exit")
        exit_action.triggered.connect(quit)
        self.setContextMenu(self.menu)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read_maildir)
        self.mails = []
        self.tool_tip = ""
        self.unread_icon = QtGui.QIcon.fromTheme("mail-message-new")
        self.normal_icon = QtGui.QIcon.fromTheme("mail-read")
        self.read_maildir()
        self.timer.start(5000) # Every 5 seconds - read quota

    def update_tooltip(self):
        self.setToolTip(self.tool_tip)

    def update_icon(self):
        if self.mails:
            unread = max([i["unread"] for i in self.mails])
        else:
            unread = 0
        if unread == 0:
            self.setIcon(self.unread_icon)
        else:
            self.setIcon(self.normal_icon)

    def update_quota_menu(self):
        self.quota_menu.clear()
        self.tool_tip = ""
        tips = []
        for i in self.mails:
            percent = 100.0*i["used"]/i["soft"]
            avail = (i["soft"]-i["used"])/1024
            temp_string = u"%2.1f %% использовано, %d Мб доступно на %s" % \
                          (percent, avail, i["filesystem"])
            act = self.quota_menu.addAction(temp_string)
            act.setIcon(QtGui.QIcon.fromTheme("dialog-warning"))
            act.setIconVisibleInMenu(percent >= 95)
            tips.append(temp_string)
        self.tool_tip = "\n".join(tips)

    def read_maildir(self):
        mails = []
        self.mails = mails
        self.update_quota_menu()
        self.update_icon()
        self.update_tooltip()

def main():
    app = QtWidgets.QApplication(sys.argv)

    main_widget = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon.fromTheme("mail-read"), main_widget)

    tray_icon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
