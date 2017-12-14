import Queue
import base64
import datetime
import getopt
import hashlib
import os
import random
import re
import sys
import threading
import time
import traceback
import requests
import json
import ChangeIp
import pymysql

class SaveThread(threading.Thread):
    def __init__(self, sync):
        super(SaveThread, self).__init__()
        self.sync = sync

    def run(self):
        while True:
            try:
                item = self.sync.get_save_item()
                if not item:
                    if self.sync.flag_end:
                        break
                    else:
                        self.sync.save_event.clear()
                        self.sync.save_event.wait()
                        continue
                self.sync.save_item(item)
            except Exception as e:
                self.sync.log(str(e))
                self.sync.log(traceback.format_exc())
            finally:
                pass
