from locust import HttpLocust, TaskSet, task
from random import choice
from bs4 import BeautifulSoup
from dateutil.parser import parse
from dateutil import tz
from datetime import datetime

class DownloadDash(TaskSet):
    def on_start(self):
        self._get_mpd()

    def _get_mpd(self):
         data = self.client.get("/livesim/tfdt_32/testpic_2s/Manifest.mpd")
         self.mpd = data.text

    def _get_segment(self):
        mpd = BeautifulSoup(self.mpd, "lxml").mpd
        end = parse(mpd['availabilityendtime'])
        start = parse(mpd['availabilitystarttime'])
        duration = int(mpd.period.adaptationset.segmenttemplate['duration'])
        total_seconds = (end - start).seconds
        now = datetime.now(tz.tzutc())
        remaining = end - now
        current_time = total_seconds - remaining.seconds
        return (current_time / duration) - 2

    @task(3)
    def init(self):
        init_type = ["A48", "V300"]
        value = choice(init_type)
        path = "/livesim/tfdt_32/testpic_2s/{}/init.mp4".format(value)
        self.client.get(path)

    @task(7)
    def videos_segment(self):
        segment = self._get_segment()
        path = "/livesim/tfdt_32/testpic_2s/V300/"
        segment_path = "{}.m4s".format(segment)
        self.client.get(path + segment_path).raise_for_status()

    @task (7)
    def audio_segment(self):
        segment = self._get_segment()
        path = "/livesim/tfdt_32/testpic_2s/A48/"
        segment_path = "{}.m4s".format(segment)
        self.client.get(path + segment_path).raise_for_status()

class DashUser(HttpLocust):
    task_set = DownloadDash

