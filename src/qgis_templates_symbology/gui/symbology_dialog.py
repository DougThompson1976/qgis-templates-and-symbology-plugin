# -*- coding: utf-8 -*-

"""
 Symbology dialog class file
"""

import os

from qgis.PyQt import QtCore, QtGui, QtWidgets

from qgis.core import Qgis, QgsCoordinateReferenceSystem, QgsRectangle

from qgis.gui import QgsMessageBar

from qgis.PyQt.uic import loadUiType

from ..models import Symbology
from ..conf import settings_manager

DialogUi, _ = loadUiType(
    os.path.join(os.path.dirname(__file__), "../ui/symbology_dialog.ui")
)


class SymbologyDialog(QtWidgets.QDialog, DialogUi):
    """ Dialog for handling symbology details"""

    def __init__(
            self,
            symbology=None
    ):
        """ Constructor

        :param symbology: symbology instance
        :type symbology: models.Symbology
        """
        super().__init__()
        self.setupUi(self)
        self.symbology = symbology

        self.grid_layout = QtWidgets.QGridLayout()
        self.message_bar = QgsMessageBar()
        self.prepare_message_bar()

        self.profile = settings_manager.get_current_profile()
        self.update_inputs(False)

    def populate_properties(self, symbology):
        """ Populates the symbology dialog widgets with the
        respective information from passed symbology.

        :param symbology: Plugin symbology instance
        :type symbology: models.Symbology
        """
        symbology = symbology
        if symbology:
            id_le.setText(symbology.id)
            title_le.setText(symbology.title)
            description_le.setText(symbology.description)

            if symbology.license:
                license_le.setText(symbology.license)
            if symbology.extent:
                set_extent(symbology.extent)

        self.update_inputs(True)

    def handle_error(self, error):
        """Handles the returned response error

        :param error: Network response error
        :type error: str
        """
        self.show_message(error, level=Qgis.Critical)
        self.update_inputs(True)

    def prepare_message_bar(self):
        """ Initializes the widget message bar settings"""
        self.message_bar.setSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Fixed
        )
        self.grid_layout.addWidget(
            self.tab_widget,
            0, 0, 1, 1
        )
        self.grid_layout.addWidget(
            self.message_bar,
            0, 0, 1, 1,
            alignment=QtCore.Qt.AlignTop
        )
        self.layout().insertLayout(0, self.grid_layout)

    def show_message(
            self,
            message,
            level=Qgis.Warning
    ):
        """ Shows message on the main widget message bar

        :param message: Message text
        :type message: str

        :param level: Message level type
        :type level: Qgis.MessageLevel
        """
        self.message_bar.clearWidgets()
        self.message_bar.pushMessage(message, level=level)

    def show_progress(self, message, minimum=0, maximum=0):
        """ Shows the progress message on the main widget message bar

        :param message: Progress message
        :type message: str

        :param minimum: Minimum value that can be set on the progress bar
        :type minimum: int

        :param maximum: Maximum value that can be set on the progress bar
        :type maximum: int
        """
        self.message_bar.clearWidgets()
        message_bar_item = self.message_bar.createMessage(message)
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.progress_bar.setMinimum(minimum)
        self.progress_bar.setMaximum(maximum)
        message_bar_item.layout().addWidget(self.progress_bar)
        self.message_bar.pushWidget(message_bar_item, Qgis.Info)

    def update_inputs(self, enabled):
        """ Updates the inputs widgets state in the dialog.

        :param enabled: Whether to enable the inputs or disable them.
        :type enabled: bool
        """
        self.tab_widget.setEnabled(enabled)

    def set_extent(self, extent):
        """ Sets the symbology spatial and temporal extents

        :param extent: Instance that contain spatial and temporal extents
        :type extent: models.Extent
        """
        spatial_extent = extent.spatial
        if spatial_extent:
            self.spatialExtentSelector.setOutputCrs(
                QgsCoordinateReferenceSystem("EPSG:4326")
            )

            bbox = spatial_extent.bbox[0] \
                if spatial_extent.bbox and isinstance(spatial_extent.bbox, list) \
                else None

            original_extent = QgsRectangle(
                bbox[0],
                bbox[1],
                bbox[2],
                bbox[3]
            ) if bbox and isinstance(bbox, list) else QgsRectangle()
            self.spatialExtentSelector.setOriginalExtent(
                original_extent,
                QgsCoordinateReferenceSystem("EPSG:4326")
            )
            self.spatialExtentSelector.setOutputExtentFromOriginal()

        temporal_extents = extent.temporal
        if temporal_extents:
            pass
        else:
            self.from_date.clear()
            self.to_date.clear()