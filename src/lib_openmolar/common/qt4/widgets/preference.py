#! /usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
##                                                                           ##
##  Copyright 2010-2012, Neil Wallace <neil@openmolar.com>                   ##
##                                                                           ##
##  This program is free software: you can redistribute it and/or modify     ##
##  it under the terms of the GNU General Public License as published by     ##
##  the Free Software Foundation, either version 3 of the License, or        ##
##  (at your option) any later version.                                      ##
##                                                                           ##
##  This program is distributed in the hope that it will be useful,          ##
##  but WITHOUT ANY WARRANTY; without even the implied warranty of           ##
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            ##
##  GNU General Public License for more details.                             ##
##                                                                           ##
##  You should have received a copy of the GNU General Public License        ##
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.    ##
##                                                                           ##
###############################################################################

from PyQt4 import QtGui, QtCore

class Preference(object):
    '''
    A custom data structure used by PreferencesDialog
    '''
    def __init__(self, title):
        self.title = title
        self.widget = QtGui.QLabel(title + " hello world")
        self.icon = QtGui.QIcon.fromTheme("help-about")

    def setIcon(self, icon):
        if not icon.isNull():
            self.icon = icon

    def setWidget(self, widget):
        self.widget = widget

def _test():
    app = QtGui.QApplication([])
    preference = Preference("HELLO")
    preference.widget.show()
    app.exec_()

if __name__ == "__main__":
    _test()
