#
# FILENAME.
#       watch_dog.py - Watch Dog Python App.
#
# FUNCTIONAL DESCRIPTION.
#       The app triggers time_logger when detecting a file CSV created 
#       in a specific directory. The application is run in Mac.
#
#       The feature can leverage plist.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2023/12/24
#       Updated on 2023/12/24
#

import re
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time_logger

class MyHandler(FileSystemEventHandler):
    
    def on_created(self, event):
        print(f"{event.src_path} has been created!")
        fn = event.src_path
        bn = os.path.basename(fn)

        pattern = r'report\-\d+\.csv'
        res = re.match(pattern, bn)
        if res != None:
            print(fn)
            csv = fn
            time.sleep(5)
            time_logger.handle_csv(None, True, True, csv)       

def start_monitoring(path='.'):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:  # Keep the script running
            time.sleep(5)               # sleeps for 5 seconds.
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

def main():
    directory_to_monitor = "/Users/visualge/Library/Mobile Documents/com~apple~CloudDocs"  # change this to your directory
    start_monitoring(directory_to_monitor)

if __name__ == "__main__":
    main()

