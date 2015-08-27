from locust import HttpLocust, TaskSet, task
from random import choice

class DownloadDash(TaskSet):
    @task(1)
    def mpd(self):
        self.client.get("/livesim/tfdt_32/testpic_2s/Manifest.mpd")

    @task(3)
    def init(self):
        init_type = ["A48", "V300"]
        path = "/livesim/tfdt_32/testpic_2s/{}/init.mp4".format(init_type)
        self.client.get(link)

    @task(7)
    def videos_segment(self):
        path = "/livesim/tfdt_32/testpic_2s/V300/"
        while True:
            segment = "{}.m4s".format(self.parent.counter)
            self.client.get(path + segment).raise_for_status()
            counter += 1

    @task (7)
    def audio_segment(self):
        path = "/livesim/tfdt_32/testpic_2s/A48/"
        while True:
            segment = "{}.m4s".format(self.parent.counter)
            self.client.get(path + segment).raise_for_status()
            counter += 1

class DashUser(HttpLocust):
    task_set = DownloadDash
    counter = 1

