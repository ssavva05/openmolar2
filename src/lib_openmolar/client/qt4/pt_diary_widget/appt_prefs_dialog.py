#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
##                                                                           ##
##  Copyright 2011-2012,  Neil Wallace <neil@openmolar.com>                  ##
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

from lib_openmolar.common.qt4.dialogs import BaseDialog

RECALL_METHODS = ["post","email","sms"]

class ApptPrefsDialog(BaseDialog):
    def __init__(self, parent=None):
        BaseDialog.__init__(self, parent)
        patient = SETTINGS.current_patient
        try:
            name = patient.full_name
        except AttributeError:
            name = _("NO PATIENT LOADED")
        self.patient_label = QtGui.QLabel("%s<br /><b>%s</b>"% (
        _("Appointment Preferences for Patient"), name))

        self.patient_label.setAlignment(QtCore.Qt.AlignCenter)

        self.recall_groupbox = QtGui.QGroupBox(
            _("Recall Patient Periodically"))
        self.recall_groupbox.setCheckable(True)

        self.recdent_groupbox = QtGui.QGroupBox(
            _("Dentist Recall"))

        self.recdent_groupbox.setCheckable(True)
        self.recdent_groupbox.setChecked(False)

        self.recdent_period_spinbox = QtGui.QSpinBox()
        self.recdent_period_spinbox.setMinimum(1)
        self.recdent_period_spinbox.setMaximum(24)
        self.recdent_date_edit = QtGui.QDateEdit()
        self.recdent_date_edit.setCalendarPopup(True)
        self.recdent_date_edit.setDate(QtCore.QDate.currentDate())

        layout = QtGui.QFormLayout(self.recdent_groupbox)
        layout.addRow(_("dentist recall period (months)"),
            self.recdent_period_spinbox)
        layout.addRow(_("Next Recall"), self.recdent_date_edit)


        self.rechyg_groupbox = QtGui.QGroupBox(
            _("Hygienist Recall"))

        self.rechyg_groupbox.setCheckable(True)
        self.rechyg_groupbox.setChecked(False)


        self.rechyg_period_spinbox = QtGui.QSpinBox()
        self.rechyg_period_spinbox.setMinimum(1)
        self.rechyg_period_spinbox.setMaximum(24)
        self.rechyg_date_edit = QtGui.QDateEdit()
        self.rechyg_date_edit.setCalendarPopup(True)
        self.rechyg_date_edit.setDate(QtCore.QDate.currentDate())


        layout = QtGui.QFormLayout(self.rechyg_groupbox)
        layout.addRow(_("hygienist recall period (months)"),
            self.rechyg_period_spinbox)
        layout.addRow(_("Next Recall"), self.rechyg_date_edit)


        self.recall_method_combobox = QtGui.QComboBox()
        self.recall_method_combobox.addItems(
            [_("Post"), _("email"), _("sms")])

        #self.sms_reminders_checkbox = QtGui.QCheckBox(
        #    _("sms reminders for appointments?"))

        #self.combined_appointment_checkbox = QtGui.QCheckBox(
        #    _("Don't offer joint appointments"))

        layout = QtGui.QGridLayout(self.recall_groupbox)
        layout.addWidget(self.recdent_groupbox,0,0,1,2)
        layout.addWidget(self.rechyg_groupbox,1,0,1,2)

        layout.addWidget(QtGui.QLabel(_("Recall method")), 2,0)
        layout.addWidget(self.recall_method_combobox, 2,1)

        self.insertWidget(self.patient_label)
        self.insertWidget(self.recall_groupbox)

        #self.insertWidget(self.sms_reminders_checkbox)
        #self.insertWidget(self.combined_appointment_checkbox)

        QtCore.QTimer.singleShot(0, self.get_appt_prefs)


    def sizeHint(self):
        return QtCore.QSize(500, 400)

    def get_appt_prefs(self):
        LOGGER.warning("TODO - ApptPrefsDialog.get_appt_prefs")
        return
        appt_prefs = self.pt.appt_prefs
        self.recall_groupbox.setChecked(appt_prefs.recall_active)

        if appt_prefs.recdent_period is not None:
            self.recdent_groupbox.setChecked(True)
            self.recdent_period_spinbox.setValue(appt_prefs.recdent_period)

            self.recdent_date_edit.setDate(appt_prefs.recdent)
        if appt_prefs.rechyg_period is not None:
            self.rechyg_groupbox.setChecked(True)
            self.rechyg_period_spinbox.setValue(appt_prefs.rechyg_period)
            self.rechyg_date_edit.setDate(appt_prefs.rechyg)

        try:
            method_index = RECALL_METHODS.index(appt_prefs.recall_method)
        except ValueError:
            method_index = -1
        self.recall_method_combobox.setCurrentIndex(method_index)

        self.init_edited_signals()

    def init_edited_signals(self):
        for widg in (
        self.recall_groupbox,
        self.recdent_groupbox,
        self.rechyg_groupbox,
        #self.sms_reminders_checkbox,
        #self.combined_appointment_checkbox
         ):
            widg.toggled.connect(self._set_enabled)
        for widg in (
        self.recdent_date_edit,
        self.rechyg_date_edit,
        ):
            widg.dateChanged.connect(self._set_enabled)

        self.recdent_period_spinbox.valueChanged.connect(self._set_enabled)
        self.rechyg_period_spinbox.valueChanged.connect(self._set_enabled)
        self.recall_method_combobox.currentIndexChanged.connect(
            self._set_enabled)

    def _set_enabled(self, *args):
        self.enableApply()

    def item_edited(self):
        self.enableApply()

    def apply_changed(self):
        print "applying changes"

        self.pt.appt_prefs.recall_active = self.recall_groupbox.isChecked()

        if self.recdent_groupbox.isChecked():
            self.pt.appt_prefs.recdent_period = self.recdent_period_spinbox.value()
            self.pt.appt_prefs.recdent = self.recdent_date_edit.date().toPyDate()

        if self.rechyg_groupbox.isChecked():
            self.pt.appt_prefs.rechyg_period = self.rechyg_period_spinbox.value()
            self.pt.appt_prefs.rechyg = self.rechyg_date_edit.date().toPyDate()

        i = self.recall_method_combobox.currentIndex()
        if i == -1:
            self.pt.appt_prefs.recall_method = None
        else:
            self.pt.appt_prefs.recall_method = RECALL_METHODS[i]

    def exec_(self):
        if BaseDialog.exec_(self):
            self.apply_changed()
            return True

if __name__ == "__main__":
    app = QtGui.QApplication([])
    from lib_openmolar import client
    dl = ApptPrefsDialog()
    if dl.exec_():
        dl.apply()
