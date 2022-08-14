from aerofiles.igc import Reader
import json
import numpy as np
import geopy.distance
from datetime import datetime
import subprocess


class igcfile:
    def __init__(self, filepath):
        with open(filepath, 'r') as fp:
            self.data = Reader.read(fp, fp)

    def getflighttimes(self):
        day = self.data["header"][1]["utc_date"]
        recs = self.data["fix_records"][1]

        last = recs[0]
        possible_times = []
        for rec in recs[1:]:

            d_alt = abs(rec["gps_alt"]) - last["gps_alt"]
            distance = geopy.distance.distance(
                (rec["lon"], rec["lat"]), (last["lon"], last["lat"])).m
            d_time = datetime.combine(
                day, rec["time"]) - datetime.combine(day, last["time"])
            speed = round(distance / d_time.seconds * 3.6, 2)

            if speed <= 10 and d_alt <= 3:
                possible_times.append(datetime.combine(day, rec["time"]))

            last = rec

        diffs = list(np.diff(possible_times))
        res = diffs.index(max(diffs))
        return possible_times[res], possible_times[res+1], possible_times[res+1] - possible_times[res]

    def generate_html(self, filepath):
        raw = json.loads('''{
        "type": "FeatureCollection",
        "features": [
            {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                ]
            }
            }
        ]
        }'''
        )
        
        recs = self.data["fix_records"][1]

        raw["features"][0]["geometry"]["coordinates"] = [
            (rec["lon"], rec["lat"])for rec in recs]
        json.dump(raw, open("tmp.json", "w"))

        with open(filepath, "w") as f:
            subprocess.run(f"osmsm -f tmp.json -D".split(), stdout=f, text=True)

    def getaircraft(self):
        header = self.data["header"][1]
        if header["glider_registration"] in [None,"", " "]:
            if not header["glider_model"] in [None,"", " "]: glider = header["glider_model"]
            else: glider = ""
        else: glider = header["glider_registration"]
        return glider

