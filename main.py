import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os


class OnMyWatch:
    watchDir = "/Users/ronybot/Downloads"

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

        destination_dict = {}

        for file in os.listdir("/Users/ronybot/Downloads"):
            if os.path.isdir("/Users/ronybot/Downloads/" + file):
                destination_dict["."+file] = "/Users/ronybot/Downloads/"+file

        if event.is_directory:
            return None
        print("Watchdog received created event - % s." % event.src_path)

        ext = os.path.splitext(event.src_path)[-1]

        if ext not in destination_dict:
            path = "/Users/ronybot/Downloads/"+ext[1:]
            os.mkdir(path)
            destination_dict[ext] = path

        os.rename(event.src_path, destination_dict[ext] + "/" + os.path.basename(event.src_path))

if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()
