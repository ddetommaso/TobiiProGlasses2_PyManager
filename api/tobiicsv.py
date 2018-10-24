# Copyright (C) 2018  Davide De Tommaso
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>

import livedata
import json
import os
import codecs
import csv

class TobiiCSVProperty(object):

    def __init__(self, label, py_type):
        self.label = label
        self.py_type = py_type

    def asValue(self, value):
        return self.py_type(value)

class TobiiCSVFields:

    Recording_timestamp = TobiiCSVProperty('Recording timestamp', int)
    Event = TobiiCSVProperty('Event', str)
    Eye_movement_type = TobiiCSVProperty('Eye movement type', str)
    Gaze_event_duration = TobiiCSVProperty('Gaze event duration', int)
    Eye_movement_type_index = TobiiCSVProperty('Eye movement type index', int)
    Gaze_position_x = TobiiCSVProperty('Gaze position X', float)
    Gaze_position_y = TobiiCSVProperty('Gaze position Y', float)
    Gaze3d_position_combined_x = TobiiCSVProperty('Gaze 3D position combined X', float)
    Gaze3d_position_combined_y = TobiiCSVProperty('Gaze 3D position combined Y', float)
    Gaze3d_position_combined_z = TobiiCSVProperty('Gaze 3D position combined Z', float)
    Gaze_direction_left_x = TobiiCSVProperty('Gaze direction left X', float)
    Gaze_direction_left_y = TobiiCSVProperty('Gaze direction left Y', float)
    Gaze_direction_left_z = TobiiCSVProperty('Gaze direction left Z', float)
    Gaze_direction_right_x = TobiiCSVProperty('Gaze direction right X', float)
    Gaze_direction_right_y = TobiiCSVProperty('Gaze direction right Y', float)
    Gaze_direction_right_z = TobiiCSVProperty('Gaze direction right Z', float)

    """
    3. to define other CSV tobii properties
    """

class TobiiCSVSample:

    def __init__(self, tobii_data):
        self.__csv_sample__ = {}

        self.__csv_sample__[TobiiCSVFields.Recording_timestamp.label] = tobii_data.ts.getValue()

        if isinstance(tobii_data, livedata.GazePosition3d):
            self.__csv_sample__[TobiiCSVFields.Gaze3d_position_combined_x.label] = tobii_data.gp3.getValue()[0]
            self.__csv_sample__[TobiiCSVFields.Gaze3d_position_combined_y.label] = tobii_data.gp3.getValue()[1]
            self.__csv_sample__[TobiiCSVFields.Gaze3d_position_combined_z.label] = tobii_data.gp3.getValue()[2]

        elif isinstance(tobii_data, livedata.GazePosition):
            self.__csv_sample__[TobiiCSVFields.Gaze_position_x.label] = tobii_data.gp.getValue()[0]
            self.__csv_sample__[TobiiCSVFields.Gaze_position_y.label] = tobii_data.gp.getValue()[1]


        """
            4. to fill the other tobii properties
        """

    def __getitem__(self, key):
        return self.__csv_sample__[key]

    def __setitem__(self, key, value):
        self.__csv_sample__[key] = value

    def getCSVSample(self):
        return self.__csv_sample__
