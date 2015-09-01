from locust import HttpLocust, TaskSet, task
from random import choice
from bs4 import BeautifulSoup
from dateutil.parser import parse
from dateutil import tz
from datetime import datetime

class DownloadDash(TaskSet):
    def on_start(self):
        self.bit = choice(self.parent.bitrate)
        self.segment = self._get_segment()

    @property
    def mpd(self):
         data = self.client.get("/mpds/stream.php?streamkey=bitcodin")
         return data.text

    def _get_segment(self):
        mpd = BeautifulSoup(self.mpd, "xml").mpd
        return int(mpd.find(startNumber=True)["startNumber"])

    @task
    def videos_segment(self):
        seg = self.segment
        bit = self.bit
        init = "/dash/{}/bitcodin-init.m4v".format(bit)
        self.client.get(init).raise_for_status()
        while True:
            path = "/dash/{}/bitcodin-{}.m4v".format(bit, seg)
            self.client.get(path).raise_for_status()
            seg += 1

    @task
    def audio_segment(self):
        seg = self.segment
        bit = "250k"
        init = "/dash/{}/bitcodin-init.m4a".format(bit)
        self.client.get(init).raise_for_status()
        while True:
            path = "/dash/{}/bitcodin-{}.m4a".format(bit, seg)
            self.client.get(path).raise_for_status()
            seg += 1

class DashUser(HttpLocust):
    task_set = DownloadDash
    bitrate = [250, 500, 700, 1100, 1500, 3000]
