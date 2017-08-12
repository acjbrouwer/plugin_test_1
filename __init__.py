# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PluginTest1
                                 A QGIS plugin
 QGIS Plugin for test 1
                             -------------------
        begin                : 2017-08-12
        copyright            : (C) 2017 by Albert Brouwer
        email                : ajbrouwer@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PluginTest1 class from file PluginTest1.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .plugin_test_1 import PluginTest1
    return PluginTest1(iface)
