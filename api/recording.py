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

import tobiicsv
import livedata
import os
import csv

class TobiiRecording:

    def __init__(self):
        self.__livedatajson__= livedata.LivedataJson()

    def getLivedataJSON(self):
        return self.__livedatajson__.getData()

    def importFromJSONFile(self, filepath, filename):
        with open(os.path.join(filepath, filename)) as f:
            for line in f:
                self.__livedatajson__.addJSONLine(line)

    def getTobiiCSVSamples(self):
        csv_samples = []
        for sample in self.getLivedataJSON():
            if sample is not None:
                csv_samples.append(tobiicsv.TobiiCSVSample(sample))
        return csv_samples

    def exportCSVFile(self, filepath, filename):
        csv_samples = self.getTobiiCSVSamples()
        with open(os.path.join(filepath, filename), 'w') as csvfile:
            fieldnames = [tobiicsv.TobiiCSVFields.Recording_timestamp.label,
                          tobiicsv.TobiiCSVFields.Event.label,
                          tobiicsv.TobiiCSVFields.Eye_movement_type.label,
                          tobiicsv.TobiiCSVFields.Gaze_event_duration.label,
                          tobiicsv.TobiiCSVFields.Gaze_position_x.label,
                          tobiicsv.TobiiCSVFields.Gaze_position_y.label,
                          tobiicsv.TobiiCSVFields.Gaze3d_position_combined_x.label,
                          tobiicsv.TobiiCSVFields.Gaze3d_position_combined_y.label,
                          tobiicsv.TobiiCSVFields.Gaze3d_position_combined_z.label]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for e in csv_samples:
                writer.writerow(e.getCSVSample())
