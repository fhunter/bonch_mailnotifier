#!/usr/bin/env python3
# vim: set fileencoding=utf8 :

import sys
import os
import glob
import re
import signal
from PyQt5 import QtGui, QtCore, QtWidgets

def get_counts(maildir):
    full = len(maildir)
    re_flag_s = re.compile(":2,.*S.*$")
    read = sum(re_flag_s.search(i) is not None for i in maildir)
    return {'full': full, 'unread': full-read}

def scan_dir(maildir):
    temp  = glob.glob(maildir + "/cur/**", recursive=True)
    temp += glob.glob(maildir + "/new/**", recursive=True)
    temp += glob.glob(maildir + "/.*/cur/**", recursive=True)
    temp += glob.glob(maildir + "/.*/new/**", recursive=True)
    temp  = [i for i in temp if os.path.isfile(i)]
    return {"/":get_counts(temp)}

def totals(datalist):
    full = sum(i["full"] for i in datalist.values())
    unread = sum(i["unread"] for i in datalist.values())
    return (unread, full)

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.activated.connect(self.clicked)
        self.menu = QtWidgets.QMenu(parent)
        exit_action = self.menu.addAction(QtGui.QIcon.fromTheme("application-exit"), "Exit")
        exit_action.triggered.connect(quit)
        self.setContextMenu(self.menu)
        self.maildir = os.environ["HOME"] + "/Maildir"
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read_maildir)
        self.mails = {}
        self.tool_tip = ""
        self.unread_icon = QtGui.QIcon.fromTheme("mail-message-new")
        self.normal_icon = QtGui.QIcon.fromTheme("mail-read")
        self.read_maildir()
        self.timer.start(60*1000) # Every 60 seconds - recheck the mailbox

    def update_tooltip(self):
        self.setToolTip(self.tool_tip)

    def clicked(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            os.system("xdg-open https://mail.pivt.spbgut.ru/")

    def update_icon(self):
        if self.mails:
            unread = totals(self.mails)[0]
        else:
            unread = 0
        if unread == 0:
            self.setIcon(self.normal_icon)
        else:
            self.setIcon(self.unread_icon)

    def update_quota_menu(self):
        self.tool_tip = u"Непрочтённых %d из %d писем" % totals(self.mails)

    def read_maildir(self):
        self.mails = scan_dir(self.maildir)
        self.update_quota_menu()
        self.update_icon()
        self.update_tooltip()

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    app = QtWidgets.QApplication(sys.argv)

    main_widget = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon.fromTheme("mail-read"), main_widget)

    tray_icon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
