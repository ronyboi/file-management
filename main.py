import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

DIR = "/Users/ronybot/Downloads/"

class OnMyWatch:
    watchDir = DIR

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_created(event):

        if event.is_directory:
            return None

        if os.path.splitext(event.src_path)[0].split("/")[-1] == ".DS_Store":
            return None

        print("Watchdog received created event - % s." % event.src_path)

        destination_dict = {}

        for file in os.listdir(DIR):
            if os.path.isdir(DIR + file):
                destination_dict["." + file] = DIR + file

        ext = os.path.splitext(event.src_path)[-1]

        if ext not in destination_dict:
            path = DIR+ext[1:]
            os.mkdir(path)
            destination_dict[ext] = path

        os.rename(event.src_path, destination_dict[ext] + "/" + os.path.basename(event.src_path))

if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()
