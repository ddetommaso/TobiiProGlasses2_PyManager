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

import json

class TobiiJSONProperty:

    def __init__(self, json_key, py_type):
        self.key = json_key
        self.py_type = py_type

    def asValue(self, value):
        if type(self.py_type) is list:
            ret = []
            for i in range(0, len(value)):
                ret.append( self.py_type[i](value[i]) )
        else:
            ret = self.py_type(value)
        return ret

class TobiiJSONProperties:

    Timestamp = TobiiJSONProperty("ts", int)
    Status = TobiiJSONProperty("s", int)
    GazeIndex = TobiiJSONProperty("gidx", int)
    Eye = TobiiJSONProperty("eye", str)
    PupilCenter = TobiiJSONProperty("pc", [float, float, float])
    PupilDiameter = TobiiJSONProperty("pd", float)
    GazeDirection = TobiiJSONProperty("gd", [float, float, float])
    GazePosition = TobiiJSONProperty("gp", [float, float])
    GazePosition3d = TobiiJSONProperty("gp3", [float, float, float])
    MEMS_Gyroscope = TobiiJSONProperty("gy", [float, float, float])
    MEMS_Accelerometer = TobiiJSONProperty("acc", [float, float, float])
    PTS = TobiiJSONProperty("pts", int)
    PV = TobiiJSONProperty("pv", int)
    VTS = TobiiJSONProperty("vts", int)
    SynchPort_Dir = TobiiJSONProperty("dir", str)
    SynchPort_Sig = TobiiJSONProperty("sig", str)
    APISynch_ETS = TobiiJSONProperty("ets", str)
    APISynch_Type = TobiiJSONProperty("type", str)
    APISynch_TAG = TobiiJSONProperty("tag", str)




class TobiiJSONAttribute:

    def __init__(self, tobii_property, json_sample):
        self.__tobii_property__ = tobii_property
        self.__value__ = self.__tobii_property__.asValue(json_sample[self.__tobii_property__.key])

    def value(self):
        return self.__value__

    def key(self):
        return self.__tobii_property__.key


class PupilCenter:

    def __init__(self, json_sample):

        self.ts = TobiiJSONAttribute(TobiiJSONProperties.Timestamp, json_sample)
        self.s = TobiiJSONAttribute(TobiiJSONProperties.Status, json_sample)
        self.gidx = TobiiJSONAttribute(TobiiJSONProperties.GazeIndex, json_sample)
        self.pc = TobiiJSONAttribute(TobiiJSONProperties.PupilCenter, json_sample)
        self.eye = TobiiJSONAttribute(TobiiJSONProperties.Eye, json_sample)



class PupilDiameter:

    def __init__(self, json_sample):
        self.ts = TobiiJSONAttribute(TobiiJSONProperties.Timestamp, json_sample)
        self.s = TobiiJSONAttribute(TobiiJSONProperties.Status, json_sample)
        self.gidx = TobiiJSONAttribute(TobiiJSONProperties.GazeIndex, json_sample)
        self.pd = TobiiJSONAttribute(TobiiJSONProperties.PupilDiameter, json_sample)
        self.eye = TobiiJSONAttribute(TobiiJSONProperties.Eye, json_sample)

class GazeDirection:

    def __init__(self, json_sample):
        self.ts = TobiiJSONAttribute(TobiiJSONProperties.Timestamp, json_sample)
        self.s = TobiiJSONAttribute(TobiiJSONProperties.Status, json_sample)
        self.gidx = TobiiJSONAttribute(TobiiJSONProperties.GazeIndex, json_sample)
        self.gd = TobiiJSONAttribute(TobiiJSONProperties.GazeDirection, json_sample)
        self.eye = TobiiJSONAttribute(TobiiJSONProperties.Eye, json_sample)

class GazePosition:

    def __init__(self, json_sample):
        self.ts = TobiiJSONAttribute(TobiiJSONProperties.Timestamp, json_sample)
        self.s = TobiiJSONAttribute(TobiiJSONProperties.Status, json_sample)
        self.gidx = TobiiJSONAttribute(TobiiJSONProperties.GazeIndex, json_sample)
        self.gp = TobiiJSONAttribute(TobiiJSONProperties.GazePosition, json_sample)

class GazePosition3d:

    def __init__(self, json_sample):
        self.ts = TobiiJSONAttribute(TobiiJSONProperties.Timestamp, json_sample)
        self.s = TobiiJSONAttribute(TobiiJSONProperties.Status, json_sample)
        self.gidx = TobiiJSONAttribute(TobiiJSONProperties.GazeIndex, json_sample)
        self.gp3 = TobiiJSONAttribute(TobiiJSONProperties.GazePosition3d, json_sample)


"""

1. To define other packages from C.6.1.6 to  C.6.1.13

"""

class LivedataJson:

    def __init__(self):
        self.__livedata__ = []

    def decode(self, dct):

        if TobiiJSONProperties.PupilCenter.key in dct:
            return PupilCenter(dct)

        elif TobiiJSONProperties.PupilDiameter.key in dct:
            return PupilDiameter(dct)

        elif TobiiJSONProperties.GazeDirection.key in dct:
            return GazeDirection(dct)

        elif TobiiJSONProperties.GazePosition.key in dct:
            return GazePosition(dct)

        elif TobiiJSONProperties.GazePosition3d.key in dct:
            return GazePosition3d(dct)

            """
            2. to add other conditions
            """

        else:
            return None

    def getData(self):
        return self.__livedata__

    def addJSONLine(self, json_line):
        sample = json.loads(json_line, object_hook=self.decode)
        self.__livedata__.append(sample)
        return sample
