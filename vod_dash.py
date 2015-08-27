from locust import HttpLocust, TaskSet, task
from random import choice

class DownloadDash(TaskSet):
    @task(1)
    def mpd(self):
        self.client.get("/content/sintel/sintel.mpd")

    @task(3)
    def init(self):
        bitrate = choice(self.parent.bitrate)
        link = "/content/sintel/video/{}kbit/init.mp4".format(bitrate)
        self.client.get(link)

    @task(10)
    def videos_segment(self):
        bitrate = choice(self.parent.bitrate)
        counter = 1
        path = "/content/sintel/video/{}kbit/".format(bitrate)
        while True:
            segment = "segment_{}.m4s".format(counter)
            self.client.get(path + segment).raise_for_status()
            counter += 1

    @task (5)
    def audio_segment(self):
        counter = 1
        while True:
            path = "/content/sintel/audio/stereo/en/128kbit/"
            segment = "segment_{}.m4s".format(counter)
            self.client.get(path + segment).raise_for_status()
            counter += 1

class DashUser(HttpLocust):
    task_set = DownloadDash
    bitrate = [250, 500, 800, 1100, 1500, 2400, 3000, 4000, 6000]

