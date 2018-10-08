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

class TobiiProperty(object):

    def __init__(self, label, py_type):
        self.label = label
        self.py_type = py_type

    def asValue(self, value):
        return self.py_type(value)

class TobiiFields:

    Recording_timestamp = TobiiProperty('Recording timestamp', int)
    Event = TobiiProperty('Event', str)
    Eye_movement_type = TobiiProperty('Eye movement type', str)
    Gaze_event_duration = TobiiProperty('Gaze event duration', int)
    Eye_movement_type_index = TobiiProperty('Eye movement type index', int)
    Gaze_position_x = TobiiProperty('Gaze position X', float)
    Gaze_position_y = TobiiProperty('Gaze position Y', float)
    Gaze3d_position_combined_x = TobiiProperty('Gaze 3D position combined X', float)
    Gaze3d_position_combined_y = TobiiProperty('Gaze 3D position combined Y', float)
    Gaze3d_position_combined_z = TobiiProperty('Gaze 3D position combined Z', float)
    Gaze_direction_left_x = TobiiProperty('Gaze direction left X', float)
    Gaze_direction_left_y = TobiiProperty('Gaze direction left Y', float)
    Gaze_direction_left_z = TobiiProperty('Gaze direction left Z', float)
    Gaze_direction_right_x = TobiiProperty('Gaze direction right X', float)
    Gaze_direction_right_y = TobiiProperty('Gaze direction right Y', float)
    Gaze_direction_right_z = TobiiProperty('Gaze direction right Z', float)

    """
    3. to define other CSV tobii properties
    """

class TobiiSample:

    def __init__(self, tobii_data):
        self.__sample__ = {}

        self.__sample__[TobiiFields.Recording_timestamp.label] = tobii_data.ts.getValue()

        if isinstance(tobii_data, livedata.GazePosition3d):
            self.__sample__[TobiiFields.Gaze3d_position_combined_x.label] = tobii_data.gp3.getValue()[0]
            self.__sample__[TobiiFields.Gaze3d_position_combined_y.label] = tobii_data.gp3.getValue()[1]
            self.__sample__[TobiiFields.Gaze3d_position_combined_z.label] = tobii_data.gp3.getValue()[2]

        elif isinstance(tobii_data, livedata.GazePosition):
            self.__sample__[TobiiFields.Gaze_position_x.label] = tobii_data.gp.getValue()[0]
            self.__sample__[TobiiFields.Gaze_position_y.label] = tobii_data.gp.getValue()[1]


        """
            4. to fill the other tobii properties
        """

    def __getitem__(self, key):
        return self.__sample__[key]

    def __setitem__(self, key, value):
        self.__sample__[key] = value

    def getSample(self):
        return self.__sample__



class TobiiRecording:

    def __init__(self):
        self.__samples__ = []
        self.__livedatajson__= livedata.LivedataJson()

    def importFromJSONFile(filepath, filename):
        self.__livedatajson__.importFromJSONFile(filepath, filename)

    def addRecordingSample(self, tobii_sample):
        self.__samples__.append(TobiiSample(tobii_sample))

    def getLivedataJSON(self):
        return self.__livedatajson__.getData()

    def importFromJSONFile(self, filepath, filename):
        with open(os.path.join(filepath, filename)) as f:
            for line in f:
                sample = self.__livedatajson__.addJSONLine(line)
                if sample is not None:
                    self.addRecordingSample(sample)

    def exportCSVFile(self, filepath, filename):
        with open(os.path.join(filepath, filename), 'w') as csvfile:
            fieldnames = [TobiiFields.Recording_timestamp.label,
                          TobiiFields.Event.label,
                          TobiiFields.Eye_movement_type.label,
                          TobiiFields.Gaze_event_duration.label,
                          TobiiFields.Gaze_position_x.label,
                          TobiiFields.Gaze_position_y.label,
                          TobiiFields.Gaze3d_position_combined_x.label,
                          TobiiFields.Gaze3d_position_combined_y.label,
                          TobiiFields.Gaze3d_position_combined_z.label]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for line in self.__samples__:
                writer.writerow(line.getSample())
