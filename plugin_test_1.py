# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PluginTest1
                                 A QGIS plugin
 QGIS Plugin for test 1
                              -------------------
        begin                : 2017-08-12
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Albert Brouwer
        email                : ajbrouwer@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from plugin_test_1_dialog import PluginTest1Dialog
# Misc imports
import csv
import os
from qgis.core import QgsMessageLog

GAUL_SHP  = os.environ['IIASA_DROPBOX'] + "/GAUL/g2015_2005_2.shp"
SPAM_TIFF = os.environ['IIASA_DROPBOX'] + "/SPAM/spam2005v2r0_harvested-area_wheat_total.tiff"
FAO_CSV   = os.environ['IIASA_DROPBOX'] + "/FAOSTAT/FAOSTAT_data_8-1-2017.csv"

class PluginTest1:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PluginTest1_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Plugin Test 1')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PluginTest1')
        self.toolbar.setObjectName(u'PluginTest1')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PluginTest1', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = PluginTest1Dialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/PluginTest1/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Task 1'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Plugin Test 1'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def log(self, message):
        QgsMessageLog.logMessage(message, "Plugin Log")

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Load data
            self.log("Loading GAUL data...")
            gaul_layer = self.iface.addVectorLayer(GAUL_SHP, "GAUL", "ogr")
            if not gaul_layer.isValid():
                raise RuntimeError("Error loading " + GAUL_SHP)
            self.log("Loading SPAM data...")
            spam_layer = self.iface.addRasterLayer(SPAM_TIFF, 'SPAM')
            if not spam_layer.isValid():
                raise RuntimeError("Error loading " + SPAM_TIFF)
            self.log("Filtering FAO wheat harvested area data...")
            fao_ethiopia_2005=None
            fao_ethiopia_2014=None
            with open(FAO_CSV) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if row['Area'] == 'Ethiopia':
                        if   row['Year'] == '2005':
                            fao_ethiopia_2005 = row
                        elif row['Year'] == '2014':
                            fao_ethiopia_2014 = row
            assert fao_ethiopia_2005
            assert fao_ethiopia_2014
